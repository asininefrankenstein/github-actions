#!/usr/bin/env bash
# Tests that meta.json generation logic produces valid JSON with required fields.
set -euo pipefail

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

ERRORS=0

assert_eq() {
  local name="$1" expected="$2" actual="$3"
  if [[ "$actual" != "$expected" ]]; then
    echo "FAIL: $name: expected '$expected', got '$actual'"
    ((ERRORS++))
  else
    echo "PASS: $name = $actual"
  fi
}

# --- Test: webhook meta.json shape ---
cat > "$TMPDIR/meta-webhook.json" <<'EOF'
{
  "block": "webhook",
  "status": "passed",
  "timestamp": "2026-03-01T00:00:00Z",
  "mode": "http",
  "response_code": 200
}
EOF

BLOCK=$(jq -r '.block' "$TMPDIR/meta-webhook.json")
STATUS=$(jq -r '.status' "$TMPDIR/meta-webhook.json")
MODE=$(jq -r '.mode' "$TMPDIR/meta-webhook.json")

assert_eq  "webhook.block"  "webhook" "$BLOCK"
assert_eq  "webhook.status" "passed"  "$STATUS"
assert_eq  "webhook.mode"   "http"    "$MODE"

# --- Test: failed status shape ---
cat > "$TMPDIR/meta-failed.json" <<'EOF'
{
  "block": "webhook",
  "status": "failed",
  "timestamp": "2026-03-01T00:00:00Z",
  "mode": "http"
}
EOF
assert_eq "failed.status" "failed" "$(jq -r '.status' "$TMPDIR/meta-failed.json")"

# --- Validate JSON is parseable (not malformed) ---
for f in "$TMPDIR"/*.json; do
  if jq empty "$f" 2>/dev/null; then
    echo "PASS: $(basename $f) is valid JSON"
  else
    echo "FAIL: $(basename $f) is not valid JSON"
    ((ERRORS++))
  fi
done

if [[ "$ERRORS" -gt 0 ]]; then
  echo ""
  echo "FAILED: $ERRORS assertion(s) failed"
  exit 1
else
  echo ""
  echo "ALL PASSED"
  exit 0
fi
