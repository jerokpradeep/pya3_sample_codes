from pya3 import *
alice = Aliceblue(user_id='',api_key='')
print(alice.get_session_id())

exchange = "NFO"
symbol = "NIFTY"

print("Exchange :",exchange)
print("Symbol :",symbol)


try:
    contract_master= pd.read_csv(exchange+'.csv')
except:
    alice.get_contract_master(exchange)
    contract_master = pd.read_csv(exchange + '.csv')

banknifty_all_contract=contract_master[contract_master['Symbol']==symbol]

banknifty_expiry = banknifty_all_contract['Expiry Date'].sort_values().drop_duplicates().reset_index(drop = True)

print("Current weekly expiry :",banknifty_expiry[0])

current_month_expiry = None

for i in range(len(banknifty_expiry)):
    if exchange == 'CDS':
        if datetime.strptime(banknifty_expiry[i],'%d-%m-%Y').strftime('%m') == datetime.now().strftime('%m'):
            current_month_expiry=banknifty_expiry[i]
    else:
        if datetime.strptime(banknifty_expiry[i],'%Y-%m-%d').strftime('%m') == datetime.now().strftime('%m'):
            current_month_expiry=banknifty_expiry[i]

print("Current Month expiry :",current_month_expiry)


