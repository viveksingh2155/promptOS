# PromptOS Deployment Guide

Complete guide to deploying PromptOS to production with frontend on Vercel and backend on Render/Railway.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Environment Variables](#environment-variables)
4. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
5. [Backend Deployment (Render)](#backend-deployment-render)
6. [Alternative Backend (Railway)](#alternative-backend-railway)
7. [Ollama/AI Inference Configuration](#ollamai-inference-configuration)
8. [Database Configuration](#database-configuration)
9. [Google OAuth Setup](#google-oauth-setup)
10. [Custom Domain Configuration](#custom-domain-configuration)
11. [Troubleshooting](#troubleshooting)
12. [Production Checklist](#production-checklist)

---

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.12+
- Git
- Accounts on:
  - [Vercel](https://vercel.com) (frontend hosting)
  - [Render](https://render.com) or [Railway](https://railway.app) (backend hosting)
  - [Google Cloud Console](https://console.cloud.google.com) (OAuth)
  - Ollama instance (local or remote)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd promptos
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your local settings
# (Keep defaults for local development)

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your settings
# For local dev, keep the defaults

# Run the frontend
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 4. Ollama Setup (Local)

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull required model
ollama pull llama3.1

# Ollama runs on http://localhost:11434 by default
```

---

## Environment Variables

### Frontend Environment Variables

Create `frontend/.env.local` (for local) and configure these on Vercel (for production):

```bash
# API Base URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # Local
# NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com  # Production

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000  # Local
# NEXTAUTH_URL=https://your-app.vercel.app  # Production

# NextAuth Secret (generate with: openssl rand -base64 32)
NEXTAUTH_SECRET=your-generated-secret-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### Backend Environment Variables

Create `backend/.env` (for local) and configure on Render/Railway (for production):

```bash
# Database URL
DATABASE_URL=sqlite:///./promptos.db  # Local
# DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Production

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000  # Local
# CORS_ORIGINS=https://your-app.vercel.app,https://www.your-domain.com  # Production

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434  # Local
# OLLAMA_BASE_URL=https://your-ollama-server.com  # Remote Ollama
```

---

## Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel Dashboard

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your GitHub repository
   
3. **Configure Project**
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

4. **Add Environment Variables**
   
   In Vercel Dashboard → Settings → Environment Variables, add:
   
   ```
   NEXT_PUBLIC_API_BASE_URL = https://your-backend.onrender.com
   NEXTAUTH_URL = https://your-app.vercel.app
   NEXTAUTH_SECRET = <generate with: openssl rand -base64 32>
   GOOGLE_CLIENT_ID = your-google-client-id
   GOOGLE_CLIENT_SECRET = your-google-client-secret
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your production URL (e.g., `https://promptos.vercel.app`)

### Option 2: Deploy via Vercel CLI

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow prompts and configure as above
```

### Vercel Deployment Notes

- **Automatic Deployments**: Vercel will auto-deploy on every push to `main`
- **Preview Deployments**: Every PR gets a preview URL
- **Custom Domain**: Add in Vercel Dashboard → Settings → Domains
- **Environment Variables**: Set different values for Preview vs Production

---

## Backend Deployment (Render)

### 1. Prepare for Render

Create `render.yaml` in your repository root:

```yaml
services:
  - type: web
    name: promptos-backend
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: DATABASE_URL
        sync: false  # Set manually
      - key: CORS_ORIGINS
        sync: false  # Set manually
      - key: OLLAMA_BASE_URL
        sync: false  # Set manually
    healthCheckPath: /health
```

### 2. Deploy to Render

1. **Push code to GitHub** (if not already done)

2. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   
3. **Configure Service**
   - **Name**: `promptos-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free tier (for testing) or Starter ($7/mo)

4. **Add Environment Variables**
   
   In Render Dashboard → Environment tab, add:
   
   ```
   DATABASE_URL = <your-postgres-url>  # See Database Configuration below
   CORS_ORIGINS = https://your-app.vercel.app,https://www.your-domain.com
   OLLAMA_BASE_URL = <your-ollama-url>  # See Ollama Configuration below
   PYTHON_VERSION = 3.12.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment (~5-10 minutes)
   - Note your backend URL (e.g., `https://promptos-backend.onrender.com`)

6. **Update Frontend Environment**
   - Go to Vercel Dashboard
   - Update `NEXT_PUBLIC_API_BASE_URL` to your Render backend URL
   - Redeploy frontend

### Render Deployment Notes

- **Free Tier Limitations**:
  - Services spin down after 15 minutes of inactivity
  - Cold start takes ~30 seconds
  - 750 hours/month free (sleeps when inactive)
  
- **Paid Tier Benefits**:
  - Always-on instances
  - No cold starts
  - Better performance

- **Logs**: View in Render Dashboard → Logs tab
- **Health Checks**: Render pings `/health` endpoint every 5 minutes

---

## Alternative Backend (Railway)

### Deploy to Railway

1. **Create New Project**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service**
   - Railway auto-detects Python
   - Set **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   ```
   DATABASE_URL = <postgres-url>
   CORS_ORIGINS = https://your-app.vercel.app
   OLLAMA_BASE_URL = <ollama-url>
   ```

4. **Generate Domain**
   - Railway provides a free subdomain
   - Or add custom domain in Settings

Railway offers better free tier than Render (500 hours/month, no sleep) but requires credit card verification.

---

## Ollama/AI Inference Configuration

### Option 1: Local Ollama (Development Only)

```bash
# Install Ollama
# Visit: https://ollama.ai/download

# Pull model
ollama pull llama3.1

# Runs on http://localhost:11434
```

**Limitations**: Your deployed backend cannot reach your local machine.

### Option 2: Remote Ollama Instance

#### A. Deploy Ollama on a VPS (DigitalOcean, AWS, etc.)

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.1
ollama pull gemma2

# Configure to accept remote connections
# Edit /etc/systemd/system/ollama.service
# Add: Environment="OLLAMA_HOST=0.0.0.0:11434"

# Restart Ollama
sudo systemctl restart ollama

# Open firewall (if needed)
sudo ufw allow 11434
```

**Set backend environment variable**:
```
OLLAMA_BASE_URL=http://your-vps-ip:11434
```

#### B. Deploy Ollama on Render/Railway

Create a separate service for Ollama:

**Dockerfile for Ollama**:
```dockerfile
FROM ollama/ollama:latest

# Expose port
EXPOSE 11434

# Pull model on build (optional, can be slow)
# RUN ollama pull llama3.1

CMD ["ollama", "serve"]
```

**Note**: This requires significant memory (4GB+ RAM recommended).

#### C. Use Alternative AI Provider

If Ollama hosting is complex, consider:
- **OpenAI API**: Replace Ollama calls with OpenAI API
- **Anthropic Claude API**: Use Claude for prompt optimization
- **Hugging Face Inference API**: Hosted LLM endpoints

### Option 3: Docker Compose (Local + Self-Hosted)

For local development or self-hosting:

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - DATABASE_URL=sqlite:///./promptos.db
      - CORS_ORIGINS=http://localhost:3000
    depends_on:
      - ollama

volumes:
  ollama_data:
```

Run with: `docker-compose up -d`

---

## Database Configuration

### Local Development (SQLite)

SQLite works out of the box for local development:

```bash
DATABASE_URL=sqlite:///./promptos.db
```

### Production (PostgreSQL Recommended)

SQLite is **not recommended** for production multi-user deployments.

#### Option 1: Render PostgreSQL

1. **Create PostgreSQL Database**
   - Render Dashboard → "New +" → "PostgreSQL"
   - Choose region (same as backend)
   - Instance Type: Free or Starter
   
2. **Get Connection String**
   - Copy "Internal Database URL" (for Render services) or "External Database URL"
   - Format: `postgresql://user:password@host:5432/database`

3. **Set Environment Variable**
   ```
   DATABASE_URL=<your-postgres-url>
   ```

4. **Database will auto-migrate** on first backend startup

#### Option 2: Railway PostgreSQL

Railway offers one-click PostgreSQL:
- Dashboard → Add PostgreSQL
- Copy `DATABASE_URL` from Variables tab

#### Option 3: External PostgreSQL

Use any managed PostgreSQL:
- **Neon**: Free tier with generous limits
- **Supabase**: Free PostgreSQL + additional features
- **AWS RDS**: Scalable, paid
- **Heroku Postgres**: Simple, paid

Simply set the `DATABASE_URL` environment variable.

### Database Migrations

The backend automatically runs migrations on startup. To manually inspect:

```bash
cd backend
python -c "from database import engine, run_migrations; run_migrations()"
```

---

## Google OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select existing)
3. Name it "PromptOS" or similar

### 2. Enable APIs

1. Navigate to "APIs & Services" → "Library"
2. Search for "Google+ API" and enable it

### 3. Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (or "Internal" if G Suite org)
3. Fill in:
   - **App name**: PromptOS
   - **User support email**: your-email@example.com
   - **Developer contact**: your-email@example.com
4. Add scopes:
   - `userinfo.email`
   - `userinfo.profile`
5. Add test users (if in testing mode)
6. Save and continue

### 4. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Web application"
4. Configure:
   - **Name**: PromptOS Web Client
   - **Authorized JavaScript origins**:
     - `http://localhost:3000` (for local dev)
     - `https://your-app.vercel.app` (for production)
   - **Authorized redirect URIs**:
     - `http://localhost:3000/api/auth/callback/google` (local)
     - `https://your-app.vercel.app/api/auth/callback/google` (production)
5. Click "Create"
6. Copy **Client ID** and **Client Secret**

### 5. Add to Environment Variables

**Frontend (Vercel)**:
```
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456
```

### 6. Generate NextAuth Secret

```bash
openssl rand -base64 32
```

Add to frontend environment:
```
NEXTAUTH_SECRET=<generated-secret>
```

### Google OAuth Troubleshooting

- **"Redirect URI mismatch"**: Ensure exact URL match (with/without trailing slash, http vs https)
- **"Access blocked"**: Publish OAuth consent screen or add email to test users
- **"Invalid client"**: Double-check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

---

## Custom Domain Configuration

### Frontend (Vercel)

1. Purchase domain (Namecheap, Google Domains, etc.)
2. Vercel Dashboard → Settings → Domains
3. Add your domain (e.g., `promptos.app`)
4. Configure DNS records as instructed by Vercel
5. Wait for DNS propagation (~10 minutes to 48 hours)
6. Update environment variables:
   ```
   NEXTAUTH_URL=https://promptos.app
   ```
7. Update Google OAuth redirect URIs

### Backend (Render)

1. Render Dashboard → Settings → Custom Domain
2. Add domain (e.g., `api.promptos.app`)
3. Configure CNAME record in DNS:
   ```
   api.promptos.app  CNAME  promptos-backend.onrender.com
   ```
4. Wait for SSL certificate provisioning (~10 minutes)
5. Update frontend environment:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://api.promptos.app
   ```

---

## Troubleshooting

### Frontend Issues

#### Build Fails on Vercel

```
Error: Cannot find module...
```

**Fix**: Ensure all dependencies are in `package.json`, not `devDependencies`.

#### API Connection Error

```
API error 500: Failed to fetch
```

**Fix**:
1. Check `NEXT_PUBLIC_API_BASE_URL` is correct
2. Verify backend is running (visit `<backend-url>/health`)
3. Check CORS configuration on backend
4. Look at browser console for specific error

#### OAuth Redirect Error

```
OAuthCallback error: Invalid state
```

**Fix**:
1. Verify `NEXTAUTH_URL` matches your actual URL
2. Ensure `NEXTAUTH_SECRET` is set
3. Check Google OAuth redirect URIs

### Backend Issues

#### Ollama Connection Failed

```
ConnectionError: Ollama connection failed at http://localhost:11434
```

**Fix**:
1. Verify `OLLAMA_BASE_URL` is correct
2. Test Ollama endpoint: `curl <ollama-url>/api/version`
3. Check firewall/security group settings
4. Ensure Ollama service is running

#### Database Migration Error

```
OperationalError: no such table: prompt_history
```

**Fix**:
1. Check `DATABASE_URL` is correct
2. Backend auto-creates tables on startup
3. For PostgreSQL, ensure database exists
4. Check database connection: `psql <DATABASE_URL>`

#### CORS Error

```
Access to fetch blocked by CORS policy
```

**Fix**:
1. Add frontend URL to `CORS_ORIGINS`
2. Use exact URL (with https://, no trailing slash)
3. Restart backend after changing environment variables

#### Cold Start Timeout (Render Free Tier)

**Fix**:
1. Upgrade to paid tier for always-on
2. Use a service to ping `/health` every 10 minutes (e.g., UptimeRobot)
3. Warn users of ~30s initial load time

### General Debugging

#### View Backend Logs

- **Render**: Dashboard → Logs tab
- **Railway**: Dashboard → Deployments → View Logs
- **Local**: Terminal where `uvicorn` is running

#### View Frontend Logs

- **Vercel**: Dashboard → Deployments → Function Logs
- **Local**: Browser console (F12)

#### Test API Directly

```bash
# Health check
curl https://your-backend.onrender.com/health

# Test optimize endpoint (requires API)
curl -X POST https://your-backend.onrender.com/api/optimize \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","format":"gpt","model":"llama3.1","target_lang":"original"}'
```

---

## Production Checklist

### Before Going Live

- [ ] Generate secure `NEXTAUTH_SECRET` (not the example value)
- [ ] Use production Google OAuth credentials (not test credentials)
- [ ] Configure production database (PostgreSQL, not SQLite)
- [ ] Set up remote Ollama instance (or alternative AI provider)
- [ ] Configure proper `CORS_ORIGINS` (exact frontend URLs)
- [ ] Set `NEXTAUTH_URL` to actual production URL
- [ ] Set `NEXT_PUBLIC_API_BASE_URL` to actual backend URL
- [ ] Test OAuth flow end-to-end
- [ ] Test prompt optimization end-to-end
- [ ] Verify history saves correctly
- [ ] Check mobile responsiveness
- [ ] Set up monitoring (e.g., Sentry, LogRocket)
- [ ] Configure custom domain (optional)
- [ ] Add SSL certificate (usually automatic)
- [ ] Review and secure environment variables
- [ ] Enable error tracking
- [ ] Set up backup strategy for database

### Security Best Practices

- Never commit `.env` files to Git
- Rotate secrets regularly
- Use environment-specific credentials
- Enable rate limiting on backend (consider adding middleware)
- Keep dependencies updated (`npm audit`, `pip check`)
- Monitor for security vulnerabilities
- Use HTTPS everywhere
- Implement proper authentication checks on sensitive endpoints

### Performance Optimization

- Enable Vercel Edge caching where appropriate
- Optimize images (use Next.js Image component)
- Minimize bundle size (check with `npm run build`)
- Use database indexes for queries
- Consider CDN for static assets
- Monitor backend response times
- Optimize Ollama model size vs accuracy tradeoff

### Monitoring & Maintenance

- Set up uptime monitoring (UptimeRobot, Pingdom)
- Configure error tracking (Sentry)
- Monitor API rate limits
- Watch database storage usage
- Check Ollama model performance
- Review logs regularly
- Plan for database backups
- Document incident response procedures

---

## Support

For issues or questions:

1. Check this deployment guide
2. Review error logs (Vercel, Render, browser console)
3. Test each component individually
4. Verify environment variables
5. Check GitHub Issues for similar problems

---

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [NextAuth.js Documentation](https://next-auth.js.org)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Ollama Documentation](https://ollama.ai/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated**: 2024
**Version**: 1.0.0
