# -*- coding: utf-8 -*-
{
    'name': 'AssetFlow - Enterprise Asset & Resource Management',
    'version': '1.0',
    'summary': 'Simplify and digitize asset lifecycles and shared resource bookings',
    'sequence': 1,
    'depends': ['base', 'mail'],
    'data': [
        'data/ir_sequence_data.xml',  # Loaded first so sequence is ready
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}