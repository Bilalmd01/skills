---
name: render
description: Deploy and operate apps on Render. Use when the user wants to deploy, host, or publish an app; create or edit render.yaml Blueprints; add web services, static sites, private services, workers, cron jobs, Postgres, or Key Value (Redis/Valkey); configure env vars, health checks, scaling, preview environments, or projects; validate Blueprints; or get dashboard/API guidance.
metadata:
  { "openclaw": { "emoji": "☁️", "homepage": "https://render.com/docs" } }
---

# Render Skill

Deploy and manage applications on Render using Blueprints (`render.yaml`), the Dashboard, or the API. This skill covers deployment and platform features: web apps, static sites, workers, cron, Postgres, Key Value, env groups, scaling, previews, and projects.

## When to Use

- Deploy, host, or publish an app on Render
- Create or edit a `render.yaml` Blueprint (new or existing repo)
- Add web, static site, private, worker, or cron services; Postgres; or Key Value
- Configure env vars, health checks, scaling, disks, or regions
- Set up preview environments or projects/environments
- Validate a Blueprint or get dashboard/API links

## Blueprint Basics

- **File:** `render.yaml` at the **root** of the Git repository (required).
- **Root-level keys (official spec):** `services`, `databases`, `envVarGroups`, `projects`, `ungrouped`, `previews.generation`, `previews.expireAfterDays`.
- **Spec:** [Blueprint YAML Reference](https://render.com/docs/blueprint-spec). JSON Schema for IDE validation: https://render.com/schema/render.yaml.json (e.g. YAML extension by Red Hat in VS Code/Cursor).

**Validation:** `render blueprints validate render.yaml` (Render CLI v2.7.0+), or the [Validate Blueprint API](https://api-docs.render.com/reference/validate-blueprint) endpoint.

## Service Types

| type       | Purpose |
|------------|--------|
| `web`      | Public HTTP app or static site (use `runtime: static` for static) |
| `pserv`    | Private service (internal hostname only, no public URL) |
| `worker`   | Background worker (runs continuously, e.g. job queues) |
| `cron`     | Scheduled job (cron expression; runs and exits) |
| `keyvalue` | Render Key Value instance (Redis/Valkey-compatible; **defined in `services`**) |

**Note:** Private services use `pserv`, not `private`. Key Value is a service with `type: keyvalue`; do not use a separate root key for it in new Blueprints (some older blueprints use `keyValueStores` and `fromKeyValueStore`—prefer the official format).

## Runtimes

Use **`runtime`** (preferred; `env` is deprecated): `node`, `python`, `elixir`, `go`, `ruby`, `rust`, `docker`, `image`, `static`. For static sites: `type: web`, `runtime: static`, and **`staticPublishPath`** (e.g. `./build` or `./dist`) required.

## Minimal Web Service

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
```

Python example: `runtime: python`, `buildCommand: pip install -r requirements.txt`, `startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT` (or gunicorn). Set `PYTHON_VERSION` / `NODE_VERSION` in envVars when needed.

## Static Site

```yaml
- type: web
  name: my-blog
  runtime: static
  buildCommand: yarn build
  staticPublishPath: ./build
```

Optional: `headers`, `routes` (redirects/rewrites). See [Static Sites](https://render.com/docs/static-sites).

## Environment Variables

- **Literal:** `key` + `value` (never hardcode secrets).
- **From Postgres:** `fromDatabase.name` + `fromDatabase.property` (e.g. `connectionString`).
- **From Key Value or other service:** `fromService.type` + `fromService.name` + `fromService.property` (e.g. `connectionString`, `host`, `port`, `hostport`) or `fromService.envVarKey` for another service’s env var.
- **Secret / user-set:** `sync: false` (user is prompted in Dashboard on first create; add new secrets manually later). **Cannot be used inside env var groups.**
- **Generated:** `generateValue: true` (base64 256-bit value).
- **Shared:** `fromGroup: <envVarGroups[].name>` to attach an env var group.

Env groups **cannot** reference other services (no `fromDatabase`/`fromService` in groups) and **cannot** use `sync: false`. Put secrets and DB/KV references in **service-level** `envVars`, or reference a group and add service-specific vars alongside.

## Databases (Render Postgres)

```yaml
databases:
  - name: my-db
    plan: basic-256mb
    databaseName: my_app
    user: my_user
    region: oregon
    postgresMajorVersion: "18"
```

**Plans (current):** `free`, `basic-256mb`, `basic-1gb`, `basic-4gb`, `pro-*`, `accelerated-*`. Legacy: `starter`, `standard`, `pro`, `pro plus` (no new DBs on legacy). Optional: `diskSizeGB`, `ipAllowList`, `readReplicas`, `highAvailability.enabled`. Reference in services: `fromDatabase.name`, `property: connectionString`.

## Key Value (Redis/Valkey)

Key Value instances are **services** with `type: keyvalue` (or deprecated `redis`). **`ipAllowList` is required:** use `[]` for internal-only, or `- source: 0.0.0.0/0` to allow external.

```yaml
services:
  - type: keyvalue
    name: my-cache
    ipAllowList:
      - source: 0.0.0.0/0
        description: everywhere
    plan: free
    maxmemoryPolicy: allkeys-lru
```

Reference in another service: `fromService.type: keyvalue`, `fromService.name: my-cache`, `property: connectionString`. Policies: `allkeys-lru` (caching), `noeviction` (job queues), etc. See [Key Value](https://render.com/docs/key-value).

**Note:** Some repos use root-level `keyValueStores` and `fromKeyValueStore`; the official spec uses `services` + `fromService`. Prefer the official form for new Blueprints.

## Cron Jobs

```yaml
- type: cron
  name: my-cron
  runtime: python
  schedule: "0 * * * *"
  buildCommand: "true"
  startCommand: python scripts/daily.py
  envVars: []
```

`schedule` is a cron expression (minute hour day month weekday). `buildCommand` is required (use `"true"` if no build). Free plan not available for cron/worker/pserv.

## Env Var Groups

Share vars across services. No `fromDatabase`/`fromService`/`sync: false` inside groups—only literal values or `generateValue: true`.

```yaml
envVarGroups:
  - name: app-env
    envVars:
      - key: CONCURRENCY
        value: "2"
      - key: APP_SECRET
        generateValue: true

services:
  - type: web
    name: api
    envVars:
      - fromGroup: app-env
      - key: DATABASE_URL
        fromDatabase:
          name: my-db
          property: connectionString
```

## Health Check, Region, Pre-deploy

- **Web only:** `healthCheckPath: /health` for zero-downtime deploys.
- **Region:** `region: oregon` (default), `ohio`, `virginia`, `frankfurt`, `singapore` (set at create; cannot change later).
- **Pre-deploy:** `preDeployCommand` runs after build, before start (e.g. migrations).

## Scaling

- **Manual:** `numInstances: 2`.
- **Autoscaling** (Professional workspace): `scaling.minInstances`, `scaling.maxInstances`, `scaling.targetCPUPercent` or `scaling.targetMemoryPercent`. Not available with persistent disks.

## Disks, Monorepos, Docker

- **Persistent disk:** `disk.name`, `disk.mountPath`, `disk.sizeGB` (web, pserv, worker).
- **Monorepo:** `rootDir`, `buildFilter.paths` / `buildFilter.ignoredPaths`, `dockerfilePath` / `dockerContext`.
- **Docker:** `runtime: docker` (build from Dockerfile) or `runtime: image` (pull from registry). Use `dockerCommand` instead of `startCommand` when needed.

## Preview Environments & Projects

- **Preview environments:** Root-level `previews.generation: off | manual | automatic`, optional `previews.expireAfterDays`. Per-service `previews.generation`, `previews.numInstances`, `previews.plan`.
- **Projects/environments:** Root-level `projects` with `environments` (each lists `services`, `databases`, `envVarGroups`). Use for staging/production. Optional `ungrouped` for resources not in any environment.

## Plans (Services)

`plan: free | starter | standard | pro | pro plus` (and for web/pserv/worker: `pro max`, `pro ultra`). Omit to keep existing or default to `starter` for new. Free not available for pserv, worker, cron.

## Dashboard & API

- **Dashboard:** https://dashboard.render.com — New → Blueprint, connect repo, select `render.yaml`.
- **Key Value:** https://dashboard.render.com/new/redis
- **API:** https://api-docs.render.com — create/update services, validate Blueprint, etc.

## Checklist for New Deploys

1. Add or update `render.yaml` with `services` (and optionally `databases`, `envVarGroups`, `projects`). Use `runtime` and official Key Value form (`type: keyvalue` in services, `fromService` for references).
2. Use `sync: false` for secrets in **service** envVars only; tell user to set them in Dashboard. Never put secrets in env groups.
3. For Key Value, set `ipAllowList` (required).
4. Validate: `render blueprints validate render.yaml` or API.
5. Point user to Dashboard to connect repo and deploy.

## Rules

- Prefer Blueprint for full app definition; suggest Dashboard/API only when Blueprint cannot express something.
- Never commit real API keys or secrets; use `sync: false` and document which env vars the user must set.
- Use `runtime` (not deprecated `env`). For Python/Node set `PYTHON_VERSION`/`NODE_VERSION` in envVars when required.
- When referencing Key Value or other services, use `fromService` with correct `type` (e.g. `keyvalue`, `pserv`).
