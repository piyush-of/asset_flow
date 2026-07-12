# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssetMaintenance(models.Model):
    _name = 'asset_flow.maintenance'
    _description = 'Asset Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Issue Description", required=True, tracking=True)
    asset_id = fields.Many2one('asset_flow.asset', string="Asset", required=True, tracking=True)
    requested_by = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user, required=True)
    stage = fields.Selection([
        ('draft', 'Reported'),
        ('progress', 'In Progress'),
        ('fixed', 'Resolved')
    ], default='draft', string="Stage", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AssetMaintenance, self).create(vals_list)
        for record in records:
            # If created directly in an open stage, mark the asset as under maintenance
            if record.stage in ['draft', 'progress']:
                record.asset_id.write({'state': 'maintenance'})
        return records

    def write(self, vals):
        res = super(AssetMaintenance, self).write(vals)
        if 'stage' in vals:
            for record in self:
                if record.stage == 'fixed':
                    # Guard: Check if there are ANY OTHER open maintenance tickets for this asset
                    open_tickets = self.search_count([
                        ('asset_id', '=', record.asset_id.id),
                        ('stage', '!=', 'fixed'),
                        ('id', '!=', record.id)
                    ])
                    # Only return to available if no other open tickets remain
                    if not open_tickets:
                        record.asset_id.write({'state': 'available'})
                elif record.stage in ['draft', 'progress']:
                    record.asset_id.write({'state': 'maintenance'})
        return res