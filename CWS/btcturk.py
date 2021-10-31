#Author : Ramazan AKTAS
#Date   : 12.02.2021 23:31


from base.exchange import exchange
import time

class btcturk(exchange):
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
            'id':'btcturk', 
            'name':'BTCTurk', 
            'url':'wss://ws-feed-pro.btcturk.com/',
            'wsLogEnable' : 'False',
            'Subscribe' : 151, 
            'Result' :  100,
            'OrderBook' : 431,
            'OrderBookDifference' : 432,
            'TickerAll' : 401,
            'TickerPair' : 402,
            'Channel':['ticker','trade','orderbook','obdiff'],
            'Symbols': {
                'BTCUSDT' : 'BTCUSDT',
                'BTCTRY' : 'BTCTRY',
                'XRPUSDT' : 'XRPUSDT',
                'ETHUSDT' : 'ETHUSDT',
                'USDTTRY' : 'USDTTRY',
                'ADAUSDT' : 'ADAUSDT',
                'TRXUSDT' : 'TRXUSDT',
                'EOSUSDT' : 'EOSUSDT',
                'DOTUSDT' : 'DOTUSDT',
                'XTZUSDT' : 'XTZUSDT',
                'BTCUSDT' : 'BTCUSDT',
                'XRPTRY' : 'XRPTRY',
                'MATICUSDT' : 'MATICUSDT',
                'ETHTRY' : 'ETHTRY',
                'DOGETRY' : 'DOGETRY',
                'DOGEUSDT' : 'DOGEUSDT',
                'AVAXUSDT': 'AVAXUSDT',
                'AVAXTRY': 'AVAXTRY',
                'SOLTRY': 'SOLTRY',
                'SOLUSDT': 'SOLUSDT',
                'CHZTRY': 'CHZTRY',
                'DOTTRY': 'DOTTRY',
                'MATICTRY': 'MATICTRY',
                'NEOTRY': 'NEOTRY',
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
        ''' subscribe for all symbols '''
        for symbol in symbolArr:
            self.subscribe(self.Channel[2],self.Symbols[symbol])

    def subscribe_orderbookDiff(self, symbol, params={}):
        self.subscribe(self.Channel[3],self.Symbols[symbol])

    def subscribe(self, *params):
        if self.isConnected is False:
            raise PermissionError('Not connected to websocket server.')

        jsonData = [self.Subscribe, {"type": self.Subscribe, "channel": params[0], "event": params[1], "join":True}]
        self.sendMessage(self.json(jsonData))

    def orderbook_received(self, message):
        self.parse_orderbook(message[1]['event'], message[1], 0, asksKey = 'AO', bidsKey = 'BO', priceKey = 'P', amountKey = 'A')
    
    def onMessage(self, message):
        self.parseAndRouteMessage(message[0], message)
        