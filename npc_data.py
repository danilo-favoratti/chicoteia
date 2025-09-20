# Dados dos NPCs para o jogo Giovanni's Jibber Jabber

NPCS = [
    {
        "id": "alex_frontend",
        "name": "Alexandre Silva",
        "role": "Desenvolvedor Frontend",
        "personality": "Desenvolvedor React entusiasmado que ama frameworks modernos. Sempre animado com as últimas tendências do JavaScript. Fala com energia e usa jargões técnicos.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni me orientou numa startup há 3 anos. Me ensinou padrões React mas sempre alertou sobre o hype da IA.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 2,  # Quantos argumentos necessários para convencer
        "avatar_color": "#FF6B6B",
        "bio": "5 anos construindo SPAs, atualmente obcecado por Next.js"
    },
    {
        "id": "maria_backend",
        "name": "Maria Santos", 
        "role": "Desenvolvedora Backend",
        "personality": "Desenvolvedora Python pragmática focada em arquitetura escalável. Cautelosa com novas tecnologias, prefere soluções comprovadas. Fala metodicamente.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni foi meu colega de quarto na faculdade. Sempre sonhava com tecnologia futura enquanto eu focava no básico. Perdemos contato quando ele entrou num lab de IA.",
        "ai_bubble_stance": "bubble", 
        "resistance_level": 3,
        "avatar_color": "#4ECDC4",
        "bio": "10 anos em backend, especialista Django, defensor de microsserviços"
    },
    {
        "id": "david_devops",
        "name": "David Oliveira",
        "role": "Engenheiro DevOps", 
        "personality": "Entusiasta de infraestrutura em nuvem que acha que tudo deve ser containerizado. Ama automação e eficiência. Comunicador direto.",
        "knows_giovanni": False,
        "giovanni_relationship": "Nunca ouvi falar de Giovanni. Foco em infraestrutura, não em pessoal de IA.",
        "ai_bubble_stance": "not_bubble",
        "resistance_level": 0,
        "avatar_color": "#45B7D1",
        "bio": "Mago do Kubernetes, certificado AWS, obcecado por automação"
    },
    {
        "id": "sarah_pm",
        "name": "Sarah Costa",
        "role": "Gerente de Produto",
        "personality": "Focada em negócios, sempre pensando nas necessidades dos usuários e tendências de mercado. Diplomática e estratégica nas conversas. Usa terminologia empresarial.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni apresentou sua startup de IA para nós ano passado. Cara inteligente, mas otimista demais. Recusamos suas projeções tipo bolha.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 2,
        "avatar_color": "#96CEB4",
        "bio": "Ex-consultora, agora liderando estratégia de produto para B2B SaaS"
    },
    {
        "id": "tom_ux",
        "name": "Tom Pereira",
        "role": "Designer UX",
        "personality": "Designer centrado no usuário que se preocupa profundamente com acessibilidade e experiência do usuário. Criativo e empático. Fala sobre psicologia humana.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni me contratou para sua ferramenta de IA para acessibilidade há 2 anos. Visão brilhante para ajudar usuários com deficiência. Realmente entende IA centrada no humano.",
        "ai_bubble_stance": "not_bubble", 
        "resistance_level": 0,
        "avatar_color": "#FFEAA7",
        "bio": "Especialista em design systems, defensor da acessibilidade, nerd de pesquisa com usuários"
    },
    {
        "id": "lisa_data",
        "name": "Lisa Ferreira",
        "role": "Cientista de Dados",
        "personality": "Entusiasta de ML que vê padrões em tudo. Analítica e baseada em evidências. Adora discutir algoritmos e modelos estatísticos.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni foi meu parceiro de pesquisa no doutorado. Co-autor de 3 artigos sobre redes neurais. Brilhante, mas deixou a academia pelo venture capital. Perdeu o foco da ciência pelo hype.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 3,
        "avatar_color": "#DDA0DD",
        "bio": "PhD em ML, construindo sistemas de recomendação e modelos NLP"
    },
    {
        "id": "mike_security",
        "name": "Miguel Almeida", 
        "role": "Engenheiro de Segurança",
        "personality": "Paranoico com ameaças de segurança, mas de forma positiva. Sempre pensando no que pode dar errado. Comunicador cauteloso e minucioso.",
        "knows_giovanni": False,
        "giovanni_relationship": "Giovanni? Não me lembra ninguém. Foco em ameaças de segurança, não em personalidades da IA.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 4,
        "avatar_color": "#FF7675",
        "bio": "Especialista em testes de invasão, defensor de arquitetura zero-trust"
    },
    {
        "id": "jen_founder",
        "name": "Jennifer Rodrigues",
        "role": "Fundadora de Startup",
        "personality": "Empreendedora otimista que acredita que a tecnologia pode mudar o mundo. Alta energia, pensamento visionário. Fala sobre disrupção e inovação.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni é meu co-investidor em duas startups de IA! Nos conhecemos no TechCrunch Disrupt 2022. Visão incrível para aplicações revolucionárias de IA. Planejando nosso terceiro investimento.",
        "ai_bubble_stance": "not_bubble",
        "resistance_level": 0,
        "avatar_color": "#74B9FF", 
        "bio": "Empreendedora serial, 2 exits, atualmente construindo startup fintech"
    },
    {
        "id": "robert_lead",
        "name": "Roberto Souza",
        "role": "Tech Lead",
        "personality": "Desenvolvedor experiente que viu muitos ciclos de tecnologia. Perspectiva equilibrada sobre novas tecnologias. Focado em mentoria, fala sabiamente.",
        "knows_giovanni": True,
        "giovanni_relationship": "Giovanni foi meu desenvolvedor júnior há 8 anos. Garoto ansioso, sempre perguntando sobre tecnologia futura. Ensinei design de sistemas, mas ele se envolveu na corrida do ouro da IA.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 2,
        "avatar_color": "#A29BFE",
        "bio": "15 anos em tech, liderou equipes em 3 unicornios, especialista em arquitetura"
    },
    {
        "id": "anna_qa",
        "name": "Ana Carvalho",
        "role": "Engenheira QA", 
        "personality": "Testadora orientada a detalhes que encontra bugs que outros perdem. Metódica e minuciosa. Faz perguntas investigativas e pensa em casos extremos.",
        "knows_giovanni": False,
        "giovanni_relationship": "Giovanni? Não conheço ninguém com esse nome. Interajo principalmente com desenvolvedores e equipes de produto, não pessoal de IA.",
        "ai_bubble_stance": "bubble",
        "resistance_level": 3,
        "avatar_color": "#FD79A8",
        "bio": "Especialista em testes de automação, caçadora de bugs, obcecada por qualidade"
    }
]

