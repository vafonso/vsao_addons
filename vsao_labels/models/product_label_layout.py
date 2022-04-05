from collections import defaultdict
from odoo import fields, models
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('vsaoxsemijoia95x12xesquerda', 'ZPL Labels 95x12 Semijoia Esquerda'),
        ('vsaoxsemijoia95x12xdireita', 'ZPL Labels 95x12 Semijoia Direita')
    ], ondelete={'vsaoxsemijoia95x12xesquerda': 'set default', 'vsaoxsemijoia95x12xdireita': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if 'vsaoxsemijoia95x12xesquerda' in self.print_format:
            xml_id = 'vsao_labels.label_semijoia_95x12_esquerda'
        elif 'vsaoxsemijoia95x12xdireita' in self.print_format:
            xml_id = 'vsao_labels.label_semijoia_95x12_direita'
        
        return xml_id, data
