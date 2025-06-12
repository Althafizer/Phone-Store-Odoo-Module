{
    'name': "Odoo Service Management Module",
    'version': "1.0",
    'author': "Kelompok 9 Agile",
    'application': True,
    'description': """
        This module is a Phone Store module for Company to" 
        """,
    'depends': [
        "base", 
        "contacts",
    ],
    'data': [
        "security/service_management_groups.xml",
        "security/ir.model.access.csv",

        "data/ir_sequence_data.xml",

        "wizard/service_order_done_views.xml",

        "views/service_order_views.xml",
        "views/service_menus.xml",
        "views/configuration_views.xml",
    ],
    'installable': True,
    'license': 'LGPL-3',
}