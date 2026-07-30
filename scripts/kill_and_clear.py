import psycopg2

print("--- NUKING DB LOCKS AND CLEARING CRM ---")
try:
    conn = psycopg2.connect("dbname='havano_test' user='odoo' password='odoo' host='127.0.0.1' port='5432'")
    conn.autocommit = True
    cur = conn.cursor()
    
    # Forcefully terminate all other connections to drop locks
    print("Terminating dangling Postgres connections...")
    cur.execute('''
        SELECT pg_terminate_backend(pid) 
        FROM pg_stat_activity 
        WHERE datname = 'havano_test' 
        AND pid <> pg_backend_pid();
    ''')
    
    # 1. Delete all CRM leads (and cascade through the database if necessary)
    print("Deleting all leads...")
    cur.execute("TRUNCATE TABLE crm_lead CASCADE;")
    
    # 2. Reset staging tables so we can import again
    print("Resetting staging leads...")
    cur.execute("UPDATE crm_import_lead SET is_synced = False;")
    
    print("Resetting staging todos...")
    cur.execute("UPDATE crm_import_todo SET is_synced = False;")
    
    cur.close()
    conn.close()
    print("=== DATA NUKED SUCCESSFULLY. CRM IS EMPTY! ===")
    
except Exception as e:
    print(f"Error during nuclear option: {e}")
