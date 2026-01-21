# Troubleshooting Guide

This document provides detailed troubleshooting steps for common issues encountered when working with our application stack. Follow the guidelines below to diagnose and resolve problems efficiently.

---

## Backend Issues

### 1. Database Connection Errors

#### Symptoms
- Application fails to connect to the database
- Error messages like `Connection refused` or `Authentication failed`
- Migrations fail due to connection issues

#### Possible Causes
- Incorrect `DATABASE_URL` configuration
- PostgreSQL server not running
- Invalid database credentials (username/password)
- Network connectivity issues between app and DB

#### Step-by-Step Solutions
1. **Verify DATABASE_URL**
   ```bash
   echo $DATABASE_URL
   ```
   Ensure it's correctly formatted:
   ```
   postgresql://user:password@host:port/dbname
   ```

2. **Check if PostgreSQL is Running**
   ```bash
   sudo systemctl status postgresql
   # Or on macOS:
   brew services list | grep postgresql
   ```

3. **Test Credentials**
   ```bash
   psql $DATABASE_URL
   ```

4. **Restart Services**
   ```bash
   sudo systemctl restart postgresql
   ```

#### Prevention Tips
- Always validate your `.env` file before starting the application
- Use consistent naming conventions for environment variables
- Regularly test database connectivity during development

---

### 2. Migration Errors

#### Symptoms
- Migration scripts fail to execute
- "Migration already applied" or "Migration not found" errors
- Database schema inconsistencies

#### Possible Causes
- Corrupted migration history
- Conflicting migration files
- Incomplete previous migrations

#### Step-by-Step Solutions
1. **Clear Migration History**
   ```bash
   # For Django
   python manage.py migrate --fake-initial
   
   # For Sequelize
   npx sequelize db:migrate:undo:all
   ```

2. **Drop and Recreate Database**
   ```bash
   # PostgreSQL example
   dropdb your_database_name
   createdb your_database_name
   ```

3. **Re-run Migrations**
   ```bash
   # Django
   python manage.py migrate
   
   # Sequelize
   npx sequelize db:migrate
   ```

#### Prevention Tips
- Always backup your database before major migrations
- Keep migration files under version control
- Test migrations in a staging environment first

---

### 3. Import Errors

#### Symptoms
- Module not found errors (`ImportError`)
- Missing package warnings
- Runtime import failures

#### Possible Causes
- Virtual environment not activated
- Dependencies not installed properly
- Incorrect Python path settings
- Package version conflicts

#### Step-by-Step Solutions
1. **Verify Virtual Environment**
   ```bash
   which python
   pip list
   ```

2. **Reinstall Dependencies**
   ```bash
   pip install -r requirements.txt
   # Or for npm projects:
   npm install
   ```

3. **Check Python Path**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:."
   ```

4. **Upgrade Pip and Packages**
   ```bash
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

#### Prevention Tips
- Always activate your virtual environment before development
- Pin dependency versions in requirements.txt
- Use lock files (e.g., `package-lock.json`) for npm projects

---

### 4. JWT Token Errors

#### Symptoms
- Authentication failures
- "Invalid token" or "Token expired" errors
- Unauthorized access attempts

#### Possible Causes
- Incorrect `SECRET_KEY` configuration
- Token expiration settings too short
- Clock skew between client and server
- Token tampering or corruption

#### Step-by-Step Solutions
1. **Check SECRET_KEY**
   ```bash
   echo $SECRET_KEY
   ```

2. **Verify Token Expiration Settings**
   ```python
   # Example JWT settings
   JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
   ```

3. **Synchronize System Time**
   ```bash
   sudo ntpdate -s time.nist.gov
   ```

4. **Regenerate Tokens**
   - Log out and log back in
   - Clear browser storage/cache

#### Prevention Tips
- Store secret keys securely using environment variables
- Implement proper token refresh mechanisms
- Monitor token usage patterns for anomalies

---

## Frontend Issues

### 1. API Connection Errors

#### Symptoms
- Network request failures
- "Failed to fetch" or "Network error" messages
- Data not loading in UI components

#### Possible Causes
- Incorrect `VITE_API_URL` configuration
- Backend service not running
- CORS policy violations
- Firewall blocking requests

