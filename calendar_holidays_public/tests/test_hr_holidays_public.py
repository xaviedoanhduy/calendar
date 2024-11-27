# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.addons.hr_holidays_public.tests.test_holidays_public import TestHolidaysPublic


class TestHolidaysPublicCalendar(TestHolidaysPublic):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.employee.address_id

    def test_is_not_holiday_in_country(self):
        self.assertFalse(
            self.holiday_model.is_public_holiday(
                date(1994, 11, 14), partner_id=self.partner.id
            )
        )

    def test_is_holiday_in_country(self):
        self.assertTrue(
            self.holiday_model.is_public_holiday(
                date(1994, 10, 14), partner_id=self.partner.id
            )
        )

    def test_list_holidays_in_list_country_specific(self):
        lines = self.holiday_model.get_holidays_list(1994, partner_id=self.partner.id)
        res = lines.filtered(lambda r: r.date == date(1994, 10, 14))
        self.assertEqual(len(res), 1)
        self.assertEqual(len(lines), 1)
