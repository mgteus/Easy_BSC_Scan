import regex as re

def create_coingecko_list(): 
    x = ''
    with open('coingecko_list.csv', 'r') as file:
        x = file.read()

    pattern = r"(?P<key>\"[id]*[symbol]*[name]*\"):\s*(?P<value>\"[\w*\d*\.*\-*\s*\,*\(*\)*\[*\]*\!*\:*\$*\#*\/*\'*\%*\+*\&*\\*]*\")"
    re_result = re.findall(pattern=pattern, string=x,)

    with open('coin_gecko_list.csv', 'w') as file:
        for i in range(int(len(re_result)/3)):
            id =  re_result[3*i][1].replace("'", "").replace('""', "" )
            name = re_result[3*i+2][1].replace("'", "").replace('""', "" )
            symbol = re_result[3*i+1][1].replace("'", "").replace('""', "" )
            file.write(f'{symbol},{id}\n')
    
    return

def get_coingecko_dict():
    """
    Simple funtion to get the dictionary from coingeckoAPI.csv
    """

    my_dict = {}

    with open('coin_gecko_list.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            sym, id = line.replace('"', "").replace('\n', '').split(',')
            
            my_dict[sym] = id
    
    return my_dict
    

if __name__ == '__main__':

    print(get_coingecko_dict())

