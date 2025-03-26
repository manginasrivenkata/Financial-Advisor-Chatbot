"""Insurance advice prompt creation module."""

def create_insurance_prompt(user_data):
    """Create insurance advice prompt from user data."""
    return f"""
    You are an AI financial advisor specializing in insurance planning.
    Please provide comprehensive insurance advice based on the following information:

    Age: {user_data.get('age', 'N/A')}
    Occupation: {user_data.get('occupation', 'N/A')}
    Monthly Income: ₹{user_data.get('monthly_income', 'N/A')}
    Family Members: {user_data.get('family_members', 'N/A')}
    Existing Insurance: {user_data.get('existing_insurance', 'N/A')}
    Health Conditions: {user_data.get('health_conditions', 'N/A')}
    Coverage Needed: ₹{user_data.get('coverage_needed', 'N/A')}
    Risk Profile: {user_data.get('risk_profile', 'N/A')}

    Please provide detailed advice covering:
    1. Recommended insurance types
    2. Coverage amounts
    3. Premium estimates
    4. Important policy features
    5. Risk assessment
    6. Claims process overview
    """ 