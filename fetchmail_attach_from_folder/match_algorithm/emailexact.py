# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import Base
from openerp.tools.safe_eval import safe_eval
from openerp.tools.mail import email_split


class EmailExact(Base):

    name = 'Exact mailadress'
    required_fields = ['model_field', 'mail_field']

    def _get_mailaddresses(self, conf, mail_message):
        mailaddresses = []
        fields = conf.mail_field.split(',')
        for field in fields:
            if field in mail_message:
                mailaddresses += email_split(mail_message[field])
        return [addr.lower() for addr in mailaddresses]

    def _get_mailaddress_search_domain(
            self, conf, mail_message, operator='=', values=None):
        mailaddresses = values or self._get_mailaddresses(
            conf, mail_message)
        if not mailaddresses:
            return [(0, '=', 1)]
        search_domain = ((['|'] * (
            len(mailaddresses) - 1)) + [(conf.model_field, operator, addr)
                                        for addr in mailaddresses] +
                         safe_eval(conf.domain or '[]'))
        return search_domain

    def search_matches(self, cr, uid, conf, mail_message, mail_message_org):
        conf_model = conf.pool.get(conf.model_id.model)
        search_domain = self._get_mailaddress_search_domain(conf, mail_message)
        return conf_model.search(
            cr, uid, search_domain, order=conf.model_order)
