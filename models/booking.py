# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetBooking(models.Model):
    _name = 'asset_flow.booking'
    _description = 'Shared Resource Booking'

    asset_id = fields.Many2one('asset_flow.asset', string="Resource", domain="[('is_bookable', '=', True)]", required=True)
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, required=True)
    start_time = fields.Datetime(string="Start Time", required=True)
    end_time = fields.Datetime(string="End Time", required=True)
    state = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='upcoming', string="Status")

    @api.constrains('start_time', 'end_time', 'asset_id')
    def _check_booking_overlap(self):
        for record in self:
            if record.start_time and record.end_time:
                if record.start_time >= record.end_time:
                    raise ValidationError("The booking start time must occur prior to the end time.")

                # Look for any existing database records for this asset that cross this timeline
                overlapping_bookings = self.search([
                    ('id', '!=', record.id),
                    ('asset_id', '=', record.asset_id.id),
                    ('state', '!=', 'cancelled'),
                    ('start_time', '<', record.end_time),
                    ('end_time', '>', record.start_time)
                ])
                if overlapping_bookings:
                    raise ValidationError(f"Conflict detected: The asset '{record.asset_id.name}' is already reserved during this time framework.") 