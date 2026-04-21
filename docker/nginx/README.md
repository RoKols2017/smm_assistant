# Nginx Deployment Notes

This directory contains the container-side reverse proxy configuration for VPS deployments.

## Current mode

- HTTP-first rollout through `docker-compose.production.yml`
- `nginx` listens on port `80`
- requests are proxied to `web:8000`
- `GET /healthz` is forwarded directly to Flask without redirects

## Mounted paths

- `docker/nginx/nginx.conf` -> base nginx runtime config
- `docker/nginx/conf.d/default.conf` -> application vhost and upstream rules
- `docker/nginx/includes/proxy_params.conf` -> forwarded headers and proxy defaults
- `docker/nginx/certs/` -> reserved for future TLS certificate mounts
- `docker/nginx/www/` -> reserved for future ACME webroot challenges

## First VPS bootstrap

1. Start the stack with the production override.
2. Confirm `docker compose logs -f nginx web` shows healthy upstream traffic.
3. Check `curl http://<server>/healthz` before adding DNS/TLS changes.

Expected healthy log signals:

- `nginx` access log with `GET /healthz` and `status=200`
- `web` log entries from `[main.healthz]`
- no repeated upstream `502` or `504` errors

## TLS follow-up

The current rollout intentionally does not terminate TLS inside the container yet.
When HTTPS is added later, reuse these directories for certificates and ACME webroot content instead of redesigning the compose topology.
