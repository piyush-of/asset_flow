# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetAllocation(models.Model):
    _name = 'asset_flow.allocation'
    _description = 'Asset Allocation Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    asset_id = fields.Many2one('asset_flow.asset', string="Asset", required=True, tracking=True)
    employee_id = fields.Many2one('res.users', string="Employee", default=lambda self: self.env.user, required=True, tracking=True)
    expected_return_date = fields.Date(string="Expected Return Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('returned', 'Returned')
    ], default='draft', string="Status", tracking=True)

    @api.constrains('state', 'asset_id')
    def _check_asset_availability(self):
        for record in self:
            if record.state == 'approved':
                # Block approval if the asset is already checked out or broken
                if record.asset_id.state in ['allocated', 'maintenance']:
                    raise ValidationError(f"The asset '{record.asset_id.name}' cannot be allocated because its current status is '{record.asset_id.state}'.")

    def action_approve(self):
        for record in self:
            record._check_asset_availability()
            record.write({'state': 'approved'})
            # Automatically update the parent asset's tracking metrics
            record.asset_id.write({
                'state': 'allocated',
                'current_holder_id': record.employee_id.id
            })

    def action_return(self):
        for record in self:
            if record.state != 'approved':
                raise ValidationError("Only approved allocations can be returned.")
        record.write({'state': 'returned'})
        record.asset_id.write({'state': 'available', 'current_holder_id': False})
            
        