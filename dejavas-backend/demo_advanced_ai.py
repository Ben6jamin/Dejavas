#!/usr/bin/env python3
"""
Dejavas Advanced AI Demo

This script demonstrates the enhanced AI capabilities of Dejavas,
including real LLM integration, advanced agent behavior, and
sophisticated market intelligence.
"""

import asyncio
import json
from typing import Dict, Any

from agents import AgentFactory, AgentType
from simulation import AdvancedSimulator, NetworkTopology
from llm_integration import llm_integration, AgentContext, AgentRole

async def demo_advanced_agents():
    """Demo the advanced AI agent capabilities"""
    print("🧠 Dejavas Advanced AI Demo")
    print("=" * 50)
    
    # Create a sample product brief
    brief = {
        "product_name": "AI-Powered Marketing Assistant",
        "features": [
            {
                "title": "Real-time Market Analysis",
                "description": "Analyze any product or marketing content instantly using AI agents that think like real customers, competitors, and influencers."
            },
            {
                "title": "Browser Extension Integration",
                "description": "Get instant insights on any webpage, just like Grammarly but for market intelligence."
            },
            {
                "title": "Competitive Intelligence",
                "description": "Understand how competitors would react to your features and identify market opportunities."
            }
        ]
    }
    
    # Create market context
    market_context = {
        "category": "SaaS Marketing Tools",
        "target_market": "Product Marketers, Growth Teams, Founders",
        "competitive_landscape": "Highly competitive with established players",
        "trends": ["AI-powered tools", "Real-time analytics", "Browser extensions"],
        "competitors": {
            "direct": ["Hotjar", "Mixpanel", "Amplitude"],
            "indirect": ["Grammarly", "Hemingway", "Copy.ai"]
        }
    }
    
    print("\n📋 Product Brief:")
    print(f"Product: {brief['product_name']}")
    for i, feature in enumerate(brief['features'], 1):
        print(f"  {i}. {feature['title']}")
        print(f"     {feature['description'][:80]}...")
    
    print(f"\n🏢 Market Context:")
    print(f"Category: {market_context['category']}")
    print(f"Target: {market_context['target_market']}")
    print(f"Competitors: {len(market_context['competitors']['direct'])} direct, {len(market_context['competitors']['indirect'])} indirect")
    
    # Create advanced simulator
    simulator = AdvancedSimulator(NetworkTopology.REAL_FOLLOWER)
    
    # Configure agents
    config = {
        'customer_percentage': 60,
        'competitor_percentage': 20,
        'influencer_percentage': 10,
        'internal_team_percentage': 10
    }
    
    print(f"\n🤖 Running Advanced AI Simulation...")
    print("This will use real LLM integration for intelligent agent behavior.")
    
    # Run simulation
    result = await simulator.run_simulation(brief, config, num_rounds=3, market_context=market_context)
    
    # Display results
    print(f"\n📊 Simulation Results:")
    print(f"Adoption Score: {result['adoption_score']:.1f}%")
    print(f"AI Powered: {result.get('advanced_insights', {}).get('ai_powered', False)}")
    
    print(f"\n🔍 Top Objections:")
    for i, objection in enumerate(result['top_objections'][:3], 1):
        print(f"  {i}. {objection}")
    
    print(f"\n🔧 Must Fix:")
    for i, fix in enumerate(result['must_fix'][:3], 1):
        print(f"  {i}. {fix}")
    
    # Display advanced insights
    if 'advanced_insights' in result:
        insights = result['advanced_insights']
        
        print(f"\n🧠 Advanced AI Insights:")
        print(f"Simulation Confidence: {insights.get('simulation_confidence', 0):.1%}")
        
        if 'market_insights' in insights:
            market = insights['market_insights']
            print(f"\n📈 Market Insights:")
            print(f"Adoption Score: {market.get('adoption_score', 0):.1f}%")
            print(f"Confidence: {market.get('confidence_score', 0):.1%}")
            
            print(f"\nTop Objections:")
            for obj in market.get('top_objections', [])[:2]:
                print(f"  • {obj}")
            
            print(f"\nTop Suggestions:")
            for sug in market.get('top_suggestions', [])[:2]:
                print(f"  • {sug}")
        
        if 'persona_insights' in insights:
            persona = insights['persona_insights']
            print(f"\n👥 Persona Insights:")
            receptiveness = persona.get('persona_receptiveness', {})
            for persona_type, score in receptiveness.items():
                print(f"  {persona_type}: {score:+.3f}")
    
    # Display agent summaries
    print(f"\n🤖 Agent Behavior Summary:")
    for agent in result['agent_summaries'][:5]:  # Show first 5 agents
        print(f"  {agent['name']} ({agent['type']}): {agent['final_opinion']:.2f} opinion, {agent['influence_score']:.2f} influence")
    
    print(f"\n🎯 Arena Health Metrics:")
    health = result['arena_health']
    print(f"  Polarization: {health['polarization_score']:.1%}")
    print(f"  Advocate Ratio: {health['advocate_to_saboteur_ratio']:.2f}")
    print(f"  Viral Path Length: {health['viral_path_length']:.2f}")
    print(f"  Engagement Density: {health['engagement_density']:.2f}")
    
    return result

