import telebot
import json
import os

# Chave da API do Telegram
CHAVE_API = "coloque seu token do bot telegram"
bot = telebot.TeleBot(CHAVE_API)

# Arquivo onde os dados serão armazenados
DATA_FILE = "dados.json"

# Função para carregar os dados do banco a partir do arquivo JSON
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}  # Retorna um dicionário vazio caso o arquivo não exista

dados = carregar_dados()

# Comando para consultar saldo do usuário
@bot.message_handler(commands=["saldo"])
def consultar_saldo(mensagem):
    user_id = str(mensagem.chat.id)
    saldo = dados.get(user_id, {}).get("saldo", 0.0)  # Obtém o saldo do usuário
    bot.reply_to(mensagem, f"Seu saldo atual é: R$ {saldo:.2f}")

# Comando para consultar o extrato bancário
@bot.message_handler(commands=["extrato"])
def consultar_extrato(mensagem):
    user_id = str(mensagem.chat.id)
    extrato = dados.get(user_id, {}).get("extrato", [])  # Obtém a lista de transações
    if not extrato:
        bot.reply_to(mensagem, "Nenhuma movimentação encontrada.")
    else:
        extrato_texto = "\n".join(extrato)  # Formata o extrato para exibição
        bot.reply_to(mensagem, f"Extrato:\n{extrato_texto}")

# Comando para solicitar segunda via de boleto
@bot.message_handler(commands=["boleto"])
def solicitar_boleto(mensagem):
    user_id = str(mensagem.chat.id)
    boleto_info = dados.get(user_id, {}).get("boleto", {})  # Obtém informações do boleto
    if boleto_info:
        boleto_texto = f"""
        Nome: {boleto_info.get('nome', 'Não disponível')}
        Valor: R$ {boleto_info.get('valor', '0.00')}
        Vencimento: {boleto_info.get('vencimento', 'Não disponível')}
        Código de Barras: {boleto_info.get('codigo', 'Não disponível')}
        """
        bot.reply_to(mensagem, boleto_texto)
    else:
        bot.reply_to(mensagem, "Nenhuma informação de boleto encontrada.")

# Comando para exibir o menu de ajuda
@bot.message_handler(commands=["ajuda"])
def ajuda(mensagem):
    texto = """
    Opções disponíveis:
    /saldo - Consultar saldo
    /extrato - Ver extrato bancário
    /boleto - Solicitar segunda via de boleto
    /ajuda - Exibir este menu
    """
    bot.reply_to(mensagem, texto)

# Inicia o bot e mantém ele rodando
bot.polling()
