from collections import defaultdict
from odoo import fields, models
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[
        ('etiqueta95x12_esquerda', 'Etiqueta 95x12 Semijoia Esquerda (ZPL)'),
        ('etiqueta95x12_direita', 'Etiqueta 95x12 Semijoia Direita (ZPL)')
    ], ondelete={'etiqueta95x12_esquerda': 'set default','etiqueta95x12_direita': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        if 'etiqueta95x12_esquerda' in self.print_format:
            xml_id = 'vsao_product_label.action_vsao_labels_report_joia95x12_esquerda'
        elif 'etiqueta95x12_direita' in self.print_format:
            xml_id = 'vsao_product_label.action_vsao_labels_report_joia95x12_direita'
        
        return xml_id, data