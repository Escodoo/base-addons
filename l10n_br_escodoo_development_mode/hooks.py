# Copyright 2024 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

from odoo.addons.l10n_br_fiscal.constants.fiscal import (
    SITUACAO_EDOC_A_ENVIAR,
    SITUACAO_EDOC_EM_DIGITACAO,
    SITUACAO_EDOC_ENVIADA,
    SITUACAO_EDOC_REJEITADA,
)

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Switch NFe environment to homologation for all companies and related fiscal
    documents in development mode."""

    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    companies.write({"nfe_environment": "2"})
    _logger.info("NFe environment switched to homologation for all companies.")

    document_states = (
        SITUACAO_EDOC_EM_DIGITACAO,
        SITUACAO_EDOC_A_ENVIAR,
        SITUACAO_EDOC_ENVIADA,
        SITUACAO_EDOC_REJEITADA,
    )
    l10n_br_nfe_module = env["ir.module.module"].search(
        [("name", "=", "l10n_br_nfe"), ("state", "=", "installed")]
    )
    if l10n_br_nfe_module:
        fiscal_documents = env["l10n_br_fiscal.document"].search(
            [("company_id", "in", companies.ids), ("state", "in", document_states)]
        )
        fiscal_documents.write({"nfe_environment": "2"})
        _logger.info("NFe environment switched to homologation for fiscal documents.")
