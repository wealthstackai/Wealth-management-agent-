#!/usr/bin/env python3
"""
Test script for Wealth Management Agent
Demonstrates key functionalities programmatically
"""

from Ai_agent_wealth import (
    WealthManagementAgent, 
    ClientProfile, 
    Portfolio, 
    RiskTolerance,
    AssetClass
)
from datetime import datetime

def test_wealth_management_agent():
    """Comprehensive test of the wealth management agent capabilities."""
    
    print("🧪 TESTING WEALTH MANAGEMENT AGENT")
    print("="*50)
    
    # Initialize agent
    agent = WealthManagementAgent()
    
    # Test 1: Create client profile
    print("\n1. Creating Client Profile...")
    client = ClientProfile(
        client_id="TEST001",
        name="Test Client",
        age=35,
        risk_tolerance=RiskTolerance.MODERATE,
        investment_goals=["retirement", "wealth_building"],
        time_horizon=25,
        current_portfolio_value=250000,
        monthly_contribution=3000,
        liquid_cash_reserve=50000,
        annual_income=120000,
        debt_obligations=80000
    )
    
    success = agent.add_client(client)
    print(f"✅ Client added: {success}")
    
    # Test 2: Create portfolio
    print("\n2. Creating Portfolio...")
    portfolio = Portfolio(
        client_id="TEST001",
        holdings={
            "VTI": 100000,    # Total Stock Market
            "BND": 75000,     # Total Bond Market
            "VEA": 30000,     # International
            "VNQ": 20000,     # Real Estate
        },
        cash_position=15000,
        last_updated=datetime.now()
    )
    
    success = agent.update_portfolio(portfolio)
    print(f"✅ Portfolio updated: {success}")
    
    # Test 3: Portfolio analysis
    print("\n3. Portfolio Analysis...")
    metrics = agent.calculate_portfolio_metrics("TEST001")
    if metrics:
        print(f"   Total Value: ${metrics.get('total_value', 0):,.2f}")
        print(f"   Expected Return: {metrics.get('expected_return', 0)*100:.2f}%")
        print(f"   Volatility: {metrics.get('volatility', 0)*100:.2f}%")
        print(f"   Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}")
        print(f"   Cash %: {metrics.get('cash_percentage', 0):.1f}%")
    else:
        print("   ❌ No portfolio metrics available")
    
    # Test 4: Risk assessment
    print("\n4. Risk Assessment...")
    risk_data = agent.assess_risk_profile("TEST001")
    if risk_data:
        print(f"   Risk Capacity: {risk_data.get('risk_capacity_score', 0):.2f}/1.0")
        print(f"   Risk Tolerance: {risk_data.get('risk_tolerance_score', 0):.2f}/1.0")
        print(f"   Portfolio Risk: {risk_data.get('portfolio_risk_level', 0)*100:.1f}%")
        print(f"   Risk Alignment: {risk_data.get('risk_alignment_score', 0)*100:.1f}%")
        
        recommendations = risk_data.get('recommendations', [])
        if recommendations:
            print("   Recommendations:")
            for rec in recommendations:
                print(f"   • {rec}")
    else:
        print("   ❌ No risk assessment available")
    
    # Test 5: Asset allocation
    print("\n5. Asset Allocation Recommendation...")
    allocation = agent.generate_asset_allocation("TEST001")
    if allocation:
        print("   Recommended Allocation:")
        for asset_class, percentage in allocation.items():
            print(f"   • {asset_class.value.replace('_', ' ').title()}: {percentage*100:.1f}%")
    else:
        print("   ❌ No allocation recommendation available")
    
    # Test 6: Investment recommendations
    print("\n6. Investment Recommendations...")
    recommendations = agent.recommend_investments("TEST001", 50000)
    if recommendations:
        print("   Investment Suggestions for $50,000:")
        for rec in recommendations[:3]:  # Show top 3
            print(f"   • {rec['symbol']}: ${rec['recommended_amount']:,.0f}")
            print(f"     ({rec['name']}) - {rec['allocation_percentage']:.1f}%")
    else:
        print("   ❌ No investment recommendations available")
    
    # Test 7: Comprehensive report
    print("\n7. Comprehensive Report...")
    report = agent.generate_portfolio_report("TEST001")
    if report:
        print("   ✅ Comprehensive report generated")
        client_info = report['client_info']
        print(f"   Client: {client_info['name']}")
        print(f"   Risk Tolerance: {client_info['risk_tolerance']}")
        
        portfolio_metrics = report['portfolio_metrics']
        if portfolio_metrics:
            print(f"   Portfolio Value: ${portfolio_metrics.get('total_value', 0):,.0f}")
    else:
        print("   ❌ No report generated")
    
    # Test 8: Chat interface
    print("\n8. Chat Interface Test...")
    test_queries = [
        "How is my portfolio performing?",
        "What's my risk assessment?",
        "Show me my asset allocation"
    ]
    
    for query in test_queries:
        response = agent.chat_interface("TEST001", query)
        print(f"   Q: {query}")
        print(f"   A: {response[:100]}..." if len(response) > 100 else f"   A: {response}")
        print()
    
    print("\n🎉 ALL TESTS COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    test_wealth_management_agent()