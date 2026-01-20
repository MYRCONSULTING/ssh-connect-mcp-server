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

    def update_costos_valorizacion(self):
        logger.info('UPDATE VALORIZACiON ' + str(self.id))
        # Available variables:
        #  - env: Odoo Environment on which the action is triggered
        #  - model: Odoo Model of the record on which the action is triggered; is a void recordset
        #  - record: record on which the action is triggered; may be void
        #  - records: recordset of all records on which the action is triggered in multi-mode; may be void
        #  - time, datetime, dateutil, timezone: useful Python libraries
        #  - float_compare: Odoo function to compare floats based on specific precisions
        #  - log: log(message, level='info'): logging function to record debug information in ir.logging table
        #  - UserError: Warning Exception to use with raise
        #  - Command: x2Many commands namespace
        # To return an action, assign: action = {...}

        #svlList = env['stock.valuation.layer'].search([('id','in',[1355,1356])])
        svlList = self.env['stock.valuation.layer'].search([('reference','like',self.name)])
        #LISTA DE COMPONENTES
        total_valorizado = 0

        ################################ ACTUALIZAR COMPONENTES
        for svl in svlList:
            if svl.stock_move_id.picking_type_id.code=='mrp_operation' and svl.stock_move_id.location_dest_id.id==15 : # PRE PRODUCCION
                unit_cost = svl.product_id.with_context(date_to='{}-{}-{}'.format(svl.x_account_date.year, svl.x_account_date.month, svl.x_account_date.day)).avg_cost
                if unit_cost <= 0:
                    unit_cost = (svl.product_id.standard_price)
                total = svl.quantity * unit_cost
                xdescription = svl.description +' ajustado 06112023'
                svl.write({'unit_cost': unit_cost,'value': total,'description': xdescription})
                total = total * -1
                for am in svl.account_move_id:
                    am.write({'state': 'draft'})
                    for aml in am.line_ids:
                        if aml.debit>0:
                            aml.write({'debit': total})
                        if aml.credit>0:
                            aml.write({'credit': total})
                am.write({'state': 'posted'})
                total_valorizado = total_valorizado + svl.value

        ################################ ACTUALIZAR PRODUCTO TERMINADOS
        for svl in svlList:
            if svl.stock_move_id.picking_type_id.code=='mrp_operation' and svl.stock_move_id.location_dest_id.id==60 : # PRODUCTOS TERMINADOS
                unit_cost = (total_valorizado / svl.quantity) * -1
                total = svl.quantity * unit_cost
                xdescription = svl.description +' ajustado 06112023'
                svl.write({'unit_cost': unit_cost,'value': total,'description': xdescription})
                for am in svl.account_move_id:
                    am.write({'state': 'draft'})
                    for aml in am.line_ids:
                        if aml.debit>0:
                            aml.write({'debit': total})
                        if aml.credit>0:
                            aml.write({'credit': total})
                    am.write({'state': 'posted'})
            


        
        return True

    