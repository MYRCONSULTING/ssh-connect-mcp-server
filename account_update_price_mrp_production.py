# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import datetime
import math
import re
from ast import literal_eval
from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import OrderedSet, format_date, groupby as tools_groupby

from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES

import logging

logger = logging.getLogger(__name__)



class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_toggle_is_locked(self):
        logger.info('BLOQUEADO X1 ' + str(self.is_locked))
        if not self.is_locked:
            logger.info('BLOQUEADO X2 ' + str(self.is_locked))
            self._post_inventory()
        self.ensure_one()
        self.is_locked = not self.is_locked
        return True

    def _cal_price(self, consumed_moves):
        logger.info('PRECIO X11 ' + str(consumed_moves))
    
        """Set a price unit on the finished move according to `consumed_moves`.
        """
        #super(MrpProduction, self)._cal_price(consumed_moves)
        logger.info('PRECIO X1A ' + str(consumed_moves))
        work_center_cost = 0
        #finished_move = self.move_finished_ids.filtered(lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel') and x.quantity_done > 0)
        finished_move = self.move_finished_ids.filtered(lambda x: x.product_id == self.product_id and x.state not in ('cancel') and x.quantity_done > 0)
        if finished_move:
            logger.info('PRECIO X2 ' + str(consumed_moves))
            logger.info('PRECIO FINISH X2 ' + str(finished_move))
            finished_move.ensure_one()
            for work_order in self.workorder_ids:
                time_lines = work_order.time_ids.filtered(
                    lambda x: x.date_end and not x.cost_already_recorded)
                duration = sum(time_lines.mapped('duration'))
                time_lines.write({'cost_already_recorded': True})
                work_center_cost += (duration / 60.0) * \
                    work_order.workcenter_id.costs_hour
            qty_done = finished_move.product_uom._compute_quantity(finished_move.quantity_done, finished_move.product_id.uom_id)
            extra_cost = self.extra_cost * qty_done
            total_cost = 0

            for m in consumed_moves.sudo():
                for x in m.stock_valuation_layer_ids:
                    total_cost = total_cost + (-1*x.value)
            
            total_cost = total_cost +  work_center_cost + extra_cost

            #total_cost = (sum(-m.stock_valuation_layer_ids.value for m in consumed_moves.sudo()) + work_center_cost + extra_cost)
            logger.info('PRECIO X2AA >> ' + str(total_cost))
            byproduct_moves = self.move_byproduct_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.quantity_done > 0)
            byproduct_cost_share = 0
            for byproduct in byproduct_moves:
                logger.info('PRECIO X3 ' + str(consumed_moves))
                if byproduct.cost_share == 0:
                    continue
                byproduct_cost_share += byproduct.cost_share
                if byproduct.product_id.cost_method in ('fifo', 'average'):
                    logger.info('PRECIO X4 ' + str(consumed_moves))
                    byproduct.price_unit = total_cost * byproduct.cost_share / 100 / byproduct.product_uom._compute_quantity(byproduct.quantity_done, byproduct.product_id.uom_id)
            if finished_move.product_id.cost_method in ('fifo', 'average'):
                logger.info('PRECIO X5 ' + str(consumed_moves))
                xunit = total_cost * float_round(1 - byproduct_cost_share / 100, precision_rounding=0.0001) / qty_done
                #xunit = 5.55
                finished_move.price_unit = xunit
                
                for svl in finished_move.stock_valuation_layer_ids:
                    unit_cost = xunit
                    total = svl.quantity * unit_cost
                    xdescription = svl.description +' Ajuste  por cambio en los componentes'
                    svl.write({'unit_cost': unit_cost,'value': total,'description': xdescription,'remaining_value':total})
                    for am in svl.account_move_id:
                        am.write({'state': 'draft'})
                        for aml in am.line_ids:
                            if aml.debit>0:
                                aml.write({'debit': total})
                            if aml.credit>0:
                                aml.write({'credit': total})
                        am.write({'state': 'posted'})

            
            super(MrpProduction, self)._cal_price(consumed_moves)
        return True
    
    def _post_inventory(self, cancel_backorder=False):
        logger.info('INVENTARIO K1')
        moves_to_do, moves_not_to_do = set(), set()
        for move in self.move_raw_ids:
            if move.state == 'done':
                moves_not_to_do.add(move.id)
            elif move.state != 'cancel':
                moves_to_do.add(move.id)
                if move.product_qty == 0.0 and move.quantity_done > 0:
                    move.product_uom_qty = move.quantity_done
        self.env['stock.move'].browse(moves_to_do)._action_done(cancel_backorder=cancel_backorder)
        moves_to_do = self.move_raw_ids.filtered(lambda x: x.state == 'done') - self.env['stock.move'].browse(moves_not_to_do)
        # Create a dict to avoid calling filtered inside for loops.
        moves_to_do_by_order = defaultdict(lambda: self.env['stock.move'], [
            (key, self.env['stock.move'].concat(*values))
            for key, values in tools_groupby(moves_to_do, key=lambda m: m.raw_material_production_id.id)
        ])
        for order in self:
            logger.info('INVENTARIO K2')
            finish_moves = order.move_finished_ids.filtered(lambda m: m.product_id == order.product_id and m.state not in ('done', 'cancel'))
            # the finish move can already be completed by the workorder.
            if finish_moves and not finish_moves.quantity_done:
                finish_moves._set_quantity_done(float_round(order.qty_producing - order.qty_produced, precision_rounding=order.product_uom_id.rounding, rounding_method='HALF-UP'))
                finish_moves.move_line_ids.lot_id = order.lot_producing_id
            #logger.info('INVENTARIO K3 >> ' +str(moves_to_do_by_order[order.id]))
            logger.info('INVENTARIO K4 >>' + str(order.move_raw_ids))
            #order._cal_price(moves_to_do_by_order[order.id])
            order._cal_price(order.move_raw_ids)
            
        moves_to_finish = self.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
        moves_to_finish = moves_to_finish._action_done(cancel_backorder=cancel_backorder)
        self.action_assign()
        for order in self:
            consume_move_lines = moves_to_do_by_order[order.id].mapped('move_line_ids')
            order.move_finished_ids.move_line_ids.consume_line_ids = [(6, 0, consume_move_lines.ids)]
        return True