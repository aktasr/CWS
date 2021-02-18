# CWS
Crypto currency exchanges WebSocket Library

This is a generic cryptocurrency exchange websocket library.
You can obtain data which is same formatted for all exchanges from websocket. So that, you don't deal with the structure complexity. 
(Each exchanges sends data on its own data structure format.)

Simple use, just call instance by giving specific subscribe parameters, f.e: subscribe orderbook for BTCUSDT. Then start to use parsed or raw data syncronously or asyncronously, whatever you want.

| Exchanges | Supported Functions/Events  |
| --------- | -------------------         |
| BTCTURK   | fetch_orderbook(symbol)<br>onOrderbookMsg<br>onMsg<br>  |
| BINANCE   | -                           |

| Functions/Events      | Description |
|---------------------- |-------------|
| func: fetch_orderbook(symbol) | Used for fetch parsed orderbook data at any time from another thread.  |
| event: onOrderbooMsg          | It is called as soon as the message arrives from websocket. This event provides parsed orderbook data.     |
| event: onMsg                  | It is called as soon as the message arrives from websocket. This event provides raw data.           |

## Exchanges Under Development:
BINANCE

## Functions Under Development:
ticker<br>
trade<br>

## Preconditions
install websocket_client

## Synchronous Usage Example

Usage example is also described in CWS.py file.
```python

from btcturk import btcturk

def onOrderbook(*args):
    print(args[0])

def onMessage(*args):
    print(args[0])

def start():
  btc = btcturk(subscribe_orderbook=['BTCTRY','BTCUSDT'])
  btc.onOrderbookMsg = onOrderbook
  btc.onMsg = onMessage
  btc.start()

if __name__ == "__main__":
    start()
```

## Asynchronous Usage Example

Usage example is also described in CWS.py file.
```python

from btcturk import btcturk

def start():
  btc = btcturk(subscribe_orderbook=['BTCTRY','BTCUSDT'])
  thr = threading.Thread(target=btc.start)
  thr.daemon = True
  thr.start()

  ''' Fetch parsed data from main thread. '''
  while True:
    print(btc.fetch_orderbook(symbol='BTCTRY'))
    time.sleep(1)
    
if __name__ == "__main__":
    start()
```

Please let me know if this helps you.
