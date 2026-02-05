```markdown
# Priority Todo List - Setup Guide

This document provides comprehensive setup instructions for the Priority Todo List application across different environments.

## Table of Contents
1. [Local Development](#local-development)
   - [Prerequisites Installation](#prerequisites-installation)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
   - [Verification Steps](#verification-steps)
2. [Docker Development](#docker-development)
   - [Prerequisites](#prerequisites)
   - [Build and Run](#build-and-run)
   - [Access Services](#access-services)
   - [View Logs](#view-logs)
   - [Stop Services](#stop-services)
3. [Production Deployment](#production-deployment)
   - [Server Requirements](#server-requirements)
   - [Environment Setup](#environment-setup)
   - [Build Process](#build-process)
   - [Database Setup](#database-setup)
   - [Deployment Steps](#deployment-steps)
   - [Monitoring](#monitoring)
4. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites Installation

#### Python 3.11+
Install Python 3.11 or higher:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# macOS (using Homebrew)
brew install python@3.11

# Windows
# Download from https://www.python.org/downloads/
```

#### Node.js 20+
Install Node.js 20+:
```bash
# Using NodeSource repository (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Using nvm (macOS/Linux)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20

# Windows
# Download from https://nodejs.org/en/download/
```

#### PostgreSQL 15+
Install PostgreSQL 15:
```bash
# Ubuntu/Debian
sudo apt install postgresql-15 postgresql-client-15

# macOS (using Homebrew)
brew install postgresql@15

# Windows
# Download from https://www.postgresql.org/download/windows/
```

### Backend Setup

#### Clone Repository
```bash
git clone <repository-url>
cd priority-todo-list
```

#### Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Setup Database
```bash
# Start PostgreSQL service
sudo systemctl start postgresql

# Create database user and database
sudo -u postgres psql
CREATE USER todo_user WITH PASSWORD 'todo_password';
CREATE DATABASE todo_db OWNER todo_user;
GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
\q
```

#### Run Migrations
```bash
# Ensure you're in the backend directory
cd backend

# Apply database migrations
python manage.py migrate
```

#### Configure Environment Variables
Create `.env` file in the `backend` directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Start Server
```bash
python manage.py runserver
```

### Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment
Create `.env` file in the `frontend` directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_NODE_ENV=development
```

#### Start Dev Server
```bash
npm start
```

### Verification Steps

1. **Backend Verification**
   - Visit `http://localhost:8000/api/health/`
   - Should return a JSON response indicating healthy status

2. **Frontend Verification**
   - Visit `http://localhost:3000`
   - Should display the main application interface
   - Verify that you can create and view todos

3. **Database Verification**
   - Connect to PostgreSQL: `psql -U todo_user -d todo_db`
   - Run `\dt` to list tables
   - Should see tables like `todos_todo`, `auth_user`, etc.

---

## Docker Development

### Prerequisites

1. Install Docker Engine (version 20.10+):
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose

   # macOS
   brew install docker

   # Windows
   # Download from https://desktop.docker.com/win/main/amd64/docker-desktop-4.28.0.exe
   ```

2. Ensure Docker Compose is available:
   ```bash
   docker-compose --version
   ```

### Build and Run

1. **Build Images**
   ```bash
   docker-compose build
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

### Access Services

1. **Backend API**
   - URL: `http://localhost:8000/api/`
   - Health check: `http://localhost:8000/api/health/`

2. **Frontend Application**
   - URL: `http://localhost:3000`

3. **Database**
   - Host: `localhost`
   - Port: `5432`
   - User: `todo_user`
   - Password: `todo_password`
   - Database: `todo_db`

### View Logs

```bash
# View all container logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database

# Follow logs in real-time
docker-compose logs -f
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (data will be lost)
docker-compose down -v
```

---

## Production Deployment

### Server Requirements

1. **Operating System**: Ubuntu 20.04 LTS or later
2. **Memory**: Minimum 2GB RAM
3. **Storage**: Minimum 10GB free space
4. **Network**: Public IP address with ports 80 and 443 open
5. **Firewall**: Allow traffic on ports 80 (HTTP), 443 (HTTPS), 22 (SSH)

### Environment Setup

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Required Packages**
   ```bash
   sudo apt install -y python3-pip python3-venv nginx git curl
   ```

3. **Install PostgreSQL 15**
   ```bash
   sudo apt install postgresql-15 postgresql-client-15
   ```

4. **Configure Firewall**
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

### Build Process

1. **Clone Repository**
   ```bash
   cd /opt
   sudo git clone <repository-url> priority-todo-list
   cd priority-todo-list
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Build Frontend**
   ```bash
   cd frontend
   npm ci --only=production
   npm run build
   cd ..
   ```

### Database Setup

1. **Create Database and User**
   ```bash
   sudo -u postgres psql
   CREATE USER todo_user WITH PASSWORD 'secure_password_here';
   CREATE DATABASE todo_db OWNER todo_user;
   GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
   \q
   ```

2. **Configure PostgreSQL**
   Edit `/etc/postgresql/15/main/postgresql.conf`:
   ```conf
   listen_addresses = '*'
   port = 5432
   ```

   Edit `/etc/postgresql/15/main/pg_hba.conf`:
   ```conf
   host    todo_db    todo_user    127.0.0.1/32    md5
   host    todo_db    todo_user    ::1/128         md5
   ```

3. **Restart PostgreSQL**
   ```bash
   sudo systemctl restart postgresql
   ```

### Deployment Steps

1. **Configure Environment Variables**
   Create `/opt/priority-todo-list/.env`:
   ```env
   DEBUG=False
   SECRET_KEY=your-very-secure-secret-key-here
   DATABASE_URL=postgresql://todo_user:secure_password_here@localhost:5432/todo_db
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