#### Step-by-Step Solutions
1. **Verify VITE_API_URL**
   ```bash
   echo $VITE_API_URL
   ```

2. **Check Backend Status**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Inspect Browser Console**
   - Open DevTools → Network tab
   - Look for failed requests and their details

4. **Configure CORS**
   ```javascript
   // In your backend config
   const corsOptions = {
     origin: process.env.FRONTEND_URL || 'http://localhost:3000',
     credentials: true
   };
   ```

#### Prevention Tips
- Set up proper error boundaries in React components
- Implement retry logic for API calls
- Use environment-specific URLs for different environments

---

### 2. Build Errors

#### Symptoms
- Compilation failures
- "Module not found" errors during build
- Build process hangs or crashes

#### Possible Causes
- Outdated dependencies
- Node.js version mismatch
- Corrupted node_modules directory
- Missing build dependencies

#### Step-by-Step Solutions
1. **Clear node_modules**
   ```bash
   rm -rf node_modules
   rm package-lock.json
   ```

2. **Reinstall Dependencies**
   ```bash
   npm install
   # Or with yarn:
   yarn install
   ```

3. **Check Node Version**
   ```bash
   node --version
   npm --version
   ```

4. **Use Node Version Manager**
   ```bash
   nvm install node
   nvm use node
   ```

#### Prevention Tips
- Pin specific Node.js versions in `.nvmrc`
- Regularly update dependencies with caution
- Use Docker for consistent builds across environments

---

### 3. Routing Issues

#### Symptoms
- Pages not rendering correctly
- Navigation breaks unexpectedly
- 404 errors on valid routes

#### Possible Causes
- Incorrect React Router setup
- Misconfigured route paths
- Missing route components
- History API issues

#### Step-by-Step Solutions
1. **Verify React Router Setup**
   ```jsx
   import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
   
   <Router>
     <Routes>
       <Route path="/" element={<Home />} />
       {/* Other routes */}
     </Routes>
   </Router>
   ```

2. **Check Route Paths**
   ```jsx
   // Make sure paths match exactly
   <Route path="/users/:id" element={<UserDetail />} />
   ```

3. **Add Fallback Routes**
   ```jsx
   <Route path="*" element={<NotFound />} />
   ```

4. **Debug with Console Logs**
   ```jsx
   useEffect(() => {
     console.log('Current location:', location.pathname);
   }, [location]);
   ```

#### Prevention Tips
- Use consistent naming for routes and components
- Implement route guards for protected pages
- Test navigation thoroughly in different scenarios

---

## Docker Issues

### 1. Container Won't Start

#### Symptoms
- Container exits immediately after starting
- No logs visible in `docker logs`
- Service unavailable

#### Possible Causes
- Environment variable misconfiguration
- Port conflicts
- Missing dependencies inside container
- Incorrect command in Dockerfile

#### Step-by-Step Solutions
1. **Check Container Logs**
   ```bash
   docker logs <container_id>
   ```

2. **Verify Environment Variables**
   ```yaml
   # docker-compose.yml
   environment:
     - DATABASE_URL=postgresql://...
   ```

3. **Check Port Conflicts**
   ```bash
   netstat -tuln | grep :8000
   ```

4. **Run Container Interactively**
   ```bash
   docker run -it <image_name> /bin/bash
   ```

#### Prevention Tips
- Validate your `docker-compose.yml` before deployment
- Use health checks in your Docker configurations
- Test containers locally before pushing to production

---

### 2. Volume Permission Errors

#### Symptoms
- File write/read failures
- "Permission denied" errors
- Data not persisting between container restarts

#### Possible Causes
- Incorrect user mapping in Docker
- File ownership issues on host system
- Mount point permissions

#### Step-by-Step Solutions
1. **Fix File Permissions**
   ```bash
   sudo chown -R $(id -u):$(id -g) ./data
   ```

2. **Use Named Volumes**
   ```yaml
   # docker-compose.yml
   volumes:
     app-data:
   ```

3. **Set Correct User in Dockerfile**
   ```dockerfile
   USER node
   ```

4. **Run with Proper UID/GID**
   ```bash
   docker run -u "$(id -u):$(id -g)" <image_name>
   ```

