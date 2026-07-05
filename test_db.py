import psycopg2

try:
    # Usamos psycopg2 en lugar de asyncpg para ver el error real
    conn = psycopg2.connect("postgresql://postgres:sugi2026@127.0.0.1:5432/sugi")
    print("¡Conexión exitosa, papu! El problema es 100% de asyncpg.")
    conn.close()
except Exception as e:
    print("EL ERROR REAL DE POSTGRES ES:")
    print(e)