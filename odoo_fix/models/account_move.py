from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    quantidade_volumes = fields.Integer('Qtde. Volumes')
    peso_bruto = fields.Float(string="Peso Bruto")
