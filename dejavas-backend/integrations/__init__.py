"""
Dejavas Ubiquitous Integration System

This module enables Dejavas to be integrated everywhere - like Grammarly.
It provides browser extensions, API integrations, and real-time scanning
capabilities for seamless market intelligence.
"""

from typing import Dict, List, Optional, Any, Union
import re
import json
import asyncio
from enum import Enum
from dataclasses import dataclass
import aiohttp
from urllib.parse import urlparse, parse_qs

class IntegrationType(Enum):
    BROWSER_EXTENSION = "browser_extension"
    API_WEBHOOK = "api_webhook"
    CHROME_EXTENSION = "chrome_extension"
    FIREFOX_EXTENSION = "firefox_extension"
    SHOPIFY_APP = "shopify_app"
    WORDPRESS_PLUGIN = "wordpress_plugin"
    SLACK_BOT = "slack_bot"
    DISCORD_BOT = "discord_bot"

class ContentType(Enum):
    PRODUCT_PAGE = "product_page"
    MARKETING_COPY = "marketing_copy"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    LANDING_PAGE = "landing_page"
    COMPETITOR_ANALYSIS = "competitor_analysis"

@dataclass
class ScannedContent:
    """Represents content that has been scanned by Dejavas"""
    content_type: ContentType
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    features: List[str] = None
    target_audience: Optional[str] = None
    competitive_advantages: List[str] = None
    raw_text: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []
        if self.competitive_advantages is None:
            self.competitive_advantages = []
        if self.metadata is None:
            self.metadata = {}