# Argumentos que podem ser usados para convencer NPCs
ARGUMENTS = [
    {
        "text": "chicoteia",
        "description": "A palavra mágica que tem 50% de chance de funcionar",
        "success_rate": 0.5,
        "special": True
    },
    {
        "text": "IA está salvando vidas na medicina com diagnósticos mais precisos",
        "description": "Argumento da saúde",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "Grandes empresas estão integrando IA nas operações principais, não experimentando",
        "description": "Argumento empresarial",
        "success_rate": 0.4,
        "special": False
    },
    {
        "text": "IA está automatizando tarefas repetitivas, liberando humanos para trabalho criativo",
        "description": "Argumento de automação",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "Assistentes de IA estão ajudando pessoas com deficiência a navegar no mundo",
        "description": "Argumento de acessibilidade",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "IA está otimizando energia e reduzindo desperdício em data centers globais",
        "description": "Argumento ambiental",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "Carros autônomos estão reduzindo acidentes de trânsito significativamente",
        "description": "Argumento de segurança no trânsito",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "IA está democratizando educação com tutores personalizados para todos",
        "description": "Argumento educacional",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "Sistemas de IA estão detectando fraudes financeiras em tempo real",
        "description": "Argumento de segurança financeira",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "IA está acelerando descobertas científicas em anos, não décadas",
        "description": "Argumento científico",
        "success_rate": 0.4,
        "special": False
    },
    {
        "text": "Tradução instantânea de IA está conectando culturas globalmente",
        "description": "Argumento cultural",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "IA está otimizando cadeias de suprimentos, reduzindo custos para consumidores",
        "description": "Argumento econômico",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "Modelos de IA estão prevendo desastres naturais com mais precisão",
        "description": "Argumento de prevenção",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "IA está personalizando tratamentos médicos para cada paciente individual",
        "description": "Argumento de medicina personalizada",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "Robôs com IA estão cuidando de idosos, resolvendo crise demográfica",
        "description": "Argumento demográfico",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "IA está criando novos empregos em áreas que nem existiam antes",
        "description": "Argumento de criação de empregos",
        "success_rate": 0.35,
        "special": False
    },
    {
        "text": "Sistemas de IA estão melhorando segurança cibernética contra ataques",
        "description": "Argumento de cibersegurança",
        "success_rate": 0.4,
        "special": False
    },
    {
        "text": "IA está ajudando agricultores a produzir mais comida com menos recursos",
        "description": "Argumento agrícola",
        "success_rate": 0.3,
        "special": False
    },
    {
        "text": "Assistentes de código IA estão acelerando desenvolvimento de software",
        "description": "Argumento de produtividade",
        "success_rate": 0.35,
        "special": False
    }
]
