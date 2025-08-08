from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

from langgraph_simulation import LangGraphSimulator

app = FastAPI()
simulator = LangGraphSimulator()

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
def simulate(session_id: str):
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
