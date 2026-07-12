# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AssetFlowAsset(models.Model):
    _name = 'asset_flow.asset'
    _description = 'Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )
    asset_tag = fields.Char(
        string='Asset Tag',
        readonly=True,
        copy=False,
        default='New',
    )
    category_id = fields.Many2one(
        comodel_name='asset_flow.category',
        string='Category',
        required=True,
    )
    serial_number = fields.Char(
        string='Serial Number',
    )
    acquisition_date = fields.Date(
        string='Acquisition Date',
        default=fields.Date.context_today,
    )
    acquisition_cost = fields.Float(
        string='Acquisition Cost',
    )
    condition = fields.Selection(
        selection=[
            ('new', 'New'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('damaged', 'Damaged'),
        ],
        string='Condition',
        default='new',
    )
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('allocated', 'Allocated'),
            ('reserved', 'Reserved'),
            ('maintenance', 'Under Maintenance'),
            ('lost', 'Lost'),
            ('retired', 'Retired'),
            ('disposed', 'Disposed'),
        ],
        string='Status',
        default='available',
        tracking=True,
    )
    is_bookable = fields.Boolean(
        string='Shared / Bookable Resource',
        default=False,
    )
    current_holder_id = fields.Many2one(
        comodel_name='res.users',
        string='Current Holder',
        readonly=True,
    )

    _sql_constraints = [
        (
            'asset_tag_unique',
            'unique(asset_tag)',
            'The Asset Tag must be unique across all assets!',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('asset_tag', 'New') == 'New':
                vals['asset_tag'] = self.env['ir.sequence'].next_by_code(
                    'asset_flow.asset'
                ) or 'New'
        return super().create(vals_list)
