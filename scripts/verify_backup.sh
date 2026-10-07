#!/usr/bin/env bash
# Restores the latest archive into a temporary directory without touching the live forum.
set -Eeuo pipefail
umask 077

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"
if [[ ! -f .env.production || ! -f .env.backup ]]; then
  echo "Missing .env.production or .env.backup" >&2
  exit 1
fi
set -a
source .env.backup
set +a
: "${RESTIC_REPOSITORY:?Missing RESTIC_REPOSITORY}"
: "${RESTIC_PASSWORD_FILE:?Missing RESTIC_PASSWORD_FILE}"

staging="$(mktemp -d "${TMPDIR:-/tmp}/nexus-arcana-restore.XXXXXXXX")"
trap 'rm -rf -- "$staging"' EXIT

restic restore latest --target "$staging"
database_dump="$(find "$staging" -name database.dump -type f -print -quit)"
media_archive="$(find "$staging" -name media.tar -type f -print -quit)"
if [[ -z "$database_dump" || -z "$media_archive" ]]; then
  echo "Database dump or media archive missing from the restored snapshot" >&2
  exit 1
fi

docker compose --env-file .env.production -f compose.prod.yml exec -T db pg_restore -l < "$database_dump" >/dev/null
tar -tf "$media_archive" >/dev/null
echo "Latest backup restored to a temporary directory; database dump and media archive are readable."
