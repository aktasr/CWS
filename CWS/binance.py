#Author : Ramazan AKTAS
#Date   : 20.02.2021 22:30


from base.exchange import exchange
import time

class binance(exchange):
    """description of class"""

    # user can be subscribe one or more market(symbol). F.e: suscriber_trade = ['BTCTRY', 'BTCUSDT']
    # also user can be subscribe all markets(symbols). F.e: suscriber_trade = ['all']
    def __init__(self, subscribe_ticker:list = [], subscribe_trade:list = [], subscribe_orderbook:list = [], subscribe_obDiff:list = []):
        super().__init__({ 'onOpenEvent' : {
            'subscribe_ticker' : subscribe_ticker,
            'subscribe_trade' : subscribe_trade,
            'subscribe_orderbook' : subscribe_orderbook,
            'subscribe_orderbookDiff' : subscribe_obDiff
            }})
        self.connect()

    def describe(self):
        return self.deep_extend(super().describe(), {
            'id':'binance', 
            'name':'BINANCE', 
            'url':'wss://stream.binance.com:9443/ws',
            'wsLogEnable' : 'False',
            'Subscribe' : 'SUBSCRIBE', 
            'Result' :  'result',
            'OrderBook' : 'depth20',
            'OrderBookDifference' : 'depth',
            'TickerAll' : 401,
            'TickerPair' : 402,
            'Channel':['ticker','trades','depth20@100ms','depth'],
            'Symbols': {
                'BTCUSDT' : 'btcusdt',
                'BTCTRY' : 'btctry',
                'XRPUSDT' : 'xrpusdt',
                'ETHUSDT' : 'ethusdt',
                'USDTTRY' : 'usdttry',
                'ADAUSDT' : 'adausdt',
                'TRXUSDT' : 'trxusdt',
                'EOSUSDT' : 'eosusdt',
                'DOTUSDT' : 'dotusdt',
                'XTZUSDT' : 'xtzusdt',
                'BTCUSDT' : 'btcusdt',
                'XRPTRY' : 'xrptry',                
                'MATICUSDT' : 'maticusdt',
                'ETHTRY' : 'ethtry',
                'DOGETRY' : 'dogetry',
                'DOGEUSDT' : 'dogeusdt',
                'AVAXUSDT': 'avaxusdt',
                'AVAXTRY': 'avaxtry',
                'SOLTRY': 'soltry',
                'SOLUSDT': 'solusdt',
                'CHZTRY': 'chztry',
                'DOTTRY': 'dottry',
                'MATICTRY': 'matictry',
                'NEOTRY': 'neotry',
                'ALL' : 'all',
                },
            'has': {
                'tickerSubscribe': True,
                'tradeSubscribe': True,
                'orderbookSubscribe': True,
                'orderbookDiffSubscribe': True
                }})

    def subscribe_ticker(self, symbol, params={}):
        try: 
            self.subscribe(self.Channel[0], self.Symbols[symbol])
        except:
            print("Holaa")
     
    def subscribe_trade(self, symbol, params={}):
        self.subscribe(self.Channel[1],self.Symbols[symbol])
    
    def subscribe_orderbook(self, symbolArr:list = [], params = {}):        
        symbols = []
        for x in symbolArr:
            symbols.append(self.Symbols[x])

        self.subscribe(self.Channel[2],symbols)
            
    def subscribe_orderbookDiff(self, symbol, params={}):
        self.subscribe(self.Channel[3],self.Symbols[symbol])

    def subscribe(self, *params):
        if self.isConnected is False:
            raise PermissionError('Not connected to websocket server.')

        subscribeParams = []
        symbols = params[1]
        channel = params[0]

        for symbol in symbols:
            param = symbol + "@" + channel
            subscribeParams.append(param)

        jsonData = {"method": self.Subscribe, "params" : subscribeParams, "id" : 1}
        self.sendMessage(self.json(jsonData))

    def orderbook_received(self, message):
        symbol = self.getSymbolFromStream(message['stream'])
        orderbook = message['data']

        self.parse_orderbook(symbol, orderbook)
    
    def onMessage(self, message):
        channel = self.getChannelFromStream(message['stream'])
        self.parseAndRouteMessage(channel, message)

    def onOpen(self):
        ''' in this project, combined subscribe is used. Response data must include owner stream information. '''
        data = {"method": "SET_PROPERTY", "params": ["combined",True],"id": 5}
        self.sendMessage(self.json(data))
        super().onOpen()

    def getSymbolFromStream(self, stream):
        ''' class specific function '''
        return (self.parseStream(stream)[0])
    
    def getChannelFromStream(self, stream):
        ''' class specific function '''
        return (self.parseStream(stream)[1])
    
    def parseStream(self, stream):
        ''' class specific function '''
        return stream.split("@")
