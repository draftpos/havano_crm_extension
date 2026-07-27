from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # ── ERPNext Legacy Fields ──────────────────────────────────────────────────
    custom_naming_series   = fields.Char(string='Legacy ID (ERPNext)')
    custom_lead_source     = fields.Char(string='Lead Source (Legacy)')
    custom_territory       = fields.Char(string='Territory')
    custom_industry        = fields.Char(string='Industry')

    # Product & Deal Info - Many2one selection to product catalog
    product_id             = fields.Many2one('product.product', string='Product Interest')
    custom_product         = fields.Char(string='Product Interest (Legacy)')
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
    custom_demo_type       = fields.Selection([
        ('Online', 'Online'),
        ('Onsite', 'Onsite'),
        ('N/A', 'N/A'),
    ], string='Demo Done Online or Onsite')

    # Proposal
    custom_proposal_status = fields.Selection([
        ('Not Yet', 'Not Yet'),
        ('Proposed', 'Proposed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ], string='Proposal')
    custom_proposal_date   = fields.Date(string='Proposal Date')

    # Preserve actual dates from the old system
    legacy_create_date     = fields.Datetime(string='Original Creation Date')

    # Link to To-Do tasks
    todo_ids = fields.One2many('todo.task', 'lead_id', string='To-Do Tasks')

    # Computed latest Activity / To-Do note for display in list views
    last_todo_note = fields.Text(
        string='Last To-Do / Note',
        compute='_compute_last_todo_note',
        store=True,
        help='Displays the most recent Activity or To-Do note attached to this lead.'
    )

    @api.depends('activity_ids', 'activity_ids.summary', 'activity_ids.note', 'activity_ids.date_deadline', 'todo_ids', 'todo_ids.name')
    def _compute_last_todo_note(self):
        for record in self:
            note_val = False
            if record.activity_ids:
                latest_act = record.activity_ids.sorted(
                    key=lambda a: (a.date_deadline or a.create_date or False, a.id),
                    reverse=True
                )[0]
                note_val = latest_act.summary or latest_act.note
            if not note_val and record.todo_ids:
                latest_todo = record.todo_ids.sorted(
                    key=lambda t: (t.date or t.create_date or False, t.id),
                    reverse=True
                )[0]
                note_val = latest_todo.name
            
            record.last_todo_note = note_val
