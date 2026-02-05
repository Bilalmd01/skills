---
name: klaviyo
description: |
  Klaviyo API integration with managed OAuth. Access profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks. Use this skill when users want to manage email marketing, customer data, or integrate with Klaviyo workflows.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Klaviyo

Access the Klaviyo API with managed OAuth authentication. Manage profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks for email marketing and customer engagement.

## Quick Start

```python
import requests
import os

# List profiles
response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
profiles = response.json()
```

## Base URL

```
https://gateway.maton.ai/klaviyo/{native-api-path}
```

Replace `{native-api-path}` with the actual Klaviyo API endpoint path. The gateway proxies requests to `a.klaviyo.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## API Versioning

Klaviyo uses date-based API versioning. Include the `revision` header in all requests:

```
revision: 2024-10-15
```

## Connection Management

Manage your Klaviyo OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```python
import requests
import os

response = requests.get(
    "https://ctrl.maton.ai/connections",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    params={"app": "klaviyo", "status": "ACTIVE"}
)
connections = response.json()
```

### Create Connection

```python
import requests
import os

response = requests.post(
    "https://ctrl.maton.ai/connections",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    json={"app": "klaviyo"}
)
connection = response.json()
```

### Get Connection

```python
import requests
import os

connection_id = "21fd90f9-5935-43cd-b6c8-bde9d915ca80"
response = requests.get(
    f"https://ctrl.maton.ai/connections/{connection_id}",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}
)
connection = response.json()
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "klaviyo",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```python
import requests
import os

connection_id = "21fd90f9-5935-43cd-b6c8-bde9d915ca80"
response = requests.delete(
    f"https://ctrl.maton.ai/connections/{connection_id}",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}
)
```

### Specifying Connection

If you have multiple Klaviyo connections, specify which one to use with the `Maton-Connection` header:

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15",
        "Maton-Connection": "21fd90f9-5935-43cd-b6c8-bde9d915ca80"
    }
)
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Profiles

Manage customer data and consent.

#### Get Profiles

Query parameters:
- `filter` - Filter profiles (e.g., `filter=equals(email,"test@example.com")`)
- `fields[profile]` - Comma-separated list of fields to include
- `page[cursor]` - Cursor for pagination
- `page[size]` - Number of results per page (max 100)
- `sort` - Sort field (prefix with `-` for descending)

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={
        "fields[profile]": "email,first_name,last_name",
        "page[size]": 10
    }
)
profiles = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "profile",
      "id": "01GDDKASAP8TKDDA2GRZDSVP4H",
      "attributes": {
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Johnson"
      }
    }
  ],
  "links": {
    "self": "https://a.klaviyo.com/api/profiles",
    "next": "https://a.klaviyo.com/api/profiles?page[cursor]=..."
  }
}
```

#### Get a Profile

```python
import requests
import os

profile_id = "01GDDKASAP8TKDDA2GRZDSVP4H"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/profiles/{profile_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
profile = response.json()
```

#### Create a Profile

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "profile",
            "attributes": {
                "email": "newuser@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+15551234567",
                "properties": {
                    "custom_field": "value"
                }
            }
        }
    }
)
created = response.json()
```

#### Update a Profile

```python
import requests
import os

profile_id = "01GDDKASAP8TKDDA2GRZDSVP4H"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/profiles/{profile_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "profile",
            "id": profile_id,
            "attributes": {
                "first_name": "Jane"
            }
        }
    }
)
updated = response.json()
```

#### Merge Profiles

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/profile-merge",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "profile-merge",
            "id": "01GDDKASAP8TKDDA2GRZDSVP4H",
            "relationships": {
                "profiles": {
                    "data": [
                        {"type": "profile", "id": "01GDDKASAP8TKDDA2GRZDSVP4I"}
                    ]
                }
            }
        }
    }
)
merged = response.json()
```

#### Get Profile Lists

```python
import requests
import os

profile_id = "01GDDKASAP8TKDDA2GRZDSVP4H"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/profiles/{profile_id}/lists",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
lists = response.json()
```

#### Get Profile Segments

```python
import requests
import os

profile_id = "01GDDKASAP8TKDDA2GRZDSVP4H"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/profiles/{profile_id}/segments",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
segments = response.json()
```

### Lists

Organize subscribers into static lists.

#### Get Lists

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/lists",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[list]": "name,created,updated"}
)
lists = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "list",
      "id": "Y6nRLr",
      "attributes": {
        "name": "Newsletter Subscribers",
        "created": "2024-01-15T10:30:00Z",
        "updated": "2024-03-01T14:22:00Z"
      }
    }
  ]
}
```

