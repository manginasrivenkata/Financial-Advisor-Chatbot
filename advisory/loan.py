"""Loan advice prompt creation module."""

def create_loan_prompt(user_data):
    """Create loan advice prompt from user data."""
    return f"""
    You are an AI financial advisor specializing in loan planning.
    Please provide comprehensive loan advice based on the following information:

    Age: {user_data.get('age', 'N/A')}
    Occupation: {user_data.get('occupation', 'N/A')}
    Monthly Income: ₹{user_data.get('monthly_income', 'N/A')}
    Loan Type: {user_data.get('loan_type', 'N/A')}
    Loan Amount: ₹{user_data.get('loan_amount', 'N/A')}
    Loan Term: {user_data.get('loan_term', 'N/A')}
    Credit Score: {user_data.get('credit_score', 'N/A')}
    Existing Loans: {user_data.get('existing_loans', 'N/A')}

    Please provide detailed advice covering:
    1. Loan eligibility assessment
    2. Interest rate recommendations
    3. EMI calculations
    4. Documentation requirements
    5. Risk assessment
    6. Repayment strategies
    """ 