from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # ── ERPNext Legacy Fields ──────────────────────────────────────────────────
    custom_naming_series   = fields.Char(string='Legacy ID (ERPNext)')
    custom_lead_source     = fields.Char(string='Lead Source (Legacy)')
    custom_territory       = fields.Char(string='Territory')
    custom_industry        = fields.Char(string='Industry')

    # Product & Deal Info
    custom_product         = fields.Char(string='Product Interest')
    custom_deal_size       = fields.Float(string='Deal Size')
    custom_type_of_business= fields.Char(string='Type of Business')

    # Quote Info
    custom_quote           = fields.Selection([
        ('Quote', 'Quoted'),
        ('Not yet Quoted', 'Not Yet Quoted'),
    ], string='Quote Status')
    custom_quote_date      = fields.Date(string='Quote Date')

    # Technician / Assignment
    custom_technician      = fields.Char(string='Technician Assigned')

    # Demo
    custom_demo_done       = fields.Boolean(string='Demo Done')

    # Preserve actual dates from the old system
    legacy_create_date     = fields.Datetime(string='Original Creation Date')

    # Link to our To-Do tasks
    todo_ids = fields.One2many('todo.task', 'lead_id', string='To-Do Tasks')
