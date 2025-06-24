# 🔥❌ BurnStop

<div align="center">

**The Ultimate Self-Hosted Startup Cost Tracking & Optimization Platform**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Powered-412991?logo=openai&logoColor=white)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Self-Hosted](https://img.shields.io/badge/Self--Hosted-✅-brightgreen)](https://github.com/awesome-selfhosted/awesome-selfhosted)

*Stop burning money on cloud services you forgot about!*

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [🏠 Self-Hosting](#-self-hosting-guide) • [🐳 Docker](#-docker-deployment) • [🔧 API](#-api-documentation)

</div>

---

## 🌟 What is BurnStop?

BurnStop is a **powerful, self-hosted platform** that helps startups and developers track, analyze, and optimize their cloud infrastructure costs across **AWS, GCP, Azure, and other platforms**. With AI-powered insights, real-time cost tracking, and beautiful analytics, BurnStop ensures you never overspend on cloud services again.

### 💡 Why BurnStop?

- **🔥 Stop Cost Burnouts**: Track all your cloud services in one place
- **🤖 AI-Powered Insights**: Get personalized cost optimization recommendations
- **📊 Beautiful Analytics**: Visualize spending trends and predictions
- **⏰ Smart Reminders**: Never miss a renewal or billing cycle
- **🏠 Self-Hosted**: Your data stays on your servers
- **🔒 Enterprise Security**: Built with security-first principles
- **🌐 Multi-Platform**: AWS, GCP, Azure, and custom services

---

## 📊 Features

### 🎯 **Core Features**
- **Multi-Platform Support**: Track services across AWS, GCP, Azure, and other platforms
- **Real-Time Cost Tracking**: Monitor spending with live updates and budget alerts
- **Smart Budget Management**: Set budgets and get warned before overspending
- **Service Organization**: Group services by teams, projects, or environments

### 🤖 **AI-Powered Intelligence**
- **Cost Optimization**: AI analyzes your spending patterns and suggests savings
- **Security Insights**: Get recommendations for improving service security
- **Performance Analysis**: Optimize resource utilization across platforms
- **Trend Predictions**: Forecast future costs with machine learning

### 📈 **Advanced Analytics**
- **Cost Trend Visualization**: Beautiful charts showing spending over time
- **Platform Distribution**: See which platforms cost you the most
- **Budget vs. Actual**: Track performance against your budgets
- **Predictive Analytics**: Linear regression for cost forecasting

### ⏰ **Smart Reminders**
- **Renewal Notifications**: Never miss a service renewal
- **Budget Alerts**: Get notified when approaching budget limits
- **Cost Spikes**: Immediate alerts for unusual spending patterns
- **Custom Schedules**: Set reminders for any service or billing cycle

### 🎨 **Modern UI/UX**
- **Dark/Light Themes**: Beautiful interface that adapts to your preference
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-Time Updates**: Live data updates without page refresh
- **Intuitive Dashboard**: Everything you need at a glance

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- **Node.js 18+** & **Python 3.12+** (for manual setup)
- **Redis** (included in Docker setup)
- **Nginx** (for production/subdomain setup)

### ⚡ 1-Minute Docker Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/burn-stop.git
cd burn-stop

# Start the application
docker-compose up --build

# Visit your application
open http://localhost:3000
```

**That's it!** 🎉 BurnStop is now running with:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🏠 Self-Hosting Guide

### 🌐 Production Deployment with Custom Domain

#### Step 1: Server Requirements

**Minimum Requirements:**
- **RAM**: 2GB (4GB recommended)
- **Storage**: 10GB (SSD recommended)
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Network**: Static IP with domain access

**Recommended VPS Providers:**
- **DigitalOcean**: $12/month droplet
- **Linode**: $12/month VPS
- **Vultr**: $12/month instance
- **Hetzner**: €9/month VPS

#### Step 2: Domain Setup

1. **Purchase a domain** (Namecheap, Cloudflare, etc.)
2. **Create DNS A record**:
   ```
   Type: A
   Name: burnstop (or your preferred subdomain)
   Value: YOUR_SERVER_IP
   TTL: 300
   ```

#### Step 3: Automated Server Setup

Our script handles everything automatically:

```bash
# Clone the repository
git clone https://github.com/yourusername/burn-stop.git
cd burn-stop

# Make setup script executable
chmod +x setup-nginx.sh

# Run the automated setup
./setup-nginx.sh
```

The script will:
- ✅ Install Nginx and Certbot
- ✅ Configure SSL certificates (Let's Encrypt)
- ✅ Setup reverse proxy for your domain
- ✅ Configure security headers and rate limiting
- ✅ Create systemd service for auto-startup
- ✅ Setup automatic SSL renewal

#### Step 4: Application Deployment

```bash
# Start BurnStop in production mode
docker-compose up -d

# Verify everything is running
docker-compose ps
```

### 🔧 Manual Production Setup

<details>
<summary><b>Click to expand manual setup instructions</b></summary>

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install -y nginx certbot python3-certbot-nginx
```

#### 2. Configure Nginx

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/burnstop.yourdomain.com
```

```nginx
server {
    listen 80;
    server_name burnstop.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Enable SSL

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/burnstop.yourdomain.com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d burnstop.yourdomain.com
```

#### 4. Production Environment

Create `.env` file:

```bash
# Backend Configuration
SECRET_KEY=your-super-secure-secret-key-here
ENVIRONMENT=production
REDIS_HOST=redis
REDIS_PORT=6379

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://burnstop.yourdomain.com/api
```

</details>

### 🔄 Updates & Maintenance

```bash
# Update to latest version
git pull origin main
docker-compose down
docker-compose up --build -d

# View logs
docker-compose logs -f

# Backup data
docker run --rm -v burn-stop_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .

# Restore data
docker run --rm -v burn-stop_redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /data
```

---

## 🐳 Docker Deployment

### 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │───▶│   Next.js       │───▶│   FastAPI       │
│   (Port 80/443) │    │   Frontend      │    │   Backend       │
└─────────────────┘    │   (Port 3000)   │    │   (Port 8000)   │
                       └─────────────────┘    └─────────┬───────┘
                                                        │
                                              ┌─────────▼───────┐
                                              │   Redis Cache   │
                                              │   (Port 6379)   │
                                              └─────────────────┘
```

### 📝 Docker Compose Services

| Service    | Purpose           | Port | Health Check |
|------------|-------------------|------|--------------|
| `frontend` | Next.js App       | 3000 | HTTP         |
| `backend`  | FastAPI Server    | 8000 | `/docs`      |
| `redis`    | Data Storage      | 6379 | Redis ping   |

### 🛠️ Development vs Production

#### Development Configuration
```yaml
# docker-compose.yml
volumes:
  - ./frontend:/app          # Hot reload
  - ./backend:/app           # Hot reload
command: npm run dev         # Development mode
```

#### Production Configuration
```yaml
# docker-compose.prod.yml
volumes:
  - redis_data:/data         # Persistent storage only
command: npm run start       # Production mode
```

### 🔍 Container Management

```bash
# View running services
docker-compose ps

# Scale services
docker-compose up --scale backend=2

# Service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in containers
docker-compose exec backend python -c "print('Hello from backend')"
docker-compose exec redis redis-cli ping

# Resource usage
docker stats
```

---

## 🔧 API Documentation

### 🌐 OpenAPI/Swagger

Visit `/docs` on your backend server for interactive API documentation:
- **Local**: http://localhost:8000/docs
- **Production**: https://your-domain.com/api/docs

### 🔑 Authentication

BurnStop uses **JWT tokens** for authentication:

```bash
# Login and get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token in subsequent requests
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/organizations/"
```

### 📊 Key Endpoints

#### Organizations
- `GET /organizations/` - List user organizations
- `POST /organizations/` - Create new organization
- `DELETE /organizations/{org_id}` - Delete organization

#### Services
- `GET /organizations/{org_id}/services` - List services
- `POST /organizations/{org_id}/services` - Add service
- `PUT /services/{service_id}` - Update service
- `DELETE /services/{service_id}` - Delete service

#### AI Insights
- `POST /organizations/api-key/openai` - Save OpenAI API key
- `POST /organizations/{org_id}/ai-insights` - Generate insights

#### Analytics
- `GET /organizations/{org_id}/reminders` - Upcoming reminders
- `GET /services/{service_id}/cost-history` - Historical cost data

---

## 🛡️ Security

### 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt with salt rounds
- **Rate Limiting**: Nginx-based request throttling
- **CORS Protection**: Properly configured cross-origin requests
- **Security Headers**: XSS, CSRF, and clickjacking protection
- **SSL/TLS**: Automatic Let's Encrypt certificates
- **Input Validation**: Pydantic models for data validation
- **SQL Injection Prevention**: Redis-based storage (NoSQL)

### 🔑 Environment Variables

```bash
# Backend Security
SECRET_KEY=your-super-secure-secret-key-here  # 32+ character random string
ENVIRONMENT=production                        # production/development

# Redis Configuration
REDIS_HOST=redis                             # Container name or IP
REDIS_PORT=6379                              # Redis port

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://your-domain.com/api
```

### 🚨 Security Checklist

- [ ] Change default `SECRET_KEY` to a secure random string
- [ ] Use HTTPS in production (automated with setup script)
- [ ] Configure firewall to only allow necessary ports (80, 443, 22)
- [ ] Regularly update Docker images and dependencies
- [ ] Monitor application logs for suspicious activity
- [ ] Backup Redis data regularly
- [ ] Use strong passwords for user accounts

---

## 🔧 Configuration

### ⚙️ Environment Variables

#### Backend Configuration
```bash
# Required
SECRET_KEY=your-secret-key-here
REDIS_HOST=redis
REDIS_PORT=6379

# Optional
ENVIRONMENT=production          # development/production
LOG_LEVEL=INFO                 # DEBUG/INFO/WARNING/ERROR
```

#### Frontend Configuration
```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional  
NEXT_PUBLIC_APP_NAME=BurnStop
NEXT_PUBLIC_THEME=system       # light/dark/system
```

### 🎨 Customization

#### Branding
Update frontend branding in `frontend/app/layout.tsx`:
```typescript
export const metadata = {
  title: 'Your Company - Cost Tracker',
  description: 'Your custom description'
}
```

#### Themes
BurnStop supports custom themes. Edit `frontend/app/globals.css`:
```css
:root {
  --primary: your-color;
  --secondary: your-secondary-color;
}
```

---

## 🚀 Development

### 🏃‍♂️ Local Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/burn-stop.git
cd burn-stop

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload

# Redis (new terminal)
redis-server
```

### 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test
npm run test:e2e

# Backend tests
cd backend
python -m pytest
python -m pytest --cov

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### 🔄 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📈 Roadmap

### 🎯 Upcoming Features

- [ ] **Multi-Cloud Integration**: Direct API integration with AWS, GCP, Azure
- [ ] **Team Collaboration**: Multi-user organizations with role-based access
- [ ] **Advanced Analytics**: More chart types and custom dashboards
- [ ] **Slack/Discord Integration**: Cost alerts in your team channels
- [ ] **Mobile App**: React Native app for iOS/Android
- [ ] **Kubernetes Support**: Helm charts for Kubernetes deployment
- [ ] **Plugin System**: Custom integrations and extensions
- [ ] **Advanced AI**: More sophisticated cost optimization algorithms

### 🔮 Long-term Vision

- **Enterprise Features**: SSO, audit logs, compliance reporting
- **Marketplace**: Community plugins and integrations
- **AI Recommendations**: Automated cost optimization actions
- **Real-time Monitoring**: Live cost tracking with WebSocket updates

---

## 🐛 Troubleshooting

### 💥 Common Issues

#### Port Conflicts
```bash
# Check what's using a port
sudo lsof -i :3000

# Change ports in docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

#### Redis Connection Issues
```bash
# Check Redis container
docker-compose logs redis

# Connect to Redis CLI
docker-compose exec redis redis-cli ping
```

#### SSL Certificate Problems
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew --dry-run
```

#### Memory Issues
```bash
# Check container resource usage
docker stats

# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M
```

### 📋 Debug Commands

```bash
# View all logs
docker-compose logs -f

# Check container health
docker-compose ps

# Restart specific service
docker-compose restart backend

# Complete reset
docker-compose down -v
docker-compose up --build
```

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Amazing Python web framework
- **Next.js** - Fantastic React framework
- **Redis** - Blazing fast data storage
- **Docker** - Making deployment easy
- **OpenAI** - Powering our AI insights
- **Nginx** - Reliable reverse proxy
- **Let's Encrypt** - Free SSL certificates

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 🆓 What does this mean?

- ✅ **Free to use** for personal and commercial projects
- ✅ **Modify and distribute** as you see fit
- ✅ **No warranty** - use at your own risk
- ✅ **Attribution appreciated** but not required

The MIT License is one of the most permissive open source licenses, giving you maximum freedom to use BurnStop however you want!

---

## 📞 Support

### 🆘 Need Help?

- **Documentation**: Check our comprehensive guides above
- **Issues**: [GitHub Issues](https://github.com/yourusername/burn-stop/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/burn-stop/discussions)
- **Email**: support@burnstop.dev

### 💬 Community

- **Discord**: [Join our Discord](https://discord.gg/burnstop)
- **Twitter**: [@BurnStopApp](https://twitter.com/BurnStopApp)
- **Blog**: [BurnStop Blog](https://blog.burnstop.dev)

---

<div align="center">

## 🔥 Made with ❤️ by [Vishrut Kumar](https://kumarthevishrut.github.io/Portfolio-Website/)

**[⭐ Star us on GitHub](https://github.com/yourusername/burn-stop)** • **[🐳 Docker Hub](https://hub.docker.com/r/burnstop/burnstop)** • **[📚 Documentation](https://docs.burnstop.dev)**

---

### 🏷️ **FOSS • Self-Hostable • Docker Ready • AI-Powered**

*Stop burning money on forgotten cloud services. Start saving today!* 💰

[![Deploy to DigitalOcean](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/yourusername/burn-stop/tree/main)

</div>


