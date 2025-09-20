from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from game_logic import GameState
from ai_engine import AIEngine

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize AI engine
ai_engine = AIEngine()

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Initialize a new game"""
    session['game'] = GameState().__dict__
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    return jsonify({
        'success': True,
        'npcs': list(game_state.npcs.values()),
        'status': game_state.get_game_status()
    })

@app.route('/api/start_conversation/<npc_id>', methods=['POST'])
def start_conversation(npc_id):
    """Start conversation with an NPC"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    result = game_state.start_conversation(npc_id)
    session['game'] = game_state.__dict__
    
    return jsonify(result)

@app.route('/api/ask_giovanni/<npc_id>', methods=['POST'])
def ask_giovanni(npc_id):
    """Ask NPC if they know Giovanni"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    result = game_state.ask_about_giovanni(npc_id)
    session['game'] = game_state.__dict__
    
    return jsonify(result)

@app.route('/api/ask_ai_opinion/<npc_id>', methods=['POST'])
def ask_ai_opinion(npc_id):
    """Ask NPC about AI bubble opinion"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
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
    
    session['game'] = game_state.__dict__
    return jsonify(result)

@app.route('/api/make_argument/<npc_id>', methods=['POST'])
def make_argument(npc_id):
    """Make an argument to convince NPC"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    data = request.json
    argument = data.get('argument', '')
    
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    result = game_state.make_argument(npc_id, argument)
    session['game'] = game_state.__dict__
    
    return jsonify(result)

@app.route('/api/chat/<npc_id>', methods=['POST'])
def chat_with_npc(npc_id):
    """Free-form chat with NPC using AI"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    data = request.json
    message = data.get('message', '')
    
    game_state = GameState()
    game_state.__dict__ = session['game']
    
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
        
        session['game'] = game_state.__dict__
        
        return jsonify({
            'response': ai_response,
            'npc': npc
        })
        
    except Exception as e:
        return jsonify({'error': f'AI service error: {str(e)}'}), 500

@app.route('/api/game_status')
def game_status():
    """Get current game status"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    return jsonify(game_state.get_game_status())

@app.route('/api/available_arguments')
def available_arguments():
    """Get available arguments"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    return jsonify(game_state.get_available_arguments())

@app.route('/api/random_arguments')
def random_arguments():
    """Get 3 random arguments for current conversation"""
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400
        
    game_state = GameState()
    game_state.__dict__ = session['game']
    
    return jsonify(game_state.get_random_arguments(3))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
