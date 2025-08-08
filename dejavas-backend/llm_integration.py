"""
Dejavas LLM Integration - Real AI Intelligence for Agents

This module provides the core LLM integration that powers the AI agents
with real intelligence, enabling sophisticated market analysis and
behavioral simulation.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from openai import AsyncOpenAI
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.prompts import ChatPromptTemplate
    from langchain.output_parsers import PydanticOutputParser
    from pydantic import BaseModel, Field
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM dependencies not installed. Using mock responses.")

class AgentRole(Enum):
    CUSTOMER = "customer"
    COMPETITOR = "competitor"
    INFLUENCER = "influencer"
    INTERNAL_TEAM = "internal_team"

@dataclass
class AgentContext:
    """Context information for an AI agent"""
    role: AgentRole
    genome: Dict[str, Any]
    current_opinion: float
    memory: List[str]
    relationships: Dict[str, float]
    attention_tokens: int

@dataclass
class FeatureAnalysis:
    """Analysis of a product feature by an AI agent"""
    feature_title: str
    opinion_shift: float
    reasoning: str
    objections: List[str]
    suggestions: List[str]
    influence_impact: float
    attention_spent: int

class AgentResponse(BaseModel):
    """Structured response from an AI agent"""
    opinion_shift: float = Field(description="How much this feature changes the agent's opinion (-1 to 1)")
    reasoning: str = Field(description="Detailed reasoning for the opinion change")
    objections: List[str] = Field(description="Specific objections or concerns")
    suggestions: List[str] = Field(description="Suggestions for improvement")
    attention_spent: int = Field(description="Number of attention tokens spent (1-50)")
    influence_impact: float = Field(description="How much this agent can influence others (0-1)")

class LLMIntegration:
    """Core LLM integration for Dejavas agents"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm_available = LLM_AVAILABLE and self.api_key
        
        if self.llm_available:
            self.client = AsyncOpenAI(api_key=self.api_key)
            self.chat_model = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7,
                max_tokens=1000
            )
        else:
            self.client = None
            self.chat_model = None
    
    async def analyze_feature_as_agent(self, 
                                     feature: Dict[str, Any], 
                                     context: AgentContext,
                                     market_context: Dict[str, Any]) -> FeatureAnalysis:
        """Analyze a feature from the perspective of a specific agent"""
        
        if not self.llm_available:
            return self._mock_analysis(feature, context)
        
        # Create the agent prompt
        prompt = self._create_agent_prompt(feature, context, market_context)
        
        try:
            # Get structured response
            response = await self._get_structured_response(prompt, context.role)
            
            # Create feature analysis
            analysis = FeatureAnalysis(
                feature_title=feature.get('title', 'Unknown Feature'),
                opinion_shift=response.opinion_shift,
                reasoning=response.reasoning,
                objections=response.objections,
                suggestions=response.suggestions,
                influence_impact=response.influence_impact,
                attention_spent=response.attention_spent
            )
            
            return analysis
            
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return self._mock_analysis(feature, context)
    
    def _create_agent_prompt(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> str:
        """Create a detailed prompt for the agent"""
        
        role_descriptions = {
            AgentRole.CUSTOMER: "You are a real customer with specific needs, preferences, and pain points.",
            AgentRole.COMPETITOR: "You are a strategic competitor analyzing this feature for competitive threats and opportunities.",
            AgentRole.INFLUENCER: "You are a social media influencer who shapes public opinion about products and features.",
            AgentRole.INTERNAL_TEAM: "You are an internal team member with specific department concerns and company goals."
        }
        
        prompt = f"""
You are an AI agent in the Dejavas marketing intelligence simulation. 

{role_descriptions[context.role]}

## Your Profile (Genome):
- Demographics: {json.dumps(context.genome.get('demographics', {}), indent=2)}
- Psychographics: {json.dumps(context.genome.get('psychographics', {}), indent=2)}
- Personality Traits: {context.genome.get('personality_traits', [])}
- Current Opinion: {context.current_opinion:.2f} (0 = very negative, 1 = very positive)
- Influence Score: {context.genome.get('influence_score', 0.5):.2f}
- Attention Tokens Remaining: {context.attention_tokens}

## Market Context:
- Product Category: {market_context.get('category', 'Unknown')}
- Target Market: {market_context.get('target_market', 'General')}
- Competitive Landscape: {market_context.get('competitive_landscape', 'Unknown')}
- Current Trends: {market_context.get('trends', [])}

## Feature to Analyze:
Title: {feature.get('title', 'Unknown')}
Description: {feature.get('description', 'No description provided')}

## Your Task:
Analyze this feature from your perspective and provide a structured response including:
1. How much this feature changes your opinion (opinion_shift)
2. Detailed reasoning for your reaction
3. Specific objections or concerns
4. Suggestions for improvement
5. How much attention you'll spend on this feature
6. Your potential influence on others

Think like a real person in your role would think. Be specific, honest, and provide actionable insights.
"""
        return prompt
    
    async def _get_structured_response(self, prompt: str, role: AgentRole) -> AgentResponse:
        """Get a structured response from the LLM"""
        
        # Create the parser
        parser = PydanticOutputParser(pydantic_object=AgentResponse)
        
        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert market analyst. Provide structured, actionable insights."),
            ("human", "{prompt}\n\n{format_instructions}")
        ])
        
        # Format the prompt
        formatted_prompt = prompt_template.format_messages(
            prompt=prompt,
            format_instructions=parser.get_format_instructions()
        )
        
        # Get response
        response = await self.chat_model.ainvoke(formatted_prompt)
        
        # Parse the response
        return parser.parse(response.content)
    
    def _mock_analysis(self, feature: Dict[str, Any], context: AgentContext) -> FeatureAnalysis:
        """Provide mock analysis when LLM is not available"""
        import random
        
        # Simple heuristics based on agent type
        base_shift = 0.0
        
        if context.role == AgentRole.CUSTOMER:
            if 'user' in feature.get('description', '').lower():
                base_shift = 0.1
            elif 'price' in feature.get('description', '').lower():
                base_shift = -0.05
        elif context.role == AgentRole.COMPETITOR:
            if 'innovative' in feature.get('description', '').lower():
                base_shift = -0.15
            else:
                base_shift = 0.05
        elif context.role == AgentRole.INFLUENCER:
            if 'trendy' in feature.get('description', '').lower():
                base_shift = 0.2
            else:
                base_shift = 0.05
        
        return FeatureAnalysis(
            feature_title=feature.get('title', 'Unknown'),
            opinion_shift=base_shift + random.uniform(-0.1, 0.1),
            reasoning=f"Mock analysis for {context.role.value} agent",
            objections=["Mock objection 1", "Mock objection 2"],
            suggestions=["Mock suggestion 1", "Mock suggestion 2"],
            influence_impact=context.genome.get('influence_score', 0.5),
            attention_spent=random.randint(5, 20)
        )
    
    async def generate_market_insights(self, 
                                     features: List[Dict[str, Any]], 
                                     agent_analyses: List[FeatureAnalysis],
                                     market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level market insights from agent analyses"""
        
        if not self.llm_available:
            return self._mock_market_insights(features, agent_analyses)
        
        # Aggregate agent responses
        total_opinion_shift = sum(analysis.opinion_shift for analysis in agent_analyses)
        avg_opinion_shift = total_opinion_shift / len(agent_analyses) if agent_analyses else 0
        
        # Get top objections and suggestions
        all_objections = []
        all_suggestions = []
        for analysis in agent_analyses:
            all_objections.extend(analysis.objections)
            all_suggestions.extend(analysis.suggestions)
        
        prompt = f"""
Based on the following agent analyses of product features, provide strategic market insights:

## Features Analyzed:
{json.dumps([f.get('title', 'Unknown') for f in features], indent=2)}

## Agent Reactions Summary:
- Average Opinion Shift: {avg_opinion_shift:.3f}
- Total Objections: {len(all_objections)}
- Total Suggestions: {len(all_suggestions)}

## Market Context:
{json.dumps(market_context, indent=2)}

## Top Objections:
{json.dumps(all_objections[:5], indent=2)}

## Top Suggestions:
{json.dumps(all_suggestions[:5], indent=2)}

Provide strategic insights including:
1. Overall market reception prediction
2. Key success factors
3. Potential failure points
4. Competitive positioning
5. Recommended next steps
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            insights = response.choices[0].message.content
            
            return {
                "market_insights": insights,
                "adoption_score": max(0, min(100, (avg_opinion_shift + 1) * 50)),
                "top_objections": all_objections[:5],
                "top_suggestions": all_suggestions[:5],
                "confidence_score": 0.85
            }
            
        except Exception as e:
            print(f"Market insights generation failed: {e}")
            return self._mock_market_insights(features, agent_analyses)
    
    def _mock_market_insights(self, features: List[Dict[str, Any]], agent_analyses: List[FeatureAnalysis]) -> Dict[str, Any]:
        """Provide mock market insights"""
        return {
            "market_insights": "Mock market insights - LLM not available",
            "adoption_score": 65.0,
            "top_objections": ["Mock objection 1", "Mock objection 2"],
            "top_suggestions": ["Mock suggestion 1", "Mock suggestion 2"],
            "confidence_score": 0.5
        }
    
    async def generate_competitive_analysis(self, 
                                          product_features: List[Dict[str, Any]], 
                                          competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive analysis using LLM"""
        
        if not self.llm_available:
            return {"competitive_analysis": "Mock competitive analysis"}
        
        prompt = f"""
Analyze the competitive positioning of this product:

## Our Product Features:
{json.dumps([f.get('title', 'Unknown') for f in product_features], indent=2)}

## Competitor Information:
{json.dumps(competitor_data, indent=2)}

Provide a competitive analysis including:
1. Competitive advantages
2. Vulnerabilities
3. Market positioning
4. Differentiation opportunities
5. Threat assessment
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            
            return {
                "competitive_analysis": response.choices[0].message.content,
                "threat_level": "medium",
                "opportunity_score": 0.7
            }
            
        except Exception as e:
            print(f"Competitive analysis failed: {e}")
            return {"competitive_analysis": "Analysis failed"}
    
    async def generate_persona_insights(self, 
                                      agent_contexts: List[AgentContext], 
                                      feature_analyses: List[FeatureAnalysis]) -> Dict[str, Any]:
        """Generate insights about different customer personas"""
        
        if not self.llm_available:
            return {"persona_insights": "Mock persona insights"}
        
        # Group analyses by agent role
        role_analyses = {}
        for i, context in enumerate(agent_contexts):
            if context.role not in role_analyses:
                role_analyses[context.role] = []
            role_analyses[context.role].append(feature_analyses[i])
        
        prompt = f"""
Based on the following agent analyses grouped by persona type, provide insights about different customer segments:

## Customer Personas Analysis:
{json.dumps({role.value: [a.opinion_shift for a in analyses] for role, analyses in role_analyses.items()}, indent=2)}

## Feature Reactions by Persona:
{json.dumps({role.value: [a.reasoning[:100] + "..." for a in analyses] for role, analyses in role_analyses.items()}, indent=2)}

Provide insights about:
1. Which personas are most receptive
2. Which personas have the most objections
3. How to tailor messaging for each persona
4. Prioritization recommendations
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            
            return {
                "persona_insights": response.choices[0].message.content,
                "persona_receptiveness": {
                    role.value: sum(a.opinion_shift for a in analyses) / len(analyses) 
                    for role, analyses in role_analyses.items()
                }
            }
            
        except Exception as e:
            print(f"Persona insights generation failed: {e}")
            return {"persona_insights": "Analysis failed"}

# Global LLM integration instance
llm_integration = LLMIntegration()
