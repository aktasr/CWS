#Author : Ramazan AKTAS
#Date   : 12.02.2021 23:31

import json
import asyncio
import websocket as ws
import inspect
import time
from base.lockable import lockable

class exchange(object):
    """base exchange class"""
    id = None
    name = None
    url = None

    # stock market ram
    orderbooks = None

    # webSocket
    websocket = None
    wsLogEnable = False
    isConnected = False

    # webSocket Models 
    # Client -> Server
    Subscribe = None

    # Server -> Client
    Result = None
    OrderBook = None
    OrderBookDifference = None
    TickerAll = None
    TickerPair = None

    # Server Channels (is an array)
    Channel = None

    # Supported Symbol Pairs (Markets).
    # It can change for each exchanges. F.e: In x exchange, BTCUSDT named as Btc_Usdt
    Symbols = { 
        'BTCUSDT' : 'BTCUSDT',
        'BTCTRY' : 'BTCTRY',
        'XRPUSDT' : 'XRPUSDT',
        'ALL' : 'ALL'
        }

    # API method metainfo
    has = {
        'tickerSubscribe' : False,
        'tradeSubscribe' : False,
        'orderbookSubscribe' : False,
        'orderbookDiffSubscribe' : False 
        }

    # on Open Events
    onOpenEvent = {
        'subscribe_ticker' : [],
        'subscribe_trade' : [],
        'subscribe_orderbook' : [],
        'subscribe_orderbookDiff' : []
        }
    # events
    # used to get raw data
    onMsg = None
    onCloseEvent = None

    # used to get parsed data
    onOrderbookMsg = None
    onObdiffMsg = None    
    onTickerMsg = None
    onTradeMsg = None

    def __init__(self, config={}):
        settings = self.deep_extend(self.describe(), config)

        for key in settings:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, self.deep_extend(getattr(self, key), settings[key]))
            else:
                setattr(self, key, settings[key])

        self.orderbooks = lockable({'BTCUSDT' : None,
                                    'BTCTRY' : None,
                                    'XRPUSDT' : None,
                                    'ETHUSDT' : None,
                                    'USDTTRY' : None,
                                    'ADAUSDT' : None,
                                    'TRXUSDT' : None,
                                    'EOSUSDT' : None,
                                    'DOTUSDT' : None,
                                    'XTZUSDT' : None,
                                    'MATICUSDT' : None,
                                    'XRPTRY': None,
                                    'ETHTRY': None,
                                    'DOGETRY': None,
                                    'DOGEUSDT': None,
                                    'AVAXUSDT': None,
                                    'AVAXTRY': None,
                                    'SOLTRY': None,
                                    'SOLUSDT': None,
                                    'CHZTRY': None,
                                    'DOTTRY': None,
                                    'MATICTRY': None,
                                    'NEOTRY': None})

    def describe(self):
        return {}

    def sendMessage(self, params={}):
        print("Message will be sent:", params)
        self.websocket.send(params)

    def recv(self):
        pass
        #print(self.websocket.recv())

    def connect(self):
        if self.wsLogEnable is True:
            ws.enableTrace(self.wsLogEnable)
        self.websocket = ws.WebSocketApp(self.url, on_open = self.on_open, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

    def isAlive(self):
        if self.websocket is not None :
            return self.websocket.keep_running
        return False

    def start(self):
        self.websocket.run_forever()

    def subscribe_ticker(self, symbol, params={}):
        raise NotSupported('subscribe_ticker() not supported yet')

    def subscribe_trade(self, symbol, params={}):
        raise NotSupported('subscribe_trade() not supported yet')

    def subscribe_orderbook(self, symbol, params={}):
        raise NotSupported('subscribe_orderbook() not supported yet')
    
    def subscribe_orderbook(self, *params):
        raise NotSupported('subscribe_orderbook() not supported yet')
        
    def subscribe_orderbookDiff(self, symbol, params={}):
        raise NotSupported('subscribe_orderbookdifference() not supported yet')

    def subscribe(self, params={}):
        raise NotSupported('subscribe not supported yet')

    def orderbook_received(self, message):
        raise NotSupported('orderbook received supported yet')

    #Websocket calls when connection ended.
    def onClose(self):
        raise NotSupported('subscribe not supported yet')
        
    #Websocket calls when error occured.
    def onError(self, error):
        raise NotSupported('subscribe not supported yet')
    
    #Websocket calls for message.    
    def onMessage(self, message):
        raise NotSupported('subscribe not supported yet')
    
    #Websocket calls when connection established.    
    def onOpen(self):
        self.isConnected = True

        subsTicker_arr:list  = self.onOpenEvent['subscribe_ticker'];
        subsTrade_arr:list  = self.onOpenEvent['subscribe_trade'];
        subsOrderbook_arr:list  = self.onOpenEvent['subscribe_orderbook'];

        if subsTicker_arr:
            for x in subsTicker_arr:
                self.subscribe_ticker(x)
        
        if subsTrade_arr:
            for x in subsTrade_arr:
                self.subscribe_trade(x)

        if subsOrderbook_arr:
            self.subscribe_orderbook(subsOrderbook_arr)
            #for x in subsOrderbook_arr:
            #    self.subscribe_orderbook(x)

    def on_close(socket):
        print("Socket closed\n")
        exchange.callEvent(socket.onCloseEvent)
        socket.onClose()

    def on_error(socket, error):
        print("Socket error received. Error: ", error, "\n")
        socket.onError(error)
            
    def on_message(socket, message):
        #print("in message is: ", message)
        exchange.callEvent(socket.onMsg, message)  
        socket.onMessage(exchange.unjson(message))

    def on_open(socket):        
        socket.onOpen()

    def parseAndRouteMessage(self, model, message):
        if self.Result is not None and model == self.Result:
            pass
        elif self.OrderBook is not None and model == self.OrderBook:
            self.orderbook_received(message)
        elif self.OrderBookDifference is not None and model == self.OrderBookDifference:
            pass
        elif self.TickerAll is not None and model == self.TickerAll:
            pass
        elif self.TickerPair is not None and model == self.TickerPair:
            pass
    
    # to fetch all data, don't give parameter
    def fetch_orderbook(self, symbol = None):
        return self.orderbooks.GetValue(symbol)

    def parse_ticker(self):
        raise 

    # inspired from: ccxt library
    def parse_orderbook(self, symbol, orderbook, timestamp=None, bidsKey='bids', asksKey='asks', priceKey=0, amountKey=1):    
        
        _orderbook = {}
        
        if(timestamp is None):
            timestamp = self.getTimeInMs()
        
        bids = self.sort_by(self.parse_bids_asks(orderbook[bidsKey], priceKey, amountKey) if (bidsKey in orderbook) and isinstance(orderbook[bidsKey], list) else [], 0, True)
        asks = self.sort_by(self.parse_bids_asks(orderbook[asksKey], priceKey, amountKey) if (asksKey in orderbook) and isinstance(orderbook[asksKey], list) else [], 0)
        
        _orderbook['bids'] = bids
        _orderbook['asks'] = asks
        _orderbook['timestamp'] = timestamp

        symbolKey = exchange.getKeysByValue(self.Symbols,symbol)
        self.orderbooks.SetValue(_orderbook, key = symbolKey)
        
        exchange.callEvent(self.onOrderbookMsg, {symbolKey:_orderbook})    
            

    # source: ccxt library
    def parse_bid_ask(self, bidask, price_key=0, amount_key=0):
        return [float(bidask[price_key]), float(bidask[amount_key])]

    # source: ccxt library
    def parse_bids_asks(self, bidasks, price_key=0, amount_key=1):
        result = []
        if len(bidasks):
            if type(bidasks[0]) is list:
                for bidask in bidasks:
                    if bidask[price_key] and bidask[amount_key]:
                        result.append(self.parse_bid_ask(bidask, price_key, amount_key))
            elif type(bidasks[0]) is dict:
                for bidask in bidasks:
                    if (price_key in bidask) and (amount_key in bidask) and (bidask[price_key] and bidask[amount_key]):
                        result.append(self.parse_bid_ask(bidask, price_key, amount_key))
            else:
                raise ExchangeError('unrecognized bidask format: ' + str(bidasks[0]))
        return result

    def getTimeInMs(self):
        return time.time() * 1000 
    
    @staticmethod
    def callEvent(event, *args):
        if inspect.isfunction(event) or inspect.isroutine(event):
            event(args)
        else:
            #print(" Event is not function!\n")
            pass
     
    @staticmethod
    def getKeysByValue(dictOfElements, valueToFind):
        listOfItems = dictOfElements.items()
        for item  in listOfItems:
            if item[1] == valueToFind:
                return item[0]

    @staticmethod
    def sort_by(array, key, descending=False):
        return sorted(array, key=lambda k: k[key] if k[key] is not None else "", reverse=descending)

    @staticmethod
    def unjson(input):
        return json.loads(input)

    @staticmethod
    def json(data, params=None):
        return json.dumps(data, separators=(',', ':'))
        
    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict):
                if not isinstance(result, dict):
                    result = {}
                for key in arg:
                    result[key] = exchange.deep_extend(result[key] if key in result else None, arg[key])
            else:
                result = arg
        return result