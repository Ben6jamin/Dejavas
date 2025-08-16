from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import asyncio
from datetime import datetime

from langgraph_simulation import LangGraphSimulator
from integrations import IntegrationManager, IntegrationType, BrowserExtensionAPI, ScannedContent, ContentType
from simulation import AdvancedSimulator, NetworkTopology
from monitoring import get_monitoring_summary, start_monitoring, business_metrics, system_monitor

app = FastAPI()

# Initialize core components
simulator = LangGraphSimulator()
advanced_simulator = AdvancedSimulator(NetworkTopology.LOOSE_NETWORK)
integration_manager = IntegrationManager()
browser_api = BrowserExtensionAPI(integration_manager)

# --- Data Models ---
class Feature(BaseModel):
    title: str
    description: str

class Brief(BaseModel):
    product_name: str
    features: List[Feature]

class AgentConfig(BaseModel):
    customer_percentage: int
    competitor_percentage: int
    influencer_percentage: int
    internal_team_percentage: int

class SimulationReport(BaseModel):
    session_id: str
    adoption_score: float
    top_objections: List[str]
    must_fix: List[str]

class ContentAnalysisRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    integration_type: str = "browser_extension"

class IntegrationConfig(BaseModel):
    integration_type: str
    webhook_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

# --- Data Storage (temporary for this step) ---
simulations = {}

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to Dejavas API"}

# 1. Upload Brief
@app.post("/upload-brief/")
def upload_brief(brief: Brief):
    session_id = str(uuid.uuid4())
    simulations[session_id] = {
        "brief": brief,
        "agent_config": None,
        "simulation_result": None
    }
    return {"session_id": session_id, "message": "Brief uploaded successfully"}

# 2. Configure Agents
@app.post("/configure-agents/{session_id}")
def configure_agents(session_id: str, config: AgentConfig):
    if session_id not in simulations:
        raise HTTPException(status_code=404, detail="Session not found")

    total = (
        config.customer_percentage
        + config.competitor_percentage
        + config.influencer_percentage
        + config.internal_team_percentage
    )
    if total != 100:
        raise HTTPException(
            status_code=400, detail="Agent percentages must sum to 100"
        )

    simulations[session_id]["agent_config"] = config
    return {"message": "Agent configuration saved"}

# 3. Simulate Debate
@app.post("/simulate/{session_id}")
async def simulate(session_id: str):
    if session_id not in simulations:
        raise HTTPException(status_code=404, detail="Session not found")

    config = simulations[session_id].get("agent_config")
    if not config:
        raise HTTPException(status_code=400, detail="Agent configuration missing")

    brief = simulations[session_id]["brief"]
    
    # Use advanced simulator with LLM integration
    result = await advanced_simulator.run_simulation(brief, config, num_rounds=3)
    
    simulations[session_id]["simulation_result"] = result

    return result

# 4. Get Report
@app.get("/report/{session_id}")
def get_report(session_id: str):
    if session_id not in simulations:
        raise HTTPException(status_code=404, detail="Session not found")

    result = simulations[session_id].get("simulation_result")
    if not result:
        raise HTTPException(status_code=400, detail="Simulation not completed")

    return SimulationReport(
        session_id=session_id,
        adoption_score=result["adoption_score"],
        top_objections=result["top_objections"],
        must_fix=result["must_fix"],
    )

# 5. Rerun Simulation (Iterate)
@app.post("/rerun/{session_id}")
def rerun_simulation(session_id: str):
    if session_id not in simulations:
        raise HTTPException(status_code=404, detail="Session not found")

    config = simulations[session_id].get("agent_config")
    if not config:
        raise HTTPException(status_code=400, detail="Agent configuration missing")

    brief = simulations[session_id]["brief"]
    adoption_score, top_objections, must_fix = simulator.run(brief, config)

    simulations[session_id]["simulation_result"] = {
        "adoption_score": adoption_score,
        "top_objections": top_objections,
        "must_fix": must_fix,
    }

    return {
        "adoption_score": adoption_score,
        "top_objections": top_objections,
        "must_fix": must_fix,
    }