#### Get a List

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
list_data = response.json()
```

#### Create a List

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/lists",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "list",
            "attributes": {
                "name": "VIP Customers"
            }
        }
    }
)
created = response.json()
```

#### Update a List

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "list",
            "id": list_id,
            "attributes": {
                "name": "Updated List Name"
            }
        }
    }
)
updated = response.json()
```

#### Delete a List

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Add Profiles to List

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.post(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}/relationships/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": [
            {"type": "profile", "id": "01GDDKASAP8TKDDA2GRZDSVP4H"}
        ]
    }
)
```

#### Remove Profiles from List

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}/relationships/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": [
            {"type": "profile", "id": "01GDDKASAP8TKDDA2GRZDSVP4H"}
        ]
    }
)
```

#### Get List Profiles

```python
import requests
import os

list_id = "Y6nRLr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/lists/{list_id}/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
profiles = response.json()
```

### Segments

Create dynamic audiences based on conditions.

#### Get Segments

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/segments",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[segment]": "name,created,updated"}
)
segments = response.json()
```

#### Get a Segment

```python
import requests
import os

segment_id = "XyZ123"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/segments/{segment_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
segment = response.json()
```

#### Create a Segment

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/segments",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "segment",
            "attributes": {
                "name": "High Value Customers",
                "definition": {
                    "condition_groups": []
                }
            }
        }
    }
)
created = response.json()
```

#### Update a Segment

```python
import requests
import os

segment_id = "XyZ123"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/segments/{segment_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "segment",
            "id": segment_id,
            "attributes": {
                "name": "Updated Segment Name"
            }
        }
    }
)
updated = response.json()
```

#### Delete a Segment

```python
import requests
import os

segment_id = "XyZ123"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/segments/{segment_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Get Segment Profiles

```python
import requests
import os

segment_id = "XyZ123"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/segments/{segment_id}/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
profiles = response.json()
```

### Campaigns

Design and send email campaigns.

#### Get Campaigns

Query parameters:
- `filter` - Filter campaigns (e.g., `filter=equals(messages.channel,'email')`)
- `fields[campaign]` - Fields to include
- `sort` - Sort by field

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/campaigns",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"filter": 'equals(messages.channel,"email")'}
)
campaigns = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "campaign",
      "id": "01GDDKASAP8TKDDA2GRZDSVP4I",
      "attributes": {
        "name": "Spring Sale 2024",
        "status": "Draft",
        "audiences": {
          "included": ["Y6nRLr"],
          "excluded": []
        },
        "send_options": {
          "use_smart_sending": true
        }
      }
    }
  ]
}
```

#### Get a Campaign

```python
import requests
import os

campaign_id = "01GDDKASAP8TKDDA2GRZDSVP4I"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/campaigns/{campaign_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
campaign = response.json()
```

#### Create a Campaign

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/campaigns",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "campaign",
            "attributes": {
                "name": "Summer Newsletter",
                "audiences": {
                    "included": ["Y6nRLr"]
                },
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email"
                        }
                    }]
                }
            }
        }
    }
)
created = response.json()
```

#### Update a Campaign

```python
import requests
import os

campaign_id = "01GDDKASAP8TKDDA2GRZDSVP4I"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/campaigns/{campaign_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "campaign",
            "id": campaign_id,
            "attributes": {
                "name": "Updated Campaign Name"
            }
        }
    }
)
updated = response.json()
```

#### Delete a Campaign

```python
import requests
import os

campaign_id = "01GDDKASAP8TKDDA2GRZDSVP4I"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/campaigns/{campaign_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Send a Campaign

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/campaign-send-jobs",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "campaign-send-job",
            "id": "01GDDKASAP8TKDDA2GRZDSVP4I"
        }
    }
)
```

#### Get Recipient Estimation

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/campaign-recipient-estimations",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "campaign-recipient-estimation",
            "id": "01GDDKASAP8TKDDA2GRZDSVP4I"
        }
    }
)
estimation = response.json()
```

### Flows

Build automated customer journeys.

#### Get Flows

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/flows",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[flow]": "name,status,created,updated"}
)
flows = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "flow",
      "id": "VJvBNr",
      "attributes": {
        "name": "Welcome Series",
        "status": "live",
        "created": "2024-01-10T08:00:00Z",
        "updated": "2024-02-15T12:30:00Z"
      }
    }
  ]
}
```

