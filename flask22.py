from flask import Flask, request, jsonify
from crewai import Crew, Agent, Task, Process
from flask_ngrok import run_with_ngrok
import os


Here we connect with the GAIANET NODE

# Check if running in development mode
is_dev_mode = os.environ.get('FLASK_ENV') == 'development'
is_dev_mode = True
app = Flask(__name__)

# Conditionally use ngrok for development
if is_dev_mode:
    run_with_ngrok(app)

# Define Payment Agent and Task
def create_payment_crew():
    # Define the Payment Processing Agent
    payment_agent = Agent(
        role="Payment Processor",
        goal="Process payment transactions securely and efficiently.",
        backstory=(
            "You are a highly reliable payment processing system with expertise in "
            "handling secure transactions, identifying fraudulent activities, and ensuring customer satisfaction."
        )
    )

    # Define the Payment Task
    payment_task = Task(
        description=(
            "Handle a payment transaction using the provided details. "
            "Validate the transaction, process the payment securely, and confirm the status."
        ),
        expected_output=(
            "A confirmation of the transaction, including success/failure status "
            "and any relevant details about the payment."
        ),
        agent=payment_agent,
    )

    # Create the Crew for payment processing
    payment_crew = Crew(
        agents=[payment_agent],
        tasks=[payment_task],
        process=Process.sequential
    )

    return payment_crew

@app.route('/run_crew', methods=['POST'])
def run_crew():
    try:
        data = request.json
        crew_inputs = data.get('inputs', {})  # Payment details from the request payload

        # Create the Payment Crew
        payment_crew = create_payment_crew()

        # Kick off the payment Crew
        result = payment_crew.kickoff(inputs=crew_inputs)
        return jsonify({
            'status': 'success',
            'result': result
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'CrewAI Flask server is running'
    })

if __name__ == '__main__':
    # Install with: pip install flask-ngrok
    if is_dev_mode:
        print("Running in development mode with ngrok")
        app.run()
    else:
        # Production mode
        app.run(host='0.0.0.0', port=5000)
