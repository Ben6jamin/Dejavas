"""
Dejavas Hybrid Simulation System

This module implements a hybrid approach combining:
1. Direct LLM for fast content analysis
2. LangGraph for complex multi-agent interactions
3. Intelligent routing between the two approaches
"""

import asyncio
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass

from .llm_integration import llm_integration, FeatureAnalysis
from .agents import Agent, AgentFactory
from .simulation import AdvancedSimulator

class SimulationMode(Enum):
    """Different simulation modes based on complexity"""
    QUICK_ANALYSIS = "quick_analysis"      # Direct LLM - fast, simple
    STANDARD_SIMULATION = "standard"       # Current approach - balanced
    COMPLEX_WAR_ROOM = "war_room"          # LangGraph - complex interactions
    COMPETITIVE_ANALYSIS = "competitive"   # Specialized competitive analysis

@dataclass
class SimulationRequest:
    """Request for simulation with mode selection"""
    content: Dict[str, Any]  # URL, text, or features
    mode: SimulationMode
    agent_config: Dict[str, int]
    market_context: Optional[Dict[str, Any]] = None
    complexity_threshold: float = 0.7  # When to use LangGraph

class HybridSimulator:
    """Hybrid simulation system that routes to appropriate backend"""
    
    def __init__(self):
        self.direct_simulator = AdvancedSimulator()
        self.langgraph_simulator = None  # Will be initialized when needed
        self.mode_router = SimulationModeRouter()
    
    async def simulate(self, request: SimulationRequest) -> Dict[str, Any]:
        """Route simulation to appropriate backend based on complexity"""
        
        # Determine the best approach
        recommended_mode = self.mode_router.recommend_mode(
            request.content, 
            request.mode, 
            request.complexity_threshold
        )
        
        print(f"🎯 Routing to: {recommended_mode.value}")
        
        if recommended_mode == SimulationMode.QUICK_ANALYSIS:
            return await self._quick_analysis(request)
        elif recommended_mode == SimulationMode.COMPLEX_WAR_ROOM:
            return await self._langgraph_simulation(request)
        else:
            return await self._standard_simulation(request)
    
    async def _quick_analysis(self, request: SimulationRequest) -> Dict[str, Any]:
        """Fast analysis using direct LLM - perfect for content analysis"""
        
        print("⚡ Using Quick Analysis (Direct LLM)")
        
        # Create a single comprehensive agent analysis
        agent = AgentFactory.create_customer_agent()
        
        if 'url' in request.content:
            # Analyze URL content
            from .integrations import ContentScanner
            scanner = ContentScanner()
            scanned_content = await scanner.scan_url(request.content['url'])
            features = [{'title': scanned_content.title or 'Content', 'description': scanned_content.raw_text[:500]}]
        elif 'text' in request.content:
            features = [{'title': 'Content Analysis', 'description': request.content['text']}]
        else:
            features = request.content.get('features', [])
        
        # Get comprehensive analysis from a single agent
        analysis = await agent.process_feature(features[0], request.market_context or {})
        
        # Generate market insights
        market_insights = await llm_integration.generate_market_insights(
            features, [analysis], request.market_context or {}
        )
        
        return {
            'mode': 'quick_analysis',
            'adoption_score': market_insights['adoption_score'],
            'top_objections': market_insights['top_objections'][:3],
            'must_fix': market_insights['top_suggestions'][:3],
            'analysis_time': 'fast',
            'cost': 'low',
            'insights': market_insights['market_insights'],
            'agent_analysis': analysis
        }
    
    async def _standard_simulation(self, request: SimulationRequest) -> Dict[str, Any]:
        """Standard simulation using current approach"""
        
        print("🔄 Using Standard Simulation (Current Approach)")
        
        # Use the current advanced simulator
        result = await self.direct_simulator.run_simulation(
            request.content, 
            request.agent_config, 
            num_rounds=3, 
            market_context=request.market_context
        )
        
        result['mode'] = 'standard_simulation'
        result['analysis_time'] = 'medium'
        result['cost'] = 'medium'
        
        return result
    
    async def _langgraph_simulation(self, request: SimulationRequest) -> Dict[str, Any]:
        """Complex simulation using LangGraph for true multi-agent interactions"""
        
        print("🧠 Using LangGraph War Room Simulation")
        
        # Initialize LangGraph simulator if not already done
        if self.langgraph_simulator is None:
            self.langgraph_simulator = await self._initialize_langgraph()
        
        # Run complex multi-agent simulation
        result = await self.langgraph_simulator.run_complex_simulation(
            request.content,
            request.agent_config,
            request.market_context
        )
        
        result['mode'] = 'langgraph_war_room'
        result['analysis_time'] = 'slow'
        result['cost'] = 'high'
        result['complexity'] = 'high'
        
        return result
    
    async def _initialize_langgraph(self):
        """Initialize LangGraph simulator when needed"""
        try:
            from .langgraph_simulation import LangGraphSimulator
            return LangGraphSimulator()
        except ImportError:
            print("⚠️ LangGraph not available, falling back to standard simulation")
            return None

