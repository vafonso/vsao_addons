from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Customer modification for PDV'

    vsao_POS_filter_Partner = fields.Boolean(string='Mostrar somente Clientes do PDV?')