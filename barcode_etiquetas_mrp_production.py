# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
import calendar

from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
import math
from odoo.tools import float_is_zero, float_round
import logging

_logger = logging.getLogger(__name__)
class MrpProduction(models.Model):
    _inherit = "mrp.production"
    #x_capacidad_maquina = fields.Float(string='PESO X CADA INGRESO( KG)',related='x_studio_many2one_field_Xb13u.default_capacity',digits=(12,3))
    x_name_producto = fields.Char(compute='_compute_producto',default=' ',string="Nombre de Producto",store=True)
    x_codigo_barra_producto_terminado = fields.Char(compute='_compute_producto',default=' ',string="Código de Barra de Producto",store=True)
    x_nombre_lote = fields.Char(string="Lote")
    x_nombre_peso = fields.Char(string="Peso")
    x_nombre_fecha = fields.Char(compute='_compute_producto',default=' ',string="Fecha Producción",store=True)


    @api.depends('name')
    def _compute_producto(self):
        for rec in self:
            if rec.product_id:
                rec.x_name_producto = rec.product_id.name
                rec.x_codigo_barra_producto_terminado = rec.product_id.barcode
                if rec.date_planned_start:
                    #fecha_obj = datetime.strptime(str(rec.date_planned_start), '%Y-%m-%d %H:%M:%S')
                    #mes=str(rec.date_planned_start.month)
                    mes = str(calendar.month_name[rec.date_planned_start.month])[:3].upper()
                    dia=str(rec.date_planned_start.day)
                    #mes = fecha_obj.month
                    #dia = fecha_obj.day
                    rec.x_nombre_fecha = mes + '-' + dia
    
    




