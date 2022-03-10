from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Customer modification for PDV'

    vsao_POS_available = fields.Boolean(string='Mostra no PDV?')