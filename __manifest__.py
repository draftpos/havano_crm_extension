{
    'name': 'CRM Extension',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Extends CRM Lead with custom fields for data import',
    'description': """
        This module extends the standard CRM Lead/Opportunity model 
        to add custom fields required for migrating data from the old system.
    """,
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/data_import_wizard_views.xml',
        'views/todo_task_views.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
}
