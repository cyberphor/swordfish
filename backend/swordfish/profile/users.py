from psycopg2 import connect


def create_user_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, user_id TEXT, last_name TEXT, first_name TEXT, email_address TEXT, user_name TEXT)"
    )
    connection.commit()
    connection.close()


def get_user(user_id: str):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT user_id, last_name, first_name, email_address, user_name FROM users WHERE user_id =  %s ORDER BY created_at",
        (user_id,),
    )
    rows = cursor.fetchall()
    connection.close()
    if not rows:
        return None
    return rows


def create_user(
    user_id: str, last_name: str, first_name: str, email_address: str, user_name: str
):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, last_name, first_name, email_address, user_name) VALUES (%s, %s, %s, %s, %s)",
        (user_id, last_name, first_name, email_address, user_name),
    )
    connection.commit()
    connection.close()


def get_or_create_user_handler(
    user_id: str, last_name: str, first_name: str, email_address: str, user_name: str
):
    rows = get_user(user_id)
    if not rows:
        create_user(user_id, last_name, first_name, email_address, user_name)
    rows = get_user(user_id)
    return rows[0]
