import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from bscscan_utils import show_df_of_adress_trades


def WebApp():
    """
    Streamlit WebApp Function
    """

    st.set_page_config(page_title='BSC Scan', page_icon="📊")

    menu = ['Welcome Page', 'Easy Scan', 'About']

    tab = st.sidebar.selectbox('Menu', menu)

    if tab == 'Welcome Page':
        st.subheader('Welcome to Easy BSC Scan WebApp')
        st.subheader('A basic WebApp to check the transactions '\
                    +'of the given wallet address ' \
                    +'based on the Binance Smart Chain.')

        st.markdown('***Select the Easy Scan tab to procede to the application.***')
        
        st.markdown('***Beta Version 1.0.0***')
    elif tab == 'Easy Scan':
        st.subheader('EasyScan App')
        st.markdown('Write at the text input below ' \
                    + 'the wallet address which you want to' \
                    + 'check the trade history out')

        wallet_address = st.text_area('Text Input',
                            placeholder='0x0000000000000000000000000')


        if st.checkbox('Check Transactions'):
            df = show_df_of_adress_trades(address=wallet_address)

            if isinstance(df, str):
                st.error("Can't resolve the information of the given address, sorry...")
                st.warning(df)
            elif isinstance(df, pd.DataFrame):
                AgGrid(df, fit_columns_on_grid_load=True, theme='streamlit')
                st.markdown("ps: The total USD value is based on the current token value, not the token value at transaction date. ")
                st.markdown("ps2: There is a chance of some ad-token transactions to appear in the address history. Don't worry, they are not real.")

    elif tab == "About":
        st.subheader('WebApp developed by [@mgteus](https://github.com/mgteus)')
        st.markdown('Source Code avaible at [EasyScan](https://github.com/mgteus/Easy_BSC_Scan)', unsafe_allow_html=True)

        st.text('Table with accurate prices coming soon')

        

if __name__ == '__main__':
    WebApp()
    # """ 
    #     Use CoinGeckoAPI to get token price at transaction date.
    #     https://algotrading101.com/learn/coingecko-api-guide/
    # """
        

