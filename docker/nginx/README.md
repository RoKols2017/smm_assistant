# Nginx Deployment Notes

This directory contains the container-side reverse proxy configuration for VPS deployments.

## Current mode

- HTTPS-ready rollout through `docker-compose.production.yml`
- `deploy_vps.sh` asks for the domain during deploy
- `nginx` listens on ports `80` and `443`
- regular HTTP traffic is redirected to HTTPS
- `GET /healthz` is forwarded directly to Flask without redirects

## Mounted paths

- `docker/nginx/nginx.conf` -> base nginx runtime config
- `docker/nginx/templates/default.conf.template` -> envsubst template for HTTP/HTTPS vhost rules
- `docker/nginx/includes/proxy_params.conf` -> forwarded headers and proxy defaults
- `docker/nginx/certs/` -> runtime symlinks to the selected certificate pair
- `docker/nginx/www/` -> ACME webroot challenges if needed later

## First VPS bootstrap

1. Put the certificate files under `/root/cert/<domain>/`.
2. Run `./deploy_vps.sh` and enter the domain when prompted.
3. Confirm `docker compose logs -f nginx web` shows healthy upstream traffic.
4. Check `curl http://<server>/healthz` and `curl -I https://<domain>/`.

Expected healthy log signals:

- `nginx` access log with `GET /healthz` and `status=200`
- `nginx` access log with HTTP `301` redirects to HTTPS
- `web` log entries from `[main.healthz]`
- no repeated upstream `502` or `504` errors
