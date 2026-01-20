from odoo import api, fields, models
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class MrpProductionn(models.Model):
    _inherit = 'mrp.production'

   
    def write(self, vals):
        _logger.info('MRP X11111111111')

        for rec in self:
            if "PROCESO" in rec.product_id.name:
                vals['location_dest_id'] = 62
            else:
                vals['location_dest_id'] = 60

            return super(MrpProductionn, self).write(vals)