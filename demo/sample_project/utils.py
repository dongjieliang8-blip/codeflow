MAGIC_NUMBER = 86400  # unexplained constant

def do_stuff(a, b):
    # unclear naming
    x = a * MAGIC_NUMBER
    y = b * MAGIC_NUMBER
    return x + y

def fetch_all():
    # N+1 query pattern
    users = db_query("SELECT id FROM users")
    results = []
    for u in users:
        results.append(db_query(f"SELECT * FROM profiles WHERE user_id = {u['id']}"))
    return results

def db_query(sql):
    print(f"Executing: {sql}")
    return [{"id": 1}, {"id": 2}]
