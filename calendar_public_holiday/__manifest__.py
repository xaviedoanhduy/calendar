# Copyright 2015 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# Copyright 2020 InitOS Gmbh
# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Calendar Holidays Public",
    "summary": """
        Manage Public Holidays
    """,
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "category": "HR/Calendar",
    "author": "Camptocamp," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/calendar",
    "depends": ["calendar"],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/calendar_public_holiday_view.xml",
        "wizards/calendar_public_holiday_next_year_wizard.xml",
    ],
}