class SimulationModeRouter:
    """Intelligent router that determines the best simulation mode"""
    
    def recommend_mode(self, content: Dict[str, Any], requested_mode: SimulationMode, complexity_threshold: float) -> SimulationMode:
        """Recommend the best simulation mode based on content and requirements"""
        
        # If user specifically requests a mode, respect it
        if requested_mode != SimulationMode.STANDARD_SIMULATION:
            return requested_mode
        
        # Analyze content complexity
        complexity_score = self._calculate_complexity(content)
        
        # Route based on complexity
        if complexity_score < 0.3:
            return SimulationMode.QUICK_ANALYSIS
        elif complexity_score > complexity_threshold:
            return SimulationMode.COMPLEX_WAR_ROOM
        else:
            return SimulationMode.STANDARD_SIMULATION
    
    def _calculate_complexity(self, content: Dict[str, Any]) -> float:
        """Calculate complexity score of the content"""
        complexity = 0.0
        
        # Check content type
        if 'url' in content:
            complexity += 0.2  # URL analysis is moderate complexity
        if 'text' in content and len(content['text']) > 1000:
            complexity += 0.3  # Long text is more complex
        if 'features' in content and len(content['features']) > 3:
            complexity += 0.4  # Multiple features increase complexity
        
        # Check for competitive analysis indicators
        if any(word in str(content).lower() for word in ['competitor', 'rival', 'market', 'positioning']):
            complexity += 0.3
        
        # Check for multi-stakeholder analysis
        if any(word in str(content).lower() for word in ['customer', 'influencer', 'internal', 'team']):
            complexity += 0.2
        
        return min(1.0, complexity)

class SimulationComparison:
    """Compare results from different simulation modes"""
    
    @staticmethod
    async def compare_modes(content: Dict[str, Any], agent_config: Dict[str, int]) -> Dict[str, Any]:
        """Run the same content through different modes and compare results"""
        
        simulator = HybridSimulator()
        
        # Test all modes
        modes = [
            SimulationMode.QUICK_ANALYSIS,
            SimulationMode.STANDARD_SIMULATION,
            SimulationMode.COMPLEX_WAR_ROOM
        ]
        
        results = {}
        
        for mode in modes:
            try:
                request = SimulationRequest(
                    content=content,
                    mode=mode,
                    agent_config=agent_config
                )
                
                result = await simulator.simulate(request)
                results[mode.value] = {
                    'adoption_score': result.get('adoption_score', 0),
                    'analysis_time': result.get('analysis_time', 'unknown'),
                    'cost': result.get('cost', 'unknown'),
                    'insights_count': len(result.get('top_objections', [])) + len(result.get('must_fix', []))
                }
                
            except Exception as e:
                results[mode.value] = {'error': str(e)}
        
        return {
            'comparison': results,
            'recommendation': SimulationComparison._get_recommendation(results)
        }
    
    @staticmethod
    def _get_recommendation(results: Dict[str, Any]) -> str:
        """Get recommendation based on comparison results"""
        
        if 'quick_analysis' in results and 'standard_simulation' in results:
            quick_score = results['quick_analysis'].get('adoption_score', 0)
            standard_score = results['standard_simulation'].get('adoption_score', 0)
            
            if abs(quick_score - standard_score) < 10:
                return "Use Quick Analysis for speed and cost efficiency"
            else:
                return "Use Standard Simulation for more accurate results"
        
        return "Use Standard Simulation for balanced approach"

# Global hybrid simulator instance
hybrid_simulator = HybridSimulator()
