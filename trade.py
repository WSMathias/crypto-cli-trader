#!/usr/bin/env python
"""
This program to provide cli for https://bittrex.com
with high speed order management.
"""
from time import sleep
import sys, traceback
import os
from bittrex import bittrex
from innum import Input
from threading import Thread

# Get these from https://bittrex.com/Account/ManageApiKey
KEY = '<your_key>'
SECRET = '<your_secret>'

# default values
TRADE = 'USDT'
COIN = 'BTC'
MARKET = "{}-{}".format(TRADE,COIN)
api = bittrex(KEY, SECRET)
Input = Input()
def terminal_cursor_on(switch=True):
    """
    Hide and show cursor in terminal
    """
    if switch:
        os.system('setterm -cursor on')
    else:
        os.system('setterm -cursor off')

def set_market():
    """
    request Market and Coin from user
    """
    trade = input('Enter Market ({}): '.format(TRADE)).upper() or TRADE
    currency = input('Enter Coin ({}):'.format(COIN)).upper() or COIN
    market = '{0}-{1}'.format(trade, currency)
    return market

def last_price(market):
    """
    Get current price of coin
    """
    summary = api.getmarketsummary(market)
    tradeCoin = market.split('-')
    price = summary[0]['Last']
    return price


def show_last_price(market,count=1,delay=15,dynamic=False):
    """
    returns current price of coin in words
    """
    END = '\r' if dynamic else '\n'
    tradeCoin = market.split('-')
    while True:
        summary = api.getmarketsummary(market)
        if isinstance(summary,str):
            print(summary)
            break
        price = summary[0]['Last']
        print('The price for {0} is {1:.8f} {2}.'.format(tradeCoin[1], price, tradeCoin[0]),end=END)
        count -=1
        if count > 0 :
            sleep(delay)
        else:
            break
    return 

  
def list_last_price(market,count,dynamic=False):
    """
    Print given market price
    """
    terminal_cursor_on(not dynamic)
    for i in range(0,count):
        sleep(10)
        print(show_last_price(market), end= '\r' if dynamic else '\n')

def get_my_balance_value(balances):
    """
    calculate BTC and USDT value of all coin balances.
    returns the array of coins with calculated balances.
    """
    balanceValue = []
    btcUsdtValue = (api.getmarketsummary('USDT-BTC'))[0]['Last']
    for coin in balances:
        coinName = coin['Currency']
        coinBalance = coin['Balance']
        if coinBalance:
            if coinName == 'BTC':
                coinBtcValue = coinBalance
            elif coinName == 'USDT':
                coinBtcValue = coinBalance / btcUsdtValue
            else:
                btcMarket = 'BTC-{0}'.format(coinName)
                coinBtcValue = round((api.getmarketsummary(btcMarket))[0]['Last'] * coinBalance,8)
            coin['btc'] = coinBtcValue
            coin['usdt'] = btcUsdtValue * coinBtcValue
            balanceValue.append(coin)
    return balanceValue

def get_coin_balance(coin):
    """
    returns balance of given coin
    """
    balance = api.getbalance(coin)
    return balance['Balance']

def get_my_balance_total():
    """
    returns total balance in BTC and USDT
    """
    balances = get_my_balance_value(api.getbalances())
    totalBTC = 0
    totalUSDT = 0
    for coin in balances:
        totalBTC += coin['btc']
        totalUSDT += coin['usdt']
    return {'btc': totalBTC, 'usdt': totalUSDT}

def account_balance(fullBalance=True):
    """
    return Balance of all your coins
    """
    balances = get_my_balance_value(api.getbalances())
    totalBTC = 0
    totalUSDT = 0
    cw =12
    rw = (cw*4)+5
    def print_row_line():
        print('-'*rw)   
    if fullBalance:
        print_row_line()
        print('|{c1:^12}|{c2:^12}|{c3:^12}|{c4:^12}|'.format(c1='Currency',c2='Balance',c3='BTC',c4='USDT'))
        print_row_line()
    for coin in balances:
        if fullBalance:
            print('|{c1:<12}|{c2:<12f}|{c3:<12f}|{c4:<12f}|'.format(c1=coin['Currency'],c2=coin['Balance'],c3=coin['btc'],c4=coin['usdt']))
        totalBTC += coin['btc']
        totalUSDT += coin['usdt']
    if fullBalance:
        print_row_line()
        print('|{0:^25}|{1:<12f}|{2:<12f}|'.format('Total',totalBTC,totalUSDT))
        print_row_line()
    else:
        print('Total Balance :{btc:8f} BTC = {usdt:8f} USDT'.format(btc=totalBTC,usdt=totalUSDT),end='\r')
    return 0

def monitor_coin():
    market = set_market()
    show_last_price(market,count=10)

def bot_settings():
    """
    Bot setting Menu
    """
    # TODO implement this method
    global TRADE
    global COIN
    TRADE = input('Enter Market ({}): '.format(TRADE)).upper() or TRADE
    COIN = input('Enter Coin ({}):'.format(COIN)).upper() or COIN
    MARKET = "{}-{}".format(TRADE,COIN)
    if(MARKET != market):
        print("Default Values Changed successfully")
    else:
        print("No change in default values")

