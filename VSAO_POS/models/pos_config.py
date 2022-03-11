from odoo import fields, models

class pos_config(models.Model):
    _inherit = 'pos.config'
    _description = 'Customer modification for PDV'

    vsao_POS_filter_Partner = fields.Boolean(string='Mostrar somente Clientes do PDV?')