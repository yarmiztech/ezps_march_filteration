# -*- coding: utf-8 -*-
{
    'name': "Enz Rehla AUTO",
    'author':
        'Enzapps',
    'summary': """
This module will help to payment by Check.
""",

    'description': """
        Long description of module's purpose
    """,
    'website': "",
    'category': 'base',
    'version': '12.0',
    'depends': ['base','sale','contacts','account','purchase','ezp_rehlacar','rehla_march_auto'],
    "images": ['static/description/icon.png'],
    'data': [
        'views/auto_form.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
