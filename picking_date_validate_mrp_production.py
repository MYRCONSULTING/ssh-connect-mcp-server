# -*- coding: utf-8 -*-


import logging
import odoo.tools

_logger = logging.getLogger(__name__)

from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        self.executeupdate()
        return res
    
    def _action_done(self):
        res = super()._action_done()
        self.executeupdate()
        return res

    
    def executeupdate(self):
        _logger.info('PASA POR AQUI X33333 >> ' + str(self))
        if self.date_planned_start:
            # Stock Picking
            self.write({'date_finished': self.date_planned_start})
            # Stock Move Productos Finalizados
            for m in self.move_finished_ids:
                m.write({'date': self.date_planned_start})
                for svl in m.stock_valuation_layer_ids:
                    self._update_create_date(self.date_planned_start, svl.id)
                amlist = m.account_move_ids.filtered(lambda d: d.state =='posted')
                for am in amlist:
                    am.write({'date': self.date_planned_start})

                # Stock Move Line
                for m2 in m.move_line_ids:
                    m2.write({'date': self.date_planned_start})
            
            # Stock Move Componenetes
            for m in self.move_raw_ids:
                m.write({'date': self.date_planned_start})
                for svl in m.stock_valuation_layer_ids:
                    self._update_create_date(self.date_planned_start, svl.id)
                amlist = m.account_move_ids.filtered(lambda d: d.state =='posted')
                for am in amlist:
                    am.write({'date': self.date_planned_start})

                # Stock Move Line
                for m2 in m.move_line_ids:
                    m2.write({'date': self.date_planned_start})
            
   


    def _update_create_date(self, scheduled_date, svl_id):
        sql = """
            UPDATE public.stock_valuation_layer
            SET create_date='{create_date}'
            WHERE id={svl_id};
        """.format(create_date=scheduled_date, svl_id=svl_id)
        self._cr.execute(sql)
        return True
