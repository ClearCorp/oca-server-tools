# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields
from .. import match_algorithm


class FetchmailServerFolder(models.Model):
    _name = 'fetchmail.server.folder'
    _rec_name = 'path'
    _order = 'sequence'

    def _get_match_algorithms(self):
        def get_all_subclasses(cls):
            return (cls.__subclasses__() +
                    [subsub
                     for sub in cls.__subclasses__()
                     for subsub in get_all_subclasses(sub)])

        return dict([(cls.__name__, cls)
                     for cls in get_all_subclasses(
                match_algorithm.base.Base)])

    def _get_match_algorithms_sel(self):
        algorithms = []
        for cls in self._get_match_algorithms().itervalues():
            algorithms.append((cls.__name__, cls.name))
        algorithms.sort()
        return algorithms

    sequence = fields.Integer('Sequence')
    path = fields.Char(
        'Path',
        help="The path to your mail folder. Typically would be something like "
             "'INBOX.myfolder'", required=True)
    model_id = fields.Many2one(
        'ir.model', 'Model', required=True,
        help='The model to attach emails to')
    model_field = fields.Char(
        'Field (model)',
        help='The field in your model that contains the field to match '
             'against.\n'
             'Examples:\n'
             "'email' if your model is res.partner, or "
             "'partner_id.email' if you're matching sale orders")
    model_order = fields.Char(
        'Order (model)',
        help='Field(s) to order by, this mostly useful in conjunction '
             "with 'Use 1st match'")
    match_algorithm = fields.Selection(
        _get_match_algorithms_sel,
        'Match algorithm', required=True,
        help='The algorithm used to determine which object an email matches.')
    mail_field = fields.Char(
        'Field (email)',
        help='The field in the email used for matching. Typically '
             "this is 'to' or 'from'")
    server_id = fields.Many2one('fetchmail.server', 'Server')
    delete_matching = fields.Boolean(
        'Delete matches',
        help='Delete matched emails from server')
    flag_nonmatching = fields.Boolean(
        'Flag nonmatching',
        help="Flag emails in the server that don't match any object in Odoo")
    match_first = fields.Boolean(
        'Use 1st match',
        help='If there are multiple matches, use the first one. If '
             'not checked, multiple matches count as no match at all')
    domain = fields.Char(
        'Domain',
        help='Fill in a search filter to narrow down objects to match')
    msg_state = fields.Selection(
        [
            ('sent', 'Sent'),
            ('received', 'Received'),
        ],
        'Message state',
        help='The state messages fetched from this folder should be '
             'assigned in Odoo')
    active = fields.Boolean('Active')

    _defaults = {
        'flag_nonmatching': True,
        'msg_state': 'received',
        'active': True,
    }

    @api.multi
    def get_algorithm(self):
        return self._get_match_algorithms()[self.match_algorithm]()

    @api.multi
    def button_attach_mail_manually(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fetchmail.attach.mail.manually',
            'target': 'new',
            'context': dict(self.env.context, default_folder_id=self.id),
            'view_type': 'form',
            'view_mode': 'form',
        }
