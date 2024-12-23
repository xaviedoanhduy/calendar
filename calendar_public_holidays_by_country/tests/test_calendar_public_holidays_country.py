# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common

from odoo.addons.mail.tests.common import mail_new_test_user


class TestCalendarPublicHolidaysCountry(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.tz = "Europe/Brussels"
        cls.env.user.company_id.resource_calendar_id.tz = "Europe/Brussels"
        cls.company = cls.env["res.company"].create({"name": "Test company"})
        cls.env.user.company_id = cls.company
        cls.user_employee = mail_new_test_user(
            cls.env, login="test", password="test", groups="base.group_user"
        )
        cls.user_employee_id = cls.user_employee.id
        cls.country1 = cls.env["res.country"].create(
            {
                "name": "Test Country 1",
                "code": "YY",
            }
        )
        cls.country2 = cls.env["res.country"].create(
            {
                "name": "Test Country 2",
                "code": "ZZ",
            }
        )
        cls.res_partner = cls.env["res.partner"].create(
            {"name": "Employee 1", "country_id": cls.country1.id}
        )
        cls.employee_emp = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "user_id": cls.user_employee_id,
                "address_id": cls.res_partner.id,
            }
        )
        cls.employee_emp_id = cls.employee_emp.id
        cls.holidays_type1 = cls.env["hr.leave.type"].create(
            {
                "name": "Limited",
                "requires_allocation": "yes",
                "employee_requests": "yes",
                "leave_validation_type": "hr",
                "request_unit": "day",
                "include_public_holidays_in_duration": True,
            }
        )
        cls.holidays_type2 = cls.env["hr.leave.type"].create(
            {
                "name": "Limited",
                "requires_allocation": "yes",
                "employee_requests": "yes",
                "request_unit": "day",
                "leave_validation_type": "hr",
            }
        )
        cls.leave_request = cls.env["hr.leave"].create(
            {
                "name": "Valid time period",
                "employee_id": cls.employee_emp_id,
                "holiday_status_id": cls.holidays_type2.id,
                "request_date_from": "2024-12-24",
                "request_date_to": "2024-12-26",  # 3 days
            }
        )
        cls.calendar_leave = cls.env["resource.calendar.leaves"].create(
            {
                "name": "Merry Christmas",
                "resource_id": False,
                "date_from": "2024-12-25 00:00:00",
                "date_to": "2024-12-25 23:59:59",  # 1 day
            }
        )

    def test_leave_request_with_holidays_public_standard(self):
        # leave type with not include public holidays
        self.assertEqual(self.leave_request.number_of_days, 2)
        # change leave type with include public holidays
        self.leave_request.holiday_status_id = self.holidays_type1.id
        self.assertEqual(self.leave_request.number_of_days, 3)

    def test_leave_request_with_holidays_public_have_country(self):
        # if different country, leave request will not include holidays public
        self.calendar_leave.country_id = self.country2.id
        self.assertEqual(self.leave_request.number_of_days, 3)

        # if country_id of holidays public same with country of employee
        # leave request will exclude holidays public
        self.calendar_leave.country_id = self.country1.id
        self.assertEqual(self.leave_request.number_of_days, 2)

        # also with country_id of holidays public equal False
        # holidays public will become the global holidays public
        self.calendar_leave.country_id = False
        self.assertEqual(self.leave_request.number_of_days, 2)