#### Prevention Tips
- Always specify user context in Dockerfiles
- Use named volumes for persistent data
- Test volume mounting in development environments

---

### 3. Network Issues

#### Symptoms
- Services cannot communicate
- DNS resolution failures
- Container networking problems

#### Possible Causes
- Incorrect service names in compose files
- Network configuration errors
- Docker bridge network issues

#### Step-by-Step Solutions
1. **Check Service Names**
   ```yaml
   # docker-compose.yml
   services:
     web:
       depends_on:
         - database
   ```

2. **Verify Network Configuration**
   ```bash
   docker network ls
   docker inspect <network_name>
   ```

3. **Test Connectivity**
   ```bash
   docker exec -it <container_name> ping <service_name>
   ```

4. **Recreate Networks**
   ```bash
   docker network prune
   docker-compose down && docker-compose up
   ```

#### Prevention Tips
- Define custom networks explicitly
- Use consistent naming conventions for services
- Document inter-service communication patterns

---

## General Issues

### 1. Port Already in Use

#### Symptoms
- Application fails to start
- "Address already in use" errors
- Server binding failures

#### Possible Causes
- Another process using the same port
- Previous instance still running
- Misconfigured port mappings

#### Step-by-Step Solutions
1. **Identify Process Using Port**
   ```bash
   lsof -i :8000
   # Or:
   netstat -tulpn | grep :8000
   ```

2. **Kill Process**
   ```bash
   kill -9 <PID>
   ```

3. **Change Port**
   ```bash
   export PORT=8080
   ```

4. **Use Different Port in Config**
   ```yaml
   # docker-compose.yml
   ports:
     - "8080:8000"
   ```

#### Prevention Tips
- Use different ports for local development
- Implement graceful shutdown handlers
- Monitor port usage in CI/CD pipelines

---

### 2. Permission Denied Errors

#### Symptoms
- File operations fail
- Directory creation errors
- Access control violations

#### Possible Causes
- Insufficient file system permissions
- Incorrect user/group ownership
- SELinux/AppArmor restrictions

#### Step-by-Step Solutions
1. **Check File Permissions**
   ```bash
   ls -la /path/to/directory
   ```

2. **Fix Ownership**
   ```bash
   sudo chown -R $USER:$USER /path/to/directory
   ```

3. **Adjust Permissions**
   ```bash
   chmod 755 /path/to/directory
   ```

4. **Disable Security Modules (if needed)**
   ```bash
   sudo setenforce 0  # SELinux
   ```

#### Prevention Tips
- Run applications with appropriate user privileges
- Use proper file permission management
- Configure security policies early in development

---

### 3. Environment Variables Not Loaded

#### Symptoms
- Missing configuration values
- Default values being used instead
- Runtime configuration failures

#### Possible Causes
- `.env` file not present or incorrectly named
- Variable name mismatches
- Loading order issues

#### Step-by-Step Solutions
1. **Verify .env File**
   ```bash
   cat .env
   ```

2. **Check Variable Names**
   ```bash
   echo $DATABASE_URL
   ```

3. **Load Variables Explicitly**
   ```bash
   source .env
   ```

4. **Use Dotenv Libraries**
   ```javascript
   require('dotenv').config();
   ```

#### Prevention Tips
- Include sample `.env.example` files
- Validate required environment variables at startup
- Use configuration validation libraries

---

### 4. Tests Failing

#### Symptoms
- Unit/integration tests fail
- Test suite timeouts
- Assertion failures

#### Possible Causes
- Flaky tests due to timing issues
- Environment differences
- Mock setup problems
- Dependency version conflicts

#### Step-by-Step Solutions
1. **Run Individual Tests**
   ```bash
   npm test -- --testNamePattern="specific test name"
   ```

2. **Check Test Environment**
   ```bash
   echo $NODE_ENV
   ```

3. **Reset Test State**
   ```bash
   npm run test:reset
   ```

4. **Update Snapshots**
   ```bash
   npm test -- -u
   ```

#### Prevention Tips
- Write deterministic tests
- Isolate test dependencies
- Use test fixtures consistently
- Implement proper cleanup in test teardown

---