# AssetFlow — Enterprise Asset & Resource Management for Odoo

AssetFlow is a custom Odoo 17/18 module for tracking company assets (laptops, equipment, furniture) and shared bookable resources (conference rooms, projectors) through their full lifecycle — from acquisition, to allocation, to maintenance, to retirement.

## Features

- **Asset Registry** — Central catalog of every asset with auto-generated tags (`AF-0001`, `AF-0002`, ...), category, condition, and acquisition details.
- **Categories** — Group assets by type with default warranty periods.
- **Allocation Workflow** — Check assets out to employees with an approval step (Draft → Approved → Returned), with automatic asset status sync.
- **Shared Resource Booking** — Reserve bookable resources (meeting rooms, shared equipment) on a calendar, with automatic overlap detection to prevent double-booking.
- **Maintenance Tracking** — Report issues via a Kanban board (Reported → In Progress → Resolved); the linked asset automatically flips to "Under Maintenance" and back to "Available" when resolved.
- **Full Audit Trail** — Built on `mail.thread` / `mail.activity.mixin`, so every status change, approval, and assignment is logged and followable.

## Installation

1. Copy the `asset_flow` folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Go to **Apps**, click **Update Apps List**, then search for **AssetFlow** and click **Install**.
4. (Optional) Install with demo data enabled to see sample categories, assets, and an upcoming booking pre-loaded.

## Module Structure

```
asset_flow/
├── __init__.py
├── __manifest__.py
├── data/
│   ├── ir_sequence_data.xml     # Asset tag sequence (AF-0001, AF-0002, ...)
│   └── demo_data.xml            # Sample categories, assets, and a booking
├── models/
│   ├── __init__.py
│   ├── category.py              # asset_flow.category
│   ├── asset.py                 # asset_flow.asset
│   ├── allocation.py            # asset_flow.allocation
│   ├── booking.py               # asset_flow.booking
│   └── maintenance.py           # asset_flow.maintenance
├── security/
│   └── ir.model.access.csv
└── views/
    ├── asset_views.xml
    ├── allocation_views.xml
    ├── booking_views.xml
    ├── maintenance_views.xml
    └── menus.xml
```

## Models

| Model | Description |
|---|---|
| `asset_flow.category` | Asset category with a default warranty period (in months). |
| `asset_flow.asset` | Core asset record — auto-tagged, tracked, linked to a category and current holder. |
| `asset_flow.allocation` | Check-out/check-in request linking an asset to an employee, with approval gating. |
| `asset_flow.booking` | Time-boxed reservation of a shared/bookable asset, with overlap prevention. |
| `asset_flow.maintenance` | Issue report for an asset, tracked through a Kanban pipeline. |

## Key Business Logic

- **Auto-tagging**: New assets get a sequential tag (`AF-0001`, `AF-0002`, ...) via an `ir.sequence`, unless one is explicitly provided.
- **Allocation ↔ Asset sync**: Approving an allocation sets the asset's status to `Allocated` and records the current holder; returning it resets both.
- **Booking overlap guard**: A `@api.constrains` check blocks any booking whose time window overlaps an existing, non-cancelled booking for the same asset.
- **Maintenance ↔ Asset sync**: Creating an open maintenance ticket sets the asset to `Under Maintenance`; resolving the last open ticket for that asset resets it to `Available`.

## Requirements

- Odoo 17.0 or 18.0
- Depends on Odoo's built-in `base` and `mail` modules

## License

LGPL-3