class ContentScanner:
    """Scans and extracts structured data from various content types"""
    
    def __init__(self):
        self.product_patterns = {
            'amazon': r'amazon\.com',
            'shopify': r'\.myshopify\.com',
            'ecommerce': r'(product|item|buy|purchase)',
            'saas': r'(pricing|features|signup|trial)'
        }
        
    async def scan_url(self, url: str) -> ScannedContent:
        """Scan a URL and extract relevant content"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        return self._parse_html_content(html_content, url)
        except Exception as e:
            print(f"Error scanning URL {url}: {e}")
        
        return ScannedContent(content_type=ContentType.PRODUCT_PAGE, url=url)
    
    def _parse_html_content(self, html: str, url: str) -> ScannedContent:
        """Parse HTML content and extract structured data"""
        # Basic HTML parsing (in production, use BeautifulSoup)
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1) if title_match else None
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else None
        
        # Detect content type based on URL and content
        content_type = self._detect_content_type(url, html)
        
        # Extract features (basic pattern matching)
        features = self._extract_features(html)
        
        # Extract price information
        price = self._extract_price(html)
        
        return ScannedContent(
            content_type=content_type,
            url=url,
            title=title,
            description=description,
            price=price,
            features=features,
            raw_text=self._extract_text_content(html)
        )
    
    def _detect_content_type(self, url: str, html: str) -> ContentType:
        """Detect the type of content based on URL and HTML"""
        url_lower = url.lower()
        html_lower = html.lower()
        
        if any(pattern in url_lower for pattern in ['amazon.com', 'product', 'item']):
            return ContentType.PRODUCT_PAGE
        elif any(pattern in url_lower for pattern in ['pricing', 'features', 'signup']):
            return ContentType.MARKETING_COPY
        elif any(pattern in url_lower for pattern in ['facebook.com', 'twitter.com', 'instagram.com']):
            return ContentType.SOCIAL_MEDIA
        elif any(pattern in url_lower for pattern in ['mail', 'email']):
            return ContentType.EMAIL
        elif any(pattern in html_lower for pattern in ['landing page', 'hero section', 'cta']):
            return ContentType.LANDING_PAGE
        else:
            return ContentType.PRODUCT_PAGE
    
    def _extract_features(self, html: str) -> List[str]:
        """Extract feature lists from HTML content"""
        features = []
        
        # Look for common feature patterns
        feature_patterns = [
            r'<li[^>]*>([^<]*feature[^<]*)</li>',
            r'<li[^>]*>([^<]*benefit[^<]*)</li>',
            r'<li[^>]*>([^<]*include[^<]*)</li>',
            r'<li[^>]*>([^<]*comes with[^<]*)</li>'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            features.extend(matches)
        
        return list(set(features))[:10]  # Limit to 10 unique features
    
    def _extract_price(self, html: str) -> Optional[float]:
        """Extract price information from HTML"""
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)',
            r'price[^>]*>.*?\$(\d+(?:\.\d{2})?)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def _extract_text_content(self, html: str) -> str:
        """Extract clean text content from HTML"""
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text[:2000]  # Limit text length

class IntegrationManager:
    """Manages different integration types and their configurations"""
    
    def __init__(self):
        self.scanner = ContentScanner()
        self.active_integrations = {}
        self.webhook_endpoints = {}
        
    def register_integration(self, integration_type: IntegrationType, config: Dict[str, Any]):
        """Register a new integration"""
        self.active_integrations[integration_type] = config
        
        if integration_type in [IntegrationType.API_WEBHOOK, IntegrationType.SLACK_BOT, IntegrationType.DISCORD_BOT]:
            self.webhook_endpoints[integration_type] = config.get('webhook_url')
    
    async def process_content(self, content: Union[str, ScannedContent], integration_type: IntegrationType) -> Dict[str, Any]:
        """Process content through the appropriate integration"""
        if isinstance(content, str):
            # If content is a URL, scan it
            if content.startswith(('http://', 'https://')):
                scanned_content = await self.scanner.scan_url(content)
            else:
                # Treat as raw text
                scanned_content = ScannedContent(
                    content_type=ContentType.MARKETING_COPY,
                    raw_text=content
                )
        else:
            scanned_content = content
        
        # Generate simulation brief from scanned content
        brief = self._create_brief_from_content(scanned_content)
        
        # Run simulation
        from ..simulation import AdvancedSimulator, NetworkTopology
        simulator = AdvancedSimulator(NetworkTopology.LOOSE_NETWORK)
        
        # Default agent configuration
        config = {
            'customer_percentage': 60,
            'competitor_percentage': 20,
            'influencer_percentage': 10,
            'internal_team_percentage': 10
        }
        
        simulation_result = simulator.run_simulation(brief, config, num_rounds=3)
        
        # Format response based on integration type
        return self._format_response(simulation_result, integration_type, scanned_content)
    
    def _create_brief_from_content(self, content: ScannedContent) -> Dict[str, Any]:
        """Create a simulation brief from scanned content"""
        features = []
        
        # Extract features from content
        if content.features:
            for feature in content.features:
                features.append({
                    'title': feature[:50],  # Truncate long titles
                    'description': feature
                })
        elif content.raw_text:
            # Extract potential features from raw text
            sentences = content.raw_text.split('.')
            for sentence in sentences[:5]:  # Take first 5 sentences as features
                if len(sentence.strip()) > 10:
                    features.append({
                        'title': sentence[:50],
                        'description': sentence
                    })
        
        # If no features found, create a generic one
        if not features:
            features.append({
                'title': content.title or 'Product Feature',
                'description': content.description or content.raw_text or 'Product offering'
            })
        
        return {
            'product_name': content.title or 'Scanned Product',
            'features': features,
            'metadata': {
                'content_type': content.content_type.value,
                'url': content.url,
                'price': content.price
            }
        }
    
    def _format_response(self, simulation_result: Dict[str, Any], integration_type: IntegrationType, content: ScannedContent) -> Dict[str, Any]:
        """Format simulation results for different integration types"""
        base_response = {
            'adoption_score': simulation_result['adoption_score'],
            'top_objections': simulation_result['top_objections'][:3],  # Top 3 objections
            'must_fix': simulation_result['must_fix'],
            'arena_health': simulation_result['arena_health'],
            'content_analyzed': {
                'type': content.content_type.value,
                'url': content.url,
                'title': content.title
            }
        }
        
        if integration_type == IntegrationType.BROWSER_EXTENSION:
            # Add visual indicators for browser extension
            base_response['visual_indicators'] = {
                'score_color': self._get_score_color(simulation_result['adoption_score']),
                'priority_issues': len(simulation_result['must_fix']),
                'quick_insights': self._generate_quick_insights(simulation_result)
            }
        
        elif integration_type in [IntegrationType.SLACK_BOT, IntegrationType.DISCORD_BOT]:
            # Format for chat platforms
            base_response['message'] = self._format_chat_message(simulation_result, content)
        
        return base_response
    
    def _get_score_color(self, score: float) -> str:
        """Get color indicator for adoption score"""
        if score >= 70:
            return 'green'
        elif score >= 50:
            return 'yellow'
        else:
            return 'red'
    
    def _generate_quick_insights(self, simulation_result: Dict[str, Any]) -> List[str]:
        """Generate quick insights for browser extension"""
        insights = []
        
        score = simulation_result['adoption_score']
        if score >= 70:
            insights.append("🚀 High adoption potential")
        elif score >= 50:
            insights.append("⚠️ Moderate adoption - needs refinement")
        else:
            insights.append("🔴 Low adoption - major changes needed")
        
        if simulation_result['must_fix']:
            insights.append(f"🔧 {len(simulation_result['must_fix'])} critical issues")
        
        health = simulation_result['arena_health']
        if health['polarization_score'] > 0.7:
            insights.append("⚡ High polarization - controversial features")
        
        return insights
    
    def _format_chat_message(self, simulation_result: Dict[str, Any], content: ScannedContent) -> str:
        """Format simulation results as a chat message"""
        score = simulation_result['adoption_score']
        emoji = "🚀" if score >= 70 else "⚠️" if score >= 50 else "🔴"
        
        message = f"{emoji} **Dejavas Analysis Results**\n\n"
        message += f"**Adoption Score:** {score:.1f}%\n\n"
        
        if simulation_result['top_objections']:
            message += "**Top Objections:**\n"
            for objection in simulation_result['top_objections'][:2]:
                message += f"• {objection}\n"
            message += "\n"
        
        if simulation_result['must_fix']:
            message += "**Must Fix:**\n"
            for issue in simulation_result['must_fix'][:2]:
                message += f"• {issue}\n"
        
        return message

class BrowserExtensionAPI:
    """API endpoints for browser extension integration"""
    
    def __init__(self, integration_manager: IntegrationManager):
        self.manager = integration_manager
    
    async def analyze_current_page(self, url: str) -> Dict[str, Any]:
        """Analyze the current page in browser extension"""
        return await self.manager.process_content(url, IntegrationType.BROWSER_EXTENSION)
    
    async def analyze_selected_text(self, text: str) -> Dict[str, Any]:
        """Analyze selected text in browser extension"""
        content = ScannedContent(
            content_type=ContentType.MARKETING_COPY,
            raw_text=text
        )
        return await self.manager.process_content(content, IntegrationType.BROWSER_EXTENSION)
    
    def get_extension_config(self) -> Dict[str, Any]:
        """Get configuration for browser extension"""
        return {
            'version': '1.0.0',
            'features': {
                'page_analysis': True,
                'text_selection': True,
                'real_time_feedback': True,
                'competitor_tracking': True
            },
            'settings': {
                'auto_scan': True,
                'notification_threshold': 50,
                'theme': 'light'
            }
        }
