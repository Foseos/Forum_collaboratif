#!/usr/bin/env bash
# Run on the production server after .env.backup and an off-server restic repository exist.
set -Eeuo pipefail
umask 077

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"

if [[ ! -f .env.production || ! -f .env.backup ]]; then
  echo "Missing .env.production or .env.backup" >&2
  exit 1
fi

set -a
# .env.backup is an administrator-owned shell file, never committed to Git.
source .env.backup
set +a

: "${RESTIC_REPOSITORY:?Set RESTIC_REPOSITORY in .env.backup}"
: "${RESTIC_PASSWORD_FILE:?Set RESTIC_PASSWORD_FILE in .env.backup}"
if [[ ! -f "$RESTIC_PASSWORD_FILE" ]]; then
  echo "Restic password file not found" >&2
  exit 1
fi

case "$RESTIC_REPOSITORY" in
  sftp:*|s3:*|b2:*|azure:*|gs:*|rest:*|rclone:*) ;;
  *) echo "Use an off-server restic repository, not a local path" >&2; exit 1 ;;
esac

for executable in docker restic flock mktemp tar; do
  command -v "$executable" >/dev/null || { echo "Missing command: $executable" >&2; exit 1; }
done

exec 9>"${TMPDIR:-/tmp}/nexus-arcana-backup.lock"
flock -n 9 || { echo "A backup is already running" >&2; exit 1; }

staging="$(mktemp -d "${TMPDIR:-/tmp}/nexus-arcana-backup.XXXXXXXX")"
trap 'rm -rf -- "$staging"' EXIT

compose=(docker compose --env-file .env.production -f compose.prod.yml)
"${compose[@]}" exec -T db sh -c 'exec pg_dump -Fc -U "$POSTGRES_USER" "$POSTGRES_DB"' > "$staging/database.dump"
"${compose[@]}" exec -T backend tar -C /app/media -cf - . > "$staging/media.tar"

test -s "$staging/database.dump"
test -s "$staging/media.tar"
printf 'Nexus Arcana backup\nCreated UTC: %s\nContents: PostgreSQL custom dump and uploaded media\n' \
  "$(date -u +%FT%TZ)" > "$staging/manifest.txt"

# Repository must be initialized explicitly; never silently create a new empty one.
restic snapshots --latest 1 >/dev/null
restic backup --tag nexus-arcana "$staging"
echo "Forum backup completed and uploaded to the encrypted off-server repository."
