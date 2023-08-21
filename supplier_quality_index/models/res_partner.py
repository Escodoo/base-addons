# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from datetime import datetime

from pytz import timezone

import odoo
from odoo import fields, models, tools
from odoo.tools.float_utils import float_compare
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):

    _inherit = "res.partner"

    sqi_profile_id = fields.Many2one(
        comodel_name="res.partner.sqi.profile", string="SQI Profile", tracking=True
    )
    sqi_value = fields.Integer(string="SQI Value", tracking=True, readonly=True)
    sqi_value_date = fields.Datetime(
        string="SQI Value Date", tracking=True, readonly=True
    )

    def _get_domain(self):

        domain = [("active", "=", True), ("sqi_profile_id", "!=", False)]

        return domain

    def _get_eval_context(self, profile=None):
        """Prepare the context used when evaluating python code, like the
        python formulas or code server actions.

        :param profile: the current sqi profile
        :type profile: browse record
        :returns: dict -- evaluation context given to (safe_)safe_eval"""

        def log(message, level="info"):
            with self.pool.cursor() as cr:
                cr.execute(
                    """
                    INSERT INTO ir_logging(create_date, create_uid, type, dbname, name, level,
                    message, path, line, func)
                    VALUES (NOW() at time zone 'UTC', %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        self.env.uid,
                        "server",
                        self._cr.dbname,
                        __name__,
                        level,
                        message,
                        "profile",
                        profile.id,
                        profile.name,
                    ),
                )

        eval_context = {
            "uid": self._uid,
            "user": self.env.user,
            "time": tools.safe_eval.time,
            "datetime": tools.safe_eval.datetime,
            "dateutil": tools.safe_eval.dateutil,
            "timezone": timezone,
            "float_compare": float_compare,
            "b64encode": base64.b64encode,
            "b64decode": base64.b64decode,
        }

        model_name = self._name
        model = self.env[model_name]
        record = self.id
        records = None
        eval_context.update(
            {
                # orm
                "env": self.env,
                "model": model,
                # Exceptions
                "Warning": odoo.exceptions.Warning,
                "UserError": odoo.exceptions.UserError,
                # record
                "record": record,
                "records": records,
                # helpers
                "log": log,
            }
        )
        return eval_context

    def update_sqi(self):
        for partner in self.search(self._get_domain()):
            if partner.sqi_profile_id:
                eval_context = partner._get_eval_context(profile=partner.sqi_profile_id)
                code = partner.sqi_profile_id.code.strip()
                safe_eval(code, eval_context, mode="exec", nocopy=True)
                result = eval_context.get("result")
                values = {"sqi_value": result, "sqi_value_date": datetime.today()}
                partner.write(values)
