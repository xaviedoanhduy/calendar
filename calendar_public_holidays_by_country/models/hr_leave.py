# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from pytz import UTC

from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        self = self.with_context(employee_id=self.employee_id.id)
        return super()._get_durations(check_leave_type, resource_calendar)

    def _get_domain_from_get_unusual_days(self, date_from, date_to=None):
        domain = [("date_from", ">=", date_from)]
        employee_id = self.env.context.get("employee_id", False)
        employee = (
            self.env["hr.employee"].browse(employee_id)
            if employee_id
            else self.env.user.employee_id
        )
        if date_to:
            domain.append(
                (
                    "date_to",
                    "<",
                    date_to,
                )
            )
        country_id = employee.address_id.country_id
        if country_id:
            domain.append(("country_id", "in", (country_id.id, False)))
        return domain

    @api.model
    def get_unusual_days(self, date_from, date_to=None):
        domain = self._get_domain_from_get_unusual_days(
            date_from=date_from, date_to=date_to
        )
        calendar_leaves = self.env["resource.calendar.leaves"].search(domain)
        if not calendar_leaves:
            return super().get_unusual_days(date_from, date_to)
        unusual_days = {}
        for leaf in calendar_leaves:
            calendar_id = leaf.calendar_id
            unusual_days.update(
                calendar_id.sudo(False)._get_unusual_days(
                    datetime.combine(
                        fields.Date.from_string(leaf.date_from), time.min
                    ).replace(tzinfo=UTC),
                    datetime.combine(
                        fields.Date.from_string(leaf.date_to), time.max
                    ).replace(tzinfo=UTC),
                )
            )
        return unusual_days
