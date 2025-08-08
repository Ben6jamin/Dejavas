from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import asyncio

from langgraph_simulation import LangGraphSimulator
from integrations import IntegrationManager, IntegrationType, BrowserExtensionAPI, ScannedContent, ContentType
from simulation import AdvancedSimulator, NetworkTopology

app = FastAPI(title="Dejavas API", description="AI-Powered Marketing Intelligence Arena", version="1.0.0")

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
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "integrations": list(integration_manager.active_integrations.keys()),
        "simulations_running": len(simulations),
        "ai_powered": True,
        "llm_available": True
    }
