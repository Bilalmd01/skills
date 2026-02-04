---
name: google-workspace-admin
description: |
  Google Workspace Admin SDK integration with managed OAuth. Manage users, groups, organizational units, and domain settings. Use this skill when users want to administer Google Workspace.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Google Workspace Admin

Access the Google Workspace Admin SDK with managed OAuth authentication. Manage users, groups, organizational units, roles, and domain settings for Google Workspace.

## Quick Start

```bash
# List users in the domain
curl -s -X GET 'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer&maxResults=10' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## Base URL

```
https://gateway.maton.ai/google-workspace-admin/{native-api-path}
```

Replace `{native-api-path}` with the actual Admin SDK API endpoint path. The gateway proxies requests to `admin.googleapis.com` and automatically injects your OAuth token.

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

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-workspace-admin&status=ACTIVE' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Create Connection

```bash
curl -s -X POST 'https://ctrl.maton.ai/connections' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"app": "google-workspace-admin"}'
```

### Get Connection

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
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
    "app": "google-workspace-admin",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Specifying Connection

If you have multiple Google Workspace Admin connections, specify which one to use with the `Maton-Connection` header:

```bash
curl -s -X GET 'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80'
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Users

#### List Users

```bash
GET /google-workspace-admin/admin/directory/v1/users?customer=my_customer&maxResults=100
```

Query parameters:
- `customer` - Customer ID or `my_customer` for your domain (required)
- `domain` - Filter by specific domain
- `maxResults` - Maximum results per page (1-500, default 100)
- `orderBy` - Sort by `email`, `familyName`, or `givenName`
- `query` - Search query (e.g., `email:john*`, `name:John*`)
- `pageToken` - Token for pagination

**Example:**

```bash
curl -s -X GET 'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer&query=email:john*' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "kind": "admin#directory#users",
  "users": [
    {
      "id": "123456789",
      "primaryEmail": "john@example.com",
      "name": {
        "givenName": "John",
        "familyName": "Doe",
        "fullName": "John Doe"
      },
      "isAdmin": false,
      "isDelegatedAdmin": false,
      "suspended": false,
      "creationTime": "2024-01-15T10:30:00.000Z",
      "lastLoginTime": "2025-02-01T08:00:00.000Z",
      "orgUnitPath": "/Sales"
    }
  ],
  "nextPageToken": "..."
}
```

#### Get User

```bash
GET /google-workspace-admin/admin/directory/v1/users/{userKey}
```

`userKey` can be the user's primary email or unique user ID.

#### Create User

```bash
POST /google-workspace-admin/admin/directory/v1/users
Content-Type: application/json

{
  "primaryEmail": "newuser@example.com",
  "name": {
    "givenName": "Jane",
    "familyName": "Smith"
  },
  "password": "temporaryPassword123!",
  "changePasswordAtNextLogin": true,
  "orgUnitPath": "/Engineering"
}
```

#### Update User

```bash
PUT /google-workspace-admin/admin/directory/v1/users/{userKey}
Content-Type: application/json

{
  "name": {
    "givenName": "Jane",
    "familyName": "Smith-Johnson"
  },
  "suspended": false,
  "orgUnitPath": "/Sales"
}
```

#### Patch User (partial update)

```bash
PATCH /google-workspace-admin/admin/directory/v1/users/{userKey}
Content-Type: application/json

{
  "suspended": true
}
```

#### Delete User

```bash
DELETE /google-workspace-admin/admin/directory/v1/users/{userKey}
```

#### Make User Admin

```bash
POST /google-workspace-admin/admin/directory/v1/users/{userKey}/makeAdmin
Content-Type: application/json

{
  "status": true
}
```

### Groups

#### List Groups

```bash
GET /google-workspace-admin/admin/directory/v1/groups?customer=my_customer
```

Query parameters:
- `customer` - Customer ID or `my_customer` (required)
- `domain` - Filter by domain
- `maxResults` - Maximum results (1-200)
- `userKey` - List groups for a specific user

#### Get Group

```bash
GET /google-workspace-admin/admin/directory/v1/groups/{groupKey}
```

`groupKey` can be the group's email or unique ID.

#### Create Group

```bash
POST /google-workspace-admin/admin/directory/v1/groups
Content-Type: application/json

{
  "email": "engineering@example.com",
  "name": "Engineering Team",
  "description": "All engineering staff"
}
```

