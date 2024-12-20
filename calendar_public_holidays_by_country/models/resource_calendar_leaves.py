# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    country_id = fields.Many2one("res.country", "Country")
