# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Calendar Public Holidays By Country",
    "summary": """Helps manage public holidays by country""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Camptocamp," "Odoo Community Association (OCA)",
    "maintainers": ["xaviedoanhduy"],
    "website": "https://github.com/OCA/calendar",
    "depends": [
        "hr_holidays",
    ],
    "data": [
        "views/resource_calendar_leaves_view.xml",
    ],
    "installable": True,
}
