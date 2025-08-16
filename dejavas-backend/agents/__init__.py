"""
Dejavas Agent System - Deep Persona DNA Implementation

This module implements the core agent system with "genome" profiles that define
each agent's demographics, psychographics, and behavioral patterns.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import random
import json
import asyncio

from llm_integration import llm_integration, AgentContext, AgentRole, FeatureAnalysis

class AgentType(Enum):
    CUSTOMER = "customer"
    COMPETITOR = "competitor"
    INFLUENCER = "influencer"
    INTERNAL_TEAM = "internal_team"

class PersonalityTrait(Enum):
    EARLY_ADOPTER = "early_adopter"
    LATE_MAJORITY = "late_majority"
    LAGGARD = "laggard"
    INFLUENCER = "influencer"
    SKEPTIC = "skeptic"
    ENTHUSIAST = "enthusiast"

class AgentGenome:
    """Deep Persona DNA - Each agent's unique behavioral profile"""
    
    def __init__(self, agent_type: AgentType, **kwargs):
        self.agent_type = agent_type
        self.demographics = kwargs.get('demographics', {})
        self.psychographics = kwargs.get('psychographics', {})
        self.behavioral_patterns = kwargs.get('behavioral_patterns', {})
        self.influence_score = kwargs.get('influence_score', 0.5)
        self.attention_tokens = kwargs.get('attention_tokens', 100)
        self.personality_traits = kwargs.get('personality_traits', [])
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_type': self.agent_type.value,
            'demographics': self.demographics,
            'psychographics': self.psychographics,
            'behavioral_patterns': self.behavioral_patterns,
            'influence_score': self.influence_score,
            'attention_tokens': self.attention_tokens,
            'personality_traits': [trait.value for trait in self.personality_traits]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentGenome':
        return cls(
            agent_type=AgentType(data['agent_type']),
            demographics=data.get('demographics', {}),
            psychographics=data.get('psychographics', {}),
            behavioral_patterns=data.get('behavioral_patterns', {}),
            influence_score=data.get('influence_score', 0.5),
            attention_tokens=data.get('attention_tokens', 100),
            personality_traits=[PersonalityTrait(trait) for trait in data.get('personality_traits', [])]
        )

