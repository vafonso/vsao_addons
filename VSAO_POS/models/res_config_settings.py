from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Customer modification for PDV settings'

    vsao_POS_filter_Partner = fields.Boolean(string='Mostrar somente Clientes do PDV?')