import sqlite3

conn = sqlite3.connect('promptos.db')
cur = conn.cursor()

cur.execute('SELECT id, title, created_at FROM prompt_history ORDER BY created_at ASC')
rows = cur.fetchall()
print(f'Total records: {len(rows)}')
for i, r in enumerate(rows):
    print(f'{i+1}. [{r[2]}] {r[1][:60]}')

if len(rows) <= 3:
    print('\nAlready 3 or fewer records. Nothing to delete.')
else:
    ids_to_keep = [r[0] for r in rows[:3]]
    placeholders = ','.join('?' * len(ids_to_keep))
    cur.execute(f'DELETE FROM prompt_history WHERE id NOT IN ({placeholders})', ids_to_keep)
    conn.commit()
    remaining = cur.execute('SELECT COUNT(*) FROM prompt_history').fetchone()[0]
    print(f'\nDeleted {len(rows) - remaining} record(s). {remaining} record(s) remaining.')

conn.close()
