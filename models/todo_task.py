from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Imported To-Do Task'

    name = fields.Char(string='Subject', required=True)
    status = fields.Selection([
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled')
    ], string='Status', default='Open')
    
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    
    # Linking ToDo to Lead
    # Link to our new To-Do tasks
    lead_id = fields.Many2one('crm.lead', string='Related Lead / Opportunity')
    
    # Other potential imported fields
    allocated_to = fields.Char(string='Allocated To (Old System)')
    reference_type = fields.Char(string='Reference Type')
    reference_name = fields.Char(string='Reference Name')
    
    legacy_create_date = fields.Datetime(string='Original Creation Date')
