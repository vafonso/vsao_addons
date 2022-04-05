from collections import defaultdict
from odoo import fields, models

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('zplxsemijoia95x12xesquerda', 'ZPL Labels 95x12 Semijoia Esquerda'),
        ('zplxsemijoia95x12xdireita', 'ZPL Labels 95x12 Semijoia Direita')
    ], ondelete={'zplxsemijoia95x12xesquerda': 'set default', 'zplxsemijoia95x12xdireita': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if 'zplxsemijoia95x12xesquerda' in self.print_format:
            xml_id = 'product.report_semijoia_95x12_esquerda'
        elif 'zplxsemijoia95x12xdireita' in self.print_format:
            xml_id = 'product.report_semijoia_95x12_direita'
        
        return xml_id, data