async def demo_individual_agent_analysis():
    """Demo individual agent analysis with LLM"""
    print(f"\n🔬 Individual Agent Analysis Demo")
    print("=" * 50)
    
    # Create sample agents
    customer_agent = AgentFactory.create_customer_agent()
    competitor_agent = AgentFactory.create_competitor_agent()
    influencer_agent = AgentFactory.create_influencer_agent()
    
    # Sample feature
    feature = {
        "title": "AI-Powered Content Analysis",
        "description": "Automatically analyze any marketing content and get instant feedback on messaging, tone, and effectiveness from AI agents that think like real customers."
    }
    
    market_context = {
        "category": "Marketing Technology",
        "target_market": "Marketing Professionals",
        "trends": ["AI", "Automation", "Content Marketing"]
    }
    
    print(f"Feature: {feature['title']}")
    print(f"Description: {feature['description']}")
    
    # Analyze with each agent type
    agents = [customer_agent, competitor_agent, influencer_agent]
    agent_types = ["Customer", "Competitor", "Influencer"]
    
    for agent, agent_type in zip(agents, agent_types):
        print(f"\n{agent_type} Agent Analysis:")
        print("-" * 30)
        
        result = await agent.process_feature(feature, market_context)
        
        print(f"Agent: {result['agent_name']}")
        print(f"Opinion: {result['opinion']:.2f}")
        print(f"Reasoning: {result['reasoning'][:100]}...")
        print(f"Objections: {len(result.get('objections', []))}")
        print(f"Suggestions: {len(result.get('suggestions', []))}")
        print(f"Influence Impact: {result['influence_impact']:.2f}")

async def demo_competitive_analysis():
    """Demo competitive analysis capabilities"""
    print(f"\n🏆 Competitive Analysis Demo")
    print("=" * 50)
    
    # Sample product features
    product_features = [
        {"title": "Real-time Market Analysis", "description": "Instant insights on any product"},
        {"title": "Browser Extension", "description": "Works everywhere like Grammarly"},
        {"title": "AI Agent Simulation", "description": "Realistic customer behavior modeling"}
    ]
    
    # Sample competitor data
    competitor_data = {
        "direct_competitors": [
            {
                "name": "Competitor A",
                "strengths": ["Established brand", "Large user base"],
                "weaknesses": ["Slow innovation", "High pricing"],
                "features": ["Basic analytics", "Manual reporting"]
            },
            {
                "name": "Competitor B", 
                "strengths": ["Modern UI", "Good pricing"],
                "weaknesses": ["Limited features", "Poor support"],
                "features": ["Simple dashboard", "Basic insights"]
            }
        ],
        "market_position": "Emerging challenger",
        "pricing_strategy": "Premium with freemium tier"
    }
    
    print("Analyzing competitive positioning...")
    
    # Generate competitive analysis
    analysis = await llm_integration.generate_competitive_analysis(
        product_features, competitor_data
    )
    
    print(f"Competitive Analysis Results:")
    print(f"Threat Level: {analysis.get('threat_level', 'Unknown')}")
    print(f"Opportunity Score: {analysis.get('opportunity_score', 0):.1%}")
    
    if 'competitive_analysis' in analysis:
        print(f"\nAnalysis: {analysis['competitive_analysis'][:200]}...")

async def main():
    """Run all demos"""
    print("🚀 Dejavas Advanced AI Capabilities Demo")
    print("=" * 60)
    
    # Check LLM availability
    if llm_integration.llm_available:
        print("✅ LLM Integration: Available (Real AI Intelligence)")
    else:
        print("⚠️  LLM Integration: Not available (Using mock responses)")
        print("   Set OPENAI_API_KEY environment variable for real AI analysis")
    
    # Run demos
    await demo_advanced_agents()
    await demo_individual_agent_analysis()
    await demo_competitive_analysis()
    
    print(f"\n🎉 Demo Complete!")
    print("=" * 60)
    print("This demonstrates the advanced AI capabilities of Dejavas:")
    print("• Real LLM-powered agent intelligence")
    print("• Sophisticated market analysis")
    print("• Competitive intelligence")
    print("• Persona-specific insights")
    print("• Ubiquitous integration ready")

if __name__ == "__main__":
    asyncio.run(main())
