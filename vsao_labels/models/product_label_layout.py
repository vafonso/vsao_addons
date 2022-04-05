from collections import defaultdict
from odoo import fields, models

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('zplxsemijoia95x12xesquerda', 'ZPL Labels 95x12 Semijoia Esquerda'),
        ('zplxsemijoia95x12xdireita', 'ZPL Labels 95x12 Semijoia Direita')
    ], ondelete={'zplxsemijoia95x12xesquerda': 'set default', 'zplxsemijoia95x12xdireita': 'set default'})