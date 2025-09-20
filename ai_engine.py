from openai import OpenAI
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self):
        self.client = OpenAI()  # api key from OPENAI_API_KEY env
        
    def generate_npc_response(self, npc: Dict, conversation_history: List[Dict], user_message: str, game_context: Dict) -> str:
        """Generate AI response for NPC based on personality and context"""
        
        # Build system prompt based on NPC personality and current game state
        system_prompt = self._build_system_prompt(npc, game_context)
        
        # Build conversation history for context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for entry in conversation_history[-5:]:  # Keep last 5 exchanges for context
            if entry.get("type") == "user_message":
                messages.append({"role": "user", "content": entry["message"]})
            elif entry.get("type") == "ai_response":
                messages.append({"role": "assistant", "content": entry["response"]})
                
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=60,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._get_fallback_response(npc, user_message)
            
    def _build_system_prompt(self, npc: Dict, game_context: Dict) -> str:
        """Build system prompt for NPC personality"""
        
        base_prompt = f"""Você é {npc['name']}, um(a) {npc['role']} numa conferência de tecnologia. 

PERSONALIDADE: {npc['personality']}
BACKGROUND: {npc['bio']}

REGRAS IMPORTANTES DO JOGO:
- Você está numa conferência de tecnologia para desenvolvedores backend e frontend
- Mantenha-se no personagem {npc['name']} o tempo todo
- Mantenha respostas com no máximo 40 palavras - seja conciso!
- Não quebre a quarta parede ou mencione que isso é um jogo
- RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO
"""

        # Add context based on conversation phase
        phase = npc.get('conversation_phase', 'initial')
        
        if phase == 'initial':
            base_prompt += "\n- Esta é sua primeira interação com esta pessoa\n- Seja amigável e profissional"
            
        elif phase == 'giovanni_check':
            if npc['knows_giovanni']:
                base_prompt += f"\n- Você conhece Giovanni e já trabalhou com ele antes\n- Você deve ficar curioso sobre por que estão perguntando sobre Giovanni"
            else:
                base_prompt += f"\n- Você não conhece ninguém chamado Giovanni\n- Você deve expressar que não reconhece o nome"
                
        elif phase == 'ai_opinion':
            base_prompt += f"\n- Seu relacionamento com Giovanni: {npc.get('giovanni_relationship', 'Você conhece Giovanni.')}"
            if npc['ai_bubble_stance'] == 'bubble':
                base_prompt += f"\n- Você acredita que o mercado de IA está numa bolha\n- Expresse ceticismo sobre as avaliações e hype da IA\n- Referencie sua experiência com Giovanni se relevante\n- Seja específico sobre por que acha que é uma bolha"
            else:
                base_prompt += f"\n- Você acredita que IA não é bolha mas está criando valor real\n- Seja otimista sobre o potencial da IA\n- Referencie sua experiência positiva com Giovanni se relevante\n- Dê exemplos específicos de valor real da IA"
                
        elif phase == 'argument_phase':
            base_prompt += f"\n- Você atualmente acha que IA é uma bolha\n- Você está aberto a ouvir argumentos mas um pouco cético\n- Você precisa de {npc.get('resistance_level', 1)} argumentos bons a mais para mudar de opinião"
            
        elif phase == 'safe':
            base_prompt += f"\n- Você foi convencido de que IA não é uma bolha\n- Seja positivo sobre a conversa e o futuro da IA"
            
        return base_prompt
        
    def _get_fallback_response(self, npc: Dict, user_message: str) -> str:
        """Fallback response when AI fails"""
        fallbacks = [
            f"Interessante! Como {npc['role']}, adoraria ouvir mais sobre sua perspectiva.",
            f"Hmm, deixe-me pensar sobre isso. Qual sua opinião?",
            f"Bom ponto! Não havia considerado por esse ângulo antes.",
            f"Forma fascinante de ver isso. Me conte mais!"
        ]
        
        import random
        return random.choice(fallbacks)
        
    def generate_ai_bubble_response(self, npc: Dict) -> str:
        """Generate AI bubble opinion response based on NPC's relationship with Giovanni"""
        try:
            if npc['ai_bubble_stance'] == 'bubble':
                prompt = f"""Como {npc['name']}, dê sua opinião sobre se o mercado de IA é uma bolha. 
                Seu relacionamento com Giovanni: {npc.get('giovanni_relationship', '')}
                Você acredita que É uma bolha. Seja específico mas muito breve.
                Mantenha sob 40 palavras e permaneça no personagem como {npc['role']}."""
            else:
                prompt = f"""Como {npc['name']}, dê sua opinião sobre se o mercado de IA é uma bolha.
                Seu relacionamento com Giovanni: {npc.get('giovanni_relationship', '')}
                Você acredita que NÃO é uma bolha. Dê exemplos breves de valor real da IA.
                Mantenha sob 40 palavras e permaneça no personagem como {npc['role']}."""
            
            system_prompt = f"""Você é {npc['name']}, um(a) {npc['role']}.
            Personalidade: {npc['personality']}
            Background: {npc['bio']}
            Responda naturalmente e conversacionalmente em português brasileiro."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI Error: {e}")
            # Fallback responses
            if npc['ai_bubble_stance'] == 'bubble':
                return "Acho que estamos numa bolha de IA. As avaliações estão loucas e todo mundo só coloca 'IA' em tudo."
            else:
                return "Não é bolha. IA está criando valor real na saúde, automação e acessibilidade."

    def generate_custom_response(self, npc: Dict, prompt: str) -> str:
        """Generate a custom response for specific game scenarios"""
        try:
            system_prompt = f"""Você é {npc['name']}, um(a) {npc['role']}. 
            Personalidade: {npc['personality']}
            Background: {npc['bio']}
            Seu relacionamento com Giovanni: {npc.get('giovanni_relationship', 'Você pode ou não conhecer Giovanni.')}
            
            Responda no personagem, mantendo sob 40 palavras em português brasileiro."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI Error: {e}")
            return "Isso é muito interessante! Adoraria continuar essa conversa."
