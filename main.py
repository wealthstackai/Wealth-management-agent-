#!/usr/bin/env python3
"""
Wealth Management Agent - Main Application
A comprehensive AI agent for wealth management firms.
"""

import argparse
import json
from datetime import datetime
from Ai_agent_wealth import (
    WealthManagementAgent, 
    ClientProfile, 
    Portfolio, 
    RiskTolerance,
    AssetClass
)

def create_demo_clients(agent: WealthManagementAgent):
    """Create sample clients for demonstration."""
    
    # Conservative investor - older client
    client1 = ClientProfile(
        client_id="C001",
        name="Robert Johnson",
        age=58,
        risk_tolerance=RiskTolerance.CONSERVATIVE,
        investment_goals=["retirement", "capital_preservation"],
        time_horizon=7,
        current_portfolio_value=850000,
        monthly_contribution=3000,
        liquid_cash_reserve=100000,
        annual_income=120000,
        debt_obligations=15000
    )
    
    # Moderate investor - middle-aged client
    client2 = ClientProfile(
        client_id="C002",
        name="Sarah Williams",
        age=42,
        risk_tolerance=RiskTolerance.MODERATE,
        investment_goals=["children_education", "retirement", "house_upgrade"],
        time_horizon=20,
        current_portfolio_value=450000,
        monthly_contribution=4500,
        liquid_cash_reserve=75000,
        annual_income=150000,
        debt_obligations=280000
    )
    
    # Aggressive investor - young professional
    client3 = ClientProfile(
        client_id="C003",
        name="Michael Chen",
        age=28,
        risk_tolerance=RiskTolerance.AGGRESSIVE,
        investment_goals=["wealth_building", "early_retirement"],
        time_horizon=35,
        current_portfolio_value=125000,
        monthly_contribution=2800,
        liquid_cash_reserve=25000,
        annual_income=95000,
        debt_obligations=45000
    )
    
    # Add clients to agent
    agent.add_client(client1)
    agent.add_client(client2)
    agent.add_client(client3)
    
    # Create sample portfolios
    portfolio1 = Portfolio(
        client_id="C001",
        holdings={
            "BND": 400000,  # Bond ETF
            "VTI": 200000,  # Total market
            "VNQ": 50000,   # Real Estate
        },
        cash_position=85000,
        last_updated=datetime.now()
    )
    
    portfolio2 = Portfolio(
        client_id="C002",
        holdings={
            "VOO": 200000,  # S&P 500
            "BND": 150000,  # Bonds
            "VEA": 50000,   # International
            "VNQ": 25000,   # Real Estate
        },
        cash_position=15000,
        last_updated=datetime.now()
    )
    
    portfolio3 = Portfolio(
        client_id="C003",
        holdings={
            "VTI": 75000,   # Total market
            "VEA": 25000,   # International
            "QQQ": 15000,   # Technology
        },
        cash_position=8000,
        last_updated=datetime.now()
    )
    
    agent.update_portfolio(portfolio1)
    agent.update_portfolio(portfolio2)
    agent.update_portfolio(portfolio3)
    
    print("Demo clients and portfolios created successfully!")
    return ["C001", "C002", "C003"]

def interactive_mode(agent: WealthManagementAgent):
    """Interactive mode for client consultation."""
    print("\n" + "="*60)
    print("🏦 WEALTH MANAGEMENT AGENT - INTERACTIVE MODE")
    print("="*60)
    
    while True:
        print("\nAvailable Commands:")
        print("1. List clients")
        print("2. Client profile")
        print("3. Portfolio analysis")
        print("4. Risk assessment")
        print("5. Investment recommendations")
        print("6. Generate report")
        print("7. Chat with client")
        print("8. Demo mode")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            list_clients(agent)
        elif choice == "2":
            client_profile_menu(agent)
        elif choice == "3":
            portfolio_analysis_menu(agent)
        elif choice == "4":
            risk_assessment_menu(agent)
        elif choice == "5":
            investment_recommendations_menu(agent)
        elif choice == "6":
            generate_report_menu(agent)
        elif choice == "7":
            chat_menu(agent)
        elif choice == "8":
            demo_mode(agent)
        elif choice == "9":
            print("Thank you for using Wealth Management Agent!")
            break
        else:
            print("Invalid choice. Please try again.")

def list_clients(agent: WealthManagementAgent):
    """List all clients."""
    if not agent.clients:
        print("\nNo clients found.")
        return
    
    print("\n📋 CLIENT LIST:")
    print("-" * 80)
    for client_id, client in agent.clients.items():
        portfolio_value = 0
        if client_id in agent.portfolios:
            metrics = agent.calculate_portfolio_metrics(client_id)
            portfolio_value = metrics.get('total_value', 0)
        
        print(f"ID: {client_id} | Name: {client.name} | Age: {client.age} | "
              f"Risk: {client.risk_tolerance.value} | Portfolio: ${portfolio_value:,.0f}")

