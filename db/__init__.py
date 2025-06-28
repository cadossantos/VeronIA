# import psycopg

# conn = psycopg.connect(
#     dbname="minimo",
#     user="minimo",
#     password="FolhadeArruda",
#     host="localhost",
#     port=5433
# )

# with conn.cursor() as cur:
#     cur.execute("SELECT version();")
#     print(cur.fetchone())
