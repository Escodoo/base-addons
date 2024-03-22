# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Escodoo Development Mode",
    "summary": """
        This module changes some data and parameters of the copied database that will
        be used in development or approval environments.""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/base-addons",
    "depends": [
        "fetchmail",
        "web_environment_ribbon",
    ],
    "auto_install": True,
    "post_init_hook": "post_init_hook",
}
