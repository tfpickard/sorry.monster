# Deployment Guide

## Server Requirements

- Ubuntu 22.04 LTS or newer
- Docker 24+ and Docker Compose v2
- NGINX 1.18+
- Certbot for Let's Encrypt
- 2GB RAM minimum
- 20GB disk space

## Port Restrictions

**CRITICAL**: The following ports are FORBIDDEN on the shared server:
- ❌ 3000
- ❌ 4000
- ❌ 8000

**REQUIRED** ports:
- ✅ 8082 - sorry.monster frontend
- ✅ 8083 - API backend
- ✅ 8085 - oops.ninja instant service

## Initial Server Setup

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install NGINX
sudo apt install nginx

# Install Certbot
sudo apt install certbot python3-certbot-nginx
```

### 2. Create Deploy User

```bash
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy
sudo mkdir -p /home/deploy/sorry.monster
sudo chown -R deploy:deploy /home/deploy/sorry.monster
```

### 3. Configure SSH Key

```bash
# On your local machine, generate a key if needed:
ssh-keygen -t ed25519 -C "deploy@sorry.monster"

# Copy public key to server:
ssh-copy-id deploy@your.server.com

# Test connection:
ssh deploy@your.server.com
```

### 4. Obtain SSL Certificates

```bash
# For sorry.monster
sudo certbot certonly --nginx -d sorry.monster -d www.sorry.monster

# For oops.ninja
sudo certbot certonly --nginx -d oops.ninja -d www.oops.ninja

# Verify certificates
sudo ls -la /etc/letsencrypt/live/sorry.monster/
sudo ls -la /etc/letsencrypt/live/oops.ninja/
```

### 5. Configure NGINX

The NGINX configs will be deployed automatically via CI/CD to:
- `/etc/nginx/sites-available/sorry.monster.conf`
- `/etc/nginx/sites-available/oops.ninja.conf`

They will be symlinked to `sites-enabled/` during deployment.

### 6. Configure GitHub Secrets

In your GitHub repository, go to **Settings → Secrets and variables → Actions** and add:

```
SSH_HOST          = your.server.com
SSH_USER          = deploy
SSH_KEY           = [paste private SSH key]
TARGET_DIR        = /home/deploy/sorry.monster
ENV_FILE_B64      = [base64 encoded .env file]
```

To create `ENV_FILE_B64`:
```bash
# Create your .env file with:
# OPENAI_API_KEY=sk-...
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
# etc.

# Then base64 encode it:
base64 -w 0 .env
# Copy the output to GitHub secret
```

## Automated Deployment

Once GitHub Actions is configured, deployment happens automatically:

1. **Push to main** triggers the deploy workflow
2. **Builds** frontend and backend
3. **Rsyncs** files to server
4. **Restarts** Docker services
5. **Updates** NGINX configs
6. **Reloads** NGINX

## Manual Deployment

If you need to deploy manually:

```bash
# SSH to server
ssh deploy@your.server.com
cd /home/deploy/sorry.monster

# Pull latest code
git pull origin main

# Build and restart
docker compose pull
docker compose up -d --build

# Update NGINX configs
sudo ln -sf /home/deploy/sorry.monster/nginx/sorry.monster.conf \
  /etc/nginx/sites-available/sorry.monster.conf
sudo ln -sf /home/deploy/sorry.monster/nginx/oops.ninja.conf \
  /etc/nginx/sites-available/oops.ninja.conf
sudo ln -sf /etc/nginx/sites-available/sorry.monster.conf \
  /etc/nginx/sites-enabled/
sudo ln -sf /etc/nginx/sites-available/oops.ninja.conf \
  /etc/nginx/sites-enabled/

# Test and reload NGINX
sudo nginx -t
sudo systemctl reload nginx
```

## Rollback

To rollback to a previous version:

```bash
ssh deploy@your.server.com
cd /home/deploy/sorry.monster

# Find previous commit
git log --oneline -n 10

# Rollback
git reset --hard <commit-hash>
docker compose up -d --build
sudo systemctl reload nginx
```

## Monitoring

### Health Checks

```bash
# Check service status
curl https://sorry.monster/health
curl https://oops.ninja/health
curl http://localhost:8083/health

# Check Docker services
docker compose ps
docker compose logs -f
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f sorry_api
docker compose logs -f sorry_frontend
docker compose logs -f oops_service

# NGINX logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart sorry_api

# Reload NGINX
sudo systemctl reload nginx
```

## SSL Certificate Renewal

Certbot should auto-renew, but to manually renew:

```bash
sudo certbot renew
sudo systemctl reload nginx
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using a port
sudo lsof -i :8082
sudo lsof -i :8083
sudo lsof -i :8085

# Kill process if needed
sudo kill -9 <PID>
```

### Docker Issues

```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Rebuild from scratch
docker compose down -v
docker compose up -d --build
```

### NGINX Issues

```bash
# Test configuration
sudo nginx -t

# Check status
sudo systemctl status nginx

# Restart NGINX
sudo systemctl restart nginx
```

## Security Hardening

### Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Regular Updates

```bash
# Set up unattended upgrades
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## Performance Tuning

### NGINX

Edit `/etc/nginx/nginx.conf`:
```nginx
worker_processes auto;
worker_connections 4096;
keepalive_timeout 65;
gzip on;
```

### Docker

Edit `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## Backup Strategy

### Database Backups

```bash
# Backup PostgreSQL
docker compose exec postgres pg_dump -U sorry sorrydb > backup.sql

# Restore
docker compose exec -T postgres psql -U sorry sorrydb < backup.sql
```

### Configuration Backups

```bash
# Backup .env and configs
tar -czf backup-$(date +%Y%m%d).tar.gz .env nginx/ docker-compose.yml
```

## Support

For deployment issues, check:
1. GitHub Actions logs
2. Docker logs: `docker compose logs`
3. NGINX logs: `/var/log/nginx/`
4. System logs: `journalctl -xe`
