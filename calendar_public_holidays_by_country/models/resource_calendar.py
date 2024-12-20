# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from pytz import timezone

from odoo import models

from odoo.addons.resource.models.resource_resource import Intervals
from odoo.addons.resource.models.utils import datetime_to_string, string_to_datetime


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def _leave_intervals_batch(
        self, start_dt, end_dt, resources=None, domain=None, tz=None, any_calendar=False
    ):
        employee_id = self.env.context.get("employee_id")
        if not employee_id:
            return super()._leave_intervals_batch(
                start_dt, end_dt, resources, domain, tz, any_calendar
            )
        employee = self.env["hr.employee"].browse(employee_id)
        if not (employee.address_id and employee.address_id.country_id):
            return super()._leave_intervals_batch(
                start_dt, end_dt, resources, domain, tz, any_calendar
            )
        if not resources:
            resources = self.env["resource.resource"]
            resources_list = [resources]
        else:
            resources_list = list(resources) + [self.env["resource.resource"]]
        if domain is None:
            domain = [("time_type", "=", "leave")]
        if not any_calendar:
            domain += [("calendar_id", "in", [False, self.id])]
        # for the computation, express all datetimes in UTC
        # Public leave don't have a resource_id
        domain += [
            ("resource_id", "in", [False] + [r.id for r in resources_list]),
            ("date_from", "<=", datetime_to_string(end_dt)),
            ("date_to", ">=", datetime_to_string(start_dt)),
            ("country_id", "in", (False, employee.address_id.country_id.id)),
        ]
        result = defaultdict(lambda: [])
        tz_dates = {}
        all_leaves = self.env["resource.calendar.leaves"].search(domain)
        for leave in all_leaves:
            leave_resource = leave.resource_id
            leave_company = leave.company_id
            leave_date_from = leave.date_from
            leave_date_to = leave.date_to
            for resource in resources_list:
                if leave_resource.id not in [False, resource.id] or (
                    not leave_resource
                    and resource
                    and resource.company_id != leave_company
                ):
                    continue
                tz = tz if tz else timezone((resource or self).tz)
                if (tz, start_dt) in tz_dates:
                    start = tz_dates[(tz, start_dt)]
                else:
                    start = start_dt.astimezone(tz)
                    tz_dates[(tz, start_dt)] = start
                if (tz, end_dt) in tz_dates:
                    end = tz_dates[(tz, end_dt)]
                else:
                    end = end_dt.astimezone(tz)
                    tz_dates[(tz, end_dt)] = end
                dt0 = string_to_datetime(leave_date_from).astimezone(tz)
                dt1 = string_to_datetime(leave_date_to).astimezone(tz)
                result[resource.id].append((max(start, dt0), min(end, dt1), leave))
        return {r.id: Intervals(result[r.id]) for r in resources_list}
