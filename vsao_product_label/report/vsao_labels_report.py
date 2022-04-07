from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError


class ReportProductLabel(models.AbstractModel):
    _name = 'report.vsao_product_label.product_joia95x12_esquerda'
    _description = 'Etiquetas para Produtos'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)

class ReportProductLabel2(models.AbstractModel):
    _name = 'report.vsao_product_label.product_joia95x12_direita'
    _description = 'Etiquetas para Produtos'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, data)

def _prepare_data(env, data):
    # change product ids by actual product object to get access to fields in xml template
    # we needed to pass ids because reports only accepts native python types (int, float, strings, ...)
    if data.get('active_model') == 'product.template':
        Product = env['product.template'].with_context(display_default_code=False)
    elif data.get('active_model') == 'product.product':
        Product = env['product.product'].with_context(display_default_code=False)
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

