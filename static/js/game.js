// Giovanni's Jibber Jabber - Game JavaScript

class Game {
    constructor() {
        this.currentNpc = null;
        this.gameData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.startNewGame();
    }

    bindEvents() {
        // Back button
        document.getElementById('backBtn').addEventListener('click', () => {
            this.showConferenceRoom();
        });

        // Play again button
        document.getElementById('playAgainBtn').addEventListener('click', () => {
            this.startNewGame();
            this.hideModal();
        });

        // Send message button
        document.getElementById('sendMessageBtn').addEventListener('click', () => {
            this.sendCustomMessage();
        });

        // Enter key for message input
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendCustomMessage();
            }
        });

        // ESC key to return to conference room
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Only work if we're in a conversation (chat interface is visible)
                const chatInterface = document.getElementById('chatInterface');
                if (chatInterface.style.display === 'flex') {
                    this.showConferenceRoom();
                }
            }
        });
    }

    async startNewGame() {
        // Track game start
        if (typeof gtag !== 'undefined') {
            gtag('event', 'game_start', {
                event_category: 'game',
                event_label: 'new_game'
            });
        }
        
        this.showLoading();
        try {
            const response = await fetch('/api/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            if (data.success) {
                this.gameData = data;
                this.renderNPCs(data.npcs);
                this.updateProgress(data.status);
                this.showConferenceRoom();
            }
        } catch (error) {
            console.error('Failed to start game:', error);
            alert('Falha ao iniciar jogo. Por favor, atualize e tente novamente.');
        } finally {
            this.hideLoading();
        }
    }

    renderNPCs(npcs) {
        const grid = document.getElementById('npcsGrid');
        grid.innerHTML = '';

        npcs.forEach(npc => {
            const card = document.createElement('div');
            card.className = `npc-card ${npc.status}`;
            
            // Debug: Log each NPC status
            console.log(`NPC ${npc.name} status: ${npc.status}`);
            
            // Determine status icon and class
            let statusIcon = '?';
            let statusClass = 'danger';
            
            if (npc.status === 'safe') {
                statusIcon = '✅';
                statusClass = 'safe';
            } else if (npc.status === 'needs_convincing') {
                statusIcon = '💬';
                statusClass = 'needs-convincing';
            }
            
            // Check if NPC has a custom avatar image
            let avatarContent = `${npc.name.charAt(0)}`;
            let avatarStyle = `background-color: ${npc.avatar_color}`;
            
            const customAvatars = {
                'alex_frontend': 'alexandre.jpg',
                'david_devops': 'david.jpg', 
                'maria_backend': 'maria.jpg',
                'sarah_pm': 'sarah.jpg',
                'tom_ux': 'tom.jpg',
                'lisa_data': 'lisa.jpg',
                'mike_security': 'miguel.jpg',
                'jen_founder': 'jennifer.jpg',
                'robert_lead': 'roberto.jpg',
                'anna_qa': 'ana.jpg'
            };
            
            if (customAvatars[npc.id]) {
                avatarContent = `<img src="/static/images/avatars/${customAvatars[npc.id]}" alt="${npc.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
                avatarStyle = 'background-color: transparent';
            }
            
            card.innerHTML = `
                <div class="npc-avatar" style="${avatarStyle}">
                    ${avatarContent}
                </div>
                <div class="npc-name">${npc.name}</div>
                <div class="npc-role">${npc.role}</div>
                <div class="npc-bio">${npc.bio}</div>
                <div class="status-indicator ${statusClass}">
                    ${statusIcon}
                </div>
            `;
            
            card.addEventListener('click', () => {
                this.startConversation(npc.id);
            });
            
            grid.appendChild(card);
        });
    }

    async startConversation(npcId) {
        // Track conversation start
        if (typeof gtag !== 'undefined') {
            gtag('event', 'conversation_start', {
                event_category: 'game',
                event_label: npcId
            });
        }
        
        this.showLoading();
        try {
            const response = await fetch(`/api/start_conversation/${npcId}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            this.currentNpc = data.npc;
            this.showChatInterface();
            this.updateChatHeader();
            this.hideLoading();
            
            // Show typing for initial greeting
            this.showTyping();
            await this.simulateTypingDelay(data.message);
            this.hideTyping();
            
            this.addMessage('npc', data.message);
            await this.updateChatActions(data.phase);
        } catch (error) {
            console.error('Failed to start conversation:', error);
            alert('Falha ao iniciar conversa. Por favor, tente novamente.');
            this.hideLoading();
        }
    }

    async askAboutGiovanni() {
        // Track Giovanni question
        if (typeof gtag !== 'undefined') {
            gtag('event', 'ask_giovanni', {
                event_category: 'game',
                event_label: this.currentNpc
            });
        }
        
        this.addMessage('user', 'Você conhece o Giovanni?');
        this.showTyping();
        
        try {
            const response = await fetch(`/api/ask_giovanni/${this.currentNpc.id}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            // Simulate typing time based on response length
            await this.simulateTypingDelay(data.response);
            
            this.hideTyping();
            this.addMessage('npc', data.response);
            
            if (data.status === 'safe') {
                this.addMessage('system', '✅ Este NPC está seguro! Não conhece Giovanni.');
                await this.updateChatActions('safe');
            } else {
                await this.updateChatActions(data.phase);
            }
            
            await this.refreshGameStatus();
        } catch (error) {
            console.error('Failed to ask about Giovanni:', error);
            this.hideTyping();
            this.addMessage('system', 'Failed to get response. Please try again.');
        }
    }

    async askAIOpinion() {
        // Track AI opinion question
        if (typeof gtag !== 'undefined') {
            gtag('event', 'ask_ai_opinion', {
                event_category: 'game',
                event_label: this.currentNpc
            });
        }
        
        this.addMessage('user', 'O que você acha do mercado de IA? É uma bolha?');
        this.showTyping();
        
        try {
            const response = await fetch(`/api/ask_ai_opinion/${this.currentNpc.id}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            // For AI responses, simulate a slightly longer typing time
            const extraDelay = 500; // Extra delay for "thinking"
            await this.simulateTypingDelay(data.response);
            await new Promise(resolve => setTimeout(resolve, extraDelay));
            
            this.hideTyping();
            this.addMessage('npc', data.response);
            
            if (data.status === 'safe') {
                this.addMessage('system', '✅ Este NPC está seguro! Não acha que IA é uma bolha.');
                await this.updateChatActions('safe');
            } else {
                await this.updateChatActions(data.phase);
            }
            
            await this.refreshGameStatus();
        } catch (error) {
            console.error('Failed to ask AI opinion:', error);
            this.hideTyping();
            this.addMessage('system', 'Failed to get response. Please try again.');
        }
    }

    async makeArgument(argumentText) {
        // Track argument made
        if (typeof gtag !== 'undefined') {
            gtag('event', 'make_argument', {
                event_category: 'game',
                event_label: this.currentNpc,
                custom_parameters: {
                    argument_type: argumentText === 'chicoteia' ? 'special' : 'regular'
                }
            });
        }
        
        this.addMessage('user', argumentText);
        this.showTyping();
        
        try {
            const response = await fetch(`/api/make_argument/${this.currentNpc.id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ argument: argumentText })
            });
            
            const data = await response.json();
            
            // Simulate typing time based on response length
            await this.simulateTypingDelay(data.response);
            
            this.hideTyping();
            this.addMessage('npc', data.response);
            
            if (data.success) {
                this.addMessage('system', '✅ Argumento bem-sucedido! NPC foi convencido.');
                await this.updateChatActions('safe');
            } else {
                this.addMessage('system', '❌ Argumento não os convenceu. Tente novamente!');
                await this.updateChatActions(data.phase);
            }
            
            await this.refreshGameStatus();
        } catch (error) {
            console.error('Failed to make argument:', error);
            this.hideTyping();
            this.addMessage('system', 'Failed to get response. Please try again.');
        }
    }

    async sendCustomMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        input.value = '';
        this.addMessage('user', message);
        this.showTyping();
        
        try {
            const response = await fetch(`/api/chat/${this.currentNpc.id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            // For custom AI responses, add extra thinking time
            const extraDelay = 700; // Extra delay for AI processing
            await this.simulateTypingDelay(data.response);
            await new Promise(resolve => setTimeout(resolve, extraDelay));
            
            this.hideTyping();
            this.addMessage('npc', data.response);
        } catch (error) {
            console.error('Failed to send message:', error);
            this.hideTyping();
            this.addMessage('system', 'Falha ao enviar mensagem. Por favor, tente novamente.');
        }
    }

    async updateChatActions(phase) {
        const actions = document.getElementById('chatActions');
        const customInput = document.getElementById('customMessageInput');
        
        actions.innerHTML = '';
        customInput.style.display = 'none';
        
        switch (phase) {
            case 'initial':
                actions.innerHTML = `
                    <button class="action-btn" onclick="game.askAboutGiovanni()">
                        Perguntar sobre Giovanni
                    </button>
                    <button class="action-btn secondary" onclick="game.showCustomInput()">
                        Conversar livremente
                    </button>
                `;
                break;
                
            case 'ai_opinion':
                actions.innerHTML = `
                    <button class="action-btn" onclick="game.askAIOpinion()">
                        Perguntar sobre bolha de IA
                    </button>
                    <button class="action-btn secondary" onclick="game.showCustomInput()">
                        Conversar livremente
                    </button>
                `;
                break;
                
            case 'argument_phase':
                await this.loadRandomArguments(actions);
                break;
                
            case 'safe':
                actions.innerHTML = `
                    <button class="action-btn" onclick="game.showConferenceRoom()">
                        ← Voltar à Conferência
                    </button>
                    <button class="action-btn secondary" onclick="game.showCustomInput()">
                        Continuar conversando
                    </button>
                `;
                break;
        }
    }

    async loadRandomArguments(actionsElement) {
        try {
            const response = await fetch('/api/random_arguments');
            const randomArgs = await response.json();
            
            let buttonsHtml = `
                <button class="action-btn special" onclick="game.makeArgument('chicoteia')">
                    🎯 Dizer "chicoteia"
                </button>
            `;
            
            // Add 3 random argument buttons
            randomArgs.forEach(arg => {
                const escapedArg = arg.text.replace(/'/g, "\\'");
                buttonsHtml += `
                    <button class="action-btn" onclick="game.makeArgument('${escapedArg}')" title="${arg.description}">
                        ${arg.description}
                    </button>
                `;
            });
            
            buttonsHtml += `
                <button class="action-btn secondary" onclick="game.showCustomInput()">
                    Argumento personalizado
                </button>
            `;
            
            actionsElement.innerHTML = buttonsHtml;
            
        } catch (error) {
            console.error('Failed to load random arguments:', error);
            // Fallback to static arguments
            actionsElement.innerHTML = `
                <button class="action-btn special" onclick="game.makeArgument('chicoteia')">
                    🎯 Dizer "chicoteia"
                </button>
                <button class="action-btn" onclick="game.makeArgument('IA está salvando vidas na medicina com diagnósticos mais precisos')">
                    Argumento da saúde
                </button>
                <button class="action-btn" onclick="game.makeArgument('Grandes empresas estão integrando IA nas operações principais, não experimentando')">
                    Argumento empresarial
                </button>
                <button class="action-btn secondary" onclick="game.showCustomInput()">
                    Argumento personalizado
                </button>
            `;
        }
    }

    showCustomInput() {
        document.getElementById('customMessageInput').style.display = 'flex';
        document.getElementById('messageInput').focus();
    }

    addMessage(type, text) {
        const messages = document.getElementById('chatMessages');
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    updateChatHeader() {
        document.getElementById('chatNpcName').textContent = this.currentNpc.name;
        document.getElementById('chatNpcRole').textContent = this.currentNpc.role;
        
        const avatar = document.getElementById('chatNpcAvatar');
        
        const customAvatars = {
            'alex_frontend': 'alexandre.jpg',
            'david_devops': 'david.jpg',
            'maria_backend': 'maria.jpg', 
            'sarah_pm': 'sarah.jpg',
            'tom_ux': 'tom.jpg',
            'lisa_data': 'lisa.jpg',
            'mike_security': 'miguel.jpg',
            'jen_founder': 'jennifer.jpg',
            'robert_lead': 'roberto.jpg',
            'anna_qa': 'ana.jpg'
        };
        
        if (customAvatars[this.currentNpc.id]) {
            avatar.style.backgroundColor = 'transparent';
            avatar.innerHTML = `<img src="/static/images/avatars/${customAvatars[this.currentNpc.id]}" alt="${this.currentNpc.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
        } else {
            avatar.style.backgroundColor = this.currentNpc.avatar_color;
            avatar.textContent = this.currentNpc.name.charAt(0);
            avatar.innerHTML = '';
        }
    }

    async refreshGameStatus() {
        try {
            const response = await fetch('/api/game_status');
            const status = await response.json();
            this.updateProgress(status);
            
            if (status.game_won) {
                setTimeout(() => {
                    this.showWinModal();
                }, 1000);
            }
        } catch (error) {
            console.error('Failed to refresh game status:', error);
        }
    }

    updateProgress(status) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        const percentage = (status.safe_count / status.total_npcs) * 100;
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = `${status.safe_count}/${status.total_npcs} NPCs Seguros`;
        
        // Debug: Log the status to see what we're getting
        console.log('Game Status Update:', status);
        
        // Always update NPC cards with latest status - they'll be visible when user returns to conference room
        this.renderNPCs([...status.safe_npcs, ...status.needs_convincing, ...status.unknown]);
    }

    showConferenceRoom() {
        document.getElementById('conferenceRoom').style.display = 'block';
        document.getElementById('chatInterface').style.display = 'none';
        document.getElementById('chatMessages').innerHTML = '';
    }

    showChatInterface() {
        document.getElementById('conferenceRoom').style.display = 'none';
        document.getElementById('chatInterface').style.display = 'flex';
    }

    showWinModal() {
        // Track game completion
        if (typeof gtag !== 'undefined') {
            gtag('event', 'game_complete', {
                event_category: 'game',
                event_label: 'victory'
            });
        }
        
        document.getElementById('winModal').style.display = 'flex';
    }

    hideModal() {
        document.getElementById('winModal').style.display = 'none';
    }

    showLoading() {
        document.getElementById('loading').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showTyping() {
        const messages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <span>${this.currentNpc.name} está digitando</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        messages.appendChild(typingDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async simulateTypingDelay(text) {
        // Calculate typing delay based on text length
        // Average typing speed: ~40-60 WPM (words per minute)
        // That's roughly 200-300 characters per minute, or 3-5 chars per second
        
        const baseDelay = 600; // Minimum delay (ms)
        const typingSpeed = 35; // Characters per second (faster for shorter messages)
        const maxDelay = 2000; // Maximum delay (ms)
        
        const textLength = text.length;
        const calculatedDelay = Math.min(baseDelay + (textLength * (1000 / typingSpeed)), maxDelay);
        
        return new Promise(resolve => {
            setTimeout(resolve, calculatedDelay);
        });
    }
}

// Initialize game when page loads
let game;
document.addEventListener('DOMContentLoaded', () => {
    game = new Game();
});
