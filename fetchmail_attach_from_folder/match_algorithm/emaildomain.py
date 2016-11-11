# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .email_exact import EmailExact


class EmailDomain(EmailExact):
    name = 'Domain of email address'

    def search_matches(self, cr, uid, conf, mail_message, mail_message_org):
        ids = super(EmailDomain, self).search_matches(
            cr, uid, conf, mail_message, mail_message_org)
        if not ids:
            domains = []
            for addr in self._get_mailaddresses(conf, mail_message):
                domains.append(addr.split('@')[-1])
            ids = conf.pool.get(conf.model_id.model).search(
                cr, uid,
                self._get_mailaddress_search_domain(
                    conf, mail_message,
                    operator='like',
                    values=['%@' + domain for domain in set(domains)]),
                order=conf.model_order)
        return ids
