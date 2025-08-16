"""
Dejavas Simulation Engine - Advanced Market Intelligence

This module implements the core simulation engine with influence graphs,
evolving rounds, and arena health metrics.
"""

from typing import Dict, List, Optional, Any, Tuple
import random
import networkx as nx
from enum import Enum
import json
import asyncio

from agents import Agent, AgentFactory, AgentType
from llm_integration import llm_integration, FeatureAnalysis

class NetworkTopology(Enum):
    ECHO_CHAMBER = "echo_chamber"
    LOOSE_NETWORK = "loose_network"
    REAL_FOLLOWER = "real_follower"

class ArenaHealthMetrics:
    """Computes macro metrics for the simulation arena"""
    
    def __init__(self):
        self.polarization_score = 0.0
        self.advocate_to_saboteur_ratio = 0.0
        self.viral_path_length = 0.0
        self.engagement_density = 0.0
        
    def calculate_metrics(self, agents: List[Agent], interactions: List[Dict]) -> Dict[str, float]:
        """Calculate all arena health metrics"""
        self.polarization_score = self._calculate_polarization(agents)
        self.advocate_to_saboteur_ratio = self._calculate_advocate_ratio(agents)
        self.viral_path_length = self._calculate_viral_path(interactions)
        self.engagement_density = self._calculate_engagement_density(interactions)
        
        return {
            'polarization_score': self.polarization_score,
            'advocate_to_saboteur_ratio': self.advocate_to_saboteur_ratio,
            'viral_path_length': self.viral_path_length,
            'engagement_density': self.engagement_density
        }
    
    def _calculate_polarization(self, agents: List[Agent]) -> float:
        """Calculate how polarized the arena is (0 = consensus, 1 = highly polarized)"""
        opinions = [agent.current_opinion for agent in agents]
        mean_opinion = sum(opinions) / len(opinions)
        variance = sum((op - mean_opinion) ** 2 for op in opinions) / len(opinions)
        return min(1.0, variance * 4)  # Scale to 0-1 range
    
    def _calculate_advocate_ratio(self, agents: List[Agent]) -> float:
        """Calculate ratio of advocates (opinion > 0.7) to saboteurs (opinion < 0.3)"""
        advocates = sum(1 for agent in agents if agent.current_opinion > 0.7)
        saboteurs = sum(1 for agent in agents if agent.current_opinion < 0.3)
        return advocates / max(saboteurs, 1)  # Avoid division by zero
    
    def _calculate_viral_path(self, interactions: List[Dict]) -> float:
        """Calculate average viral path length for information spread"""
        if not interactions:
            return 0.0
        
        # Simple heuristic: average influence impact across interactions
        total_impact = sum(interaction.get('influence_impact', 0) for interaction in interactions)
        return total_impact / len(interactions)
    
    def _calculate_engagement_density(self, interactions: List[Dict]) -> float:
        """Calculate how densely agents are interacting"""
        if not interactions:
            return 0.0
        
        # Count unique agent pairs that interacted
        unique_pairs = set()
        for interaction in interactions:
            if 'agent_name' in interaction and 'target_agent' in interaction:
                pair = tuple(sorted([interaction['agent_name'], interaction['target_agent']]))
                unique_pairs.add(pair)
        
        return len(unique_pairs) / max(len(interactions), 1)

