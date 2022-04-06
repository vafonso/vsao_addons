from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

class ProductLabelLayout(models.TransientModel):
    _inherit = 'report.stock.label_product_product_view'

    def _get_report_values(self, docids, data):
        if data.get('active_model') == 'product.template':
            Product = self.env['product.template']
        elif data.get('active_model') == 'product.product':
            Product = self.env['product.product']
        else:
            raise UserError(_('Product model not defined, Please contact your administrator.'))

        quantity_by_product = defaultdict(list)
        for p, q in data.get('quantity_by_product').items():
            product = Product.browse(int(p))
            quantity_by_product[product].append((product.barcode, q))
        if data.get('custom_barcodes'):
            # we expect custom barcodes to be: {product: [(barcode, qty_of_barcode)]}
            for product, barcodes_qtys in data.get('custom_barcodes').items():
                quantity_by_product[Product.browse(int(product))] += (barcodes_qtys)
        data['quantity'] = quantity_by_product

        return data