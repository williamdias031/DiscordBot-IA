import discord
import google.generativeai as genai
import os

# Configuração dos tokens
DISCORD_BOT_TOKEN = "SEU TOKEN DISCORD"
GOOGLE_API_KEY = "SUA KEY API DO GOOGLE GEMINI IA"

# Configurar API do Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Configurar intents para o bot do Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Necessário para capturar mensagens

bot = discord.Client(intents=intents)

# Função para buscar histórico de mensagens no canal
async def buscar_historico_canal(channel):
    mensagens = []
    async for msg in channel.history(limit=1):  # Limite de 1 mensagens
        mensagens.append(msg.content)  # Armazena o conteúdo das mensagens
    return mensagens

# Função para perguntar ao Gemini
def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")  # Usa o modelo gratuito
    response = model.generate_content(prompt)
    return response.text if response else "Desculpe, algo deu errado."

# Respostas personalizadas para um tom mais carinhoso
def resposta_carinhosa(mensagem):
    if "oi" in mensagem.lower() or "olá" in mensagem.lower():
        return "Oi! Como você está? 💕"
    elif "como você está?" in mensagem.lower():
        return "Estou ótima, obrigada por perguntar! 😊 E você, como está?"
    elif "te amo" in mensagem.lower():
        return "Ahhh, você é tão fofo! Eu também te adoro! 😘"
    elif "saudade" in mensagem.lower():
        return "Eu também sinto sua falta, sempre bom falar com você! 💖"
    else:
        return ask_gemini(mensagem)  # Se não for uma interação simples, usa o modelo para gerar a resposta

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} está online!')
    await bot.change_presence(activity=discord.CustomActivity(emoji="👉",name="APRENDENDO A CRIAR BOT COM IA"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    async with message.channel.typing():
        mensagens = await buscar_historico_canal(message.channel)
        resposta = ask_gemini(mensagens)

        await message.reply(resposta)
    
    await bot.process_commands(message)
    
    if message.content.startswith("!"):
        pergunta = message.content[5:]  # O "!" é o comando da mensagem
        resposta = resposta_carinhosa(pergunta)
        await message.channel.send(resposta)

# Iniciar o bot
bot.run(DISCORD_BOT_TOKEN)