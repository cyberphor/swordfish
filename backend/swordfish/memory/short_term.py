from psycopg2 import connect


def create_chat_history_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS chat_history (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, session_id TEXT, query TEXT, response TEXT)"
    )
    connection.commit()
    connection.close()


def save_chat_history(session_id, query, response):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO chat_history (session_id, query, response) VALUES (%s, %s, %s)",
        (session_id, query, response),
    )
    connection.commit()
    connection.close()


def get_chat_history(session_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT query, response FROM chat_history WHERE session_id =  %s ORDER BY created_at",
        (session_id,),
    )
    messages = []
    for row in cursor.fetchall():
        messages.extend(
            [
                {"role": "user", "content": row[0]},
                {"role": "assistant", "content": row[1]},
            ]
        )
    connection.close()
    return messages