def user_buy():
    """
    Manual buy
    """ 
    market = set_market()
    trade,currency = market.split('-')
    lastPrice = last_price(market)
    price = Input.get_float("Enter Price in {} ({}): ".format(trade,lastPrice),lastPrice)
    amount = Input.get_float("Enter amount of {} to buy : ".format(currency))
    print ('Buying {0} {1} for {2:.8f} {3}.'.format(amount, currency, price, trade))
    print(api.buylimit(market, amount, price))
    print("New balances:")
    print('{:<6}: {:8f}'.format(trade,get_coin_balance(trade)))
    print('{:<6}: {:8f}'.format(currency,get_coin_balance(currency)))
    
def user_sell():
    """
    Manual sell
    """
    market = set_market()
    trade,currency = market.split('-')
    lastPrice = last_price(market)
    price = Input.get_float("Enter Price in {} ({}): ".format(trade,lastPrice),lastPrice)
    balance = get_coin_balance(currency)
    amount = Input.get_float("Enter amount of {} to sell ({}): ".format(currency,balance),balance)
    print('Selling {0} {1} for {2:.8f} {3}.'.format(amount, currency, price, trade))
    print(api.selllimit(market, amount, price))
    print("New balances:")
    print('{:<6}: {:8f}'.format(trade,get_coin_balance(trade)))
    print('{:<6}: {:8f}'.format(currency,get_coin_balance(currency)))

def open_orders():
    """
    Print open orders
    """
    market = set_market()
    print(' Loading...',end='\r')
    openOrders = api.getorderhistory(market,4)   
    uuid = []
    orderCount = len(openOrders)
    if orderCount :
        orderSerialNumber =  0
        cw =12
        rw = (cw*5)+6
        def print_row_line():
            print('-'*rw)
        print("List of openorders in {}".format(market))
        print_row_line()
        print('|{:^12}|{:^12}|{:^12}|{:^12}|{:^12}|'.format('S.No','Date','Time','Qty','Price'))
        print_row_line()
        for order in openOrders:
            openedDate,openedTime = order['Opened'].split('T')
            quantity = order['QuantityRemaining']
            price = order['Limit']
            uuid.append(order['OrderUuid'])
            orderSerialNumber += 1
            print('|{:^12}|{:<12}|{:<12}|{:<12f}|{:12.8f}|'.format(orderSerialNumber,openedDate,openedTime,quantity,price))
        print_row_line()
    else:
        print("No open orders in {} market".format(market))
    return uuid

def close_order():
    """
    Manually close open orders
    """
    OpenOrderUuid = open_orders()
    if len(OpenOrderUuid):
        cancelOrder = Input.get_int('Enter Serial No of Order to be Canceled (1): ', 1)
        api.cancel(OpenOrderUuid[cancelOrder])

def order_history():
    """
    print order history
    """
    market = set_market()
    count = Input.get_int(message="Enter number of History's (5):",default=5)
    print(' Loading...',end='\r')
    openOrders = api.getorderhistory(market,count)   
    uuid = []
    orderCount = len(openOrders)
    if orderCount :
        orderSerialNumber =  0
        cw =12
        rw = (cw*5)+6
        def print_row_line():
            print('-'*rw)
        print("List of openorders in {}".format(market))
        print_row_line()
        print('|{:^12}|{:^12}|{:^12}|{:^12}|{:^12}|'.format('S.No','Date','Time','Qty','Price'))
        print_row_line()
        for order in openOrders:
            openedDate,openedTime = order['TimeStamp'].split('T')
            quantity = order['Quantity']
            price = order['Limit']
            orderType = order['OrderType']
            uuid.append(order['OrderUuid'])
            orderSerialNumber += 1
            print('|{:^12}|{:<12}|{:<12}|{:<12f}|{:12.8f}|'.format(orderType,openedDate,openedTime,quantity,price))
        print_row_line()
    else:
        print("No open orders in {} market".format(market))
    return uuid

def trade_bot():
    # TODO implement this function
    pass

def all_coins():
    """
    print the list off all coins trading on bittrex
    """
    allCoins = api.getcurrencies()
    for coin in allCoins:
        print(" {:<6}: {:<25}{:<3}".format(coin['Currency'],coin['CurrencyLong'],'yes' if coin['IsActive'] else 'No' ))
    print("Total :{}".format(len(allCoins)))

def bot_home(mode=None):
    """
    print cli-menu 
    """
    homeOptions =[
        'Account Balance',
        'Check Coin Value',
        'All Coins',
        'Buy',
        'Sell',
        'Open Orders',
        'Close Order',
        'Order History',
        'autotrade',
        'Settings',
        'Monitor Coin',
        'exit'
    ]
    
    def last_price_home():
        """
        Display last price for selected coin once.
        """
        show_last_price(set_market())

    dOptions = {
        1 : account_balance,
        2 : last_price_home,
        3 : all_coins,
        4 : user_buy,
        5 : user_sell,
        6 : open_orders,
        7 : close_order,
        8 : order_history,
        9 : trade_bot,
        10 : bot_settings,
        11 : monitor_coin,
        12 : sys.exit
    }
    options = enumerate(homeOptions, start=1)
    for option in options:
        print('  ',option[0],option[1])
    botHome = Input.get_int("Select Option (1):",1) # read user input default is 1
    if botHome  <= len(homeOptions):
        print(' Loading...',end='\r')
        dOptions[botHome]()
        input("Press ENTER to continue...")
    else:
        print("[!] Invalid Selection try again")
    bot_home(mode)
    
def main():
    try:
        bot_home()
    except KeyboardInterrupt:
        print("\rShutdown requested...exiting")

    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        terminal_cursor_on()
    sys.exit(0)

if __name__ == "__main__":
    main()