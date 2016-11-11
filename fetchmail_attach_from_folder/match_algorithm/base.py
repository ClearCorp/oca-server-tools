# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class Base(object):
    name = None
    required_fields = []
    readonly_fields = []

    def search_matches(self, cr, uid, conf, mail_message, mail_message_org):
        return []

    def handle_match(
            self, cr, uid, connection, object_id, folder,
            mail_message, mail_message_org, msgid, context=None):
        return folder.server_id.attach_mail(connection, object_id, folder,
                                            mail_message, msgid)
