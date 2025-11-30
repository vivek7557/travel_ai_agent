from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = TravelAgentOrchestrator()

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from user
    """
    data = request.json
    user_message = data['message']
    customer_id = data.get('customer_id', 'anonymous')
    
    # Run the AI agent
    result = agent.run(user_message, customer_id)
    
    # Get the agent's response
    agent_response = result["messages"][-1]["content"]
    
    return jsonify({
        "response": agent_response,
        "booking_status": result.get("booking_confirmed", False),
        "confirmation": result.get("confirmation_number")
    })

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Handle WhatsApp messages via Twilio
    """
    from twilio.twiml.messaging_response import MessagingResponse
    
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    
    # Run agent
    result = agent.run(incoming_msg, sender)
    agent_response = result["messages"][-1]["content"]
    
    # Send response via WhatsApp
    resp = MessagingResponse()
    resp.message(agent_response)
    
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
