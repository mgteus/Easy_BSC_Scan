import requests


def get_token_price_by_address(address: str =' '):
    """
    Simple function to get crypto price from PancakeSwap API
    """
    url_ = "https://api.pancakeswap.info/api/v2/tokens/" + address
    x = requests.get(url_)

    x = x.json()

    price = float(x['data']['price'])

    return round(price, 2)



if __name__ == '__main__':
    address = '0x00e1656e45f18ec6747f5a8496fd39b50b38396d'
    test = '0x00e1656e45f18ec6747f5a8496fd39b50b38396d'
    #get_token_price_by_address(address=test)
    print(requests.__version__)
