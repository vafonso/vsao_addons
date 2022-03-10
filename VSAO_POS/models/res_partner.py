from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vsao_POS_available = fields.Boolean(string="Mostra no PDV?")