#### Update Group

```bash
PUT /google-workspace-admin/admin/directory/v1/groups/{groupKey}
Content-Type: application/json

{
  "name": "Engineering Department",
  "description": "Updated description"
}
```

#### Delete Group

```bash
DELETE /google-workspace-admin/admin/directory/v1/groups/{groupKey}
```

### Group Members

#### List Members

```bash
GET /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members
```

#### Add Member

```bash
POST /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members
Content-Type: application/json

{
  "email": "user@example.com",
  "role": "MEMBER"
}
```

Roles: `OWNER`, `MANAGER`, `MEMBER`

#### Update Member Role

```bash
PATCH /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members/{memberKey}
Content-Type: application/json

{
  "role": "MANAGER"
}
```

#### Remove Member

```bash
DELETE /google-workspace-admin/admin/directory/v1/groups/{groupKey}/members/{memberKey}
```

### Organizational Units

#### List Org Units

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits
```

Query parameters:
- `type` - `all` (default) or `children`
- `orgUnitPath` - Parent org unit path

#### Get Org Unit

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
```

#### Create Org Unit

```bash
POST /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits
Content-Type: application/json

{
  "name": "Engineering",
  "parentOrgUnitPath": "/",
  "description": "Engineering department"
}
```

#### Update Org Unit

```bash
PUT /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
Content-Type: application/json

{
  "description": "Updated description"
}
```

#### Delete Org Unit

```bash
DELETE /google-workspace-admin/admin/directory/v1/customer/my_customer/orgunits/{orgUnitPath}
```

### Domains

#### List Domains

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/domains
```

#### Get Domain

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/domains/{domainName}
```

### Roles

#### List Roles

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/roles
```

#### List Role Assignments

```bash
GET /google-workspace-admin/admin/directory/v1/customer/my_customer/roleassignments
```

Query parameters:
- `userKey` - Filter by user
- `roleId` - Filter by role

#### Create Role Assignment

```bash
POST /google-workspace-admin/admin/directory/v1/customer/my_customer/roleassignments
Content-Type: application/json

{
  "roleId": "123456789",
  "assignedTo": "user_id",
  "scopeType": "CUSTOMER"
}
```

## Code Examples

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// List users
const users = await fetch(
  'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users?customer=my_customer',
  { headers }
).then(r => r.json());

// Create user
await fetch(
  'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      primaryEmail: 'newuser@example.com',
      name: { givenName: 'New', familyName: 'User' },
      password: 'TempPass123!',
      changePasswordAtNextLogin: true
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# List users
users = requests.get(
    'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
    headers=headers,
    params={'customer': 'my_customer'}
).json()

# Create user
response = requests.post(
    'https://gateway.maton.ai/google-workspace-admin/admin/directory/v1/users',
    headers=headers,
    json={
        'primaryEmail': 'newuser@example.com',
        'name': {'givenName': 'New', 'familyName': 'User'},
        'password': 'TempPass123!',
        'changePasswordAtNextLogin': True
    }
)
```

## Notes

- Use `my_customer` as the customer ID for your own domain
- User keys can be primary email or unique user ID
- Group keys can be group email or unique group ID
- Org unit paths start with `/` (e.g., `/Engineering/Frontend`)
- Admin privileges are required for most operations
- Password must meet Google's complexity requirements

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Workspace Admin connection |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient admin privileges |
| 404 | User, group, or resource not found |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Admin SDK API |

## Resources

- [Admin SDK Overview](https://developers.google.com/admin-sdk)
- [Directory API Users](https://developers.google.com/admin-sdk/directory/reference/rest/v1/users)
- [Directory API Groups](https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups)
- [Directory API Members](https://developers.google.com/admin-sdk/directory/reference/rest/v1/members)
- [Directory API Org Units](https://developers.google.com/admin-sdk/directory/reference/rest/v1/orgunits)
- [Directory API Domains](https://developers.google.com/admin-sdk/directory/reference/rest/v1/domains)
- [Directory API Roles](https://developers.google.com/admin-sdk/directory/reference/rest/v1/roles)
- [Admin SDK Guides](https://developers.google.com/admin-sdk/directory/v1/guides)
