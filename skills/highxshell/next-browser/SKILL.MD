---
name: next-browser
description: Use Nextbrowser cloud API to spin up cloud browsers for Openclaw and run autonomous browser tasks. Primary use is creating browser sessions with profiles (persisted logins/cookies) that Openclaw can control. Secondary use is running task subagents for fast autonomous browser automation. Docs at docs.nextbrowser.com.
---

# Nextbrowser

Nextbrowser provides cloud browsers and autonomous browser automation via API.

**Docs:**
- Cloud API: https://docs.nextbrowser.com/getting-started

## Setup

**API Key** is read from openclaw config at `skills.entries.next-browser.apiKey`.

If not configured, tell the user:
> To use Nextbrowser, you need an API key. Get one at https://app.nextbrowser.com/user-settings (new signups get 2000 free credits). Then configure it:
> ```
> openclaw config set skills.entries.next-browser.apiKey "nb_your_key_here"
> ```

Base URL: `https://app.nextbrowser.com/api/v1`

All requests need header: `Authorization: x-api-key <apiKey>`

---

## 1. Profiles

Profiles persist cookies and login state across browser sessions. Create one, log into your accounts in the browser, and reuse it.

```bash
# List profiles
curl "https://app.nextbrowser.com/api/v1/browser/profiles" -H "Authorization: x-api-key $API_KEY"

# Create browser profile
curl -X POST "https://app.nextbrowser.com/api/v1/browser/profiles" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "<profile-name>", "browser_settings": {"os_type": "<os-type>", "browser_type": "chrome"},
   "proxy_settings":{"protocol":"<http|https|socks5>","country":"<iso-2-country-code>","mode":"built-in"}}'

# Delete profile
curl -X DELETE "https://app.nextbrowser.com/api/v1/browser/profiles/<profile-id>" \
  -H "Authorization: x-api-key $API_KEY"
```

---

## 3. Tasks (Subagent)

Run autonomous browser tasks - like a subagent that handles browser interactions for you. Give it a prompt and it completes the task.

**Always use `fast` mode** - optimized for browser tasks, 3-5x faster than other models.
**Always use `true` for skip_plan_approval** - optimized for automated tasks, skips the approval and improve performance.

```bash
curl -X POST "https://app.nextbrowser.com/api/v1/chat/tasks" \
  -H "Authorization: x-api-key $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Go to amazon.com and find the price of the MacBook Air M3",
    "mode": "fast",
    "profile_id": "<profile-id>",
    "skip_plan_approval": true
  }'
```

### Poll for completion

```bash
curl "https://app.nextbrowser.com/api/v1/chat/tasks/<task-id>" -H "Authorization: x-api-key $API_KEY"
```

**Response:**
```json
{
    "success": true,
    "payload": {
        "status": "finished",
        "output": "The current price for a new 2024 MacBook Air 13-inch with M3 chip on Amazon is CAD 2,046.01",
        "isSuccess": true
    },
    "errors": {},
    "description": "Task retrieved successfully"
}
```

Status values: `processing`, `completed`, `failed`, `stopped`

### Task options

| Option | Description            |
|--------|------------------------|
| `task_description` | Your prompt (required) |
| `mode` | Always use `fast` |
| `profile_id` | Use a profile for auth |
| `skip_plan_approval` | Always use `true`|

---

## Full API Reference

See [references/api.md](references/api.md) for all endpoints including Sessions, Files, Skills, and Skills Marketplace.
