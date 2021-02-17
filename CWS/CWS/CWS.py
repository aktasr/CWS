#Author      : Ramazan AKTAS
#Date        : 14.02.2021 23:00
#Description : Usage examples

from btcturk import btcturk
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
import threading

def onOrderbook(*args):
    print(args[0])

def start():
    ''' start func '''
    
    ''' user can be subscribe one or more market(symbol). F.e: suscriber_trade = ['BTCTRY', 'BTCUSDT']
    also user can be subscribe all markets(symbols). F.e: suscriber_trade = ['all'] '''

    btc = btcturk(subscribe_orderbook=['BTCTRY','BTCUSDT'])
    
    ''' creates websocket, don't subscribe anything. After connection established, you can subscribe any channel for any symbol 
    command out below code and command above code to try it.'''
    #btc = btcturk()

    ''' to prevent exception on manual subscription, you can check isConnected flag for a time: 
    command out below code to try it.'''
    #MaxTryCount = 10 
    #tryCount = 0
    #try:
    #    while tryCount < MaxTryCount:          
    #        if btc.isConnected is False:
    #            time.sleep(0.5)
    #            continue
    #        else: 
    #            break

    #    btc.subscribe_orderbook('BTCTRY')
    #except :
    #    print("\nTried to subscribe before connection!!!\n")



    # start to thread for continuous websocket communication
    thr = threading.Thread(target=btc.start)
    thr.daemon = True
    thr.start()
    
    ''' parsed orderbook message is can be directly used in this func. 
    User can use if want to use synchronously 
                      Symbol       Bids    Price   Amount     Asks     Price  Amount
    Format example: {'BTCUSDT' : {'bids':[[40000, 0.980][]], 'asks': [[40100, 0.980][]]}}
    When websocket sends an orderbook message, this event is called in websocket thread.'''    
    
    btc.onOrderbookMsg = onOrderbook


    '''Also parsed orderbook message is can be achieved at any time from another thread by using fetch_orderbook() function.
    It can be custumized giving symbol as a parameter f.e: fetch_orderbook(symbol = 'BTCTRY')
    It can used if want to use asynchronously 
    Command out below code to try it'''
    #while True:
    #  print(btc.fetch_orderbook(symbol='BTCTRY'))
    #  time.sleep(1)

    
    #task = asyncio.create_task(deneme())

    

    while True:
        time.sleep(20)


    #asyncio.run(test2())


    #time.sleep(1)
    #btc.subscribe_ticker('BTCTRY')
    #time.sleep(1)
    #btc.subscribe_trade('BTCTRY')


def test():
    while True:
        print("Deniyoruz")
        print("thread count in test:", threading.active_count())
        time.sleep(1)

async def test2():
    task = asyncio.create_task(test3())
    while True:
        print("test2")
        print("thread count in test2:", threading.active_count())
        await asyncio.sleep(1)


async def test3():
    count = 5
    while count>0:
        count-=1
        print("test3")
        await asyncio.sleep(1)

if __name__ == "__main__":
    #asyncio.run(start())
    start()




