{
    'name': 'VSAO - Melhorias para PDV CM Semijoias',
    'version': '1.0',
    'description': 'Criação de pequenas melhorias para controle de visualização de registros dos atendentes do PDV',
    'summary': '1. Criação de UserGroup para visualização de registros próprios ou pessoa física'
               '2. Criação de UserGroup para visualização de todos os registros'
               '3. Inativar Record Rule res.partner.rule.private.employee',
    'author': 'Vinicius Carlos Afonso',
    'license': 'LGPL-3',
    'category': 'Generic Modules',
    'depends': ['base'],
    'data': ['views/vsao_pos.xml'],
    'auto_install': False,
    'application': False,
}