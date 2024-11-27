# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Calendar Holidays Public",
    "summary": """
        Helper functions to find public holidays did allow to use an hr.employee
to filter country and states based on the employee address.

Since only the address of the employee was used, modifying the functions
to use a res.partner instead of an hr.employee allows more possibilities
such as checking public holidays for customers and suppliers.
    """,
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/calendar",
    "depends": [
        "hr_holidays_public",
    ],
}
