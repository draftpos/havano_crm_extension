from odoo import models, fields, api

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

    # Computed latest To-Do note for display in list views
    last_todo_note = fields.Text(
        string='Last To-Do / Note',
        compute='_compute_last_todo_note',
        store=True,
        help='Displays the most recent To-Do or note attached to this lead.'
    )

    @api.depends('todo_ids', 'todo_ids.name', 'todo_ids.date', 'todo_ids.create_date')
    def _compute_last_todo_note(self):
        for record in self:
            if record.todo_ids:
                latest_todo = record.todo_ids.sorted(
                    key=lambda t: (t.date or t.create_date or False, t.id),
                    reverse=True
                )[0]
                record.last_todo_note = latest_todo.name
            else:
                record.last_todo_note = False


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure context flag prevents infinite recursive creation loop
        if self.env.context.get('skip_todo_sync'):
            return super().create(vals_list)

        activities = super().create(vals_list)
        TodoTask = self.env['todo.task'].sudo()
        for activity in activities:
            if activity.res_model == 'crm.lead' and activity.res_id:
                subject_parts = []
                if activity.activity_type_id:
                    subject_parts.append(activity.activity_type_id.name)
                if activity.summary:
                    subject_parts.append(activity.summary)
                elif activity.note:
                    import re
                    clean_note = re.sub(r'<[^>]+>', ' ', activity.note)
                    clean_note = re.sub(r'\s+', ' ', clean_note).strip()
                    if clean_note:
                        subject_parts.append(clean_note[:80])
                
                subject = " : ".join(subject_parts) if subject_parts else "New Activity"
                
                TodoTask.create({
                    'name': subject,
                    'status': 'Open',
                    'date': activity.date_deadline or fields.Date.today(),
                    'lead_id': activity.res_id,
                    'allocated_to': activity.user_id.name if activity.user_id else False,
                    'description': activity.note or activity.summary or False,
                })
                lead = self.env['crm.lead'].browse(activity.res_id)
                if lead.exists():
                    lead._compute_last_todo_note()
        return activities
