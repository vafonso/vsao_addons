{
    'name': 'vsao_product_labels',
    'version': '1.0',
    'description': 'Cria etiquetas ZPL para Produtos',
    'author': 'Vinicius Carlos Afonso',
    'license': 'LGPL-3',
    'depends': ['product'],
    'data': ['report/vsao_labels_report.xml',
            'vsao_labels_template'], 
    'auto_install': False,
    'application': False,
}