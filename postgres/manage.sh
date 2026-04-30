#!/bin/bash
 
init() {
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
}

reset() {
  psql -h $PGHOST -U "$PGUSER" -d "$PGDATABASE" -c "DROP TABLE emu_profiles_acl;"
  psql -h $PGHOST -U "$PGUSER" -d "$PGDATABASE" -c "DROP TABLE emu_profiles;"
}

case $1 in
  init)
    init
  ;;
  reset)
    reset
    ;;
  *)
    echo "[x] Please enter one of the following commands:"
    echo " manage.sh init"
    echo " manage.sh reset"
    ;;
esac
