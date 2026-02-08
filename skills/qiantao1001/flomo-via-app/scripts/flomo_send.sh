#!/bin/bash
#
# flomo_send.sh - Send notes to flomo app via URL Scheme with webhook fallback
#
# Usage:
#   ./flomo_send.sh "Note content" "#tag1 #tag2"
#   ./scripts/flomo_send.sh "$(pbpaste)" "#clippings"
#   echo "Note content" | ./scripts/flomo_send.sh
#

set -e

# Get content from argument or stdin
if [ $# -ge 1 ]; then
    CONTENT="$1"
else
    # Read from stdin
    CONTENT=$(cat)
fi

# Get tags from second argument
TAGS=""
if [ $# -ge 2 ]; then
    TAGS="$2"
fi

# Combine content and tags
if [ -n "$TAGS" ]; then
    FULL_CONTENT="${CONTENT} ${TAGS}"
else
    FULL_CONTENT="${CONTENT}"
fi

# Trim whitespace (remove leading/trailing spaces and newlines)
FULL_CONTENT=$(echo "$FULL_CONTENT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Check if content is empty
if [ -z "$FULL_CONTENT" ]; then
    echo "Error: Note content is empty" >&2
    echo "Usage: $0 \"Note content\" \"#tag1 #tag2\"" >&2
    exit 1
fi

# Check content length (flomo limit: 5000 characters before encoding)
if [ "${#FULL_CONTENT}" -gt 5000 ]; then
    echo "Error: Content exceeds 5000 character limit (current: ${#FULL_CONTENT})" >&2
    exit 1
fi

# URL encode the content using Python
# Use environment variable to safely pass content with special characters
export FLOMO_CONTENT="$FULL_CONTENT"
URL_ENCODED=$(python3 -c 'import urllib.parse,os; print(urllib.parse.quote(os.environ.get("FLOMO_CONTENT","")))' 2>/dev/null || \
    python -c 'import urllib,os; print(urllib.quote(os.environ.get("FLOMO_CONTENT","")))' 2>/dev/null)

# Check if URL encoding succeeded
if [ -z "$URL_ENCODED" ]; then
    echo "Error: URL encoding failed. Python is required." >&2
    exit 1
fi

# Build flomo URL
FLOMO_URL="flomo://create?content=${URL_ENCODED}"

# Function: send via webhook fallback
send_webhook() {
    if [ -n "$FLOMO_WEBHOOK_URL" ]; then
        WEBHOOK_URL="$FLOMO_WEBHOOK_URL"
    elif [ -n "$FLOMO_WEBHOOK_TOKEN" ]; then
        WEBHOOK_URL="https://flomoapp.com/iwh/$FLOMO_WEBHOOK_TOKEN"
    else
        echo "Error: Webhook not configured. Set FLOMO_WEBHOOK_URL or FLOMO_WEBHOOK_TOKEN." >&2
        echo "URL: $FLOMO_URL" >&2
        exit 1
    fi

    # Build JSON payload using Python for safety
    PAYLOAD=$(python3 -c 'import json,os; print(json.dumps({"content": os.environ.get("FLOMO_CONTENT","")}))' 2>/dev/null || \
            python -c 'import json,os; print(json.dumps({"content": os.environ.get("FLOMO_CONTENT","")}))' 2>/dev/null)

    if [ -z "$PAYLOAD" ]; then
        echo "Error: Failed to build JSON payload" >&2
        exit 1
    fi

    RESP=$(curl -sS -w "\n%{http_code}" -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$PAYLOAD" || true)
    HTTP_STATUS=$(echo "$RESP" | tail -n1)
    BODY=$(echo "$RESP" | sed '$d')

    if echo "$HTTP_STATUS" | grep -q "^2"; then
        echo "✓ Sent to flomo webhook: ${FULL_CONTENT:0:50}..."
        exit 0
    else
        echo "Error: Webhook request failed (HTTP $HTTP_STATUS): $BODY" >&2
        exit 1
    fi
}

# Open flomo app via URL scheme. If it fails, fallback to webhook.
if command -v open &> /dev/null; then
    if open "$FLOMO_URL" 2>/dev/null; then
        echo "✓ Sent to flomo: ${FULL_CONTENT:0:50}..."
        exit 0
    else
        echo "Warning: flomo URL scheme failed, attempting webhook..." >&2
        send_webhook
    fi
else
    echo "Warning: 'open' command not found. Attempting webhook..." >&2
    send_webhook
fi
