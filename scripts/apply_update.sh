#!/usr/bin/env bash
set -Eeuo pipefail

PKG="${1:-}"
MODE="${2:-}"
MODEL_EXPECTED="Antminer S19i"
WORKDIR="/tmp/s19i-os-apply"
STAGING_DIR="/opt/s19i-os/staging"
LIVE_DIR="/opt/s19i-os/live"
REBOOT_FLAG="/tmp/s19i-os-reboot-required"

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*"
}

fail() {
  log "ERROR: $*"
  exit 1
}

[[ -n "$PKG" ]] || fail "usage: $0 /path/to/update.tar.gz [--reboot]"
[[ -f "$PKG" ]] || fail "package not found: $PKG"

command -v python3 >/dev/null 2>&1 || fail "python3 is required"
command -v tar >/dev/null 2>&1 || fail "tar is required"
command -v rsync >/dev/null 2>&1 || fail "rsync is required"

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR" "$STAGING_DIR" "$LIVE_DIR" /opt/s19i-os /tmp/s19i-os-state

log "extracting package: $PKG"
tar -xzf "$PKG" -C "$WORKDIR"

[[ -f "$WORKDIR/manifest.json" ]] || fail "manifest.json missing in package"
[[ -d "$WORKDIR/rootfs-overlay" ]] || fail "rootfs-overlay directory missing in package"

MANIFEST_INFO="$WORKDIR/.manifest.env"
python3 - "$WORKDIR/manifest.json" > "$MANIFEST_INFO" <<'PY'
import json
import shlex
import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    m = json.load(f)

for key in ('package_name', 'version', 'target_model'):
    if key not in m:
        raise SystemExit(f"missing manifest key: {key}")

for key in ('package_name', 'version', 'target_model'):
    print(f"{key.upper()}={shlex.quote(str(m[key]))}")
PY

# shellcheck disable=SC1090
source "$MANIFEST_INFO"

[[ "$TARGET_MODEL" == "$MODEL_EXPECTED" ]] || fail "target_model mismatch: got '$TARGET_MODEL' expected '$MODEL_EXPECTED'"

log "package_name=$PACKAGE_NAME version=$VERSION model=$TARGET_MODEL"
log "entering maintenance mode"
printf '1\n' > /tmp/s19i-os-state/maintenance_mode
printf 'stopped\n' > /tmp/s19i-os-state/miner_state

if [[ -x "$WORKDIR/hooks/pre_apply.sh" ]]; then
  log "running pre_apply hook"
  bash "$WORKDIR/hooks/pre_apply.sh"
fi

log "sync rootfs-overlay -> staging"
rm -rf "$STAGING_DIR/current"
mkdir -p "$STAGING_DIR/current"
rsync -a --delete "$WORKDIR/rootfs-overlay/" "$STAGING_DIR/current/"

log "promote staging -> live"
rsync -a --delete "$STAGING_DIR/current/" "$LIVE_DIR/"

printf '%s\n' "$VERSION" > /opt/s19i-os/current_version
printf '%s\n' "$PACKAGE_NAME" > /opt/s19i-os/current_package

if [[ -x "$WORKDIR/hooks/post_apply.sh" ]]; then
  log "running post_apply hook"
  bash "$WORKDIR/hooks/post_apply.sh"
fi

log "leaving maintenance mode"
printf '0\n' > /tmp/s19i-os-state/maintenance_mode
printf 'running\n' > /tmp/s19i-os-state/miner_state

if [[ "$MODE" == "--reboot" ]]; then
  log "reboot requested by updater"
  touch "$REBOOT_FLAG"
fi

log "update applied successfully"
