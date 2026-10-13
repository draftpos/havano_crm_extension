{
    'name': 'Havano CRM Extension',
    'version': '1.2',
    'category': 'Sales/CRM',
    'summary': 'Extends CRM Lead with custom fields for data import, product interest & activity tracking',
    'description': """
Havano CRM Extension
====================
* Extends standard CRM Lead/Opportunity with custom fields for legacy migrations.
* Adds CRM Product Interest association with find_or_create logic.
* Computes accurate activity deadlines across tasks, chatters, and activities.
* Unifies contact, deal, and address details into a clean 3-column layout.
    """,
    'author': 'DraftPOS / Havano Solutions',
    'website': 'https://draftpos.com',
    'license': 'LGPL-3',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_product_data.xml',
        'wizard/crm_import_wizard_views.xml',
        'views/crm_product_views.xml',
        'views/todo_task_views.xml',
        'views/crm_lead_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
}
