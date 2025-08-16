"""
Advanced Feature Tests for Dejavas

Tests the revolutionary new features including market sentiment analysis,
predictive analytics, competitive intelligence, and more.
"""

import os
import sys
import pytest
import asyncio
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app
from integrations import IntegrationManager, ScannedContent, ContentType

client = TestClient(app)

class TestAdvancedFeatures:
    """Test suite for advanced Dejavas features"""
    
    def setup_method(self):
        """Setup test environment"""
        self.client = TestClient(app)
        self.test_url = "https://example.com/product"
        self.test_text = "AI-powered automation tool with cloud integration"
    
    def test_market_sentiment_analysis(self):
        """Test real-time market sentiment analysis"""
        response = self.client.post("/market-sentiment/", json={
            "text": self.test_text
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "sentiment_score" in data
        assert "market_mood" in data
        assert "trending_topics" in data
        assert "social_buzz" in data
        assert "influencer_sentiment" in data
        assert "confidence_level" in data
        assert data["ai_powered"] is True
        assert data["real_time"] is True
        
        # Validate sentiment score range
        assert -1.0 <= data["sentiment_score"] <= 1.0
        
        # Validate market mood
        assert data["market_mood"] in ["bullish", "bearish", "neutral"]
        
        # Validate trending topics
        assert isinstance(data["trending_topics"], list)
        
        # Validate social buzz metrics
        assert "twitter_mentions" in data["social_buzz"]
        assert "linkedin_engagement" in data["social_buzz"]
        assert "reddit_discussions" in data["social_buzz"]
        assert "news_coverage" in data["social_buzz"]
    
    def test_predictive_analytics(self):
        """Test AI-powered predictive analytics"""
        response = self.client.post("/predictive-analytics/", json={
            "text": self.test_text
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "adoption_prediction" in data
        assert "market_timing" in data
        assert "risk_assessment" in data
        assert "opportunity_score" in data
        assert "competitive_threats" in data
        assert "success_probability" in data
        assert data["ai_powered"] is True
        assert data["prediction_horizon"] == "6-12 months"
        
        # Validate adoption prediction range
        assert 5.0 <= data["adoption_prediction"] <= 95.0
        
        # Validate market timing
        assert data["market_timing"] in ["immediate", "3-6 months", "6-12 months", "12+ months"]
        
        # Validate risk assessment structure
        risk_assessment = data["risk_assessment"]
        assert "level" in risk_assessment
        assert "factors" in risk_assessment
        assert risk_assessment["level"] in ["low", "medium", "high"]
        
        # Validate opportunity score range
        assert 0.0 <= data["opportunity_score"] <= 1.0
        
        # Validate success probability range
        assert 0.05 <= data["success_probability"] <= 0.95
    
    def test_competitive_intelligence(self):
        """Test AI-powered competitive intelligence"""
        response = self.client.post("/competitive-intelligence/", json={
            "text": self.test_text
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "competitive_landscape" in data
        assert "market_positioning" in data
        assert "differentiation_opportunities" in data
        assert "threat_analysis" in data
        assert "competitive_advantages" in data
        assert "market_gaps" in data
        assert data["ai_powered"] is True
        assert data["analysis_depth"] == "comprehensive"
        
        # Validate competitive landscape
        landscape = data["competitive_landscape"]
        assert "market_leader" in landscape
        assert "market_share" in landscape
        assert "competitive_intensity" in landscape
        assert "barriers_to_entry" in landscape
        
        # Validate market positioning
        positioning = data["market_positioning"]
        assert "strength" in positioning
        assert "differentiation" in positioning
        assert "target_segments" in positioning
        assert "geographic_focus" in positioning
        
        # Validate threat analysis
        threats = data["threat_analysis"]
        assert "direct_competitors" in threats
        assert "indirect_competitors" in threats
        assert "substitute_products" in threats
        assert "new_entrants" in threats
    
    def test_voice_analysis(self):
        """Test voice-enabled market analysis"""
        response = self.client.post("/voice-analysis/", json={
            "audio_data": "AI automation tool analysis"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["voice_analysis"] is True
        assert "transcribed_text" in data
        assert "analysis_results" in data
        assert data["ai_powered"] is True
        assert data["voice_enabled"] is True
    
    def test_multilingual_analysis(self):
        """Test multi-language market intelligence"""
        response = self.client.post("/multilingual-analysis/", json={
            "text": "Herramienta de automatización con IA"
        }, params={"language": "auto"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert "original_language" in data
        assert "translated_to" in data
        assert "analysis_results" in data
        assert data["multilingual_support"] is True
        assert data["ai_powered"] is True
    
    def test_market_alerts(self):
        """Test real-time market alerts setup"""
        alert_config = {
            "type": "competitive",
            "targets": ["competitor1.com", "competitor2.com"],
            "channels": ["email", "slack"]
        }
        
        response = self.client.post("/market-alerts/", json=alert_config)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "alert_id" in data
        assert data["status"] == "active"
        assert data["alert_type"] == "competitive"
        assert "monitoring_targets" in data
        assert "notification_channels" in data
        assert data["real_time"] is True
        assert data["ai_powered"] is True
    
    def test_market_research_assistant(self):
        """Test AI-powered market research assistant"""
        response = self.client.post("/market-research-assistant/", 
                                  params={"query": "AI automation tools", "research_depth": "comprehensive"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["research_query"] == "AI automation tools"
        assert data["research_depth"] == "comprehensive"
        assert "market_overview" in data
        assert "key_findings" in data
        assert "trend_analysis" in data
        assert "competitive_insights" in data
        assert "recommendations" in data
        assert data["ai_powered"] is True
        assert data["research_quality"] == "expert"
    
    def test_pricing_intelligence(self):
        """Test AI-powered pricing intelligence"""
        response = self.client.post("/pricing-intelligence/", json={
            "text": "Premium AI tool with enterprise pricing"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "pricing_analysis" in data
        assert "price_optimization" in data
        assert "competitive_pricing" in data
        assert "value_proposition" in data
        assert "pricing_recommendations" in data
        assert data["ai_powered"] is True
        assert data["pricing_intelligence"] == "advanced"
        
        # Validate pricing analysis structure
        pricing_analysis = data["pricing_analysis"]
        assert "current_pricing_model" in pricing_analysis
        assert "price_positioning" in pricing_analysis
        assert "value_perception" in pricing_analysis
        assert "competitive_pricing" in pricing_analysis
        
        # Validate price optimization structure
        price_optimization = data["price_optimization"]
        assert "optimal_price_range" in price_optimization
        assert "pricing_tiers" in price_optimization
        assert "discount_strategy" in price_optimization
        assert "upsell_opportunities" in price_optimization
    
    def test_integration_manager_advanced_features(self):
        """Test IntegrationManager advanced features directly"""
        manager = IntegrationManager()
        
        # Test market sentiment analysis
        content = ScannedContent(
            content_type=ContentType.MARKETING_COPY,
            raw_text=self.test_text
        )
        
        sentiment_data = asyncio.run(manager.analyze_market_sentiment(content))
        assert "overall_sentiment" in sentiment_data
        assert "market_mood" in sentiment_data
        assert "trending_topics" in sentiment_data
        
        # Test predictions generation
        brief = {"features": [{"title": "AI Automation", "description": "Intelligent process automation"}]}
        predictions = asyncio.run(manager.generate_predictions(brief))
        assert "adoption_prediction" in predictions
        assert "market_timing" in predictions
        assert "risk_assessment" in predictions
        
        # Test competitive intelligence
        competitive_data = asyncio.run(manager.generate_competitive_intelligence(content))
        assert "competitive_landscape" in competitive_data
        assert "market_positioning" in competitive_data
        assert "differentiation_opportunities" in competitive_data
    
    def test_error_handling(self):
        """Test error handling for advanced features"""
        # Test with invalid input
        response = self.client.post("/market-sentiment/", json={})
        assert response.status_code == 400
        
        # Test with invalid URL
        response = self.client.post("/predictive-analytics/", json={"url": "invalid-url"})
        assert response.status_code == 500  # Should handle gracefully
        
        # Test with empty text
        response = self.client.post("/competitive-intelligence/", json={"text": ""})
        assert response.status_code == 400
    
    def test_performance_metrics(self):
        """Test that advanced features return within reasonable time"""
        import time
        
        start_time = time.time()
        response = self.client.post("/market-sentiment/", json={"text": self.test_text})
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds
        
        start_time = time.time()
        response = self.client.post("/predictive-analytics/", json={"text": self.test_text})
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 3.0  # Should complete within 3 seconds

if __name__ == "__main__":
    pytest.main([__file__])
