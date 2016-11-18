# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Email gateway - folders',
    'summary': 'Attach mails in an IMAP folder to existing objects',
    'version': '8.0.1.0.1',
    'author': "Therp BV,Odoo Community Association (OCA)",
    'website': 'http://www.therp.nl',
    'license': 'AGPL-3',
    "category": "Tools",
    "depends": [
        'fetchmail'
    ],
    'data': [
        'view/fetchmail_server.xml',
        'wizard/attach_mail_manually.xml',
        'security/ir.model.access.csv',
    ],
    'installable': False,
    'auto_install': False,
}
