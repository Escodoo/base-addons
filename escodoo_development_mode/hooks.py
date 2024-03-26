# Copyright 2024 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Disable email servers for development mode."""

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Disable incoming mail servers
    fetchmail_server = env["fetchmail.server"].search([])
    if fetchmail_server:
        fetchmail_server.write({"active": False, "state": "draft"})
        _logger.info("Incoming mail servers disabled.")

    # Disable outgoing mail servers
    mail_server = env["ir.mail_server"].search([])
    if mail_server:
        mail_server.write({"active": False})
        _logger.info("Outgoing mail servers disabled.")
