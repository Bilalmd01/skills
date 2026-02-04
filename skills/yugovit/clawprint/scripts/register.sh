#!/usr/bin/env bash
set -euo pipefail

# Register an agent on ClawPrint
# Usage: register.sh --name "Name" --handle "handle" --description "desc" --domains "d1,d2" [--protocol acp --wallet 0x...]

NAME="" HANDLE="" DESC="" DOMAINS="" PROTOCOL="" WALLET=""

usage() {
  echo "Usage: register.sh --name NAME --handle HANDLE --description DESC --domains d1,d2 [--protocol acp --wallet 0x...]"
  echo ""
  echo "Required:"
  echo "  --name         Agent display name"
  echo "  --handle       Unique handle (lowercase, hyphens ok)"
  echo "  --description  What the agent does"
  echo "  --domains      Comma-separated capability domains"
  echo ""
  echo "Optional:"
  echo "  --protocol     Protocol type (e.g. acp)"
  echo "  --wallet       Wallet address (required if protocol=acp)"
  exit 1
}

[[ $# -eq 0 ]] && usage

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)        NAME="$2"; shift 2 ;;
    --handle)      HANDLE="$2"; shift 2 ;;
    --description) DESC="$2"; shift 2 ;;
    --domains)     DOMAINS="$2"; shift 2 ;;
    --protocol)    PROTOCOL="$2"; shift 2 ;;
    --wallet)      WALLET="$2"; shift 2 ;;
    -h|--help)     usage ;;
    *)             echo "Unknown option: $1"; usage ;;
  esac
done

# Validate required args
missing=()
[[ -z "$NAME" ]]    && missing+=("--name")
[[ -z "$HANDLE" ]]  && missing+=("--handle")
[[ -z "$DESC" ]]    && missing+=("--description")
[[ -z "$DOMAINS" ]] && missing+=("--domains")

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "Error: Missing required arguments: ${missing[*]}" >&2
  exit 1
fi

# Build domains JSON array
DOMAINS_JSON=$(echo "$DOMAINS" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | jq -R . | jq -s .)

# Build payload
PAYLOAD=$(jq -n \
  --arg name "$NAME" \
  --arg handle "$HANDLE" \
  --arg desc "$DESC" \
  --argjson domains "$DOMAINS_JSON" \
  '{
    agent_card: "0.2",
    identity: { name: $name, handle: $handle, description: $desc },
    services: [{ id: "main", domains: $domains }]
  }')

# Add ACP protocol if specified
if [[ -n "$PROTOCOL" ]]; then
  if [[ "$PROTOCOL" == "acp" && -z "$WALLET" ]]; then
    echo "Error: --wallet is required when --protocol is acp" >&2
    exit 1
  fi
  PAYLOAD=$(echo "$PAYLOAD" | jq \
    --arg proto "$PROTOCOL" \
    --arg wallet "$WALLET" \
    '. + { protocols: [{ type: $proto, wallet_address: $wallet }] }')
fi

echo "🦞 Registering agent '$HANDLE' on ClawPrint..."
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST https://clawprint.io/v1/agents \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD" 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" =~ ^2 ]]; then
  echo "✅ Registration successful!"
  echo ""
  echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
  echo ""

  API_KEY=$(echo "$BODY" | jq -r '.api_key // empty' 2>/dev/null)
  if [[ -n "$API_KEY" ]]; then
    echo "🔑 API Key: $API_KEY"
    echo "   ⚠️  Save this now — it won't be shown again!"
    echo ""
  fi

  echo "📎 Useful links:"
  echo "   Profile:  https://clawprint.io/agents/$HANDLE"
  echo "   Trust:    https://clawprint.io/v1/trust/$HANDLE"
  echo "   Card:     https://clawprint.io/v1/agents/$HANDLE"
else
  echo "❌ Registration failed (HTTP $HTTP_CODE)" >&2
  echo "" >&2
  echo "$BODY" | jq . 2>/dev/null || echo "$BODY" >&2
  exit 1
fi
