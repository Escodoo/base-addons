# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)

        if self.env.context.get("_partners_skip_fields_sync"):
            return partners

        for partner, vals in zip(partners, vals_list):
            partner._fields_sync(vals)
            if not partner.parent_id and partner.company_name:
                partner.create_company()
        return partners

    def write(self, vals):
        res = super().write(vals)
        if vals.get("company_name"):
            self.create_company()
        return res