def client_profile_menu(agent: WealthManagementAgent):
    """Show client profile details."""
    client_id = input("\nEnter client ID: ").strip()
    client = agent.get_client_profile(client_id)
    
    if not client:
        print("Client not found.")
        return
    
    print(f"\n👤 CLIENT PROFILE: {client.name}")
    print("-" * 50)
    print(f"Client ID: {client.client_id}")
    print(f"Age: {client.age}")
    print(f"Risk Tolerance: {client.risk_tolerance.value}")
    print(f"Investment Goals: {', '.join(client.investment_goals)}")
    print(f"Time Horizon: {client.time_horizon} years")
    print(f"Annual Income: ${client.annual_income:,.0f}")
    print(f"Monthly Contribution: ${client.monthly_contribution:,.0f}")
    print(f"Cash Reserve: ${client.liquid_cash_reserve:,.0f}")
    print(f"Debt Obligations: ${client.debt_obligations:,.0f}")

def portfolio_analysis_menu(agent: WealthManagementAgent):
    """Show portfolio analysis."""
    client_id = input("\nEnter client ID: ").strip()
    metrics = agent.calculate_portfolio_metrics(client_id)
    
    if not metrics:
        print("No portfolio data found for this client.")
        return
    
    print(f"\n📈 PORTFOLIO ANALYSIS: {client_id}")
    print("-" * 50)
    print(f"Total Value: ${metrics.get('total_value', 0):,.2f}")
    print(f"Cash Position: {metrics.get('cash_percentage', 0):.1f}%")
    print(f"Expected Annual Return: {metrics.get('expected_return', 0)*100:.2f}%")
    print(f"Portfolio Volatility: {metrics.get('volatility', 0)*100:.2f}%")
    print(f"Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}")

def risk_assessment_menu(agent: WealthManagementAgent):
    """Show risk assessment."""
    client_id = input("\nEnter client ID: ").strip()
    risk_data = agent.assess_risk_profile(client_id)
    
    if not risk_data:
        print("No risk data available for this client.")
        return
    
    print(f"\n⚖️ RISK ASSESSMENT: {client_id}")
    print("-" * 50)
    print(f"Risk Capacity Score: {risk_data.get('risk_capacity_score', 0):.2f}/1.0")
    print(f"Risk Tolerance Score: {risk_data.get('risk_tolerance_score', 0):.2f}/1.0")
    print(f"Portfolio Risk Level: {risk_data.get('portfolio_risk_level', 0)*100:.1f}%")
    print(f"Risk Alignment: {risk_data.get('risk_alignment_score', 0)*100:.1f}%")
    
    recommendations = risk_data.get('recommendations', [])
    if recommendations:
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"• {rec}")

def investment_recommendations_menu(agent: WealthManagementAgent):
    """Show investment recommendations."""
    client_id = input("\nEnter client ID: ").strip()
    try:
        amount = float(input("Enter investment amount: $").strip().replace(',', ''))
    except ValueError:
        print("Invalid amount.")
        return
    
    recommendations = agent.recommend_investments(client_id, amount)
    
    if not recommendations:
        print("No recommendations available.")
        return
    
    print(f"\n💡 INVESTMENT RECOMMENDATIONS: ${amount:,.0f}")
    print("-" * 70)
    for rec in recommendations:
        print(f"Symbol: {rec['symbol']} | {rec['name']}")
        print(f"  Amount: ${rec['recommended_amount']:,.0f} ({rec['allocation_percentage']:.1f}%)")
        print(f"  Asset Class: {rec['asset_class']} | Expense Ratio: {rec['expense_ratio']:.2f}%")
        print(f"  Reasoning: {rec['reasoning']}")
        print()

