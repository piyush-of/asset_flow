# -*- coding: utf-8 -*-

from odoo import fields, models


class AssetFlowCategory(models.Model):
    _name = 'asset_flow.category'
    _description = 'Asset Category'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
    )
    warranty_period = fields.Integer(
        string='Warranty Period (Months)',
        help='Default warranty period, in months, for assets in this category.',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