class Agent:
    """Base agent class with genome-driven behavior"""
    
    def __init__(self, genome: AgentGenome, name: str = None):
        self.genome = genome
        self.name = name or f"{genome.agent_type.value}_{random.randint(1000, 9999)}"
        self.memory = []
        self.relationships = {}
        self.current_opinion = 0.5  # Neutral starting point
        
    async def process_feature(self, feature: Dict[str, Any], market_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a feature using real AI intelligence"""
        
        # Create agent context for LLM
        context = AgentContext(
            role=AgentRole(self.genome.agent_type.value),
            genome=self.genome.to_dict(),
            current_opinion=self.current_opinion,
            memory=self.memory,
            relationships=self.relationships,
            attention_tokens=self.genome.attention_tokens
        )
        
        # Use LLM integration for intelligent analysis
        analysis = await llm_integration.analyze_feature_as_agent(
            feature, context, market_context or {}
        )
        
        # Update agent state based on LLM analysis
        self.current_opinion = max(0, min(1, self.current_opinion + analysis.opinion_shift))
        self.genome.attention_tokens -= analysis.attention_spent
        
        # Store reasoning in memory
        self.memory.append(analysis.reasoning)
        if len(self.memory) > 10:  # Keep last 10 memories
            self.memory.pop(0)
        
        return {
            'agent_name': self.name,
            'agent_type': self.genome.agent_type.value,
            'opinion': self.current_opinion,
            'tokens_spent': analysis.attention_spent,
            'reasoning': analysis.reasoning,
            'objections': analysis.objections,
            'suggestions': analysis.suggestions,
            'influence_impact': analysis.influence_impact
        }
    
    def _calculate_opinion_shift(self, feature: Dict[str, Any]) -> float:
        """Calculate how much this feature affects the agent's opinion"""
        base_shift = 0.0
        
        # Personality-based reactions
        for trait in self.genome.personality_traits:
            if trait == PersonalityTrait.EARLY_ADOPTER:
                base_shift += 0.1
            elif trait == PersonalityTrait.SKEPTIC:
                base_shift -= 0.05
            elif trait == PersonalityTrait.ENTHUSIAST:
                base_shift += 0.15
                
        # Demographics-based reactions
        age = self.genome.demographics.get('age', 35)
        if age < 25:
            base_shift += 0.05  # Younger users more open to new features
        elif age > 50:
            base_shift -= 0.03  # Older users more conservative
            
        # Psychographics-based reactions
        tech_savviness = self.genome.psychographics.get('tech_savviness', 0.5)
        base_shift += (tech_savviness - 0.5) * 0.1
        
        return base_shift
    
    def _calculate_attention_spend(self, feature: Dict[str, Any]) -> int:
        """Calculate how many attention tokens to spend on this feature"""
        base_spend = 10
        
        # Spend more tokens if feature is relevant to agent type
        if self.genome.agent_type == AgentType.CUSTOMER:
            if 'user_experience' in feature.get('description', '').lower():
                base_spend += 15
        elif self.genome.agent_type == AgentType.COMPETITOR:
            if 'pricing' in feature.get('description', '').lower():
                base_spend += 20
                
        return min(base_spend, self.genome.attention_tokens)
    
    def _generate_reasoning(self, feature: Dict[str, Any], opinion_shift: float) -> str:
        """Generate reasoning for the agent's opinion"""
        if opinion_shift > 0:
            return f"Positive reaction to {feature.get('title', 'feature')} based on {self.genome.agent_type.value} perspective"
        elif opinion_shift < 0:
            return f"Concerns about {feature.get('title', 'feature')} from {self.genome.agent_type.value} viewpoint"
        else:
            return f"Neutral stance on {feature.get('title', 'feature')}"

class AgentFactory:
    """Factory for creating agents with diverse genomes"""
    
    @staticmethod
    def create_customer_agent() -> Agent:
        """Create a customer agent with realistic demographics"""
        demographics = {
            'age': random.randint(18, 65),
            'income_level': random.choice(['low', 'middle', 'high']),
            'location': random.choice(['urban', 'suburban', 'rural']),
            'education': random.choice(['high_school', 'college', 'graduate'])
        }
        
        psychographics = {
            'tech_savviness': random.uniform(0.2, 1.0),
            'price_sensitivity': random.uniform(0.3, 0.9),
            'brand_loyalty': random.uniform(0.1, 0.8),
            'social_influence': random.uniform(0.1, 0.7)
        }
        
        personality_traits = random.sample(list(PersonalityTrait), random.randint(1, 3))
        
        genome = AgentGenome(
            agent_type=AgentType.CUSTOMER,
            demographics=demographics,
            psychographics=psychographics,
            personality_traits=personality_traits,
            influence_score=random.uniform(0.1, 0.6)
        )
        
        return Agent(genome)
    
    @staticmethod
    def create_competitor_agent() -> Agent:
        """Create a competitor agent with strategic thinking"""
        genome = AgentGenome(
            agent_type=AgentType.COMPETITOR,
            psychographics={
                'aggressiveness': random.uniform(0.4, 0.9),
                'market_share': random.uniform(0.1, 0.8),
                'innovation_focus': random.uniform(0.3, 0.9)
            },
            personality_traits=[PersonalityTrait.SKEPTIC],
            influence_score=random.uniform(0.6, 0.9)
        )
        
        return Agent(genome)
    
    @staticmethod
    def create_influencer_agent() -> Agent:
        """Create an influencer agent with high social impact"""
        genome = AgentGenome(
            agent_type=AgentType.INFLUENCER,
            psychographics={
                'reach': random.uniform(0.7, 1.0),
                'credibility': random.uniform(0.5, 0.9),
                'engagement_rate': random.uniform(0.3, 0.8)
            },
            personality_traits=[PersonalityTrait.INFLUENCER],
            influence_score=random.uniform(0.7, 1.0),
            attention_tokens=150  # Influencers have more attention to spend
        )
        
        return Agent(genome)
    
    @staticmethod
    def create_internal_team_agent(role: str = "pm") -> Agent:
        """Create an internal team agent (PM, Sales, CX)"""
        genome = AgentGenome(
            agent_type=AgentType.INTERNAL_TEAM,
            demographics={'role': role},
            psychographics={
                'department_bias': random.uniform(0.3, 0.8),
                'company_loyalty': random.uniform(0.6, 0.9),
                'risk_tolerance': random.uniform(0.2, 0.7)
            },
            personality_traits=[PersonalityTrait.ENTHUSIAST],
            influence_score=random.uniform(0.4, 0.7)
        )
        
        return Agent(genome, name=f"{role.upper()}_{random.randint(100, 999)}")
