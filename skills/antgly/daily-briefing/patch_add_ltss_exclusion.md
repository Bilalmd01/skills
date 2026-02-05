Patch: Add configurable sender exclusion list (WITCH-like) and include "LTTS"

Summary
-------
This patch proposes adding a new configuration option to the daily-briefing skill to support an explicit list of sender names/domains to always exclude from "important emails" classification. It adds "LTTS" (and a suggested domain pattern) to the default exclusion list and documents the behavior.

Files changed
-------------
- skills/daily-briefing/SKILL.md (documentation only)

Proposed changes (documentation excerpt to insert under "Configuration" or near "Configuration Options"):

"""
  "emails": {
    "enabled": false,
    "icloudPassword": "",
    "limit": 10,
    "sortNewest": true,
    "starredFirst": true,
    "unreadOnly": true,
    "exclude_senders": [
      "Wipro",
      "Infosys",
      "LTTS",
      "@wipro.com",
      "@infosys.com",
      "@ltts.com"
    ]
  }

Description: "emails.exclude_senders" is an optional array of case-insensitive sender name fragments or email-domain patterns. Any email whose sender name or sender email matches any entry in this list (substring match for names, suffix match for domains beginning with '@') will be excluded from the "important emails" set regardless of other signals, except when the email is starred or the sender matches the user's contacts.

Behavior notes:
- Matches are case-insensitive.
- If an exclude entry begins with '@', it is treated as an email domain suffix (e.g., '@ltts.com').
- Starred emails and emails from contacts bypass exclusion (to avoid false negatives).
- This list is applied before semantic scoring so entries consistently prevent recruiter/outsourcing messages from surfacing.

Suggested default includes LTTS (L&T Technology Services) to meet your request.
"""

Next steps
----------
- If you want, I can apply this change directly to SKILL.md (documentation) and, if present, add runtime support in the orchestrator script (scripts/daily_briefing_orchestrator.sh) to pass the config through to the agent and ensure the classifier respects it.
- Tell me whether to (A) apply the documentation-only change now, (B) apply the docs + orchestrator/script changes now, or (C) stop here so you can review.

Patch created by assistant on request. Review and tell me how you'd like to proceed.