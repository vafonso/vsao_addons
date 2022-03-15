{
    'name': 'vsao_todo',
    'version': '1.0',
    'description': 'Tutorial App for Odoo Module creation learning',
    'summary': 'Tutorial',
    'author': 'Vinicius Carlos Afonso',
    'license': 'LGPL-3',
    'category': 'Services/Tutorial',
    'depends': ["base"],
    'auto_install': False,
    'application': True,
    'data':["views/vsao_todo_menu.xml", "security/vsao_todo_security.xml"]
}