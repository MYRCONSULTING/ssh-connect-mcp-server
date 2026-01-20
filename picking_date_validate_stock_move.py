# -*- coding: utf-8 -*-


import logging
import odoo.tools

_logger = logging.getLogger(__name__)

from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id,
                                   cost):
        account_move_vals = super()._prepare_account_move_vals(credit_account_id, debit_account_id, journal_id, qty,
                                                               description, svl_id,
                                                               cost)
        account_move_vals['date'] = self.picking_id.scheduled_date
        return account_move_vals

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id,
                                       credit_account_id, svl_id, description):
        rslt = super()._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id,
                                                      credit_account_id, svl_id, description)
        rslt['credit_line_vals']['date'] = self.picking_id.scheduled_date
        rslt['debit_line_vals']['date'] = self.picking_id.scheduled_date
        if 'price_diff_line_vals' in rslt:
            rslt['price_diff_line_vals']['date'] = self.picking_id.scheduled_date
        return rslt
