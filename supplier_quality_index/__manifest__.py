# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Supplier Quality Index",
    "summary": """
        SQI (Supplier Quality Index)""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/base-addons",
    "depends": [
        "account",
    ],
    "data": [
        "security/res_partner_sqi_profile.xml",
        "views/res_partner_sqi_profile.xml",
        "views/res_partner.xml",
        "data/res_partner_update_sqi_cron.xml",
    ],
    "demo": [
        "demo/res_partner_sqi_profile.xml",
    ],
}