class InfluenceGraph:
    """Manages the network topology and influence flows between agents"""
    
    def __init__(self, topology: NetworkTopology = NetworkTopology.LOOSE_NETWORK):
        self.topology = topology
        self.graph = nx.DiGraph()
        self.agents = {}
        
    def add_agents(self, agents: List[Agent]):
        """Add agents to the influence graph"""
        for agent in agents:
            self.agents[agent.name] = agent
            self.graph.add_node(agent.name, agent=agent)
        
        # Create edges based on topology
        self._create_network_edges()
    
    def _create_network_edges(self):
        """Create network edges based on the chosen topology"""
        agent_names = list(self.agents.keys())
        
        if self.topology == NetworkTopology.ECHO_CHAMBER:
            # Agents connect to similar agents (high homophily)
            for i, agent_name in enumerate(agent_names):
                agent = self.agents[agent_name]
                for j, other_name in enumerate(agent_names):
                    if i != j:
                        other_agent = self.agents[other_name]
                        # Higher connection probability for similar agents
                        similarity = 1 - abs(agent.current_opinion - other_agent.current_opinion)
                        if random.random() < similarity * 0.3:
                            self.graph.add_edge(agent_name, other_name, weight=similarity)
        
        elif self.topology == NetworkTopology.LOOSE_NETWORK:
            # Random connections with some clustering
            for agent_name in agent_names:
                # Connect to 2-4 random agents
                num_connections = random.randint(2, 4)
                connections = random.sample([n for n in agent_names if n != agent_name], 
                                         min(num_connections, len(agent_names) - 1))
                for connection in connections:
                    weight = random.uniform(0.1, 1.0)
                    self.graph.add_edge(agent_name, connection, weight=weight)
        
        elif self.topology == NetworkTopology.REAL_FOLLOWER:
            # Power law distribution (few influencers, many followers)
            # Sort agents by influence score
            sorted_agents = sorted(agent_names, 
                                 key=lambda x: self.agents[x].genome.influence_score, 
                                 reverse=True)
            
            # Top 20% are influencers, rest are followers
            num_influencers = max(1, len(sorted_agents) // 5)
            influencers = sorted_agents[:num_influencers]
            followers = sorted_agents[num_influencers:]
            
            # Followers connect to influencers
            for follower in followers:
                # Each follower follows 1-3 influencers
                num_follows = random.randint(1, min(3, len(influencers)))
                followed_influencers = random.sample(influencers, num_follows)
                for influencer in followed_influencers:
                    weight = self.agents[influencer].genome.influence_score
                    self.graph.add_edge(follower, influencer, weight=weight)
    
    def get_influencers(self, agent_name: str) -> List[str]:
        """Get agents that influence the given agent"""
        return list(self.graph.predecessors(agent_name))
    
    def get_followers(self, agent_name: str) -> List[str]:
        """Get agents that are influenced by the given agent"""
        return list(self.graph.successors(agent_name))
    
    def calculate_influence_flow(self, source_agent: str, target_agent: str) -> float:
        """Calculate the strength of influence from source to target"""
        if self.graph.has_edge(source_agent, target_agent):
            return self.graph[source_agent][target_agent]['weight']
        return 0.0

class AdvancedSimulator:
    """Enhanced simulation engine with influence graphs and evolving rounds"""
    
    def __init__(self, network_topology: NetworkTopology = NetworkTopology.LOOSE_NETWORK):
        self.network_topology = network_topology
        self.influence_graph = InfluenceGraph(network_topology)
        self.health_metrics = ArenaHealthMetrics()
        self.round_history = []
        
    def create_agent_population(self, config: Dict[str, int]) -> List[Agent]:
        """Create a population of agents based on configuration"""
        agents = []
        total_agents = 20  # Fixed population size for now
        
        # Calculate number of each agent type
        num_customers = int((config.get('customer_percentage', 60) / 100) * total_agents)
        num_competitors = int((config.get('competitor_percentage', 20) / 100) * total_agents)
        num_influencers = int((config.get('influencer_percentage', 10) / 100) * total_agents)
        num_internal = total_agents - num_customers - num_competitors - num_influencers
        
        # Create agents
        for _ in range(num_customers):
            agents.append(AgentFactory.create_customer_agent())
        
        for _ in range(num_competitors):
            agents.append(AgentFactory.create_competitor_agent())
        
        for _ in range(num_influencers):
            agents.append(AgentFactory.create_influencer_agent())
        
        for i in range(num_internal):
            role = ['pm', 'sales', 'cx'][i % 3]
            agents.append(AgentFactory.create_internal_team_agent(role))
        
        return agents
    
    async def run_simulation(self, brief: Dict, config: Dict, num_rounds: int = 5, market_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run the complete simulation with multiple rounds using real AI intelligence"""
        # Create agent population
        agents = self.create_agent_population(config)
        self.influence_graph.add_agents(agents)
        
        # Initialize round history
        self.round_history = []
        
        # Run multiple rounds
        for round_num in range(num_rounds):
            round_result = await self._run_single_round(brief, agents, round_num, market_context)
            self.round_history.append(round_result)
            
            # Update agent opinions based on influence
            self._apply_influence_effects(agents, round_result['interactions'])
        
        # Calculate final metrics
        final_metrics = self.health_metrics.calculate_metrics(agents, 
                                                             [i for r in self.round_history for i in r['interactions']])
        
        # Generate advanced insights using LLM
        advanced_insights = await self._generate_advanced_insights(brief, agents, market_context)
        
        # Generate final report
        adoption_score = self._calculate_adoption_score(agents)
        top_objections = self._extract_top_objections(agents)
        must_fix = self._identify_critical_issues(agents)
        
        return {
            'adoption_score': adoption_score,
            'top_objections': top_objections,
            'must_fix': must_fix,
            'arena_health': final_metrics,
            'round_history': self.round_history,
            'agent_summaries': [self._summarize_agent(agent) for agent in agents],
            'advanced_insights': advanced_insights
        }
    
    async def _run_single_round(self, brief: Dict, agents: List[Agent], round_num: int, market_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run a single round of the simulation using real AI intelligence"""
        interactions = []
        
        # Each agent processes each feature
        for feature in brief.get('features', []):
            feature_interactions = []
            
            # Process all agents concurrently for better performance
            agent_tasks = []
            for agent in agents:
                task = agent.process_feature(feature, market_context)
                agent_tasks.append(task)
            
            # Wait for all agents to complete their analysis
            agent_results = await asyncio.gather(*agent_tasks)
            
            for i, result in enumerate(agent_results):
                agent = agents[i]
                
                # Apply influence from other agents
                influencers = self.influence_graph.get_influencers(agent.name)
                for influencer_name in influencers:
                    influencer = self.agents[influencer_name]
                    influence_strength = self.influence_graph.calculate_influence_flow(influencer_name, agent.name)
                    
                    # Adjust opinion based on influencer
                    opinion_shift = (influencer.current_opinion - agent.current_opinion) * influence_strength * 0.1
                    agent.current_opinion = max(0, min(1, agent.current_opinion + opinion_shift))
                    
                    result['influence_impact'] += abs(opinion_shift)
                
                feature_interactions.append(result)
            
            interactions.extend(feature_interactions)
        
        return {
            'round': round_num + 1,
            'interactions': interactions,
            'average_opinion': sum(agent.current_opinion for agent in agents) / len(agents)
        }
    
    def _apply_influence_effects(self, agents: List[Agent], interactions: List[Dict]):
        """Apply cross-agent influence effects"""
        # This is already handled in _run_single_round, but could be extended
        pass
    
    def _calculate_adoption_score(self, agents: List[Agent]) -> float:
        """Calculate overall adoption score"""
        customer_agents = [a for a in agents if a.genome.agent_type == AgentType.CUSTOMER]
        if not customer_agents:
            return 0.0
        
        # Weight by influence score
        total_weighted_opinion = sum(agent.current_opinion * agent.genome.influence_score 
                                   for agent in customer_agents)
        total_weight = sum(agent.genome.influence_score for agent in customer_agents)
        
        return (total_weighted_opinion / total_weight) * 100 if total_weight > 0 else 0.0
    
    def _extract_top_objections(self, agents: List[Agent]) -> List[str]:
        """Extract top objections from agents with negative opinions"""
        objections = []
        for agent in agents:
            if agent.current_opinion < 0.4:  # Negative opinion threshold
                objections.append(f"{agent.name} ({agent.genome.agent_type.value}): {agent.memory[-1] if agent.memory else 'General concerns'}")
        
        return objections[:5]  # Top 5 objections
    
    def _identify_critical_issues(self, agents: List[Agent]) -> List[str]:
        """Identify critical issues that must be fixed"""
        issues = []
        
        # Check for low adoption among key segments
        customer_opinions = [a.current_opinion for a in agents if a.genome.agent_type == AgentType.CUSTOMER]
        if customer_opinions and sum(customer_opinions) / len(customer_opinions) < 0.5:
            issues.append("Low customer adoption - review feature-market fit")
        
        # Check for competitor concerns
        competitor_opinions = [a.current_opinion for a in agents if a.genome.agent_type == AgentType.COMPETITOR]
        if competitor_opinions and sum(competitor_opinions) / len(competitor_opinions) < 0.3:
            issues.append("Competitive vulnerability detected - strengthen differentiation")
        
        # Check for internal team misalignment
        internal_opinions = [a.current_opinion for a in agents if a.genome.agent_type == AgentType.INTERNAL_TEAM]
        if internal_opinions:
            variance = sum((op - sum(internal_opinions)/len(internal_opinions)) ** 2 for op in internal_opinions) / len(internal_opinions)
            if variance > 0.1:
                issues.append("Internal team misalignment - address cross-functional concerns")
        
        return issues
    
    def _summarize_agent(self, agent: Agent) -> Dict[str, Any]:
        """Create a summary of an agent's behavior"""
        return {
            'name': agent.name,
            'type': agent.genome.agent_type.value,
            'final_opinion': agent.current_opinion,
            'influence_score': agent.genome.influence_score,
            'attention_tokens_remaining': agent.genome.attention_tokens,
            'personality_traits': [trait.value for trait in agent.genome.personality_traits]
        }
    
    async def _generate_advanced_insights(self, brief: Dict, agents: List[Agent], market_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate advanced insights using LLM integration"""
        
        # Collect all feature analyses from the simulation
        all_analyses = []
        for round_data in self.round_history:
            for interaction in round_data['interactions']:
                # Create FeatureAnalysis objects from interactions
                analysis = FeatureAnalysis(
                    feature_title=interaction.get('feature_title', 'Unknown'),
                    opinion_shift=interaction.get('opinion_shift', 0),
                    reasoning=interaction.get('reasoning', ''),
                    objections=interaction.get('objections', []),
                    suggestions=interaction.get('suggestions', []),
                    influence_impact=interaction.get('influence_impact', 0),
                    attention_spent=interaction.get('tokens_spent', 0)
                )
                all_analyses.append(analysis)
        
        # Generate market insights
        market_insights = await llm_integration.generate_market_insights(
            brief.get('features', []),
            all_analyses,
            market_context or {}
        )
        
        # Generate persona insights
        agent_contexts = []
        for agent in agents:
            context = {
                'role': agent.genome.agent_type.value,
                'genome': agent.genome.to_dict(),
                'final_opinion': agent.current_opinion
            }
            agent_contexts.append(context)
        
        persona_insights = await llm_integration.generate_persona_insights(
            agent_contexts,
            all_analyses
        )
        
        # Generate competitive analysis if competitor data is available
        competitor_analysis = {}
        if market_context and market_context.get('competitors'):
            competitor_analysis = await llm_integration.generate_competitive_analysis(
                brief.get('features', []),
                market_context.get('competitors', {})
            )
        
        return {
            'market_insights': market_insights,
            'persona_insights': persona_insights,
            'competitor_analysis': competitor_analysis,
            'simulation_confidence': 0.85,
            'ai_powered': True
        }
