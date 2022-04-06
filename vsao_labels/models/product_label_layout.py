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
            Product = self.env['product.template']
        elif self.product_ids:
            products = self.product_ids.ids
            active_model = 'product.product'
            Product = self.env['product.product']

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.barcode, q))
        if data.get('custom_barcodes'):
            # we expect custom barcodes to be: {product: [(barcode, qty_of_barcode)]}
            for product, barcodes_qtys in data.get('custom_barcodes').items():
                quantity_by_product[Product.browse(int(product))] += (barcodes_qtys)
        data['quantity'] = quantity_by_product
        
        return xml_id, data
