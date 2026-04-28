# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.tests.common import TransactionCase

from ..hooks import _switch_environment, post_init_hook

_MODULE = "odoo.addons.l10n_br_escodoo_development_mode.hooks"


class TestSwitchEnvironment(TransactionCase):
    """Unit tests for the _switch_environment helper."""

    def test_writes_nfe_field_to_companies_and_documents(self):
        """_switch_environment writes nfe_environment to both record sets."""
        mock_companies = MagicMock()
        mock_documents = MagicMock()
        _switch_environment(
            self.env, mock_companies, mock_documents, "nfe_environment", "2", "NFe"
        )
        mock_companies.write.assert_called_once_with({"nfe_environment": "2"})
        mock_documents.write.assert_called_once_with({"nfe_environment": "2"})

    def test_writes_nfse_field_to_companies_and_documents(self):
        """_switch_environment writes nfse_environment to both record sets."""
        mock_companies = MagicMock()
        mock_documents = MagicMock()
        _switch_environment(
            self.env, mock_companies, mock_documents, "nfse_environment", "2", "NFSe"
        )
        mock_companies.write.assert_called_once_with({"nfse_environment": "2"})
        mock_documents.write.assert_called_once_with({"nfse_environment": "2"})


class TestPostInitHook(TransactionCase):
    def _module_search_side_effect(self, installed_names):
        installed = self.env["ir.module.module"].browse([1])
        empty = self.env["ir.module.module"].browse()

        def _search(domain, *args, **kwargs):
            name = next((v for f, _, v in domain if f == "name"), None)
            return installed if name in installed_names else empty

        return _search

    @patch(f"{_MODULE}._switch_environment")
    def test_nfe_installed_switches_nfe_environment(self, mock_switch):
        with patch.object(
            type(self.env["ir.module.module"]),
            "search",
            side_effect=self._module_search_side_effect({"l10n_br_nfe"}),
        ):
            post_init_hook(self.env)

        mock_switch.assert_called_once()
        args = mock_switch.call_args[0]
        self.assertEqual(args[3], "nfe_environment")
        self.assertEqual(args[4], "2")
        self.assertEqual(args[5], "NFe")

    @patch(f"{_MODULE}._switch_environment")
    def test_nfse_installed_switches_nfse_environment(self, mock_switch):
        with patch.object(
            type(self.env["ir.module.module"]),
            "search",
            side_effect=self._module_search_side_effect({"l10n_br_nfse"}),
        ):
            post_init_hook(self.env)

        mock_switch.assert_called_once()
        args = mock_switch.call_args[0]
        self.assertEqual(args[3], "nfse_environment")
        self.assertEqual(args[4], "2")
        self.assertEqual(args[5], "NFSe")

    @patch(f"{_MODULE}._switch_environment")
    def test_both_modules_installed_switches_both(self, mock_switch):
        with patch.object(
            type(self.env["ir.module.module"]),
            "search",
            side_effect=self._module_search_side_effect(
                {"l10n_br_nfe", "l10n_br_nfse"}
            ),
        ):
            post_init_hook(self.env)

        self.assertEqual(mock_switch.call_count, 2)
        switched_fields = {c[0][3] for c in mock_switch.call_args_list}
        self.assertIn("nfe_environment", switched_fields)
        self.assertIn("nfse_environment", switched_fields)

    @patch(f"{_MODULE}._switch_environment")
    def test_no_module_installed_no_switch(self, mock_switch):
        with patch.object(
            type(self.env["ir.module.module"]),
            "search",
            side_effect=self._module_search_side_effect(set()),
        ):
            post_init_hook(self.env)

        mock_switch.assert_not_called()
