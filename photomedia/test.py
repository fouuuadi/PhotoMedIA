import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="wheres3modestin",
        host="aws-0-eu-west-3.pooler.supabase.com",
        port="5432",
        sslmode="require"
    )
    print("✅ Connexion réussie à la base PostgreSQL")
except Exception as e:
    print("❌ Erreur de connexion :", e)