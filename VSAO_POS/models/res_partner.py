from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vsao_POS_available = fields.Boolean(string="Mostra no PDV?")