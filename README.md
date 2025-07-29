# 🏦 Wealth Management Agent

A comprehensive AI agent designed for wealth management firms to assist with portfolio analysis, risk assessment, investment recommendations, and client management.

## 🚀 Features

### Core Capabilities
- **Portfolio Analysis**: Calculate key performance metrics including returns, volatility, and Sharpe ratios
- **Risk Assessment**: Evaluate client risk tolerance and portfolio alignment
- **Investment Recommendations**: Generate personalized investment suggestions based on client profiles
- **Asset Allocation**: Optimize portfolio allocation across different asset classes
- **Market Data Integration**: Real-time market data fetching using Yahoo Finance
- **Client Management**: Comprehensive client profiling and goal tracking
- **Compliance Reporting**: Generate detailed portfolio reports for regulatory compliance
- **Conversational Interface**: Chat-based client interaction system

### Advanced Features
- **Multi-Risk Profile Support**: Conservative, Moderate, and Aggressive risk tolerances
- **Age-Based Allocation**: Automatic adjustment using the "Rule of 100"
- **Performance Metrics**: Sharpe ratio, volatility, expected returns calculation
- **Goal-Based Planning**: Investment recommendations aligned with client objectives
- **Historical Analysis**: Portfolio performance tracking and trend analysis

## 📋 Requirements

- Python 3.8+
- numpy>=1.21.0
- pandas>=1.3.0
- yfinance>=0.2.0
- requests>=2.28.0

## 🛠️ Installation

1. Clone or download the project files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### Interactive Mode (Default)
```bash
python main.py
```

### Demo Mode
```bash
python main.py --mode demo
```

### CLI Mode
```bash
# Get portfolio analysis
python main.py --mode cli --client-id C001 --action portfolio

# Get investment recommendations
python main.py --mode cli --client-id C001 --action recommend --amount 50000

# Generate comprehensive report
python main.py --mode cli --client-id C001 --action report
```

## 💼 Usage Examples

### Creating a Client Profile
```python
from Ai_agent_wealth import WealthManagementAgent, ClientProfile, RiskTolerance

agent = WealthManagementAgent()

client = ClientProfile(
    client_id="C001",
    name="John Doe",
    age=45,
    risk_tolerance=RiskTolerance.MODERATE,
    investment_goals=["retirement", "children_education"],
    time_horizon=20,
    current_portfolio_value=500000,
    monthly_contribution=5000,
    liquid_cash_reserve=100000,
    annual_income=150000,
    debt_obligations=200000
)

agent.add_client(client)
```

### Portfolio Analysis
```python
# Calculate portfolio metrics
metrics = agent.calculate_portfolio_metrics("C001")
print(f"Total Value: ${metrics['total_value']:,.2f}")
print(f"Expected Return: {metrics['expected_return']*100:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
```

### Risk Assessment
```python
# Assess client risk profile
risk_data = agent.assess_risk_profile("C001")
print(f"Risk Alignment: {risk_data['risk_alignment_score']*100:.1f}%")
print("Recommendations:", risk_data['recommendations'])
```

### Investment Recommendations
```python
# Get investment recommendations
recommendations = agent.recommend_investments("C001", 25000)
for rec in recommendations:
    print(f"{rec['symbol']}: ${rec['recommended_amount']:,.0f}")
```

## 📊 Interactive Features

The interactive mode provides a menu-driven interface with the following options:

1. **List Clients** - View all registered clients
2. **Client Profile** - Detailed client information
3. **Portfolio Analysis** - Performance metrics and analysis
4. **Risk Assessment** - Risk tolerance and alignment evaluation
5. **Investment Recommendations** - Personalized investment suggestions
6. **Generate Report** - Comprehensive portfolio reports
7. **Chat Interface** - Conversational client assistance
8. **Demo Mode** - Pre-loaded sample data for testing

## 🎭 Demo Clients

The system includes three pre-configured demo clients:

- **Robert Johnson (C001)**: Conservative 58-year-old approaching retirement
- **Sarah Williams (C002)**: Moderate 42-year-old with multiple goals
- **Michael Chen (C003)**: Aggressive 28-year-old focused on wealth building

## 📈 Asset Classes Supported

- **Stocks**: Domestic and international equity markets
- **Bonds**: Government and corporate fixed income
- **Real Estate**: REITs and real estate investments
- **Cash**: Money market and cash equivalents
- **Alternatives**: Commodities and alternative investments

## 🔒 Risk Management

The agent implements sophisticated risk assessment including:

- **Risk Capacity Analysis**: Based on age, income, time horizon, and debt
- **Risk Tolerance Mapping**: Conservative, Moderate, Aggressive profiles
- **Portfolio Risk Alignment**: Matching portfolio risk to client tolerance
- **Automated Rebalancing Suggestions**: Based on drift from target allocation

## 📝 Compliance & Reporting

- Comprehensive portfolio reports with all key metrics
- Investment recommendation history tracking
- Risk assessment documentation
- Performance attribution analysis
- Regulatory compliance data formatting

## 🤖 Chat Interface

The conversational interface can handle queries about:
- Portfolio performance and returns
- Risk assessment and recommendations
- Asset allocation suggestions
- Investment planning advice
- Market analysis and insights

Example queries:
- "How is my portfolio performing?"
- "What's my risk assessment?"
- "Show me my asset allocation"
- "I want to invest $10,000"

## 🔧 Customization

The agent can be easily extended with:
- Custom risk models
- Additional asset classes
- Enhanced market data sources
- Advanced optimization algorithms
- Integration with external systems

## 📞 Support

This wealth management agent is designed to be production-ready for financial institutions. The modular architecture allows for easy integration with existing systems and compliance frameworks.

## ⚖️ Disclaimer

This software is for educational and demonstration purposes. All investment recommendations should be reviewed by qualified financial professionals before implementation. Past performance does not guarantee future results.