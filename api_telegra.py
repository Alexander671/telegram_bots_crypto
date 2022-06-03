
import logging

from telebot import TeleBot

TG_TOKEN = "5500391029:AAG_jTkhQsuZvtx11F0G_09AD-Th4kNYlvA"
CRYPTO_RANK_TOKEN = "33b8ddcdbd654e7d58bbd4b83692ecf2474397af0f2be2141bd666dd97ab"

from requests import get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

logging.basicConfig(level=logging.NOTSET)


# Initialize bot and dispatcher
bot = TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'''Hi!
I'm Multicurrency information bot.
📈 for information about currencies such as - BTC, TON, ETH, USDC type /BTC, /USDT or other ticker.
⏱ for choose the period when the check will take place, if the price has changed by a given percentage, type /scheduler''')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f'''
Available commands:
- Rates
  - /btc
  - /usdc
  - /etc
  - /ton
- Schedule
  - /schedule
- Other
  - /start
  - /help
    ''')

def get_ticker_rate(id):
    
    url = f'https://api.cryptorank.io/v1/currencies/{id}'
    parameters = {
        'api_key' : CRYPTO_RANK_TOKEN, 
    }
    try:
        response = get(url, params=parameters)
        response.close()
        data = json.loads(response.text)
        return(data["data"]["values"]["USD"]["price"])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      return(e)

# symbol to id in crypto rank API
symbol_to_id = {'BTC':1, 'ETH' : 2, 'TON' : 174251, 'USDC' : 5487}

@bot.message_handler(commands=["btc", "eth", "usdc", "ton"])
def cmd_ton(message):
    cryptocurrency = message.text[1:].upper()
    bot.send_message(message.chat.id, f"Current rate of {cryptocurrency} is \n {str(get_ticker_rate((symbol_to_id[cryptocurrency])))}")

bot.infinity_polling()