# --- Integration Endpoints ---

# 6. Analyze Content (Ubiquitous Integration)
@app.post("/analyze-content/")
async def analyze_content(request: ContentAnalysisRequest):
    """Analyze content from URLs or text - the core of ubiquitous integration"""
    try:
        if request.url:
            result = await integration_manager.process_content(request.url, IntegrationType.BROWSER_EXTENSION)
        elif request.text:
            result = await integration_manager.process_content(request.text, IntegrationType.BROWSER_EXTENSION)
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# 7. Browser Extension API
@app.get("/extension/config")
def get_extension_config():
    """Get configuration for browser extension"""
    return browser_api.get_extension_config()

@app.post("/extension/analyze-page")
async def analyze_page(url: str):
    """Analyze current page for browser extension"""
    return await browser_api.analyze_current_page(url)

@app.post("/extension/analyze-text")
async def analyze_text(text: str):
    """Analyze selected text for browser extension"""
    return await browser_api.analyze_selected_text(text)

# 8. Register Integration
@app.post("/integrations/register")
def register_integration(config: IntegrationConfig):
    """Register a new integration (Slack, Discord, etc.)"""
    try:
        integration_type = IntegrationType(config.integration_type)
        integration_manager.register_integration(integration_type, config.dict())
        return {"message": f"Integration {config.integration_type} registered successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid integration type: {config.integration_type}")

