# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import Base


class OdooStandard(Base):

    name = 'Odoo standard'
    readonly_fields = [
        'model_field',
        'mail_field',
        'match_first',
        'domain',
        'model_order',
        'flag_nonmatching',
    ]

    def search_matches(self, cr, uid, conf, mail_message, mail_message_org):
        return [True]

    def handle_match(
            self, cr, uid, connection, object_id, folder,
            mail_message, mail_message_org, msgid, context):
        result = folder.pool.get('mail.thread').message_process(
            cr, uid,
            folder.model_id.model, mail_message_org,
            save_original=folder.server_id.original,
            strip_attachments=(not folder.server_id.attach),
            context=context
        )

        if folder.delete_matching:
            connection.store(msgid, '+FLAGS', '\\DELETED')

        return [result]
