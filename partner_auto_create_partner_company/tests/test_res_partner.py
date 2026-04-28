# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerAutoCreateCompany(TransactionCase):
    def test_create_with_company_name_creates_parent_company(self):
        partner = self.env["res.partner"].create(
            {"name": "John Doe", "company_name": "Acme Corp"}
        )
        self.assertTrue(partner.parent_id)
        self.assertEqual(partner.parent_id.name, "Acme Corp")
        self.assertTrue(partner.parent_id.is_company)

    def test_create_without_company_name_does_not_create_parent(self):
        partner = self.env["res.partner"].create({"name": "Jane Doe"})
        self.assertFalse(partner.parent_id)

    def test_create_with_parent_id_does_not_create_company(self):
        company = self.env["res.partner"].create(
            {"name": "Existing Corp", "is_company": True}
        )
        partner = self.env["res.partner"].create(
            {"name": "Bob", "parent_id": company.id, "company_name": "Other Corp"}
        )
        self.assertEqual(partner.parent_id, company)

    def test_write_company_name_creates_parent_company(self):
        partner = self.env["res.partner"].create({"name": "Alice"})
        self.assertFalse(partner.parent_id)
        partner.write({"company_name": "New Company"})
        self.assertTrue(partner.parent_id)
        self.assertEqual(partner.parent_id.name, "New Company")
        self.assertTrue(partner.parent_id.is_company)

    def test_write_without_company_name_does_not_create_parent(self):
        partner = self.env["res.partner"].create({"name": "Charlie"})
        partner.write({"email": "charlie@example.com"})
        self.assertFalse(partner.parent_id)

    def test_create_multi_with_company_name(self):
        partners = self.env["res.partner"].create(
            [
                {"name": "Partner A", "company_name": "Company A"},
                {"name": "Partner B", "company_name": "Company B"},
                {"name": "Partner C"},
            ]
        )
        self.assertTrue(partners[0].parent_id)
        self.assertEqual(partners[0].parent_id.name, "Company A")
        self.assertTrue(partners[1].parent_id)
        self.assertEqual(partners[1].parent_id.name, "Company B")
        self.assertFalse(partners[2].parent_id)

    def test_skip_fields_sync_context_skips_auto_create(self):
        partner = (
            self.env["res.partner"]
            .with_context(_partners_skip_fields_sync=True)
            .create({"name": "Skip Me", "company_name": "Should Not Exist"})
        )
        self.assertFalse(partner.parent_id)
