"""
Dejavas LLM Integration - Real AI Intelligence for Agents

This module provides the core LLM integration that powers the AI agents
with real intelligence, enabling sophisticated market analysis and
behavioral simulation.
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Pydantic (required for data models)
from pydantic import BaseModel, Field

# Try to import LLM dependencies with graceful fallbacks
try:
    from openai import AsyncOpenAI
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.prompts import ChatPromptTemplate
    from langchain.output_parsers import PydanticOutputParser
    LLM_AVAILABLE = True
    logger.info("✅ LLM dependencies loaded successfully")
except ImportError as e:
    LLM_AVAILABLE = False
    logger.warning(f"⚠️ LLM dependencies not available: {e}")
    logger.info("🔄 Falling back to enhanced mock AI system")

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

class EnhancedMockAI:
    """Advanced mock AI system that provides realistic, contextual responses"""
    
    def __init__(self):
        self.market_knowledge = self._load_market_knowledge()
        self.persona_templates = self._load_persona_templates()
        
    def _load_market_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive market knowledge for realistic responses"""
        return {
            "trends": {
                "2024": ["AI integration", "Sustainability", "Personalization", "Mobile-first", "Voice interfaces"],
                "2023": ["Remote work tools", "Cybersecurity", "Cloud migration", "Data privacy", "Automation"]
            },
            "customer_segments": {
                "early_adopters": {"risk_tolerance": 0.8, "innovation_seeking": 0.9, "price_sensitivity": 0.4},
                "early_majority": {"risk_tolerance": 0.5, "innovation_seeking": 0.6, "price_sensitivity": 0.6},
                "late_majority": {"risk_tolerance": 0.3, "innovation_seeking": 0.3, "price_sensitivity": 0.8},
                "laggards": {"risk_tolerance": 0.1, "innovation_seeking": 0.1, "price_sensitivity": 0.9}
            },
            "competitive_factors": ["pricing", "features", "user_experience", "customer_support", "brand_reputation", "innovation_speed"],
            "market_dynamics": ["supply_demand", "regulatory_changes", "economic_conditions", "technological_disruption"]
        }
    
    def _load_persona_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load detailed persona templates for realistic agent behavior"""
        return {
            "customer": {
                "pain_points": ["complexity", "high_cost", "poor_ux", "lack_of_integration", "slow_performance"],
                "desires": ["simplicity", "value", "efficiency", "reliability", "innovation"],
                "decision_factors": ["price", "features", "reviews", "brand", "support"]
            },
            "competitor": {
                "strategic_focus": ["market_share", "innovation", "cost_leadership", "differentiation", "customer_loyalty"],
                "threat_assessment": ["feature_parity", "pricing_pressure", "talent_poaching", "patent_infringement"],
                "opportunity_areas": ["market_gaps", "customer_pain_points", "technology_advantages"]
            },
            "influencer": {
                "content_preferences": ["trendy", "authentic", "educational", "entertaining", "controversial"],
                "audience_engagement": ["high", "medium", "low"],
                "credibility_factors": ["expertise", "authenticity", "reach", "engagement_rate"]
            },
            "internal_team": {
                "department_goals": {
                    "pm": ["user_satisfaction", "feature_completion", "market_fit"],
                    "sales": ["revenue", "conversion_rate", "customer_acquisition"],
                    "cx": ["customer_retention", "satisfaction_score", "support_efficiency"]
                }
            }
        }
    
    def analyze_feature(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> FeatureAnalysis:
        """Provide sophisticated mock analysis based on real market knowledge"""
        
        # Analyze feature characteristics
        feature_score = self._analyze_feature_characteristics(feature, context)
        
        # Apply persona-specific logic
        persona_analysis = self._apply_persona_logic(feature, context, market_context)
        
        # Generate realistic reasoning
        reasoning = self._generate_realistic_reasoning(feature, context, feature_score, persona_analysis)
        
        # Create objections and suggestions
        objections, suggestions = self._generate_objections_suggestions(feature, context, feature_score)
        
        # Calculate attention spend based on relevance
        attention_spent = self._calculate_attention_spend(feature, context, feature_score)
        
        return FeatureAnalysis(
            feature_title=feature.get('title', 'Unknown Feature'),
            opinion_shift=feature_score,
            reasoning=reasoning,
            objections=objections,
            suggestions=suggestions,
            influence_impact=context.genome.get('influence_score', 0.5),
            attention_spent=attention_spent
        )
    
    def _analyze_feature_characteristics(self, feature: Dict[str, Any], context: AgentContext) -> float:
        """Analyze feature characteristics and return opinion shift"""
        base_score = 0.0
        description = feature.get('description', '').lower()
        title = feature.get('title', '').lower()
        
        # Positive indicators
        positive_keywords = ['ai', 'automation', 'integration', 'mobile', 'cloud', 'secure', 'fast', 'easy', 'intuitive']
        for keyword in positive_keywords:
            if keyword in description or keyword in title:
                base_score += 0.1
        
        # Negative indicators
        negative_keywords = ['complex', 'expensive', 'slow', 'difficult', 'limited', 'basic', 'outdated']
        for keyword in negative_keywords:
            if keyword in description or keyword in title:
                base_score -= 0.15
        
        # Apply personality modifiers
        personality_modifier = self._calculate_personality_modifier(context)
        base_score *= personality_modifier
        
        # Add some randomness for realism
        base_score += random.uniform(-0.05, 0.05)
        
        return max(-1.0, min(1.0, base_score))
    
    def _calculate_personality_modifier(self, context: AgentContext) -> float:
        """Calculate personality-based modifier for opinion shifts"""
        personality_traits = context.genome.get('personality_traits', [])
        modifier = 1.0
        
        for trait in personality_traits:
            if isinstance(trait, str):
                trait = trait.lower()
            else:
                trait = trait.value.lower()
                
            if 'early_adopter' in trait:
                modifier += 0.3
            elif 'skeptic' in trait:
                modifier -= 0.4
            elif 'enthusiast' in trait:
                modifier += 0.2
            elif 'laggard' in trait:
                modifier -= 0.3
        
        return max(0.3, min(2.0, modifier))
    
    def _apply_persona_logic(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply persona-specific analysis logic"""
        role = context.role.value
        analysis = {}
        
        if role == "customer":
            analysis = self._analyze_customer_perspective(feature, context, market_context)
        elif role == "competitor":
            analysis = self._analyze_competitor_perspective(feature, context, market_context)
        elif role == "influencer":
            analysis = self._analyze_influencer_perspective(feature, context, market_context)
        elif role == "internal_team":
            analysis = self._analyze_internal_perspective(feature, context, market_context)
        
        return analysis
    
    def _analyze_customer_perspective(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature from customer perspective"""
        demographics = context.genome.get('demographics', {})
        psychographics = context.genome.get('psychographics', {})
        
        analysis = {
            "value_perception": 0.5,
            "ease_of_use": 0.5,
            "need_alignment": 0.5
        }
        
        # Age-based analysis
        age = demographics.get('age', 35)
        if age < 25:
            analysis["ease_of_use"] += 0.2  # Younger users expect intuitive UX
        elif age > 50:
            analysis["ease_of_use"] -= 0.1  # Older users may struggle with complex features
        
        # Tech savviness impact
        tech_savviness = psychographics.get('tech_savviness', 0.5)
        analysis["value_perception"] += (tech_savviness - 0.5) * 0.3
        
        # Price sensitivity
        price_sensitivity = psychographics.get('price_sensitivity', 0.5)
        if 'free' in feature.get('description', '').lower() or 'trial' in feature.get('description', '').lower():
            analysis["value_perception"] += 0.2 * (1 - price_sensitivity)
        
        return analysis
    
    def _analyze_competitor_perspective(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature from competitor perspective"""
        psychographics = context.genome.get('psychographics', {})
        
        analysis = {
            "threat_level": 0.5,
            "competitive_advantage": 0.5,
            "market_impact": 0.5
        }
        
        # Aggressiveness affects threat perception
        aggressiveness = psychographics.get('aggressiveness', 0.5)
        if 'ai' in feature.get('description', '').lower() or 'automation' in feature.get('description', '').lower():
            analysis["threat_level"] += 0.3 * aggressiveness
        
        # Innovation focus affects competitive advantage assessment
        innovation_focus = psychographics.get('innovation_focus', 0.5)
        analysis["competitive_advantage"] += (innovation_focus - 0.5) * 0.4
        
        return analysis
    
    def _analyze_influencer_perspective(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature from influencer perspective"""
        psychographics = context.genome.get('psychographics', {})
        
        analysis = {
            "trendiness": 0.5,
            "shareability": 0.5,
            "audience_appeal": 0.5
        }
        
        # Check if feature aligns with current trends
        current_trends = self.market_knowledge["trends"]["2024"]
        description = feature.get('description', '').lower()
        
        for trend in current_trends:
            if trend.lower() in description:
                analysis["trendiness"] += 0.3
                analysis["shareability"] += 0.2
        
        # Engagement rate affects audience appeal calculation
        engagement_rate = psychographics.get('engagement_rate', 0.5)
        analysis["audience_appeal"] += (engagement_rate - 0.5) * 0.3
        
        return analysis
    
    def _analyze_internal_perspective(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature from internal team perspective"""
        demographics = context.genome.get('demographics', {})
        role = demographics.get('role', 'pm')
        
        analysis = {
            "strategic_alignment": 0.5,
            "implementation_feasibility": 0.5,
            "resource_requirements": 0.5
        }
        
        # Role-specific analysis
        if role == "pm":
            if 'user' in feature.get('description', '').lower() or 'customer' in feature.get('description', '').lower():
                analysis["strategic_alignment"] += 0.3
        elif role == "sales":
            if 'pricing' in feature.get('description', '').lower() or 'roi' in feature.get('description', '').lower():
                analysis["strategic_alignment"] += 0.3
        elif role == "cx":
            if 'support' in feature.get('description', '').lower() or 'help' in feature.get('description', '').lower():
                analysis["strategic_alignment"] += 0.3
        
        return analysis
    
    def _generate_realistic_reasoning(self, feature: Dict[str, Any], context: AgentContext, feature_score: float, persona_analysis: Dict[str, Any]) -> str:
        """Generate realistic reasoning for the agent's opinion"""
        role = context.role.value
        feature_title = feature.get('title', 'this feature')
        
        if feature_score > 0.3:
            if role == "customer":
                return f"As a customer, I'm impressed by {feature_title}. It addresses real pain points and offers clear value. The implementation looks solid and user-friendly."
            elif role == "competitor":
                return f"This {feature_title} represents a significant competitive threat. The innovation level and market positioning are concerning for our market share."
            elif role == "influencer":
                return f"{feature_title} is exactly what my audience needs right now. It's trendy, innovative, and has great shareability potential."
            else:
                return f"From an internal perspective, {feature_title} aligns well with our strategic goals and should drive positive business outcomes."
        
        elif feature_score < -0.3:
            if role == "customer":
                return f"I have serious concerns about {feature_title}. The implementation seems complex and doesn't address my core needs effectively."
            elif role == "competitor":
                return f"This {feature_title} has several vulnerabilities we can exploit. The approach seems flawed and won't pose a significant threat."
            elif role == "influencer":
                return f"{feature_title} doesn't align with current trends and won't resonate with my audience. It feels outdated and uninspired."
            else:
                return f"Internally, {feature_title} raises concerns about resource allocation and strategic alignment with our core objectives."
        
        else:
            return f"My opinion on {feature_title} is mixed. While it has some positive aspects, there are also areas that need improvement before I can fully endorse it."
    
    def _generate_objections_suggestions(self, feature: Dict[str, Any], context: AgentContext, feature_score: float) -> Tuple[List[str], List[str]]:
        """Generate realistic objections and suggestions"""
        objections = []
        suggestions = []
        
        description = feature.get('description', '').lower()
        role = context.role.value
        
        # Generate role-specific objections
        if role == "customer":
            if 'complex' in description or 'advanced' in description:
                objections.append("Feature complexity may overwhelm average users")
            if 'expensive' in description or 'premium' in description:
                objections.append("Pricing may be too high for target market")
            if 'integration' in description:
                objections.append("Integration requirements may be too complex")
        
        elif role == "competitor":
            if 'ai' in description or 'automation' in description:
                objections.append("AI features may not be mature enough for production")
            if 'mobile' in description:
                objections.append("Mobile-first approach may alienate desktop users")
        
        elif role == "influencer":
            if 'technical' in description:
                objections.append("Too technical for general audience engagement")
            if 'niche' in description:
                objections.append("Limited appeal may reduce shareability")
        
        # Generate suggestions for improvement
        if feature_score < 0:
            suggestions.append("Simplify the user interface and onboarding process")
            suggestions.append("Provide better documentation and support resources")
            suggestions.append("Consider phased rollout to gather user feedback")
        
        if len(objections) == 0:
            objections.append("No major objections identified")
        
        if len(suggestions) == 0:
            suggestions.append("Feature appears well-implemented")
        
        return objections[:3], suggestions[:3]  # Limit to top 3
    
    def _calculate_attention_spend(self, feature: Dict[str, Any], context: AgentContext, feature_score: float) -> int:
        """Calculate realistic attention token spend"""
        base_spend = 15
        
        # Spend more tokens on controversial or complex features
        if abs(feature_score) > 0.5:
            base_spend += 10
        
        # Role-specific attention patterns
        role = context.role.value
        if role == "competitor":
            base_spend += 5  # Competitors pay more attention
        elif role == "influencer":
            base_spend += 8  # Influencers need to understand deeply
        
        # Feature complexity affects attention
        description = feature.get('description', '')
        if len(description) > 100:
            base_spend += 5
        
        return min(base_spend, context.attention_tokens)

    def generate_market_insights(self, features: List[Dict[str, Any]], agent_analyses: List[FeatureAnalysis]) -> Dict[str, Any]:
        """Generate realistic market insights from agent analyses"""
        if not agent_analyses:
            return {
                "market_insights": "Insufficient data for market analysis",
                "adoption_score": 50.0,
                "top_objections": ["No agent feedback available"],
                "top_suggestions": ["Gather more agent feedback"],
                "confidence_score": 0.3
            }
        
        # Calculate adoption score from agent opinions
        total_opinion_shift = sum(analysis.opinion_shift for analysis in agent_analyses)
        avg_opinion_shift = total_opinion_shift / len(agent_analyses)
        
        # Convert to 0-100 scale
        adoption_score = max(0, min(100, (avg_opinion_shift + 1) * 50))
        
        # Aggregate objections and suggestions
        all_objections = []
        all_suggestions = []
        for analysis in agent_analyses:
            all_objections.extend(analysis.objections)
            all_suggestions.extend(analysis.suggestions)
        
        # Generate market insights based on trends
        current_trends = self.market_knowledge["trends"]["2024"]
        feature_titles = [f.get('title', '') for f in features]
        
        trend_alignment = 0
        for trend in current_trends:
            for title in feature_titles:
                if trend.lower() in title.lower():
                    trend_alignment += 1
        
        if trend_alignment > 0:
            market_insights = f"Features show strong alignment with 2024 trends including {', '.join(current_trends[:3])}. Market reception should be positive."
        else:
            market_insights = "Features may need trend alignment updates to maximize market appeal in 2024."
        
        return {
            "market_insights": market_insights,
            "adoption_score": adoption_score,
            "top_objections": all_objections[:5],
            "top_suggestions": all_suggestions[:5],
            "confidence_score": 0.8,
            "trend_alignment": trend_alignment
        }
    
    def generate_competitive_analysis(self, product_features: List[Dict[str, Any]], competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic competitive analysis"""
        feature_count = len(product_features)
        feature_quality = sum(1 for f in product_features if any(word in f.get('description', '').lower() 
                                                               for word in ['ai', 'automation', 'integration']))
        
        # Assess competitive positioning
        if feature_quality > feature_count * 0.6:
            competitive_position = "strong"
            threat_level = "low"
            opportunity_score = 0.8
        elif feature_quality > feature_count * 0.3:
            competitive_position = "moderate"
            threat_level = "medium"
            opportunity_score = 0.6
        else:
            competitive_position = "weak"
            threat_level = "high"
            opportunity_score = 0.3
        
        analysis = f"Product shows {competitive_position} competitive positioning with {feature_quality}/{feature_count} high-quality features. "
        analysis += f"Threat level is {threat_level} with opportunity score of {opportunity_score:.1f}."
        
        return {
            "competitive_analysis": analysis,
            "threat_level": threat_level,
            "opportunity_score": opportunity_score,
            "competitive_position": competitive_position,
            "feature_quality_ratio": feature_quality / feature_count
        }
    
    def generate_persona_insights(self, agent_contexts: List[Dict[str, Any]], feature_analyses: List[FeatureAnalysis]) -> Dict[str, Any]:
        """Generate insights about different customer personas"""
        if not agent_contexts or not feature_analyses:
            return {"persona_insights": "Insufficient data for persona analysis"}
        
        # Group analyses by agent role
        role_analyses = {}
        for i, context in enumerate(agent_contexts):
            role = context.get('role', 'unknown')
            if role not in role_analyses:
                role_analyses[role] = []
            if i < len(feature_analyses):
                role_analyses[role].append(feature_analyses[i])
        
        # Calculate receptiveness by role
        persona_receptiveness = {}
        for role, analyses in role_analyses.items():
            if analyses:
                avg_opinion = sum(a.opinion_shift for a in analyses) / len(analyses)
                persona_receptiveness[role] = avg_opinion
        
        # Generate insights
        insights = "Persona analysis reveals varying receptiveness across segments:\n"
        for role, receptiveness in persona_receptiveness.items():
            if receptiveness > 0.3:
                insights += f"• {role.title()} personas are highly receptive (score: {receptiveness:.2f})\n"
            elif receptiveness < -0.3:
                insights += f"• {role.title()} personas have significant concerns (score: {receptiveness:.2f})\n"
            else:
                insights += f"• {role.title()} personas show mixed reactions (score: {receptiveness:.2f})\n"
        
        return {
            "persona_insights": insights,
            "persona_receptiveness": persona_receptiveness,
            "recommendations": self._generate_persona_recommendations(persona_receptiveness)
        }
    
    def _generate_persona_recommendations(self, persona_receptiveness: Dict[str, float]) -> List[str]:
        """Generate recommendations based on persona receptiveness"""
        recommendations = []
        
        # Find most and least receptive personas
        if persona_receptiveness:
            most_receptive = max(persona_receptiveness.items(), key=lambda x: x[1])
            least_receptive = min(persona_receptiveness.items(), key=lambda x: x[1])
            
            if most_receptive[1] > 0.5:
                recommendations.append(f"Focus marketing efforts on {most_receptive[0]} personas as primary advocates")
            
            if least_receptive[1] < -0.3:
                recommendations.append(f"Address concerns of {least_receptive[0]} personas to improve overall adoption")
            
            # General recommendations
            if len(persona_receptiveness) > 2:
                recommendations.append("Consider persona-specific messaging to address varying receptiveness levels")
        
        return recommendations

class LLMIntegration:
    """Core LLM integration for Dejavas agents"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm_available = LLM_AVAILABLE and self.api_key
        
        if self.llm_available:
            try:
                self.client = AsyncOpenAI(api_key=self.api_key)
                self.chat_model = ChatOpenAI(
                    model="gpt-4-turbo-preview",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("✅ OpenAI integration initialized successfully")
            except Exception as e:
                logger.error(f"❌ OpenAI initialization failed: {e}")
                self.llm_available = False
                self.client = None
                self.chat_model = None
        
        # Initialize enhanced mock AI as fallback
        self.mock_ai = EnhancedMockAI()
        logger.info("🔄 Enhanced mock AI system initialized as fallback")
    
    async def analyze_feature_as_agent(self, 
                                     feature: Dict[str, Any], 
                                     context: AgentContext,
                                     market_context: Dict[str, Any]) -> FeatureAnalysis:
        """Analyze a feature from the perspective of a specific agent"""
        
        if self.llm_available:
            try:
                # Try real LLM analysis
                analysis = await self._get_llm_analysis(feature, context, market_context)
                if analysis:
                    logger.info(f"✅ LLM analysis completed for {context.role.value} agent")
                    return analysis
            except Exception as e:
                logger.warning(f"⚠️ LLM analysis failed, falling back to enhanced mock: {e}")
        
        # Use enhanced mock AI
        analysis = self.mock_ai.analyze_feature(feature, context, market_context)
        logger.info(f"🔄 Enhanced mock analysis completed for {context.role.value} agent")
        return analysis
    
    async def _get_llm_analysis(self, feature: Dict[str, Any], context: AgentContext, market_context: Dict[str, Any]) -> Optional[FeatureAnalysis]:
        """Get analysis from real LLM"""
        try:
            prompt = self._create_agent_prompt(feature, context, market_context)
            response = await self._get_structured_response(prompt, context.role)
            
            return FeatureAnalysis(
                feature_title=feature.get('title', 'Unknown Feature'),
                opinion_shift=response.opinion_shift,
                reasoning=response.reasoning,
                objections=response.objections,
                suggestions=response.suggestions,
                influence_impact=response.influence_impact,
                attention_spent=response.attention_spent
            )
        except Exception as e:
            logger.error(f"LLM analysis error: {e}")
            return None
    
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
    
    async def generate_market_insights(self, 
                                     features: List[Dict[str, Any]], 
                                     agent_analyses: List[FeatureAnalysis],
                                     market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level market insights from agent analyses"""
        
        if self.llm_available:
            try:
                return await self._get_llm_market_insights(features, agent_analyses, market_context)
            except Exception as e:
                logger.warning(f"⚠️ LLM market insights failed, using enhanced mock: {e}")
        
        return self.mock_ai.generate_market_insights(features, agent_analyses)
    
    async def _get_llm_market_insights(self, features: List[Dict[str, Any]], agent_analyses: List[FeatureAnalysis], market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get market insights from LLM"""
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
            logger.error(f"Market insights generation failed: {e}")
            raise
    
    async def generate_competitive_analysis(self, 
                                          product_features: List[Dict[str, Any]], 
                                          competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive analysis using LLM"""
        
        if self.llm_available:
            try:
                return await self._get_llm_competitive_analysis(product_features, competitor_data)
            except Exception as e:
                logger.warning(f"⚠️ LLM competitive analysis failed, using enhanced mock: {e}")
        
        return self.mock_ai.generate_competitive_analysis(product_features, competitor_data)
    
    async def _get_llm_competitive_analysis(self, product_features: List[Dict[str, Any]], competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get competitive analysis from LLM"""
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
            logger.error(f"Competitive analysis failed: {e}")
            raise
    
    async def generate_persona_insights(self, 
                                      agent_contexts: List[Dict[str, Any]], 
                                      feature_analyses: List[FeatureAnalysis]) -> Dict[str, Any]:
        """Generate insights about different customer personas"""
        
        if self.llm_available:
            try:
                return await self._get_llm_persona_insights(agent_contexts, feature_analyses)
            except Exception as e:
                logger.warning(f"⚠️ LLM persona insights failed, using enhanced mock: {e}")
        
        return self.mock_ai.generate_persona_insights(agent_contexts, feature_analyses)

# Global LLM integration instance
llm_integration = LLMIntegration()
