# Dejavas Backend - AI-Powered Marketing Intelligence Arena

Dejavas is a virtual "war-room" run by autonomous AI agents that simulate real market dynamics. This backend provides the core simulation engine and ubiquitous integration capabilities.

## 🚀 Features

### Core Simulation Engine
- **Deep Persona DNA**: Each agent has a unique "genome" with demographics, psychographics, and behavioral patterns
- **Influence Graph Mode**: Multiple network topologies (echo-chamber, loose network, real follower graph)
- **Attention Tokens**: Agents spend limited attention tokens on features, modeling real user behavior
- **Evolving Rounds**: Multi-stage simulations where agents remember and influence each other
- **Arena Health Metrics**: Real-time calculation of polarization, advocate ratios, and engagement density

### Ubiquitous Integration
- **Browser Extension API**: Real-time analysis of web pages and selected text
- **Content Scanner**: Automatic extraction of features, pricing, and competitive advantages
- **Multi-Platform Support**: Slack, Discord, Shopify, WordPress integrations
- **Grammarly-like Experience**: Seamless integration into existing workflows

## 🏗️ Architecture

```
dejavas-backend/
├── agents/                 # Deep Persona DNA system
│   ├── __init__.py        # Agent genomes and factory
│   └── behaviors.py       # Agent behavior patterns
├── simulation/            # Advanced simulation engine
│   ├── __init__.py        # Influence graphs and metrics
│   └── rounds.py          # Evolving round logic
├── integrations/          # Ubiquitous integration system
│   ├── __init__.py        # Content scanner and APIs
│   └── extensions/        # Browser extension backend
├── main.py               # FastAPI application
├── langgraph_simulation.py # LangGraph integration
└── requirements.txt      # Dependencies
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Server
```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. Test the API
```bash
# Health check
curl http://localhost:8000/health

# Analyze content
curl -X POST "http://localhost:8000/analyze-content/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/product"}'
```

## 📚 API Endpoints

### Core Simulation
- `POST /upload-brief/` - Upload product brief
- `POST /configure-agents/{session_id}` - Configure agent mix
- `POST /simulate/{session_id}` - Run simulation
- `GET /report/{session_id}` - Get simulation report
- `POST /rerun/{session_id}` - Rerun simulation

### Ubiquitous Integration
- `POST /analyze-content/` - Analyze URLs or text
- `GET /extension/config` - Browser extension configuration
- `POST /extension/analyze-page` - Analyze current page
- `POST /extension/analyze-text` - Analyze selected text
- `POST /integrations/register` - Register new integration

### Health & Monitoring
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## 🧠 Agent System

### Agent Types
1. **Customer Agents**: Real buyers with diverse demographics and psychographics
2. **Competitor Agents**: Strategic rivals that attack and defend
3. **Influencer Agents**: Social media personalities that hype or roast
4. **Internal Team Agents**: PM, Sales, CX with department biases

### Deep Persona DNA
Each agent has a unique genome:
```json
{
  "agent_type": "customer",
  "demographics": {
    "age": 28,
    "income_level": "middle",
    "location": "urban",
    "education": "college"
  },
  "psychographics": {
    "tech_savviness": 0.8,
    "price_sensitivity": 0.6,
    "brand_loyalty": 0.4
  },
  "personality_traits": ["early_adopter", "enthusiast"],
  "influence_score": 0.7,
  "attention_tokens": 100
}
```

## 🌐 Integration Examples

### Browser Extension
```javascript
// Analyze current page
const response = await fetch('/extension/analyze-page', {
  method: 'POST',
  body: JSON.stringify({ url: window.location.href })
});

// Get real-time insights
const insights = await response.json();
console.log(`Adoption Score: ${insights.adoption_score}%`);
```

### Slack Bot
```python
# Register Slack integration
await client.post("/integrations/register", json={
    "integration_type": "slack_bot",
    "webhook_url": "https://hooks.slack.com/...",
    "settings": {"channel": "#marketing"}
})
```

### Content Analysis
```python
# Analyze any URL or text
result = await client.post("/analyze-content/", json={
    "url": "https://amazon.com/product/123",
    "integration_type": "browser_extension"
})

print(f"Adoption Score: {result['adoption_score']}%")
print(f"Must Fix: {result['must_fix']}")
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
DEJAVAS_API_KEY=your_api_key
DEJAVAS_ENVIRONMENT=production

# LLM Configuration
OPENAI_API_KEY=your_openai_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Database
DATABASE_URL=postgresql://user:pass@localhost/dejavas
REDIS_URL=redis://localhost:6379

# Monitoring
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
```

### Agent Configuration
```python
# Custom agent mix
config = {
    "customer_percentage": 60,      # 60% customers
    "competitor_percentage": 20,    # 20% competitors
    "influencer_percentage": 10,    # 10% influencers
    "internal_team_percentage": 10  # 10% internal team
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_simulation_endpoints.py

# Run integration tests
pytest tests/integration/
```

## 📊 Monitoring

### Health Metrics
- **Adoption Score**: Overall feature adoption probability
- **Polarization Score**: How divided the market is (0-1)
- **Advocate-to-Saboteur Ratio**: Ratio of supporters to detractors
- **Viral Path Length**: Information spread efficiency
- **Engagement Density**: How actively agents interact

### Performance Metrics
- **Simulation Speed**: Rounds per second
- **Agent Memory Usage**: Memory consumption per agent
- **API Response Time**: Endpoint response times
- **Integration Success Rate**: Successful content analyses

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dejavas-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dejavas-backend
  template:
    metadata:
      labels:
        app: dejavas-backend
    spec:
      containers:
      - name: dejavas
        image: dejavas/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: dejavas-secrets
              key: database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.dejavas.ai](https://docs.dejavas.ai)
- **API Reference**: [api.dejavas.ai](https://api.dejavas.ai/docs)
- **Community**: [community.dejavas.ai](https://community.dejavas.ai)
- **Email**: support@dejavas.ai

---

**Dejavas** - Where AI agents battle for market truth 🚀
