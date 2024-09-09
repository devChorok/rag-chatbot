import sqlite3

def init_db():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (query TEXT, response TEXT, latency REAL)''')
    conn.commit()
    conn.close()

def store_response(query, response, latency):
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("INSERT INTO responses (query, response, latency) VALUES (?, ?, ?)",
              (query, response, latency))
    conn.commit()
    conn.close()