#### Get a Flow

```python
import requests
import os

flow_id = "VJvBNr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/flows/{flow_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
flow = response.json()
```

#### Create a Flow

> **Note:** Flow creation via API may be limited. Flows are typically created through the Klaviyo UI, then managed via API. Use GET, PATCH, and DELETE operations for existing flows.

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/flows",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "flow",
            "attributes": {
                "name": "New Flow"
            }
        }
    }
)
created = response.json()
```

#### Update Flow Status

```python
import requests
import os

flow_id = "VJvBNr"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/flows/{flow_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "flow",
            "id": flow_id,
            "attributes": {
                "status": "draft"
            }
        }
    }
)
updated = response.json()
```

#### Delete a Flow

```python
import requests
import os

flow_id = "VJvBNr"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/flows/{flow_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Get Flow Actions

```python
import requests
import os

flow_id = "VJvBNr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/flows/{flow_id}/flow-actions",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
actions = response.json()
```

#### Get Flow Messages

```python
import requests
import os

flow_id = "VJvBNr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/flows/{flow_id}/flow-messages",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
messages = response.json()
```

### Events

Track customer interactions and behaviors.

#### Get Events

Query parameters:
- `filter` - Filter events (e.g., `filter=equals(metric_id,"ABC123")`)
- `fields[event]` - Fields to include
- `sort` - Sort by field (default: `-datetime`)

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/events",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={
        "filter": "greater-than(datetime,2024-01-01T00:00:00Z)",
        "page[size]": 50
    }
)
events = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "event",
      "id": "4vRpBT",
      "attributes": {
        "metric_id": "TxVpCr",
        "profile_id": "01GDDKASAP8TKDDA2GRZDSVP4H",
        "datetime": "2024-03-15T14:30:00Z",
        "event_properties": {
          "value": 99.99,
          "product_name": "Running Shoes"
        }
      }
    }
  ]
}
```

#### Get an Event

```python
import requests
import os

event_id = "4vRpBT"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/events/{event_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
event = response.json()
```

#### Create an Event

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/events",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "event",
            "attributes": {
                "profile": {
                    "data": {
                        "type": "profile",
                        "attributes": {
                            "email": "customer@example.com"
                        }
                    }
                },
                "metric": {
                    "data": {
                        "type": "metric",
                        "attributes": {
                            "name": "Viewed Product"
                        }
                    }
                },
                "properties": {
                    "product_id": "SKU123",
                    "product_name": "Blue T-Shirt",
                    "price": 29.99
                }
            }
        }
    }
)
created = response.json()
```

#### Bulk Create Events

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/event-bulk-create-jobs",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "event-bulk-create-job",
            "attributes": {
                "events": {
                    "data": [
                        {
                            "type": "event",
                            "attributes": {
                                "profile": {"data": {"type": "profile", "attributes": {"email": "user1@example.com"}}},
                                "metric": {"data": {"type": "metric", "attributes": {"name": "Viewed Product"}}},
                                "properties": {"product_id": "SKU123"}
                            }
                        }
                    ]
                }
            }
        }
    }
)
job = response.json()
```

### Metrics

Access performance data and analytics.

#### Get Metrics

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/metrics",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
metrics = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "metric",
      "id": "TxVpCr",
      "attributes": {
        "name": "Placed Order",
        "created": "2024-01-01T00:00:00Z",
        "updated": "2024-03-01T00:00:00Z",
        "integration": {
          "object": "integration",
          "id": "shopify",
          "name": "Shopify"
        }
      }
    }
  ]
}
```

#### Get a Metric

```python
import requests
import os

metric_id = "TxVpCr"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/metrics/{metric_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
metric = response.json()
```

#### Query Metric Aggregates

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/metric-aggregates",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "metric-aggregate",
            "attributes": {
                "metric_id": "TxVpCr",
                "measurements": ["count", "sum_value"],
                "interval": "day",
                "filter": ["greater-or-equal(datetime,2024-01-01)", "less-than(datetime,2024-04-01)"]
            }
        }
    }
)
aggregates = response.json()
```

### Templates

Manage email templates.

#### Get Templates

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/templates",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[template]": "name,created,updated"}
)
templates = response.json()
```

#### Get a Template

```python
import requests
import os

template_id = "AbC123"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/templates/{template_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
template = response.json()
```