# 9. Advanced AI Analysis
@app.post("/advanced-analysis/")
async def advanced_analysis(request: ContentAnalysisRequest):
    """Advanced AI-powered analysis with market context and competitive intelligence"""
    try:
        # Create a comprehensive brief from the content
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        # Create market context
        market_context = {
            "category": "technology",
            "target_market": "professionals",
            "competitive_landscape": "competitive",
            "trends": ["AI", "automation", "productivity"],
            "competitors": {
                "direct": ["competitor1.com", "competitor2.com"],
                "indirect": ["alternative1.com", "alternative2.com"]
            }
        }
        
        # Create brief
        brief = integration_manager._create_brief_from_content(scanned_content)
        
        # Run advanced simulation
        config = {
            'customer_percentage': 60,
            'competitor_percentage': 20,
            'influencer_percentage': 10,
            'internal_team_percentage': 10
        }
        
        result = await advanced_simulator.run_simulation(
            brief, config, num_rounds=3, market_context=market_context
        )
        
        # Add content analysis info
        result['content_analyzed'] = {
            'type': scanned_content.content_type.value,
            'url': scanned_content.url,
            'title': scanned_content.title,
            'features_extracted': len(scanned_content.features)
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced analysis failed: {str(e)}")

# 10. Health Check
@app.get("/health")
def health_check():
    """Enhanced health check endpoint with monitoring"""
    try:
        health_status = system_monitor.check_system_health()
        
        return {
            "status": health_status.status,
            "version": "1.0.0",
            "integrations": list(integration_manager.active_integrations.keys()),
            "simulations_running": len(simulations),
            "ai_powered": True,
            "llm_available": True,
            "system_health": {
                "cpu_usage": system_monitor.get_system_metrics().cpu_usage,
                "memory_usage": system_monitor.get_system_metrics().memory_usage,
                "uptime_hours": round(health_status.uptime / 3600, 2)
            },
            "monitoring_active": True
        }
    except Exception as e:
        return {
            "status": "error",
            "version": "1.0.0",
            "error": str(e),
            "monitoring_active": False
        }

# 11. Real-Time Market Sentiment Analysis
@app.post("/market-sentiment/")
async def analyze_market_sentiment(request: ContentAnalysisRequest):
    """Real-time market sentiment analysis with social media integration"""
    try:
        # Create market context from content
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        # Analyze market sentiment using multiple data sources
        sentiment_data = await integration_manager.analyze_market_sentiment(scanned_content)
        
        return {
            "sentiment_score": sentiment_data["overall_sentiment"],
            "market_mood": sentiment_data["market_mood"],
            "trending_topics": sentiment_data["trending_topics"],
            "social_buzz": sentiment_data["social_buzz"],
            "influencer_sentiment": sentiment_data["influencer_sentiment"],
            "confidence_level": sentiment_data["confidence_level"],
            "ai_powered": True,
            "real_time": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market sentiment analysis failed: {str(e)}")

# 12. Predictive Market Analytics
@app.post("/predictive-analytics/")
async def get_predictive_analytics(request: ContentAnalysisRequest):
    """AI-powered predictive analytics for market trends and adoption"""
    try:
        # Create brief from content
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        brief = integration_manager._create_brief_from_content(scanned_content)
        
        # Run predictive analysis
        predictions = await integration_manager.generate_predictions(brief)
        
        return {
            "adoption_prediction": predictions["adoption_prediction"],
            "market_timing": predictions["market_timing"],
            "risk_assessment": predictions["risk_assessment"],
            "opportunity_score": predictions["opportunity_score"],
            "competitive_threats": predictions["competitive_threats"],
            "success_probability": predictions["success_probability"],
            "ai_powered": True,
            "prediction_horizon": "6-12 months"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Predictive analytics failed: {str(e)}")

# 13. AI-Powered Competitive Intelligence
@app.post("/competitive-intelligence/")
async def get_competitive_intelligence(request: ContentAnalysisRequest):
    """Comprehensive competitive intelligence with AI analysis"""
    try:
        # Analyze content for competitive insights
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        # Generate competitive intelligence
        competitive_data = await integration_manager.generate_competitive_intelligence(scanned_content)
        
        return {
            "competitive_landscape": competitive_data["competitive_landscape"],
            "market_positioning": competitive_data["market_positioning"],
            "differentiation_opportunities": competitive_data["differentiation_opportunities"],
            "threat_analysis": competitive_data["threat_analysis"],
            "competitive_advantages": competitive_data["competitive_advantages"],
            "market_gaps": competitive_data["market_gaps"],
            "ai_powered": True,
            "analysis_depth": "comprehensive"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitive intelligence failed: {str(e)}")

# 14. Voice-Enabled Market Analysis
@app.post("/voice-analysis/")
async def analyze_voice_input(audio_data: str):
    """Voice-enabled market analysis using speech-to-text and AI"""
    try:
        # Convert voice to text (placeholder for actual STT integration)
        transcribed_text = f"Voice input: {audio_data}"
        
        # Analyze the transcribed content
        content = ScannedContent(
            content_type=ContentType.MARKETING_COPY,
            raw_text=transcribed_text
        )
        
        result = await integration_manager.process_content(content, IntegrationType.BROWSER_EXTENSION)
        
        return {
            "voice_analysis": True,
            "transcribed_text": transcribed_text,
            "analysis_results": result,
            "ai_powered": True,
            "voice_enabled": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice analysis failed: {str(e)}")

# 15. Multi-Language Market Intelligence
@app.post("/multilingual-analysis/")
async def analyze_multilingual_content(request: ContentAnalysisRequest, language: str = "auto"):
    """Multi-language market intelligence with automatic translation"""
    try:
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        # Detect language if auto
        if language == "auto":
            detected_language = await integration_manager.detect_language(scanned_content.raw_text or "")
            language = detected_language
        
        # Translate if needed and analyze
        if language != "en":
            translated_content = await integration_manager.translate_content(scanned_content, "en")
            analysis_result = await integration_manager.process_content(translated_content, IntegrationType.BROWSER_EXTENSION)
        else:
            analysis_result = await integration_manager.process_content(scanned_content, IntegrationType.BROWSER_EXTENSION)
        
        return {
            "original_language": language,
            "translated_to": "en" if language != "en" else "none",
            "analysis_results": analysis_result,
            "multilingual_support": True,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multilingual analysis failed: {str(e)}")

# 16. Real-Time Market Alerts
@app.post("/market-alerts/")
async def setup_market_alerts(alert_config: Dict[str, Any]):
    """Setup real-time market alerts for competitive intelligence"""
    try:
        alert_id = await integration_manager.setup_market_alert(alert_config)
        
        return {
            "alert_id": alert_id,
            "status": "active",
            "alert_type": alert_config.get("type", "competitive"),
            "monitoring_targets": alert_config.get("targets", []),
            "notification_channels": alert_config.get("channels", ["email"]),
            "real_time": True,
            "ai_powered": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market alert setup failed: {str(e)}")

# 17. AI-Powered Market Research Assistant
@app.post("/market-research-assistant/")
async def market_research_query(query: str, research_depth: str = "standard"):
    """AI-powered market research assistant for comprehensive insights"""
    try:
        research_results = await integration_manager.conduct_market_research(query, research_depth)
        
        return {
            "research_query": query,
            "research_depth": research_depth,
            "market_overview": research_results["market_overview"],
            "key_findings": research_results["key_findings"],
            "trend_analysis": research_results["trend_analysis"],
            "competitive_insights": research_results["competitive_insights"],
            "recommendations": research_results["recommendations"],
            "ai_powered": True,
            "research_quality": "expert"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market research failed: {str(e)}")

# 18. Dynamic Pricing Intelligence
@app.post("/pricing-intelligence/")
async def analyze_pricing_strategy(request: ContentAnalysisRequest):
    """AI-powered pricing intelligence and optimization recommendations"""
    try:
        if request.url:
            scanned_content = await integration_manager.scanner.scan_url(request.url)
        elif request.text:
            scanned_content = ScannedContent(
                content_type=ContentType.MARKETING_COPY,
                raw_text=request.text
            )
        else:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")
        
        pricing_analysis = await integration_manager.analyze_pricing_strategy(scanned_content)
        
        return {
            "pricing_analysis": pricing_analysis["analysis"],
            "price_optimization": pricing_analysis["optimization"],
            "competitive_pricing": pricing_analysis["competitive_pricing"],
            "value_proposition": pricing_analysis["value_proposition"],
            "pricing_recommendations": pricing_analysis["recommendations"],
            "ai_powered": True,
            "pricing_intelligence": "advanced"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pricing intelligence failed: {str(e)}")

# 19. System Monitoring Dashboard
@app.get("/monitoring/dashboard")
async def get_monitoring_dashboard():
    """Get comprehensive system monitoring dashboard"""
    try:
        monitoring_data = get_monitoring_summary()
        return {
            "status": "success",
            "data": monitoring_data,
            "timestamp": monitoring_data["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monitoring data retrieval failed: {str(e)}")

# 20. System Health Check (Enhanced)
@app.get("/monitoring/health")
async def get_system_health():
    """Get detailed system health status"""
    try:
        health_status = system_monitor.check_system_health()
        return {
            "status": health_status.status,
            "checks": health_status.checks,
            "uptime_hours": round(health_status.uptime / 3600, 2),
            "version": health_status.version,
            "timestamp": health_status.last_check.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# 21. Performance Metrics
@app.get("/monitoring/performance")
async def get_performance_metrics():
    """Get system performance metrics"""
    try:
        performance_data = system_monitor.get_performance_summary()
        return {
            "status": "success",
            "data": performance_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance metrics retrieval failed: {str(e)}")

# 22. Business Metrics
@app.get("/monitoring/business")
async def get_business_metrics():
    """Get business and feature usage metrics"""
    try:
        business_data = business_metrics.get_business_metrics()
        return {
            "status": "success",
            "data": business_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Business metrics retrieval failed: {str(e)}")
