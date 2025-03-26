"""Main Flask application integrating financial advisory and chatbot services."""

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    GenerationConfig,
    HarmCategory,
    HarmBlockThreshold
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
import google.cloud.aiplatform as aiplatform
import time
from dotenv import load_dotenv
import base64
import tempfile

# Import advisory functions
from advisory.investment import create_investment_prompt
from advisory.insurance import create_insurance_prompt
from advisory.loan import create_loan_prompt

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.template_folder = 'templates'  # Ensure templates are found

# Get credentials from environment variables
PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
LOCATION = os.getenv('GOOGLE_LOCATION')

# Decode and set up Google credentials from environment variable
credentials_base64 = os.getenv('GOOGLE_CREDENTIALS')
if not credentials_base64:
    raise ValueError("Google credentials not found in environment variables")

# Decode base64 credentials and create temporary file
credentials_content = base64.b64decode(credentials_base64).decode()
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
    temp_file.write(credentials_content)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file.name

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 2

def init_vertexai():
    """Initialize Vertex AI with proper error handling and retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            aiplatform.init(project=PROJECT_ID, location=LOCATION)
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            return True
        except Exception as e:
            app.logger.error(
                f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {str(e)}"
            )
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                app.logger.error("Failed to initialize after all retries")
                return False

# Initialize Vertex AI
if not init_vertexai():
    app.logger.error("Could not initialize Vertex AI")

def load_financial_docs():
    """Load and process financial documents."""
    try:
        file_path = "database/General.pdf"
        data_file = PyPDFDirectoryLoader(file_path)
        docs = data_file.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        return splitter.split_documents(docs)
    except Exception as e:
        app.logger.error(f"Error loading documents: {str(e)}")
        return []

# Load documents
chunks = load_financial_docs()

# Generation configuration
GENERATION_CONFIG = GenerationConfig(
    max_output_tokens=2048,
    temperature=0.3,
    top_p=0.8,
)

# Safety settings
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: (
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: (
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: (
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    HarmCategory.HARM_CATEGORY_HARASSMENT: (
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
}

def generate_response(prompt, retries=MAX_RETRIES, stream=True):
    """Generate response using Vertex AI with retry logic."""
    for attempt in range(retries):
        try:
            model = GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(
                prompt,
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
                stream=stream,
            )

            if stream:
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                return full_response
            return response.text

        except Exception as e:
            app.logger.error(
                f"Attempt {attempt + 1}/{retries} failed: {str(e)}"
            )
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                app.logger.error("Failed to generate response after all retries")
                return None

# Routes
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('homepage.html')

@app.route('/chatbot')
def chatbot():
    """Render the chatbot interface."""
    return render_template('chatbot.html')

@app.route('/investment')
def investment():
    """Render investment advice form."""
    return render_template('investment_advice.html')

@app.route('/insurance')
def insurance():
    """Render insurance advice form."""
    return render_template('insurance_advice.html')

@app.route('/loan')
def loan():
    """Render loan advice form."""
    return render_template('loan_advice.html')

@app.route('/calculators/<calculator_name>')
def calculator(calculator_name):
    """Dynamic route for calculators."""
    calculator_map = {
        'loan-emi': 'Calculators/loan_emi.html',
        'fd': 'Calculators/fd.html',
        'ppf': 'Calculators/ppf.html',
        'recurring': 'Calculators/recurring.html',
        'sip': 'Calculators/sip_calc.html',
        'gold-loan': 'Calculators/egi_gold.html',
        'loan-eligibility': 'Calculators/egi_loan.html',
        'ipo': 'Calculators/ipo.html',
        'index': 'Calculators/index.html'
    }
    
    if calculator_name in calculator_map:
        return render_template(calculator_map[calculator_name])
    return "Calculator not found", 404

@app.route('/ask', methods=['POST'])
def ask():
    """Handle chatbot queries."""
    try:
        user_query = request.form['query']
        
        # Get relevant context from chunks
        # For simplicity, using the first chunk as context
        # In production, implement proper context retrieval
        context = chunks[0].page_content if chunks else ""
        
        prompt = f"""
        You are an AI assistant that helps people with financial advice.
        The answer should be descriptive.

        CONTEXT: {context}

        QUERY: {user_query}

        INSTRUCTIONS:
        - Use only the information provided in the CONTEXT section to answer the QUERY.
        - Do not provide information or answers outside of the given CONTEXT.
        - Provide only the answer to the query without additional information.
        - Provide the answers in proper formatting
        """
        
        response = generate_response(prompt)
        
        if response is None:
            return jsonify({
                'error': 'Service temporarily unavailable. Please try again.'
            }), 503
            
        return jsonify({'answer': response})
        
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Failed to process request'}), 500

# Advisory endpoints
@app.route('/get_investment_advice', methods=['POST'])
def get_investment_advice():
    """Handle investment advice requests."""
    try:
        user_data = request.form.to_dict()
        
        # Validate required fields
        required_fields = [
            'age', 'occupation', 'monthly_income', 'monthly_expenses',
            'current_saving', 'investment_goals', 'risk_tolerance',
            'time_horizon', 'investment_type', 'investment_amount',
            'other_investments', 'expected_returns'
        ]
        
        for field in required_fields:
            if field not in user_data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400

        prompt = create_investment_prompt(user_data)
        response = generate_response(prompt, stream=False)

        if response is None:
            return jsonify({
                'error': 'Failed to generate investment advice'
            }), 500

        return jsonify({'advice': response})
    except Exception as e:
        app.logger.error(f"Investment advice error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/get_insurance_advice', methods=['POST'])
def get_insurance_advice():
    """Handle insurance advice requests."""
    try:
        user_data = request.form.to_dict()
        prompt = create_insurance_prompt(user_data)
        response = generate_response(prompt, stream=False)

        if response is None:
            return jsonify({'error': 'Failed to generate advice'}), 500

        return jsonify({'advice': response})
    except Exception as e:
        app.logger.error(f"Insurance advice error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/get_loan_advice', methods=['POST'])
def get_loan_advice():
    """Handle loan advice requests."""
    try:
        user_data = request.form.to_dict()
        prompt = create_loan_prompt(user_data)
        response = generate_response(prompt, stream=False)

        if response is None:
            return jsonify({'error': 'Failed to generate advice'}), 500

        return jsonify({'advice': response})
    except Exception as e:
        app.logger.error(f"Loan advice error: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5100) 