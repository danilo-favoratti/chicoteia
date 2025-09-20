# 🎮 Giovanni's Jibber Jabber

A web-based conversation game where you must save the world from Giovanni's AI bubble theories!

## 🎯 Game Objective

Navigate a tech conference and talk to 10 NPCs. Your mission:
1. Ask each NPC if they know "Giovanni"
2. If they don't know Giovanni → They're safe ✅
3. If they know Giovanni → Ask about AI bubble opinion
4. If they think AI is NOT a bubble → They're safe ✅  
5. If they think AI IS a bubble → Convince them otherwise with arguments!
6. Use the special "chicoteia" argument (50% success rate) or other logical arguments
7. Save all NPCs to win! 🏆

## 🚀 Quick Start

1. **Set up environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

3. **Run the game:**
   ```bash
   python3 app.py
   ```

4. **Play the game:**
   - Open http://localhost:6060 in your browser
   - Works on desktop and mobile! 📱

## 🎨 Features

- **10 Unique NPCs** - Each with distinct personalities and tech backgrounds
- **AI-Powered Conversations** - Real GPT-4o-mini responses based on character personalities  
- **Pixel Art Style** - Retro gaming aesthetic with modern responsive design
- **Mobile Friendly** - Play on any device
- **Progressive Difficulty** - Some NPCs are harder to convince than others
- **Special "Chicoteia" Argument** - Mysterious word with 50% success rate!

## 🤖 NPCs You'll Meet

- **Alex Chen** - Frontend Developer (React enthusiast)
- **Maria Rodriguez** - Backend Developer (Python expert)  
- **David Kim** - DevOps Engineer (Kubernetes wizard)
- **Sarah Johnson** - Product Manager (Business strategist)
- **Tom Wilson** - UX Designer (Accessibility advocate)
- **Lisa Patel** - Data Scientist (ML researcher)
- **Mike Thompson** - Security Engineer (Paranoid but helpful)
- **Jennifer Lee** - Startup Founder (Serial entrepreneur)
- **Robert Zhang** - Tech Lead (Wise mentor)
- **Anna Kowalski** - QA Engineer (Bug hunter extraordinaire)

## 🛠️ Technical Stack

- **Backend:** Flask + Python
- **Frontend:** Vanilla HTML/CSS/JavaScript  
- **AI:** OpenAI GPT-4o-mini
- **Styling:** Custom pixel art CSS with responsive design

## 📁 Project Structure

```
chicoteia/
├── app.py              # Main Flask application
├── game_logic.py       # Game state management
├── ai_engine.py        # OpenAI integration
├── npc_data.py         # NPC profiles and data
├── templates/
│   └── index.html      # Game interface
├── static/
│   ├── css/style.css   # Pixel art styling
│   └── js/game.js      # Frontend game logic
└── requirements.txt    # Dependencies
```

## 🎮 How to Play

1. **Start at the Conference Room** - See all 10 NPCs with their avatars
2. **Click on any NPC** to start a conversation
3. **Follow the conversation flow:**
   - Ask about Giovanni
   - Ask about AI bubble (if they know Giovanni)
   - Make arguments to convince them (if needed)
4. **Use the special "chicoteia" word** strategically - it only works 50% of the time!
5. **Win when all NPCs are safe** and get the victory message! 🎉

## 🔧 Development Notes

- Game state is managed server-side with Flask sessions
- Each NPC has unique personality prompts for AI responses
- Responsive design works on desktop, tablet, and mobile
- Error handling for AI service failures with fallback responses

## 🎯 Win Condition

Successfully convince all NPCs that AI is not a bubble to see:
**"You saved the world from Giovanni's Jibber Jabber!"**

---

*Built with ❤️ for the tech community. May your conversations be ever convincing!*
