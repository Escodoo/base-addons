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


def _switch_environment(env, companies, fiscal_documents, field_name, value, doc_type):
    companies.write({field_name: value})
    _logger.info(f"{doc_type} environment switched to homologation for all companies.")
    fiscal_documents.write({field_name: value})
    _logger.info(
        f"{doc_type} environment switched to homologation for fiscal documents."
    )


def post_init_hook(cr, registry):
    """Switch NFe/NFSe environment to homologation for all companies and related fiscal
    documents in development mode."""

    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])

    document_states = (
        SITUACAO_EDOC_EM_DIGITACAO,
        SITUACAO_EDOC_A_ENVIAR,
        SITUACAO_EDOC_ENVIADA,
        SITUACAO_EDOC_REJEITADA,
    )

    modules_to_check = {
        "l10n_br_nfe": {"field": "nfe_environment", "doc_type": "NFe"},
        "l10n_br_nfse": {"field": "nfse_environment", "doc_type": "NFSe"},
    }

    for module_name, data in modules_to_check.items():
        module_installed = env["ir.module.module"].search(
            [("name", "=", module_name), ("state", "=", "installed")]
        )

        if module_installed:
            fiscal_documents = env["l10n_br_fiscal.document"].search(
                [("company_id", "in", companies.ids), ("state", "in", document_states)]
            )
            _switch_environment(
                env, companies, fiscal_documents, data["field"], "2", data["doc_type"]
            )
