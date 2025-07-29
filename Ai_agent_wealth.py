import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json
import logging
from dataclasses import dataclass
from enum import Enum
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskTolerance(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class AssetClass(Enum):
    STOCKS = "stocks"
    BONDS = "bonds"
    REAL_ESTATE = "real_estate"
    COMMODITIES = "commodities"
    CASH = "cash"
    ALTERNATIVES = "alternatives"

@dataclass
class ClientProfile:
    client_id: str
    name: str
    age: int
    risk_tolerance: RiskTolerance
    investment_goals: List[str]
    time_horizon: int  # years
    current_portfolio_value: float
    monthly_contribution: float
    liquid_cash_reserve: float
    annual_income: float
    debt_obligations: float

@dataclass
class Portfolio:
    client_id: str
    holdings: Dict[str, float]  # symbol -> value
    cash_position: float
    last_updated: datetime

@dataclass
class Investment:
    symbol: str
    name: str
    asset_class: AssetClass
    current_price: float
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    market_cap: Optional[float]
    risk_score: float  # 1-10 scale

class WealthManagementAgent:
    """
    AI Agent for Wealth Management Firm
    
    Capabilities:
    - Portfolio analysis and optimization
    - Risk assessment and management
    - Investment recommendations
    - Client profiling and goal tracking
    - Market analysis and reporting
    - Compliance monitoring
    """
    
    def __init__(self):
        self.clients: Dict[str, ClientProfile] = {}
        self.portfolios: Dict[str, Portfolio] = {}
        self.market_data_cache: Dict[str, Dict] = {}
        self.recommendations_history: List[Dict] = []
        
    def add_client(self, client: ClientProfile) -> bool:
        """Add a new client to the system."""
        try:
            self.clients[client.client_id] = client
            logger.info(f"Added client: {client.name} (ID: {client.client_id})")
            return True
        except Exception as e:
            logger.error(f"Error adding client: {e}")
            return False
    
    def get_client_profile(self, client_id: str) -> Optional[ClientProfile]:
        """Retrieve client profile by ID."""
        return self.clients.get(client_id)
    
    def update_portfolio(self, portfolio: Portfolio) -> bool:
        """Update or create client portfolio."""
        try:
            self.portfolios[portfolio.client_id] = portfolio
            logger.info(f"Updated portfolio for client: {portfolio.client_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating portfolio: {e}")
            return False
    
    def get_market_data(self, symbols: List[str], period: str = "1y") -> Dict[str, Dict]:
        """Fetch current market data for given symbols."""
        market_data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                info = ticker.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
                    
                    market_data[symbol] = {
                        'current_price': current_price,
                        'returns': returns.tolist(),
                        'volatility': volatility,
                        'pe_ratio': info.get('trailingPE'),
                        'dividend_yield': info.get('dividendYield'),
                        'market_cap': info.get('marketCap'),
                        'sector': info.get('sector'),
                        'beta': info.get('beta'),
                        'last_updated': datetime.now().isoformat()
                    }
                    
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                market_data[symbol] = None
        
        self.market_data_cache.update(market_data)
        return market_data
    
    def calculate_portfolio_metrics(self, client_id: str) -> Dict[str, float]:
        """Calculate key portfolio performance metrics."""
        portfolio = self.portfolios.get(client_id)
        if not portfolio:
            return {}
        
        symbols = list(portfolio.holdings.keys())
        if not symbols:
            return {'total_value': portfolio.cash_position}
        
        market_data = self.get_market_data(symbols)
        
        total_value = portfolio.cash_position
        weighted_returns = []
        weights = []
        
        for symbol, value in portfolio.holdings.items():
            if symbol in market_data and market_data[symbol]:
                total_value += value
                weight = value / (total_value if total_value > 0 else 1)
                weights.append(weight)
                
                returns = market_data[symbol]['returns']
                if returns:
                    avg_return = np.mean(returns)
                    weighted_returns.append(avg_return * weight)
        
        portfolio_return = sum(weighted_returns) if weighted_returns else 0
        
        # Calculate portfolio volatility (simplified)
        volatilities = []
        for symbol in symbols:
            if symbol in market_data and market_data[symbol]:
                volatilities.append(market_data[symbol]['volatility'])
        
        portfolio_volatility = np.mean(volatilities) if volatilities else 0
        
        # Sharpe ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        return {
            'total_value': total_value,
            'cash_percentage': (portfolio.cash_position / total_value) * 100 if total_value > 0 else 100,
            'expected_return': portfolio_return * 252,  # Annualized
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'last_calculated': datetime.now().isoformat()
        }
    
    def assess_risk_profile(self, client_id: str) -> Dict[str, Any]:
        """Assess client's risk profile and portfolio alignment."""
        client = self.clients.get(client_id)
        if not client:
            return {}
        
        portfolio_metrics = self.calculate_portfolio_metrics(client_id)
        
        # Risk score calculation based on multiple factors
        age_risk = max(0, (65 - client.age) / 65)  # Younger = higher risk capacity
        income_risk = min(1, client.annual_income / 100000)  # Higher income = higher risk capacity
        time_horizon_risk = min(1, client.time_horizon / 30)  # Longer horizon = higher risk capacity
        debt_ratio = client.debt_obligations / client.annual_income if client.annual_income > 0 else 0
        debt_risk = max(0, 1 - debt_ratio)  # Lower debt = higher risk capacity
        
        risk_capacity_score = (age_risk + income_risk + time_horizon_risk + debt_risk) / 4
        
        # Map risk tolerance to numeric values
        tolerance_mapping = {
            RiskTolerance.CONSERVATIVE: 0.3,
            RiskTolerance.MODERATE: 0.6,
            RiskTolerance.AGGRESSIVE: 0.9
        }
        
        risk_tolerance_score = tolerance_mapping.get(client.risk_tolerance, 0.5)
        
        # Portfolio risk alignment
        portfolio_volatility = portfolio_metrics.get('volatility', 0)
        risk_alignment = 1 - abs(risk_tolerance_score - min(1, portfolio_volatility))
        
        return {
            'risk_capacity_score': risk_capacity_score,
            'risk_tolerance_score': risk_tolerance_score,
            'portfolio_risk_level': portfolio_volatility,
            'risk_alignment_score': risk_alignment,
            'recommendations': self._generate_risk_recommendations(
                risk_capacity_score, risk_tolerance_score, portfolio_volatility
            )
        }
    
    def _generate_risk_recommendations(self, capacity: float, tolerance: float, current_risk: float) -> List[str]:
        """Generate risk-based recommendations."""
        recommendations = []
        
        if current_risk > tolerance + 0.2:
            recommendations.append("Consider reducing portfolio risk by increasing bond allocation")
        elif current_risk < tolerance - 0.2:
            recommendations.append("Portfolio may be too conservative for your risk tolerance")
        
        if capacity > tolerance:
            recommendations.append("You have capacity for higher risk investments given your profile")
        elif capacity < tolerance:
            recommendations.append("Consider reducing risk given your financial situation")
        
        return recommendations
    
    def generate_asset_allocation(self, client_id: str) -> Dict[AssetClass, float]:
        """Generate optimal asset allocation based on client profile."""
        client = self.clients.get(client_id)
        if not client:
            return {}
        
        # Base allocations by risk tolerance
        base_allocations = {
            RiskTolerance.CONSERVATIVE: {
                AssetClass.BONDS: 0.6,
                AssetClass.STOCKS: 0.25,
                AssetClass.CASH: 0.10,
                AssetClass.REAL_ESTATE: 0.05
            },
            RiskTolerance.MODERATE: {
                AssetClass.STOCKS: 0.50,
                AssetClass.BONDS: 0.30,
                AssetClass.REAL_ESTATE: 0.10,
                AssetClass.ALTERNATIVES: 0.05,
                AssetClass.CASH: 0.05
            },
            RiskTolerance.AGGRESSIVE: {
                AssetClass.STOCKS: 0.70,
                AssetClass.BONDS: 0.15,
                AssetClass.ALTERNATIVES: 0.10,
                AssetClass.REAL_ESTATE: 0.05
            }
        }
        
        allocation = base_allocations.get(client.risk_tolerance, base_allocations[RiskTolerance.MODERATE])
        
        # Adjust for age (rule of 100)
        age_bond_adjustment = (100 - client.age) / 100
        if AssetClass.BONDS in allocation and AssetClass.STOCKS in allocation:
            bond_target = max(0.1, min(0.8, age_bond_adjustment))
            current_bond = allocation[AssetClass.BONDS]
            adjustment = bond_target - current_bond
            
            allocation[AssetClass.BONDS] = bond_target
            allocation[AssetClass.STOCKS] = max(0.1, allocation[AssetClass.STOCKS] - adjustment)
        
        return allocation
    
    def recommend_investments(self, client_id: str, amount: float) -> List[Dict[str, Any]]:
        """Generate investment recommendations for a given amount."""
        client = self.clients.get(client_id)
        if not client:
            return []
        
        target_allocation = self.generate_asset_allocation(client_id)
        recommendations = []
        
        # Sample investment options by asset class
        investment_options = {
            AssetClass.STOCKS: [
                {'symbol': 'VTI', 'name': 'Total Stock Market ETF', 'expense_ratio': 0.03},
                {'symbol': 'VOO', 'name': 'S&P 500 ETF', 'expense_ratio': 0.03},
                {'symbol': 'VEA', 'name': 'Developed Markets ETF', 'expense_ratio': 0.05}
            ],
            AssetClass.BONDS: [
                {'symbol': 'BND', 'name': 'Total Bond Market ETF', 'expense_ratio': 0.05},
                {'symbol': 'VGIT', 'name': 'Intermediate Treasury ETF', 'expense_ratio': 0.05}
            ],
            AssetClass.REAL_ESTATE: [
                {'symbol': 'VNQ', 'name': 'Real Estate ETF', 'expense_ratio': 0.12}
            ]
        }
        
        for asset_class, allocation in target_allocation.items():
            if asset_class in investment_options:
                allocated_amount = amount * allocation
                for option in investment_options[asset_class]:
                    recommendations.append({
                        'symbol': option['symbol'],
                        'name': option['name'],
                        'asset_class': asset_class.value,
                        'recommended_amount': allocated_amount / len(investment_options[asset_class]),
                        'allocation_percentage': allocation * 100,
                        'expense_ratio': option['expense_ratio'],
                        'reasoning': f"Aligns with {allocation*100:.1f}% target allocation for {asset_class.value}"
                    })
        
        # Store recommendation in history
        self.recommendations_history.append({
            'client_id': client_id,
            'amount': amount,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
        
        return recommendations
    
    def generate_portfolio_report(self, client_id: str) -> Dict[str, Any]:
        """Generate comprehensive portfolio report."""
        client = self.clients.get(client_id)
        if not client:
            return {}
        
        portfolio_metrics = self.calculate_portfolio_metrics(client_id)
        risk_assessment = self.assess_risk_profile(client_id)
        target_allocation = self.generate_asset_allocation(client_id)
        
        return {
            'client_info': {
                'name': client.name,
                'client_id': client.client_id,
                'risk_tolerance': client.risk_tolerance.value,
                'time_horizon': client.time_horizon
            },
            'portfolio_metrics': portfolio_metrics,
            'risk_assessment': risk_assessment,
            'target_allocation': {k.value: v for k, v in target_allocation.items()},
            'recommendations': risk_assessment.get('recommendations', []),
            'report_date': datetime.now().isoformat()
        }
    
    def chat_interface(self, client_id: str, query: str) -> str:
        """Simple chat interface for client queries."""
        client = self.clients.get(client_id)
        if not client:
            return "Client not found. Please provide a valid client ID."
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['portfolio', 'performance', 'return']):
            metrics = self.calculate_portfolio_metrics(client_id)
            if metrics:
                return f"""Portfolio Performance Summary:
• Total Value: ${metrics.get('total_value', 0):,.2f}
• Expected Annual Return: {metrics.get('expected_return', 0)*100:.2f}%
• Portfolio Volatility: {metrics.get('volatility', 0)*100:.2f}%
• Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}
• Cash Position: {metrics.get('cash_percentage', 0):.1f}%"""
            else:
                return "No portfolio data available for analysis."
        
        elif any(word in query_lower for word in ['risk', 'assessment']):
            risk_data = self.assess_risk_profile(client_id)
            return f"""Risk Assessment:
• Risk Tolerance: {client.risk_tolerance.value.title()}
• Risk Capacity Score: {risk_data.get('risk_capacity_score', 0):.2f}/1.0
• Portfolio Risk Level: {risk_data.get('portfolio_risk_level', 0)*100:.1f}%
• Risk Alignment: {risk_data.get('risk_alignment_score', 0)*100:.1f}%

Recommendations:
{chr(10).join('• ' + rec for rec in risk_data.get('recommendations', []))}"""
        
        elif any(word in query_lower for word in ['allocation', 'diversification']):
            allocation = self.generate_asset_allocation(client_id)
            allocation_text = "\n".join([f"• {asset.value.title()}: {percent*100:.1f}%" 
                                       for asset, percent in allocation.items()])
            return f"Recommended Asset Allocation:\n{allocation_text}"
        
        elif any(word in query_lower for word in ['invest', 'recommendation']):
            return ("Please specify an investment amount for personalized recommendations. "
                   "Example: 'I want to invest $10,000'")
        
        else:
            return """I can help you with:
• Portfolio performance and metrics
• Risk assessment and alignment
• Asset allocation recommendations
• Investment suggestions
• Financial planning advice

What specific information would you like to know about?"""