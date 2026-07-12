from psycopg2 import connect


def create_emu_config_profile_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS emu_config_profiles (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            user_id TEXT,
            user_uid TEXT,
            api_key TEXT,
            public_key_name TEXT,
            public_key_bytes BYTEA,
            private_key_name TEXT,
            private_key_bytes BYTEA
        )""")
    connection.commit()
    connection.close()


def create_emu_config_profile_handler(
    name: str,
    user_id: str,
    user_uid: str,
    api_key: str,
    public_key_name: str,
    public_key: bytes,
    private_key_name: str,
    private_key: bytes,
):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO emu_config_profiles (
            name, user_id, user_uid, api_key, public_key_name, public_key_bytes, private_key_name, private_key_bytes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
        (
            name,
            user_id,
            user_uid,
            api_key,
            public_key_name,
            public_key,
            private_key_name,
            private_key,
        ),
    )
    connection.commit()
    connection.close()


def get_emu_config_profiles_by_user(user_id: str) -> list:
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """SELECT name, user_id, user_uid, api_key, public_key_name, public_key_bytes, private_key_name, private_key_bytes
           FROM emu_config_profiles
           WHERE user_id = %s
           ORDER BY created_at""",
        (user_id,),
    )
    rows = cursor.fetchall()
    connection.close()
    return [
        {
            "name": row[0],
            "user_id": row[1],
            "user_uid": row[2],
            "api_key": row[3],
            "public_key_name": row[4],
            "public_key_bytes": bytes(row[5]),
            "private_key_name": row[6],
            "private_key_bytes": bytes(row[7]),
        }
        for row in rows
    ]