2. **Run Migrations**
   ```bash
   cd /opt/priority-todo-list/backend
   source /opt/priority-todo-list/venv/bin/activate
   python manage.py migrate
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Create Gunicorn Service**
   Create `/etc/systemd/system/todo-gunicorn.service`:
   ```ini
   [Unit]
   Description=Gunicorn instance to serve Priority Todo List
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/priority-todo-list/backend
   ExecStart=/opt/priority-todo-list/venv/bin/gunicorn --workers 3 --bind unix:todo.sock -m 007 wsgi:application
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Create Nginx Configuration**
   Create `/etc/nginx/sites-available/todo`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location /static/ {
           alias /opt/priority-todo-list/backend/staticfiles/;
       }

       location /media/ {
           alias /opt/priority-todo-list/media/;
       }

       location / {
           proxy_pass http://unix:/opt/priority-todo-list/backend/todo.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/todo /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

6. **Start Services**
   ```bash
   sudo systemctl start todo-gunicorn
   sudo systemctl enable todo-gunicorn
   ```

### Monitoring

1. **System Monitoring**
   Install monitoring tools:
   ```bash
   sudo apt install htop iotop iftop
   ```

2. **Log Monitoring**
   Check application logs:
   ```bash
   sudo journalctl -u todo-gunicorn -f
   ```

3. **Health Checks**
   Monitor API health endpoint:
   ```bash
   curl http://your-domain.com/api/health/
   ```

4. **Performance Monitoring**
   Use tools like New Relic, Datadog, or Prometheus for advanced monitoring.

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors
**Problem**: "FATAL: password authentication failed"
**Solution**:
```bash
# Check PostgreSQL configuration
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Ensure correct authentication method is set
sudo systemctl restart postgresql
```

#### 2. Permission Denied Errors
**Problem**: "Permission denied" when running commands
**Solution**:
```bash
# Fix ownership
sudo chown -R $USER:$USER /opt/priority-todo-list
# Fix permissions
chmod +x /opt/priority-todo-list/scripts/*.sh
```

#### 3. Port Already in Use
**Problem**: "Address already in use" error
**Solution**:
```bash
# Find processes using port
sudo lsof -i :8000
# Kill process
sudo kill -9 <PID>
```

#### 4. Frontend Not Loading
**Problem**: React app shows blank screen or errors
**Solution**:
```bash
# Check build process
cd frontend
npm run build
# Verify static files are generated
ls -la build/static/
```

#### 5. Gunicorn Not Starting
**Problem**: Service fails to start
**Solution**:
```bash
# Check logs
sudo journalctl -u todo-gunicorn
# Verify Python path
which python3
# Check virtual environment activation
source /opt/priority-todo-list/venv/bin/activate
```

#### 6. Nginx Configuration Issues
**Problem**: 502 Bad Gateway errors
**Solution**:
```bash
# Test Nginx config
sudo nginx -t
# Check socket permissions
ls -la /opt/priority-todo-list/backend/todo.sock
# Restart services
sudo systemctl restart nginx
sudo systemctl restart todo-gunicorn
```

#### 7. Docker Issues
**Problem**: Containers fail to start
**Solution**:
```bash
# Check container status
docker-compose ps
# View detailed logs
docker-compose logs --tail=100
# Rebuild containers
docker-compose build --no-cache
```

#### 8. Memory Issues
**Problem**: Application crashes due to memory limits
**Solution**:
```bash
# Check system memory
free -h
# Increase swap space if needed
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 9. SSL Certificate Issues
**Problem**: HTTPS not working properly
**Solution**:
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx
# Obtain certificate
sudo certbot --nginx -d your-domain.com
# Auto-renewal
sudo crontab -e
# Add line: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 10. Environment Variable Issues
**Problem**: App doesn't read environment variables
**Solution**:
```bash
# Verify .env file exists and has correct format
cat /opt/priority-todo-list/.env
# Check variable loading in Django shell
python manage.py shell
>>> import os
>>> print(os.environ.get('SECRET_KEY'))
```

### Debugging Tips

1. **Use verbose logging** during development:
   ```bash
   export DJANGO_SETTINGS_MODULE=todo.settings.development
   python manage.py runserver --verbosity=2
   ```

2. **Check Python version compatibility**:
   ```bash
   python --version
   pip --version
   ```

3. **Verify package installations**:
   ```bash
   pip list
   npm list
   ```

4. **Test database connectivity**:
   ```bash
   psql -U todo_user -d todo_db -c "SELECT version();"
   ```

5. **Validate configuration files**:
   ```bash
   python manage.py check --deploy
   ```

### Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
```