def generate_report_menu(agent: WealthManagementAgent):
    """Generate comprehensive portfolio report."""
    client_id = input("\nEnter client ID: ").strip()
    report = agent.generate_portfolio_report(client_id)
    
    if not report:
        print("No data available for this client.")
        return
    
    print(f"\n📊 COMPREHENSIVE PORTFOLIO REPORT")
    print("="*60)
    
    # Client Info
    client_info = report['client_info']
    print(f"Client: {client_info['name']} (ID: {client_info['client_id']})")
    print(f"Risk Tolerance: {client_info['risk_tolerance']}")
    print(f"Time Horizon: {client_info['time_horizon']} years")
    
    # Portfolio Metrics
    portfolio_metrics = report['portfolio_metrics']
    if portfolio_metrics:
        print(f"\nPortfolio Value: ${portfolio_metrics.get('total_value', 0):,.2f}")
        print(f"Expected Return: {portfolio_metrics.get('expected_return', 0)*100:.2f}%")
        print(f"Volatility: {portfolio_metrics.get('volatility', 0)*100:.2f}%")
        print(f"Sharpe Ratio: {portfolio_metrics.get('sharpe_ratio', 0):.3f}")
    
    # Target Allocation
    target_allocation = report['target_allocation']
    print(f"\nRecommended Asset Allocation:")
    for asset_class, percentage in target_allocation.items():
        print(f"  {asset_class.replace('_', ' ').title()}: {percentage*100:.1f}%")
    
    # Recommendations
    recommendations = report['recommendations']
    if recommendations:
        print(f"\nRecommendations:")
        for rec in recommendations:
            print(f"• {rec}")

def chat_menu(agent: WealthManagementAgent):
    """Chat interface with client."""
    client_id = input("\nEnter client ID: ").strip()
    
    if client_id not in agent.clients:
        print("Client not found.")
        return
    
    print(f"\n💬 CHAT MODE - Client: {agent.clients[client_id].name}")
    print("Type 'exit' to return to main menu")
    print("-" * 50)
    
    while True:
        query = input(f"\n{agent.clients[client_id].name}: ").strip()
        if query.lower() == 'exit':
            break
        
        if query:
            response = agent.chat_interface(client_id, query)
            print(f"\nAdvisor: {response}")

def demo_mode(agent: WealthManagementAgent):
    """Run demonstration with sample data."""
    print("\n🎯 DEMO MODE")
    print("-" * 30)
    
    # Create demo clients if not exist
    if not agent.clients:
        client_ids = create_demo_clients(agent)
    else:
        client_ids = list(agent.clients.keys())
    
    for client_id in client_ids[:3]:  # Show first 3 clients
        client = agent.clients[client_id]
        print(f"\n📋 Analyzing Client: {client.name}")
        print("=" * 50)
        
        # Portfolio metrics
        metrics = agent.calculate_portfolio_metrics(client_id)
        if metrics:
            print(f"Portfolio Value: ${metrics.get('total_value', 0):,.0f}")
            print(f"Expected Return: {metrics.get('expected_return', 0)*100:.1f}%")
            print(f"Risk Level: {metrics.get('volatility', 0)*100:.1f}%")
        
        # Risk assessment
        risk_data = agent.assess_risk_profile(client_id)
        if risk_data:
            print(f"Risk Alignment: {risk_data.get('risk_alignment_score', 0)*100:.0f}%")
        
        # Sample recommendations
        recommendations = agent.recommend_investments(client_id, 25000)
        if recommendations:
            print(f"\nTop Investment Recommendation:")
            top_rec = recommendations[0]
            print(f"• {top_rec['symbol']}: ${top_rec['recommended_amount']:,.0f}")

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="Wealth Management Agent")
    parser.add_argument("--mode", choices=["interactive", "demo", "cli"], 
                       default="interactive", help="Application mode")
    parser.add_argument("--client-id", help="Client ID for CLI mode")
    parser.add_argument("--action", choices=["profile", "portfolio", "risk", "recommend", "report"],
                       help="Action for CLI mode")
    parser.add_argument("--amount", type=float, help="Investment amount for recommendations")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = WealthManagementAgent()
    
    print("🏦 WEALTH MANAGEMENT AGENT")
    print("="*40)
    print("Initializing agent...")
    
    if args.mode == "demo":
        create_demo_clients(agent)
        demo_mode(agent)
    elif args.mode == "cli":
        if not args.client_id or not args.action:
            print("CLI mode requires --client-id and --action parameters")
            return
        
        # CLI mode implementation
        if args.action == "profile":
            client_profile_menu(agent)
        elif args.action == "portfolio":
            metrics = agent.calculate_portfolio_metrics(args.client_id)
            print(json.dumps(metrics, indent=2))
        elif args.action == "risk":
            risk_data = agent.assess_risk_profile(args.client_id)
            print(json.dumps(risk_data, indent=2))
        elif args.action == "recommend":
            if not args.amount:
                print("Recommendation requires --amount parameter")
                return
            recommendations = agent.recommend_investments(args.client_id, args.amount)
            print(json.dumps(recommendations, indent=2))
        elif args.action == "report":
            report = agent.generate_portfolio_report(args.client_id)
            print(json.dumps(report, indent=2, default=str))
    else:
        # Interactive mode (default)
        interactive_mode(agent)

if __name__ == "__main__":
    main()