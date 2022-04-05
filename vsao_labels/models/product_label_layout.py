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
        
        active_model = ''
        if self.product_tmpl_ids:
            products = self.product_tmpl_ids.ids
            active_model = 'product.template'
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'

        # Build data to pass to the report
        data = {
            'active_model': active_model,
            'quantity_by_product': {p: self.custom_quantity for p in products},
            'layout_wizard': self.id,
            'price_included': 'xprice' in self.print_format,
        }
        return xml_id, data
