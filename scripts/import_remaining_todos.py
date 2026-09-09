import csv
import psycopg2
import html
import re

def clean_html(val):
    if not val: return ''
    s = html.unescape(str(val))
    s = re.sub(r'<[^>]+>', ' ', s).strip()
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def clean_date(val):
    if not val or str(val).strip() == '': return None
    s = str(val).strip()
    if ' ' in s: s = s.split(' ')[0]
    parts = re.split(r'[-/]', s)
    if len(parts) == 3:
        p1, p2, p3 = parts[0], parts[1], parts[2]
        if len(p1) == 4: return f"{p1}-{p2.zfill(2)}-{p3.zfill(2)}"
        elif len(p3) == 4: return f"{p3}-{p2.zfill(2)}-{p1.zfill(2)}"
    return None

conn = psycopg2.connect(
    dbname='showline_s2_havano_pro_xcynznxmwcotukbxkm',
    user='Showline',
    password='Showline@#$1234',
    host='db',
    port=5432
)
cr = conn.cursor()

print("Pre-fetching existing ToDos and Leads...")
cr.execute("SELECT legacy_id FROM todo_task WHERE legacy_id IS NOT NULL")
existing_todos = set(r[0] for r in cr.fetchall() if r[0])

cr.execute("SELECT custom_naming_series, id, user_id FROM crm_lead WHERE custom_naming_series IS NOT NULL")
lead_map = {r[0]: (r[1], r[2]) for r in cr.fetchall() if r[0]}

cr.execute("SELECT id FROM mail_activity_type LIMIT 1")
act_type_row = cr.fetchone()
activity_type_id = act_type_row[0] if act_type_row else 1

cr.execute("SELECT id FROM ir_model WHERE model='crm.lead' LIMIT 1")
model_row = cr.fetchone()
lead_model_id = model_row[0] if model_row else False

todo_csv = '/mnt/extra-addons/havano_crm_extension/data_import/ToDo.csv'
to_insert = []
activities_to_insert = []

with open(todo_csv, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for r in reader:
        tid = (r.get('ID') or r.get('name') or '').strip().strip('"')
        if not tid or tid in existing_todos:
            continue
        
        existing_todos.add(tid)
        ref_name = (r.get('Reference Name') or r.get('reference_name') or '').strip().strip('"')
        lead_info = lead_map.get(ref_name)
        lead_id = lead_info[0] if lead_info else None
        sp_id = lead_info[1] if (lead_info and lead_info[1]) else 2
        
        status = (r.get('Status') or 'Open').strip().capitalize()
        desc_raw = (r.get('Description') or '').strip().strip('"')
        desc = clean_html(desc_raw)
        subj = desc[:80] if desc else 'Imported ToDo'
        due_date = clean_date(r.get('date') or r.get('Due Date'))
        creation_date = clean_date(r.get('creation') or r.get('Qualified on'))
        allocated_to = (r.get('owner') or r.get('Assigned By') or '').strip().strip('"')
        
        to_insert.append((
            subj, status, allocated_to, lead_id, due_date, desc, tid, ref_name, 'crm.lead',
            creation_date or '2026-01-01', creation_date or '2026-01-01'
        ))
        
        if status == 'Open' and lead_id:
            activities_to_insert.append((
                lead_model_id, lead_id, 'crm.lead', activity_type_id,
                subj[:250], desc if desc and desc != subj else '',
                due_date or '2026-09-09', sp_id, True
            ))

print(f"Found {len(to_insert):,} remaining To-Dos to insert...")
if to_insert:
    # Bulk insert into todo_task
    batch_size = 500
    for i in range(0, len(to_insert), batch_size):
        chunk = to_insert[i:i + batch_size]
        query = """
            INSERT INTO todo_task (
                name, status, allocated_to, lead_id, date, description, legacy_id, reference_name, reference_type,
                create_date, legacy_create_date
            ) VALUES %s
        """
        import psycopg2.extras
        psycopg2.extras.execute_values(cr, query, chunk)
        conn.commit()
    print(f"Successfully inserted all {len(to_insert):,} remaining To-Dos!")

if activities_to_insert:
    for i in range(0, len(activities_to_insert), batch_size):
        chunk = activities_to_insert[i:i + batch_size]
        act_query = """
            INSERT INTO mail_activity (
                res_model_id, res_id, res_model, activity_type_id,
                summary, note, date_deadline, user_id, active
            ) VALUES %s
        """
        import psycopg2.extras
        psycopg2.extras.execute_values(cr, act_query, chunk)
        conn.commit()
    print(f"Successfully inserted {len(activities_to_insert):,} corresponding CRM activities!")

print("Import of remaining To-Dos is 100% COMPLETE!")
