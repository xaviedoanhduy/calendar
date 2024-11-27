# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import api, models


class HrHolidaysPublic(models.Model):
    _inherit = "hr.holidays.public"

    def _get_domain_states_filter(
        self, pholidays, start_dt, end_dt, employee_id=None, partner_id=None
    ):
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            domain = [
                ("year_id", "in", pholidays.ids),
                ("date", ">=", start_dt),
                ("date", "<=", end_dt),
            ]
            if partner and partner.state_id:
                domain.extend(
                    [
                        "|",
                        ("state_ids", "=", False),
                        ("state_ids", "=", partner.state_id.id),
                    ]
                )
            else:
                domain.append(("state_ids", "=", False))
            return domain
        return super()._get_domain_states_filter(
            pholidays, start_dt, end_dt, employee_id
        )

    @api.model
    @api.returns("hr.holidays.public.line")
    def get_holidays_list(
        self, year=None, start_dt=None, end_dt=None, employee_id=None, partner_id=None
    ):
        """
        Returns recordset of hr.holidays.public.line
        for the specified year and employee
        :param year: year as string (optional if start_dt and end_dt defined)
        :param start_dt: start_dt as date
        :param end_dt: end_dt as date
        :param employee_id: ID of the employee
        :param partner_id: ID of the partner
        :return: recordset of hr.holidays.public.line
        """
        if partner_id:
            if not start_dt and not end_dt:
                start_dt = datetime.date(year, 1, 1)
                end_dt = datetime.date(year, 12, 31)
            years = list(range(start_dt.year, end_dt.year + 1))
            holidays_filter = [("year", "in", years)]
            partner = self.env["res.partner"].browse(partner_id)
            if partner:
                if partner.country_id:
                    holidays_filter.extend(
                        [
                            "|",
                            ("country_id", "=", False),
                            ("country_id", "=", partner.country_id.id),
                        ]
                    )
                else:
                    holidays_filter.append(("country_id", "=", False))
            pholidays = self.search(holidays_filter)
            if not pholidays:
                return self.env["hr.holidays.public.line"]
            states_filter = self._get_domain_states_filter(
                pholidays, start_dt, end_dt, partner_id=partner.id
            )
            return self.env["hr.holidays.public.line"].search(states_filter)
        return super().get_holidays_list(
            year, start_dt, end_dt, employee_id=employee_id
        )

    @api.model
    def is_public_holiday(self, selected_date, employee_id=None, partner_id=None):
        """
        Returns True if selected_date is a public holiday for the employee
        :param selected_date: datetime object
        :param employee_id: ID of the employee
        :param partner_id: ID of the partner
        :return: bool
        """
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if partner:
                holidays_lines = self.get_holidays_list(
                    year=selected_date.year,
                    partner_id=partner.id,
                    employee_id=employee_id,
                )
                if holidays_lines:
                    hol_date = holidays_lines.filtered(
                        lambda r: r.date == selected_date
                    )
                    if hol_date.ids:
                        return True
            return False
        return super().is_public_holiday(selected_date, employee_id=employee_id)
