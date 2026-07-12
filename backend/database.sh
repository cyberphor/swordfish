#!/bin/bash
 
reset() {
  psql -h $PGHOST -U "$PGUSER" -d "$PGDATABASE" -c "DROP TABLE $2;"
}

case $1 in
  drop)
    drop
    ;;
  *)
    echo "[x] Please enter one of the following commands:"
    echo " database.sh drop <DATABASE>"
    ;;
esac
