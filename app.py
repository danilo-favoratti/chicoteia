from flask import Flask, render_template, request, jsonify, session
import os
import uuid
from dotenv import load_dotenv
from game_logic import GameState
from ai_engine import AIEngine

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Server-side session storage to avoid large cookies
game_sessions = {}

# Initialize AI engine
ai_engine = AIEngine()

def get_game_state():
    """Get game state from server-side storage"""
    session_id = session.get('session_id')
    if not session_id or session_id not in game_sessions:
        return None
    return game_sessions[session_id]

def save_game_state(game_state):
    """Save game state to server-side storage"""
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    game_sessions[session_id] = game_state

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Initialize a new game"""
    game_state = GameState()
    save_game_state(game_state)
    
    return jsonify({
        'success': True,
        'npcs': list(game_state.npcs.values()),
        'status': game_state.get_game_status()
    })

@app.route('/api/start_conversation/<npc_id>', methods=['POST'])
def start_conversation(npc_id):
    """Start conversation with an NPC"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
        
    result = game_state.start_conversation(npc_id)
    save_game_state(game_state)
    
    return jsonify(result)

@app.route('/api/ask_giovanni/<npc_id>', methods=['POST'])
def ask_giovanni(npc_id):
    """Ask NPC if they know Giovanni"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
        
    result = game_state.ask_about_giovanni(npc_id)
    save_game_state(game_state)
    
    return jsonify(result)

@app.route('/api/ask_ai_opinion/<npc_id>', methods=['POST'])
def ask_ai_opinion(npc_id):
    """Ask NPC about AI bubble opinion"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
        
    result = game_state.ask_ai_bubble_opinion(npc_id)
    
    # If needs AI response, generate it
    if result.get('needs_ai_response'):
        try:
            ai_response = ai_engine.generate_ai_bubble_response(result['npc'])
            
            # Add to conversation history
            history = game_state.conversation_history.get(npc_id, [])
            history.append({
                "type": "ai_opinion",
                "response": ai_response
            })
            game_state.conversation_history[npc_id] = history
            
            result['response'] = ai_response
            del result['needs_ai_response']  # Clean up
            
        except Exception as e:
            return jsonify({'error': f'AI service error: {str(e)}'}), 500
    
    save_game_state(game_state)
    return jsonify(result)

@app.route('/api/make_argument/<npc_id>', methods=['POST'])
def make_argument(npc_id):
    """Make an argument to convince NPC"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
        
    data = request.json
    argument = data.get('argument', '')
    
    result = game_state.make_argument(npc_id, argument)
    save_game_state(game_state)
    
    return jsonify(result)

@app.route('/api/chat/<npc_id>', methods=['POST'])
def chat_with_npc(npc_id):
    """Free-form chat with NPC using AI"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
        
    data = request.json
    message = data.get('message', '')
    
    npc = game_state.get_npc(npc_id)
    if not npc:
        return jsonify({'error': 'NPC not found'}), 404
        
    # Get conversation history for this NPC
    history = game_state.conversation_history.get(npc_id, [])
    
    # Generate AI response
    try:
        ai_response = ai_engine.generate_npc_response(
            npc=npc,
            conversation_history=history,
            user_message=message,
            game_context=game_state.get_game_status()
        )
        
        # Add to conversation history
        history.append({"type": "user_message", "message": message})
        history.append({"type": "ai_response", "response": ai_response})
        game_state.conversation_history[npc_id] = history
        
        save_game_state(game_state)
        
        return jsonify({
            'response': ai_response,
            'npc': npc
        })
        
    except Exception as e:
        return jsonify({'error': f'AI service error: {str(e)}'}), 500

@app.route('/api/game_status')
def game_status():
    """Get current game status"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
    
    return jsonify(game_state.get_game_status())

@app.route('/api/available_arguments')
def available_arguments():
    """Get available arguments"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
    
    return jsonify(game_state.get_available_arguments())

@app.route('/api/random_arguments')
def random_arguments():
    """Get 3 random arguments for current conversation"""
    game_state = get_game_state()
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
    
    return jsonify(game_state.get_random_arguments(3))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6060)
