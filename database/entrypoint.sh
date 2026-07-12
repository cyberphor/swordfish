#!/usr/bin/env sh
 
set -e
 
# Initialize Postgres.
if [ ! -f "/var/lib/postgresql/data/PG_VERSION" ]; then
  # Create the prerequisite databases.
  initdb -D /var/lib/postgresql/data
 
  # Start Postgres as a background process.
  postgres -D /var/lib/postgresql/data &
  POSTGRES_PID=$!
 
  # Wait for Postgres to start.
  until pg_isready; do
    sleep 1
  done

  # On first boot, set the password and then, create the database and tables required.
  psql -U "$PGUSER" -d postgres -c "ALTER USER postgres WITH PASSWORD '$PGPASSWORD';"
  psql -U "$PGUSER" -d postgres -c "CREATE DATABASE $PGDATABASE;"
  psql -U "$PGUSER" -d $PGDATABASE <<EOF
    CREATE TABLE emu_profiles (
      id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      profile_name TEXT        NOT NULL,
      api_key      TEXT        NOT NULL,
      public_cert  TEXT        NOT NULL,
      private_cert TEXT        NOT NULL,
      owner_uid    TEXT        NOT NULL,
      is_active    BOOLEAN     NOT NULL DEFAULT TRUE,
      created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
      CONSTRAINT uq_owner_profile_name UNIQUE (owner_uid, profile_name)
    );
    CREATE TABLE emu_profiles_acl (
      id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
      profile_id  UUID        NOT NULL REFERENCES emu_profiles(id) ON DELETE CASCADE,
      grantee_uid TEXT        NOT NULL,
      can_use     BOOLEAN     NOT NULL DEFAULT TRUE,
      can_view    BOOLEAN     NOT NULL DEFAULT FALSE,
      granted_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
      CONSTRAINT uq_grant UNIQUE (profile_id, grantee_uid)
    );
EOF
 
  # Stop Postgres.
  kill "$POSTGRES_PID"
  wait "$POSTGRES_PID" 2>/dev/null || true

  # Configure Postgres to listen on all network interfaces.
  echo "listen_addresses = '*'" >>/var/lib/postgresql/data/postgresql.conf

  # Configure Postgres to authenticate every user of every database from every IP address using MD5.
  echo "host  all all 0.0.0.0/0 md5" >>/var/lib/postgresql/data/pg_hba.conf
fi

# Start Postgres in the foreground.
exec postgres -D /var/lib/postgresql/data
