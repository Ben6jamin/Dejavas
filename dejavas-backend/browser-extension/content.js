// Dejavas Browser Extension - Content Script
// Provides real-time market intelligence on web pages

class DejavasAnalyzer {
    constructor() {
        this.apiBase = 'http://localhost:8000'; // Change to production URL
        this.analysisResults = null;
        this.isAnalyzing = false;
        this.init();
    }

    async init() {
        // Wait for page to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        // Add floating analysis button
        this.addFloatingButton();
        
        // Listen for text selection
        document.addEventListener('mouseup', (e) => this.handleTextSelection(e));
        
        // Auto-analyze product pages
        if (this.isProductPage()) {
            this.autoAnalyze();
        }
    }

    addFloatingButton() {
        const button = document.createElement('div');
        button.id = 'dejavas-floating-button';
        button.innerHTML = '🧠';
        button.title = 'Analyze with Dejavas';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.2s;
        `;
        
        button.addEventListener('click', () => this.analyzeCurrentPage());
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.1)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });
        
        document.body.appendChild(button);
    }

    async analyzeCurrentPage() {
        if (this.isAnalyzing) return;
        
        this.isAnalyzing = true;
        this.updateFloatingButton('⏳');
        
        try {
            const response = await fetch(`${this.apiBase}/extension/analyze-page`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: window.location.href })
            });
            
            const result = await response.json();
            this.analysisResults = result;
            this.showAnalysisResults(result);
            
        } catch (error) {
            console.error('Dejavas analysis failed:', error);
            this.showError('Analysis failed. Please try again.');
        } finally {
            this.isAnalyzing = false;
            this.updateFloatingButton('🧠');
        }
    }

    async analyzeSelectedText(text) {
        if (!text || text.trim().length < 10) return;
        
        try {
            const response = await fetch(`${this.apiBase}/extension/analyze-text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text.trim() })
            });
            
            const result = await response.json();
            this.showQuickAnalysis(result, text);
            
        } catch (error) {
            console.error('Dejavas text analysis failed:', error);
        }
    }

    handleTextSelection(event) {
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();
        
        if (selectedText.length > 10) {
            // Show quick analyze button near selection
            this.showQuickAnalyzeButton(event.pageX, event.pageY, selectedText);
        }
    }

    showQuickAnalyzeButton(x, y, text) {
        // Remove existing quick analyze button
        const existing = document.getElementById('dejavas-quick-analyze');
        if (existing) existing.remove();
        
        const button = document.createElement('div');
        button.id = 'dejavas-quick-analyze';
        button.innerHTML = '🧠 Analyze';
        button.style.cssText = `
            position: absolute;
            left: ${x}px;
            top: ${y - 40}px;
            background: #667eea;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            z-index: 10001;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        `;
        
        button.addEventListener('click', () => {
            this.analyzeSelectedText(text);
            button.remove();
        });
        
        document.body.appendChild(button);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (button.parentNode) button.remove();
        }, 3000);
    }

    showAnalysisResults(result) {
        const modal = this.createModal();
        
        const scoreColor = this.getScoreColor(result.adoption_score);
        const scoreEmoji = this.getScoreEmoji(result.adoption_score);
        
        modal.innerHTML = `
            <div class="dejavas-modal-content">
                <div class="dejavas-header">
                    <h2>${scoreEmoji} Dejavas Analysis Results</h2>
                    <button class="dejavas-close">&times;</button>
                </div>
                
                <div class="dejavas-score-section">
                    <div class="dejavas-score ${scoreColor}">
                        <div class="score-number">${result.adoption_score.toFixed(1)}%</div>
                        <div class="score-label">Adoption Score</div>
                    </div>
                </div>
                
                <div class="dejavas-insights">
                    <h3>Quick Insights</h3>
                    <ul>
                        ${result.visual_indicators.quick_insights.map(insight => 
                            `<li>${insight}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                ${result.top_objections.length > 0 ? `
                    <div class="dejavas-objections">
                        <h3>Top Objections</h3>
                        <ul>
                            ${result.top_objections.map(obj => 
                                `<li>${obj}</li>`
                            ).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${result.must_fix.length > 0 ? `
                    <div class="dejavas-fixes">
                        <h3>Must Fix</h3>
                        <ul>
                            ${result.must_fix.map(fix => 
                                `<li>${fix}</li>`
                            ).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="dejavas-arena-health">
                    <h3>Arena Health</h3>
                    <div class="health-metrics">
                        <div class="metric">
                            <span class="metric-label">Polarization:</span>
                            <span class="metric-value">${(result.arena_health.polarization_score * 100).toFixed(1)}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Advocate Ratio:</span>
                            <span class="metric-value">${result.arena_health.advocate_to_saboteur_ratio.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.addModalStyles();
        document.body.appendChild(modal);
        
        // Close modal functionality
        modal.querySelector('.dejavas-close').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }

    showQuickAnalysis(result, originalText) {
        const tooltip = document.createElement('div');
        tooltip.className = 'dejavas-quick-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-header">
                <span class="score ${this.getScoreColor(result.adoption_score)}">
                    ${result.adoption_score.toFixed(0)}%
                </span>
                <span class="close">&times;</span>
            </div>
            <div class="tooltip-content">
                <p><strong>Adoption Score:</strong> ${result.adoption_score.toFixed(1)}%</p>
                ${result.top_objections.length > 0 ? 
                    `<p><strong>Top Issue:</strong> ${result.top_objections[0]}</p>` : ''
                }
            </div>
        `;
        
        // Position tooltip near selected text
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        tooltip.style.cssText = `
            position: absolute;
            left: ${rect.left + window.scrollX}px;
            top: ${rect.bottom + window.scrollY + 10}px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10002;
            max-width: 300px;
            font-size: 14px;
        `;
        
        document.body.appendChild(tooltip);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (tooltip.parentNode) tooltip.remove();
        }, 5000);
        
        // Close button
        tooltip.querySelector('.close').addEventListener('click', () => {
            tooltip.remove();
        });
    }

    createModal() {
        const modal = document.createElement('div');
        modal.className = 'dejavas-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10003;
        `;
        return modal;
    }

    addModalStyles() {
        if (document.getElementById('dejavas-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'dejavas-styles';
        styles.textContent = `
            .dejavas-modal-content {
                background: white;
                border-radius: 12px;
                padding: 24px;
                max-width: 500px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            }
            
            .dejavas-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            
            .dejavas-header h2 {
                margin: 0;
                color: #333;
            }
            
            .dejavas-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #666;
            }
            
            .dejavas-score-section {
                text-align: center;
                margin-bottom: 24px;
            }
            
            .dejavas-score {
                display: inline-block;
                padding: 20px;
                border-radius: 50%;
                width: 100px;
                height: 100px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            }
            
            .dejavas-score.green { background: #10b981; }
            .dejavas-score.yellow { background: #f59e0b; }
            .dejavas-score.red { background: #ef4444; }
            
            .score-number {
                font-size: 24px;
                line-height: 1;
            }
            
            .score-label {
                font-size: 12px;
                margin-top: 4px;
            }
            
            .dejavas-insights, .dejavas-objections, .dejavas-fixes, .dejavas-arena-health {
                margin-bottom: 20px;
            }
            
            .dejavas-insights h3, .dejavas-objections h3, .dejavas-fixes h3, .dejavas-arena-health h3 {
                margin: 0 0 12px 0;
                color: #333;
                font-size: 16px;
            }
            
            .dejavas-insights ul, .dejavas-objections ul, .dejavas-fixes ul {
                margin: 0;
                padding-left: 20px;
            }
            
            .dejavas-insights li, .dejavas-objections li, .dejavas-fixes li {
                margin-bottom: 8px;
                color: #555;
            }
            
            .health-metrics {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            
            .metric {
                display: flex;
                justify-content: space-between;
                padding: 8px 12px;
                background: #f8f9fa;
                border-radius: 6px;
            }
            
            .metric-label {
                font-weight: 500;
                color: #666;
            }
            
            .metric-value {
                font-weight: bold;
                color: #333;
            }
        `;
        
        document.head.appendChild(styles);
    }

    updateFloatingButton(text) {
        const button = document.getElementById('dejavas-floating-button');
        if (button) {
            button.innerHTML = text;
        }
    }

    getScoreColor(score) {
        if (score >= 70) return 'green';
        if (score >= 50) return 'yellow';
        return 'red';
    }

    getScoreEmoji(score) {
        if (score >= 70) return '🚀';
        if (score >= 50) return '⚠️';
        return '🔴';
    }

    isProductPage() {
        const url = window.location.href.toLowerCase();
        return url.includes('product') || 
               url.includes('amazon.com') || 
               url.includes('shopify.com') ||
               url.includes('pricing') ||
               url.includes('features');
    }

    async autoAnalyze() {
        // Auto-analyze product pages after a delay
        setTimeout(() => {
            if (!this.analysisResults) {
                this.analyzeCurrentPage();
            }
        }, 3000);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #ef4444;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            z-index: 10004;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            if (errorDiv.parentNode) errorDiv.remove();
        }, 3000);
    }
}

// Initialize Dejavas analyzer
new DejavasAnalyzer();
