from collections import defaultdict
from odoo import fields, models
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('etiqueta95x12_esquerda', 'Etiqueta 95x12 Semijoia Esquerda (ZPL)')
    ], ondelete={'etiqueta95x12_esquerda': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if 'etiqueta95x12_esquerda' in self.print_format:
            xml_id = 'vsao_labels.product_joia95x12_esquerda'
        
        return xml_id, data