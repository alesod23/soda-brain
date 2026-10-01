#!/usr/bin/env bash
# SODA BRAIN box install. Idempotent. Run as root on the box (Ubuntu 24.04):
#   sudo bash /home/da/soda-brain/tools/box-install.sh
#
# Needs /home/da/.env/soda.env (mode 0600, owner da) with SODA_DB_PASSWORD, SODA_TOKEN and SODA_DB_DSN
# (README.md "Env file"). Creates: apt postgresql + pgvector, role/db `soda`, the schema, the venv at
# /home/da/brain/venv (outside every repo), the systemd units from task-land/_system/vps, then prints /health.
set -euo pipefail

DA_USER=da
DA_HOME=/home/da
ENV_FILE=$DA_HOME/.env/soda.env
REPO=$DA_HOME/soda-brain
TOOLS=$REPO/tools
VENV=$DA_HOME/brain/venv
UNITS_SRC=$DA_HOME/task-land/_system/vps
HOST=100.85.52.84
PORT=4150

log() { printf '[brain-install] %s\n' "$*"; }
die() { printf '[brain-install] ERROR: %s\n' "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "run as root (sudo bash $0)"
[[ -d $TOOLS ]] || die "$TOOLS missing: the soda-brain repo is not on the box yet (da-repo-sync@soda-brain.timer)"
[[ -f $UNITS_SRC/da-brain.service ]] || die "$UNITS_SRC/da-brain.service missing: task-land not synced yet"

# --- 0. env file: must exist, never created here -------------------------------------------------
if [[ ! -f $ENV_FILE ]]; then
    cat >&2 <<EOF
[brain-install] ERROR: $ENV_FILE does not exist. Create it as da, then re-run:

  sudo -u da mkdir -p -m 700 $DA_HOME/.env
  sudo -u da bash -c 'PW=\$(openssl rand -hex 24); TK=\$(openssl rand -hex 32); umask 077; printf "SODA_DB_PASSWORD=%s\nSODA_TOKEN=%s\nSODA_DB_DSN=postgresql://soda:%s@127.0.0.1/soda\n" "\$PW" "\$TK" "\$PW" > $ENV_FILE'
  sudo -u da chmod 600 $ENV_FILE

EOF
    exit 1
fi
getv() { grep -E "^${1}=" "$ENV_FILE" | tail -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//"; }
DB_PW=$(getv SODA_DB_PASSWORD); TOKEN=$(getv SODA_TOKEN); DSN=$(getv SODA_DB_DSN)
[[ -n $DB_PW ]] || die "SODA_DB_PASSWORD missing in $ENV_FILE"
[[ -n $TOKEN  ]] || die "SODA_TOKEN missing in $ENV_FILE"
[[ -n $DSN    ]] || die "SODA_DB_DSN missing in $ENV_FILE (postgresql://soda:<password>@127.0.0.1/soda)"
chown $DA_USER:$DA_USER "$ENV_FILE"; chmod 600 "$ENV_FILE"
log "env file ok"

# --- 1. packages ---------------------------------------------------------------------------------
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -q postgresql postgresql-16-pgvector python3-venv python3-pip curl >/dev/null
systemctl enable --now postgresql >/dev/null
log "postgresql + pgvector installed"

# --- 2. listen on localhost only -----------------------------------------------------------------
CUR=$(sudo -u postgres psql -tAc "SHOW listen_addresses")
if [[ $CUR != "localhost" ]]; then
    sudo -u postgres psql -qc "ALTER SYSTEM SET listen_addresses = 'localhost'"
    systemctl restart postgresql
    log "listen_addresses set to localhost (was: $CUR)"
fi

# --- 3. role, database, extension ----------------------------------------------------------------
if [[ $(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='soda'") != "1" ]]; then
    sudo -u postgres psql -qc "CREATE ROLE soda LOGIN"
    log "role soda created"
fi
# the env file is the source of truth for the password (safe to re-run after a rotation)
sudo -u postgres psql -qv pw="$DB_PW" -c "ALTER ROLE soda PASSWORD :'pw'"
if [[ $(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='soda'") != "1" ]]; then
    sudo -u postgres psql -qc "CREATE DATABASE soda OWNER soda"
    log "database soda created"
fi
sudo -u postgres psql -qd soda -c "CREATE EXTENSION IF NOT EXISTS vector" >/dev/null
log "extension vector present ($(sudo -u postgres psql -tAd soda -c "SELECT extversion FROM pg_extension WHERE extname='vector'"))"

# --- 4. schema (as soda, over TCP with the password: proves the DSN works) -----------------------
PGPASSWORD="$DB_PW" sudo -u $DA_USER -E psql -q -v ON_ERROR_STOP=1 -h 127.0.0.1 -U soda -d soda -f "$TOOLS/schema.sql" >/dev/null
log "schema.sql applied"

# --- 5. venv outside the repo --------------------------------------------------------------------
sudo -u $DA_USER mkdir -p "$(dirname "$VENV")"
[[ -x $VENV/bin/python ]] || sudo -u $DA_USER python3 -m venv "$VENV"
sudo -u $DA_USER "$VENV/bin/pip" install -q --upgrade pip
sudo -u $DA_USER "$VENV/bin/pip" install -q -r "$TOOLS/requirements.txt"
log "venv ready: $("$VENV/bin/python" --version), $("$VENV/bin/python" -c 'import torch,sentence_transformers,mcp,psycopg;print("torch",torch.__version__)')"
# the model is downloaded once (~470 MB into ~/.cache/huggingface) so the first timer run stays short
sudo -u $DA_USER -H HF_HUB_DISABLE_PROGRESS_BARS=1 "$VENV/bin/python" -c \
    "from sentence_transformers import SentenceTransformer as S; S('intfloat/multilingual-e5-small', device='cpu')" 2>/dev/null
log "embedding model cached"

# --- 6. units ------------------------------------------------------------------------------------
install -m 644 "$UNITS_SRC/da-brain.service" "$UNITS_SRC/da-brain-index.service" "$UNITS_SRC/da-brain-index.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now da-brain-index.timer >/dev/null
systemctl enable da-brain.service >/dev/null
systemctl restart da-brain.service
log "units installed: da-brain.service, da-brain-index.timer"

# --- 7. first index, then health -----------------------------------------------------------------
systemctl start da-brain-index.service || log "first index run failed: journalctl -u da-brain-index"
for i in $(seq 1 30); do
    if OUT=$(curl -fsS "http://$HOST:$PORT/health" 2>/dev/null); then
        log "health: $OUT"
        exit 0
    fi
    sleep 2
done
log "service not answering on $HOST:$PORT yet: journalctl -u da-brain -n 50"
exit 1
