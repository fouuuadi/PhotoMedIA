import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgresql",
        user="postgres",
        password="wheres3modestin",
        host="db.qspoobpdyzacfhedlisn.supabase.co",
        port="5432",
        sslmode="require"
    )
    print("✅ Connexion réussie à la base PostgreSQL")
except Exception as e:
    print("❌ Erreur de connexion :", e)