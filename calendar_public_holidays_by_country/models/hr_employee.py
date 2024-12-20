# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _get_public_holidays(self, date_start, date_end):
        res = super()._get_public_holidays(date_start, date_end)
        country_id = self.address_id.country_id
        if country_id:
            return res.filtered(lambda r: r.country_id.id in (country_id.id, False))
        return res
