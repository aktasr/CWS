#Author      : Ramazan AKTAS
#Date        : 14.02.2021 23:00
#Description : Usage examples

from btcturk import btcturk
from binance import binance
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
from threading import Lock, Thread
from queue import Queue 


messQueue = Queue()

def onOrderbook(*args):
    #print(args[0])
    if ('BTCTRY' in args[0][0]):
        messQueue.put(args[0])

def onMessage(*args):
    print(args[0])

def start():
    ''' start func '''
    
    ''' user can be subscribe one or more market(symbol). F.e: suscriber_trade = ['BTCTRY', 'BTCUSDT']
    also user can be subscribe all markets(symbols). F.e: suscriber_trade = ['all'] '''

    btc = btcturk(subscribe_orderbook=['BTCTRY','BTCUSDT'])
    bnc = binance(subscribe_orderbook=['BTCUSDT', 'BTCTRY'])
    
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
    thr1 = Thread(target=btc.start)
    thr1.daemon = True
    thr1.start()
    
    thr = Thread(target=bnc.start)
    thr.daemon = True
    thr.start()

    ''' parsed orderbook message is can be directly used in this func. 
    It can be used if want to use synchronously 
                      Symbol       Bids    Price   Amount     Asks     Price  Amount
    Format example: {'BTCUSDT' : {'bids':[[40000, 0.980][]], 'asks': [[40100, 0.980][]]}}
    When websocket sends an orderbook message, this event is called in websocket thread.'''    
    
    btc.onOrderbookMsg = onOrderbook

    ''' raw data is can be directly used in this func.
    It can be used if want to use synchronously.
    Command out below code to try. '''
    #btc.onMsg = onMessage

    '''Also parsed orderbook message is can be achieved at any time from another thread by using fetch_orderbook() function.
    It can be custumized giving symbol as a parameter f.e: fetch_orderbook(symbol = 'BTCTRY')
    It can be used if want to use asynchronously 
    Command out below code to try it'''
    #while True:
    #  print(btc.fetch_orderbook(symbol='BTCTRY'))
    #  time.sleep(1)

    testDelay = 0.1
    testDuration = 600/testDelay
    duration = 0
    while duration < testDuration:
        testBtcTurkChangeCount(btc,'BTCUSDT')
        testBinanceChangeCount(bnc,'BTCUSDT')
        duration += 1

        #time.sleep(10)
        
        print("Get data from queue")
       
            
        flushedData = 0
        try:
            while messQueue.qsize() > 0:
                flushedData += 1
                data =  messQueue.get(timeout = 0.1)
        except :
            print("Time is UP")
            
     
        print("Last BTC MESSAGE received. flushed data count: ", flushedData)
        #print("BtcTurk BTCTRY: ",btc.fetch_orderbook(symbol='BTCTRY'))
        #print("BtcTurk BTCUSDT: ",btc.fetch_orderbook(symbol='BTCUSDT'))
        #print("Binance BTCTRY: ",bnc.fetch_orderbook(symbol='BTCTRY'))
        #print("Binance BTCUSDT: ",bnc.fetch_orderbook(symbol='BTCUSDT'))
        time.sleep(testDelay)
        
    

    print("\nTest finished. Test duration is ", testDuration," ms with test delay", testDelay, " ms.")
    print("\nBtcTurkAskChangeCount: ",BtcTurkAskChangeCount, "\nBtcTurkBidChangeCount: ", BtcTurkBidChangeCount)
    print("\nBinanceAskChangeCount: ",BinanceAskChangeCount, "\nBinanceBidChangeCount: ", BinanceBidChangeCount)
    #task = asyncio.create_task(deneme())

    

    #while True:
    #    time.sleep(20)


    #asyncio.run(test2())


    #time.sleep(1)
    #btc.subscribe_ticker('BTCTRY')
    #time.sleep(1)
    #btc.subscribe_trade('BTCTRY')

BtcTurkAskChangeCount = 0
BtcTurkBidChangeCount = 0
BtcTurkLastAsk = None
BtcTurkLastBid = None

BinanceAskChangeCount = 0
BinanceBidChangeCount = 0
BinanceLastAsk = None
BinanceLastBid = None

def testBtcTurkChangeCount(btc, symbol):
    global BtcTurkLastAsk
    global BtcTurkLastBid
    global BtcTurkAskChangeCount
    global BtcTurkBidChangeCount

    data = btc.fetch_orderbook(symbol=symbol)
    if data == None:
        return

    ask = data['asks'][0][0]
    bid = data['bids'][0][0]

    if BtcTurkLastBid == None:
        BtcTurkLastBid = bid
        return
    elif BtcTurkLastBid == bid:
        return
    else:
        BtcTurkBidChangeCount += 1
        BtcTurkLastBid = bid

    if BtcTurkLastAsk == None:
        BtcTurkLastAsk = ask
        return
    elif BtcTurkLastAsk == ask:
        return
    else:
        BtcTurkAskChangeCount += 1
        BtcTurkLastAsk = ask


def testBinanceChangeCount(btc, symbol):
    global BinanceAskChangeCount
    global BinanceBidChangeCount
    global BinanceLastAsk
    global BinanceLastBid

    data = btc.fetch_orderbook(symbol=symbol)
    if data == None:
        return

    ask = data['asks'][0][0]
    bid = data['bids'][0][0]

    if BinanceLastBid == None:
        BinanceLastBid = bid
        return
    elif BinanceLastBid == bid:
        return
    else:
        BinanceBidChangeCount += 1
        BinanceLastBid = bid

    if BinanceLastAsk == None:
        BinanceLastAsk = ask
        return
    elif BinanceLastAsk == ask:
        return
    else:
        BinanceAskChangeCount += 1
        BinanceLastAsk = ask

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




