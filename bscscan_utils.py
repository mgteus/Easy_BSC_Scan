import asyncio
from datetime import datetime
import pandas as pd
import platform
import bscscan
import requests
import time
from bscscan import BscScan
from pycoingecko import CoinGeckoAPI
from regex_utils import get_coingecko_dict



from pancake_api import get_token_price_by_address

YOUR_API_KEY = "KFASP5HBW6XAF8SJCIANDKF6MCSI6G83FZ"

def read_txt():
    """
    Function to read the txt file with wallet information
    """
    path = r'C:\Users\mateu\Desktop\wallet_address.txt'

    with open(path, 'r') as file:
        x = file.read()

    return x



def get_token_price_at_date(token: str = '', 
                            date: str = ''):
    """
    Simple function to get the token price at specific date with
    coin gecko API by token and date

    date format = %d-%m-%Y
    """
    cg = CoinGeckoAPI()
    times = 0
    while times < 35:
        try:
            price = cg.get_coin_history_by_id(id=token, date=date,
                    localization=False)['market_data']['current_price']['usd']
            break
        except:
            time.sleep(1)
            times += 1

    return price


async def get_address_trades(address: str = '',
                api_key: str = "KFASP5HBW6XAF8SJCIANDKF6MCSI6G83FZ"):
    """
    Function to read information of the given wallet address 
    """
    coin_gecko_dict = get_coingecko_dict()

    my_dict = {'DATE':[],
               'SIDE':[],
               'TOKEN':[],
               'QUANTITY':[],            
               'TOKEN_PRICE_TODAY':[],
               'TOTAL_USD':[]}

    async with BscScan(api_key) as client:
        
        infos = await client.get_bep20_token_transfer_events_by_address(
                address=address,
                startblock=0,
                endblock=999999999,
                sort="desc")

        for trade in infos:
            try:
                # defining date
                date = datetime.fromtimestamp(float(trade['timeStamp'])).strftime(r'%Y-%m-%d')
                date_coingecko = datetime.fromtimestamp(float(trade['timeStamp'])).strftime(r'%d-%m-%Y')
                # defining side 
                if address.upper() == trade['from'].upper():
                    side = 'OUT'
                else:
                    side = 'IN'
                # defining token
                token = trade['tokenSymbol']

                # getting coingecko id by token
                if token.lower() in coin_gecko_dict:
                    coingecko_id = coin_gecko_dict[token.lower()]
                    # getting price at date
                    token_price_at_date = get_token_price_at_date(token=coingecko_id,
                                                                date=date_coingecko)

                else:   # dealing with these ad-coins
                    coingecko_id = 'busd'
                    token_price_at_date = 1.0

                    


                # defining quantity
                quantity = f"{float(trade['value'])/10**float(trade['tokenDecimal']):.8f}"

                # defining price 
                token_price = get_token_price_by_address(address=trade['contractAddress'])

                # defining total in USD today
                # trade_price_usd = round(float(quantity)*token_price, 2)

                # definig total in USD at date
                trade_price_at_date = round(float(quantity)*float(token_price_at_date), 2)


                my_dict['DATE'].append(date)
                my_dict['SIDE'].append(side)
                my_dict['TOKEN'].append(token)
                my_dict['QUANTITY'].append(quantity[:7])
                my_dict['TOKEN_PRICE_TODAY'].append(token_price)
                my_dict['TOTAL_USD'].append(trade_price_at_date)
                #my_dict['TOTAL USD'].append(trade_price_usd)

                

            except Exception as e:
                print(e)
                print(trade)

    return my_dict



def show_df_of_adress_trades(address: list or str = [],
                            init_date: datetime or str = datetime(2021,6,1),
                            final_date:datetime or str = datetime.today()):
    """
    Function which shows a pd.DataFrame of the given addresses
    """
    trade_df = pd.DataFrame()
    if isinstance(address, str):
        address = [address]

    for wallet in address: # wallets address loop
        if platform.system()=='Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        try:

            wallet_trades = asyncio.run(get_address_trades(address=wallet))
            trade_df = pd.DataFrame.from_dict(wallet_trades)
            

        except Exception as e: 
            trade_df = e
        
    return trade_df



"""
[DEIXAR ALGUNS JOGOS PRE DEFINIDOS]
"""



if __name__ == '__main__':

    wallet_address = "0x83A2977e85A439461F9d36D48E3bF66525DDC1B3"
    wall = '0x83a2977e85a439461f9d36d48e3bf66525ddc1b3'

    print(show_df_of_adress_trades(address=wallet_address))


    #x = requests.get("https://api.coingecko.com/api/v3/coins/list")
    #response.setCharacterEncoding("utf-8")




    #print(get_token_current_price())