#### Create a Template

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/templates",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "template",
            "attributes": {
                "name": "Welcome Email",
                "editor_type": "CODE",
                "html": "<html><body><h1>Welcome!</h1></body></html>"
            }
        }
    }
)
created = response.json()
```

#### Update a Template

```python
import requests
import os

template_id = "AbC123"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/templates/{template_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "template",
            "id": template_id,
            "attributes": {
                "name": "Updated Template Name"
            }
        }
    }
)
updated = response.json()
```

#### Delete a Template

```python
import requests
import os

template_id = "AbC123"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/templates/{template_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Render a Template

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/template-render",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "template",
            "id": "AbC123",
            "attributes": {
                "context": {
                    "first_name": "John"
                }
            }
        }
    }
)
rendered = response.json()
```

#### Clone a Template

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/template-clone",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "template",
            "id": "AbC123",
            "attributes": {
                "name": "Cloned Template"
            }
        }
    }
)
cloned = response.json()
```

### Catalogs

Manage product catalogs.

#### Get Catalog Items

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/catalog-items",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[catalog-item]": "title,price,url"}
)
items = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "type": "catalog-item",
      "id": "$custom:::$default:::PROD-001",
      "attributes": {
        "title": "Blue Running Shoes",
        "price": 129.99,
        "url": "https://store.example.com/products/blue-running-shoes"
      }
    }
  ]
}
```

#### Get a Catalog Item

```python
import requests
import os

catalog_item_id = "$custom:::$default:::PROD-001"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/catalog-items/{catalog_item_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
item = response.json()
```

#### Create Catalog Items

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/catalog-items",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "catalog-item",
            "attributes": {
                "external_id": "PROD-002",
                "title": "Red Running Shoes",
                "price": 149.99,
                "url": "https://store.example.com/products/red-running-shoes"
            }
        }
    }
)
created = response.json()
```

#### Update Catalog Item

```python
import requests
import os

catalog_item_id = "$custom:::$default:::PROD-001"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/catalog-items/{catalog_item_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "catalog-item",
            "id": catalog_item_id,
            "attributes": {
                "price": 119.99
            }
        }
    }
)
updated = response.json()
```

#### Delete Catalog Item

```python
import requests
import os

catalog_item_id = "$custom:::$default:::PROD-001"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/catalog-items/{catalog_item_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Get Catalog Variants

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/catalog-variants",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
variants = response.json()
```

#### Get Catalog Categories

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/catalog-categories",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
categories = response.json()
```

### Tags

Organize resources with tags.

#### Get Tags

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/tags",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
tags = response.json()
```

#### Create a Tag

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/tags",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "tag",
            "attributes": {
                "name": "Promotional"
            }
        }
    }
)
created = response.json()
```

#### Update a Tag

```python
import requests
import os

tag_id = "abc123"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/tags/{tag_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "tag",
            "id": tag_id,
            "attributes": {
                "name": "Updated Tag Name"
            }
        }
    }
)
updated = response.json()
```

#### Delete a Tag

```python
import requests
import os

tag_id = "abc123"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/tags/{tag_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Tag a Campaign

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/tag-campaign-relationships",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": [
            {"type": "campaign", "id": "01GDDKASAP8TKDDA2GRZDSVP4I"}
        ]
    }
)
```

#### Tag a Flow

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/tag-flow-relationships",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": [
            {"type": "flow", "id": "VJvBNr"}
        ]
    }
)
```

### Coupons

Manage discount codes.

#### Get Coupons

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/coupons",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
coupons = response.json()
```

#### Create a Coupon

> **Note:** The `external_id` must match regex `^[0-9_A-z]+$` (alphanumeric and underscores only, no hyphens).

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/coupons",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "coupon",
            "attributes": {
                "external_id": "SUMMER_SALE_2024",
                "description": "Summer sale discount coupon"
            }
        }
    }
)
created = response.json()
```

#### Get Coupon Codes

> **Note:** This endpoint requires a filter parameter. You must filter by coupon ID or profile ID.

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/coupon-codes",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"filter": 'equals(coupon.id,"SUMMER_SALE_2024")'}
)
codes = response.json()
```

#### Create Coupon Codes

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/coupon-codes",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "coupon-code",
            "attributes": {
                "unique_code": "SAVE20NOW",
                "expires_at": "2025-12-31T23:59:59Z"
            },
            "relationships": {
                "coupon": {
                    "data": {
                        "type": "coupon",
                        "id": "SUMMER_SALE_2024"
                    }
                }
            }
        }
    }
)
created = response.json()
```

