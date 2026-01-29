#!/usr/bin/env bash
# Validate GitHub Actions workflows for common issues
# Run: ./scripts/validate-workflows.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKFLOWS_DIR="${REPO_ROOT}/.github/workflows"
ACTIONS_DIR="${REPO_ROOT}/.github/actions"

EXIT_CODE=0

echo "=== Validating GitHub Actions Workflows ==="
echo ""

# Check for potential multi-line GITHUB_OUTPUT issues
# Pattern: JSON commands piped to GITHUB_OUTPUT without jq -c
echo "Checking for potential multi-line GITHUB_OUTPUT issues..."

# Find patterns that might produce multi-line output to GITHUB_OUTPUT
# Specifically: docker inspect, curl, or other JSON-producing commands
RISKY_PATTERNS=(
    'docker.*inspect.*\$GITHUB_OUTPUT'
    'docker buildx imagetools inspect.*\$GITHUB_OUTPUT'
    'curl.*\$GITHUB_OUTPUT'
)

for pattern in "${RISKY_PATTERNS[@]}"; do
    # Look for the pattern without jq -c on the same line
    while IFS= read -r file; do
        if grep -n "format.*json" "$file" | grep -v "jq -c" | grep -q "GITHUB_OUTPUT"; then
            echo "::warning file=${file}::Potential multi-line JSON output to GITHUB_OUTPUT without jq -c"
            echo "  Consider using: | jq -c . to compact JSON to single line"
            EXIT_CODE=1
        fi
    done < <(find "${WORKFLOWS_DIR}" "${ACTIONS_DIR}" -name "*.yml" -o -name "*.yaml" 2>/dev/null)
done

# Check for echo with JSON to GITHUB_OUTPUT (common pattern that can fail)
echo "Checking for JSON echo patterns to GITHUB_OUTPUT..."
while IFS= read -r file; do
    # Look for lines that capture JSON and echo to GITHUB_OUTPUT
    if grep -En 'echo.*metadata=.*\$GITHUB_OUTPUT' "$file" | grep -v "jq -c" | grep -qv "EOF"; then
        LINE=$(grep -En 'echo.*metadata=.*\$GITHUB_OUTPUT' "$file" | grep -v "jq -c" | head -1)
        echo "::warning file=${file}::Potential issue: metadata output without JSON compaction"
        echo "  Line: ${LINE}"
        echo "  Consider using jq -c or heredoc syntax for multi-line values"
    fi
done < <(find "${WORKFLOWS_DIR}" "${ACTIONS_DIR}" -name "*.yml" -o -name "*.yaml" 2>/dev/null)

# YAML syntax validation
echo ""
echo "Validating YAML syntax..."
if command -v yamllint &> /dev/null; then
    if ! yamllint -d "{extends: relaxed, rules: {line-length: disable}}" "${WORKFLOWS_DIR}"/*.yml 2>/dev/null; then
        EXIT_CODE=1
    fi
else
    echo "yamllint not found, skipping YAML validation"
fi

echo ""
if [[ ${EXIT_CODE} -eq 0 ]]; then
    echo "✅ All workflow validations passed"
else
    echo "❌ Some workflow validations failed"
fi

exit ${EXIT_CODE}
