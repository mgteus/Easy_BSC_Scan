import asyncio
from datetime import datetime
import pandas as pd
import platform
import bscscan
from bscscan import BscScan


from pancake_api import get_token_price_by_address

YOUR_API_KEY = "KFASP5HBW6XAF8SJCIANDKF6MCSI6G83FZ"

# async def main():
#     async with BscScan(YOUR_API_KEY) as bsc:
#         print(await bsc.get_bnb_balance(address="0x83A2977e85A439461F9d36D48E3bF66525DDC1B3"))
#     return

def read_txt():
    """
    Function to read the txt file with wallet information
    """
    path = r'C:\Users\mateu\Desktop\wallet_address.txt'

    with open(path, 'r') as file:
        x = file.read()

    return x


async def get_address_trades(address: str = '',
                api_key: str = "KFASP5HBW6XAF8SJCIANDKF6MCSI6G83FZ"):
    """
    Function to read information of the given wallet address 
    """
    my_dict = {'DATE':[],
               'SIDE':[],
               'TOKEN':[],
               'QUANTITY':[],
               'TOKEN_PRICE':[],
               'TOTAL USD':[]}

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
                # defining side 
                if address.upper() == trade['from'].upper():
                    side = 'OUT'
                else:
                    side = 'IN'
                # defining token
                token = trade['tokenSymbol']

                # defining quantity
                quantity = f"{float(trade['value'])/10**float(trade['tokenDecimal']):.8f}"

                # defining price 
                token_price = get_token_price_by_address(address=trade['contractAddress'])

                # defining total in USD
                trade_price_usd = round(float(quantity)*token_price, 2)


                my_dict['DATE'].append(date)
                my_dict['SIDE'].append(side)
                my_dict['TOKEN'].append(token)
                my_dict['QUANTITY'].append(quantity[:7])
                my_dict['TOKEN_PRICE'].append(token_price)
                my_dict['TOTAL USD'].append(trade_price_usd)

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

            wallet_addres_1 = asyncio.run(get_address_trades(address=wallet))
            trade_df = pd.DataFrame.from_dict(wallet_addres_1)
            

        except Exception as e: 
            trade_df = e
        
    return trade_df



"""
[DEIXAR ALGUNS JOGOS PRE DEFINIDOS]
"""



if __name__ == '__main__':

    wallet_address = "0x83A2977e85A439461F9d36D48E3bF66525DDC1B3"
    wall = '0x83a2977e85a439461f9d36d48e3bf66525ddc1b3'

    #show_df_of_adress_trades(address=wallet_address)

    print(bscscan.__version__)
