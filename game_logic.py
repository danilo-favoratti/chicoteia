import random
from typing import Dict, List, Optional
from npc_data import NPCS, ARGUMENTS

class GameState:
    def __init__(self):
        self.npcs = {npc["id"]: self._init_npc(npc) for npc in NPCS}
        self.current_npc = None
        self.conversation_history = {}
        self.game_won = False
        
    def _init_npc(self, npc_data: Dict) -> Dict:
        """Initialize NPC with game state"""
        npc = npc_data.copy()
        npc["status"] = "unknown"  # unknown, safe, needs_convincing
        npc["arguments_used"] = []
        npc["chicoteia_used"] = False
        npc["conversation_phase"] = "initial"  # initial, giovanni_check, ai_opinion, argument_phase, safe
        return npc
        
    def get_npc(self, npc_id: str) -> Optional[Dict]:
        """Get NPC by ID"""
        return self.npcs.get(npc_id)
        
    def start_conversation(self, npc_id: str) -> Dict:
        """Start conversation with an NPC"""
        self.current_npc = npc_id
        npc = self.npcs[npc_id]
        
        if npc_id not in self.conversation_history:
            self.conversation_history[npc_id] = []
            
        return {
            "npc": npc,
            "phase": npc["conversation_phase"],
            "message": self._get_initial_message(npc)
        }
        
    def _get_initial_message(self, npc: Dict) -> str:
        """Get initial greeting message from NPC"""
        greetings = [
            f"Oi! Eu sou {npc['name']}, {npc['role']}. Como está a conferência?",
            f"Olá! {npc['name']} aqui. Ótimas palestras hoje, né?", 
            f"Oi! Sou {npc['name']}, {npc['role']}. Curtindo até agora?",
            f"E aí! {npc['name']} de {npc['role']}. O que te trouxe aqui?"
        ]
        return random.choice(greetings)
        
    def ask_about_giovanni(self, npc_id: str) -> Dict:
        """Ask NPC if they know Giovanni"""
        npc = self.npcs[npc_id]
        
        if npc["knows_giovanni"]:
            npc["conversation_phase"] = "ai_opinion"
            npc["status"] = "needs_convincing"
            # Use the specific relationship context
            response = f"Sim, conheço Giovanni! {npc['giovanni_relationship']} Por que pergunta?"
        else:
            npc["conversation_phase"] = "safe"
            npc["status"] = "safe"
            response = npc['giovanni_relationship']  # Use the specific "don't know" response
            
        self.conversation_history[npc_id].append({
            "type": "giovanni_question",
            "response": response
        })
        
        return {
            "response": response,
            "phase": npc["conversation_phase"],
            "status": npc["status"]
        }
        
    def ask_ai_bubble_opinion(self, npc_id: str) -> Dict:
        """Ask NPC about AI bubble opinion - now with AI-generated responses"""
        npc = self.npcs[npc_id]
        
        if npc["conversation_phase"] != "ai_opinion":
            return {"error": "Not in correct conversation phase"}
            
        # Mark as needing AI generation
        npc["needs_ai_response"] = True
        
        if npc["ai_bubble_stance"] == "bubble":
            npc["conversation_phase"] = "argument_phase"
        else:
            npc["conversation_phase"] = "safe"
            npc["status"] = "safe"
            
        return {
            "needs_ai_response": True,
            "phase": npc["conversation_phase"],
            "status": npc["status"],
            "npc": npc
        }
        
    def make_argument(self, npc_id: str, argument_text: str) -> Dict:
        """Make an argument to convince NPC"""
        npc = self.npcs[npc_id]
        
        if npc["conversation_phase"] != "argument_phase":
            return {"error": "Not in argument phase"}
            
        # Check if it's the special "chicoteia" argument
        if argument_text.lower() == "chicoteia":
            if npc["chicoteia_used"]:
                    return {
                        "response": "Você já tentou essa palavra mágica comigo!",
                        "success": False,
                        "phase": npc["conversation_phase"]
                    }
                
            npc["chicoteia_used"] = True
            success = random.random() < 0.5  # 50% chance
            
            if success:
                npc["conversation_phase"] = "safe"
                npc["status"] = "safe"
                response = "Chicoteia... espera, isso é... sabe de uma coisa? Você está absolutamente certo! IA não é bolha nenhuma!"
            else:
                response = "Chicoteia? Interessante, mas ainda não estou convencido de que IA não está supervalorizada."
        else:
            # Regular argument
            npc["arguments_used"].append(argument_text)
            
            # Reduce resistance
            npc["resistance_level"] = max(0, npc["resistance_level"] - 1)
            
            if npc["resistance_level"] <= 0:
                npc["conversation_phase"] = "safe"
                npc["status"] = "safe"
                success = True
                response = f"Sabe de uma coisa, esse é um ponto muito bom. Você mudou minha opinião sobre isso!"
            else:
                success = False
                response = f"Interessante, mas ainda não estou totalmente convencido..."
                
        self.conversation_history[npc_id].append({
            "type": "argument",
            "argument": argument_text,
            "response": response,
            "success": success
        })
        
        # Check if game is won
        self._check_win_condition()
        
        return {
            "response": response,
            "success": success,
            "phase": npc["conversation_phase"],
            "status": npc["status"]
        }
        
    def _check_win_condition(self):
        """Check if all NPCs are safe"""
        safe_count = sum(1 for npc in self.npcs.values() if npc["status"] == "safe")
        self.game_won = safe_count == len(self.npcs)
        
    def get_game_status(self) -> Dict:
        """Get current game status"""
        safe_npcs = [npc for npc in self.npcs.values() if npc["status"] == "safe"]
        needs_convincing = [npc for npc in self.npcs.values() if npc["status"] == "needs_convincing"]
        unknown = [npc for npc in self.npcs.values() if npc["status"] == "unknown"]
        
        return {
            "game_won": self.game_won,
            "safe_count": len(safe_npcs),
            "total_npcs": len(self.npcs),
            "safe_npcs": safe_npcs,
            "needs_convincing": needs_convincing,
            "unknown": unknown
        }
        
    def get_available_arguments(self) -> List[Dict]:
        """Get list of available arguments"""
        return ARGUMENTS.copy()
        
    def get_random_arguments(self, count: int = 3) -> List[Dict]:
        """Get random arguments excluding chicoteia"""
        non_special_args = [arg for arg in ARGUMENTS if not arg.get('special', False)]
        return random.sample(non_special_args, min(count, len(non_special_args)))
