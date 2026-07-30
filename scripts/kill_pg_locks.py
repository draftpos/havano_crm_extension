import sys
import os

sys.path.append(os.path.abspath(r'C:\Users\DELL\Desktop\odoo'))
import odoo
from odoo import tools

tools.config.parse_config(['-c', r'C:\Users\DELL\Desktop\odoo\odoo.conf', '-d', 'havano_test'])
import odoo.sql_db

db = odoo.sql_db.db_connect('havano_test')
with db.cursor() as cr:
    cr.execute("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = 'havano_test'
          AND pid <> pg_backend_pid()
          AND state = 'active'
    """)
    res = cr.fetchall()
    print("Terminated backend PIDs:", res)