### Webhooks

Configure event notifications.

#### Get Webhooks

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/webhooks",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
webhooks = response.json()
```

#### Create Webhook

```python
import requests
import os

response = requests.post(
    "https://gateway.maton.ai/klaviyo/api/webhooks",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "webhook",
            "attributes": {
                "name": "Order Placed Webhook",
                "endpoint_url": "https://example.com/webhooks/klaviyo",
                "enabled": True
            },
            "relationships": {
                "webhook-topics": {
                    "data": [
                        {"type": "webhook-topic", "id": "campaign:sent"}
                    ]
                }
            }
        }
    }
)
created = response.json()
```

#### Get a Webhook

```python
import requests
import os

webhook_id = "abc123"
response = requests.get(
    f"https://gateway.maton.ai/klaviyo/api/webhooks/{webhook_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
webhook = response.json()
```

#### Update a Webhook

```python
import requests
import os

webhook_id = "abc123"
response = requests.patch(
    f"https://gateway.maton.ai/klaviyo/api/webhooks/{webhook_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    json={
        "data": {
            "type": "webhook",
            "id": webhook_id,
            "attributes": {
                "enabled": False
            }
        }
    }
)
updated = response.json()
```

#### Delete a Webhook

```python
import requests
import os

webhook_id = "abc123"
response = requests.delete(
    f"https://gateway.maton.ai/klaviyo/api/webhooks/{webhook_id}",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
```

#### Get Webhook Topics

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/webhook-topics",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
topics = response.json()
```

### Accounts

Retrieve account information.

#### Get Accounts

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/accounts",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    }
)
accounts = response.json()
```

## Filtering

Klaviyo uses JSON:API filtering syntax. Common operators:

| Operator | Example |
|----------|---------|
| `equals` | `filter=equals(email,"test@example.com")` |
| `contains` | `filter=contains(name,"newsletter")` |
| `greater-than` | `filter=greater-than(datetime,2024-01-01T00:00:00Z)` |
| `less-than` | `filter=less-than(created,2024-03-01)` |
| `greater-or-equal` | `filter=greater-or-equal(updated,2024-01-01)` |
| `any` | `filter=any(status,["draft","scheduled"])` |

Combine filters with `and`:
```
filter=and(equals(status,"active"),greater-than(created,2024-01-01))
```

## Pagination

Klaviyo uses cursor-based pagination:

```python
import requests
import os

response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={
        "page[size]": 50,
        "page[cursor]": "CURSOR_TOKEN"
    }
)
data = response.json()
```

Response includes pagination links:

```json
{
  "data": [...],
  "links": {
    "self": "https://a.klaviyo.com/api/profiles",
    "next": "https://a.klaviyo.com/api/profiles?page[cursor]=WzE2..."
  }
}
```

## Sparse Fieldsets

Request only specific fields to reduce response size:

```python
import requests
import os

# Request only email and first_name for profiles
response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={"fields[profile]": "email,first_name"}
)

# Request specific fields for included relationships
response = requests.get(
    "https://gateway.maton.ai/klaviyo/api/profiles",
    headers={
        "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
        "revision": "2024-10-15"
    },
    params={
        "include": "lists",
        "fields[list]": "name,created"
    }
)
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/klaviyo/api/profiles?fields[profile]=email,first_name',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'revision': '2024-10-15'
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/klaviyo/api/profiles',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'revision': '2024-10-15'
    },
    params={'fields[profile]': 'email,first_name'}
)
data = response.json()
```

## Notes

- All requests use JSON:API specification
- Timestamps are in ISO 8601 RFC 3339 format (e.g., `2024-01-16T23:20:50.52Z`)
- Resource IDs are strings (often base64-encoded)
- Use sparse fieldsets to optimize response size
- Include `revision` header for API versioning (recommended: `2024-10-15`)
- Some POST endpoints return `200` instead of `201` for successful creation
- Coupon `external_id` must match regex `^[0-9_A-z]+$` (no hyphens)
- Coupon codes endpoint requires a filter (e.g., `filter=equals(coupon.id,"...")`)
- Flow creation via API may be limited; flows are typically created in the Klaviyo UI

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or missing Klaviyo connection |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden - insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited (fixed-window algorithm) |
| 4xx/5xx | Passthrough error from Klaviyo API |

## Resources

- [Klaviyo API Documentation](https://developers.klaviyo.com)
- [API Reference](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo Developer Portal](https://developers.klaviyo.com/en)
