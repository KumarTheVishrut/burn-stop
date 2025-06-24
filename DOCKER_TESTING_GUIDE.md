# 🔥❌ BurnStop - Docker Testing Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Clone and Start the Application

```bash
# Clone the repository
git clone <your-repo-url>
cd burn-stop

# Start all services
docker-compose up --build
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Redis**: localhost:6379

## 🧪 Testing Workflow

### Step 1: Account Setup
1. Navigate to http://localhost:3000
2. Click "Sign Up" to create a new account
3. Use any email/password (e.g., `test@example.com` / `password123`)

### Step 2: Create Organization
1. After login, you'll see the dashboard
2. Click "Create Your First Organization" 
3. Set name: `"My Startup"` and budget: `$12500`

### Step 3: Add Services (Test the features!)
Add these services to test all functionality:

**Service 1: ML Training Pipeline**
```
Name: ML training pipeline
Platform: GCP
Type: Vertex AI
Cost: $2000
Reminder: Set to tomorrow's date
Region: mumbai-1
Instance: g-873427403
Owner: vishrut@foo.co
Description: training ml for reco engine
```

**Service 2: Cursor Subscription**
```
Name: Cursor
Platform: Other
Type: Subscription
Cost: $20
Reminder: Set to next week
API Quota: 500 tokens
API Usage: 100 tokens
Description: used in organization
```

**Service 3: Storage Bucket**
```
Name: Storage bucket for image training pipeline
Platform: AWS
Type: S3
Cost: $140
Reminder: Set to next month
Region: ap-south-1
Instance: i-12345678
Owner: vishrut@foo.co
Description: storing images
```

### Step 4: Test Key Features

#### 🤖 AI Insights (OpenAI Integration)
1. Go to Dashboard
2. Configure OpenAI API Key in the "🤖 AI Insights" section
3. Use your OpenAI API key (get one from https://platform.openai.com/api-keys)
4. Return to your organization page
5. Click "🤖 Get AI Insights" button
6. Should generate beautiful cost optimization analysis!

#### 📊 Analytics Dashboard
- Check the "📊 Cost Analytics" section
- Verify the cost trend chart shows realistic progression
- Check platform distribution pie chart

#### ⏰ Reminders
- Set reminder dates within the next 30 days
- Check the "⏰ Upcoming Reminders" section

#### 💰 Budget Tracking
- Services should show budget percentage usage
- High-cost services (>10% of budget) get warning badges
- Very high-cost services (>20% of budget) get critical badges

## 🛠️ Development Mode

### Hot Reloading
Both frontend and backend support hot reloading:
- Backend changes auto-reload via `uvicorn --reload`
- Frontend changes auto-reload via `npm run dev`

### Logs
View logs for specific services:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Database Access
Connect to Redis for debugging:
```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# View all keys
KEYS *

# View specific data
GET "user:some-user-id"
ZRANGE "reminders:some-org-id" 0 -1 WITHSCORES
```

## 🐛 Troubleshooting

### Common Issues

**Frontend can't connect to backend:**
```bash
# Check if backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend
```

**Redis connection issues:**
```bash
# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

**OpenAI API Issues:**
- Verify API key is valid
- Check API key has sufficient credits
- Look for error messages in backend logs

### Clean Reset
```bash
# Stop and remove all containers, volumes
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build
```

## 🌟 Key Features to Test

### ✅ Authentication & Authorization
- [x] User signup/login
- [x] JWT token management
- [x] Organization-based access control

### ✅ Organization Management
- [x] Create/delete organizations
- [x] Add/remove team members
- [x] Budget setting and tracking

### ✅ Service Management
- [x] Add services across platforms (AWS, GCP, Azure, Other)
- [x] Cost tracking and budget percentage calculations
- [x] Service status indicators (warning/critical cost levels)

### ✅ AI-Powered Insights
- [x] OpenAI API integration
- [x] Cost optimization recommendations
- [x] Security and performance analysis
- [x] Beautiful markdown formatting

### ✅ Analytics & Predictions
- [x] Cost trend visualization
- [x] Platform cost distribution
- [x] Linear regression predictions
- [x] Realistic historical data generation

### ✅ Reminder System
- [x] Service renewal reminders
- [x] 30-day upcoming reminder window
- [x] Timestamp-based Redis sorted sets

### ✅ Modern UI/UX
- [x] Dark/light theme toggle
- [x] Responsive design
- [x] Professional color schemes
- [x] Loading states and error handling

## 🚢 Production Deployment

For production deployment, update the docker-compose.yml:

```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
  - SECRET_KEY=your-super-secure-secret-key-here
  - ENVIRONMENT=production
  - NEXT_PUBLIC_API_URL=https://your-domain.com
```

## 📝 API Documentation

Visit http://localhost:8000/docs for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

---

## 🔥 Made with ❤️ by [Vishrut Kumar](https://kumarthevishrut.github.io/Portfolio-Website/)

**FOSS • Self-Hostable • Docker Ready** 🐳 