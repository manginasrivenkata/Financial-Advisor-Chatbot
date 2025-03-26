"""Investment advice prompt creation module."""

def create_investment_prompt(user_data):
    """Create investment advice prompt from user data."""
    return f"""
    You are an AI financial advisor specializing in investment advice.
    Please provide comprehensive investment advice based on the following information:

    Age: {user_data['age']}
    Occupation: {user_data['occupation']}
    Monthly Income: ₹{user_data['monthly_income']}
    Monthly Expenses: ₹{user_data['monthly_expenses']}
    Current Savings: ₹{user_data['current_saving']}
    Investment Goals: {user_data['investment_goals']}
    Risk Tolerance: {user_data['risk_tolerance']}
    Time Horizon: {user_data['time_horizon']}
    Preferred Investment Type: {user_data['investment_type']}
    Amount Available for Investment: ₹{user_data['investment_amount']}
    Other Investments: {user_data['other_investments']}
    Expected Returns: {user_data['expected_returns']}

    Please provide detailed advice covering:
    1. Asset allocation strategy
    2. Recommended investment products
    3. Risk assessment and mitigation
    4. Expected returns analysis
    5. Tax implications
    6. Investment timeline recommendations
    """ 