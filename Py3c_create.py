import ccxt
import time
import math
import config
import default_config
import os
from time import gmtime, strftime
from py3cw.request import Py3CW
from pathlib import Path

p3cw = Py3CW(
    key=config.TC_API_KEY,
    secret=config.TC_API_SECRET,
    request_options={
        'request_timeout': 20,
        'nr_of_retries': 10,
        'retry_status_codes': [500, 502, 503, 504]
    }
)

ftx = ccxt.ftx({
    'apiKey': config.FTX_API_KEY,
    'secret': config.FTX_SECRET_KEY,
    'headers': {'FTX-SUBACCOUNT': config.FTX_SUBACCOUNT}
})


def get_markets():
    try:
        all_markets = ftx.load_markets(True) # https://docs.ccxt.com/en/latest/manual.html#loading-markets
        """ 
        {
        '1INCH/USD:USD': {
            'id': '1INCH-PERP', 
            'symbol': '1INCH/USD:USD', 
            'base': '1INCH', 
            'quote': 'USD', 
            'baseId': '1INCH', 
            'quoteId': 'USD', 
            'active': True, 
            'type': 'swap', 
            'linear': True, 
            'inverse': False, 
            'spot': False, 
            'swap': True, 
            'future': False, 
            'option': False, 
            'margin': False, 
            'contract': True, 
            'contractSize': 1.0, 
            'expiry': None, 
            'expiryDatetime': None, 
            'optionType': None, 
            'strike': None, 
            'settle': 'USD', 
            'settleId': 'USD', 
            'precision': {
            'amount': 1.0, 
            'price': 0.0001
            }, 
            'limits': {
            'amount': {
                'min': 1.0, 
                'max': None
            }, 
            'price': {
                'min': None, 
                'max': None
            }, 
            'cost': {
                'min': None, 
                'max': None
            }, 
            'leverage': {
                'min': 1.0, 
                'max': 20.0
            }
            }, 
            'info': {
            'name': '1INCH-PERP', 
            'enabled': True, 
            'postOnly': False, 
            'priceIncrement': '0.0001', 
            'sizeIncrement': '1.0', 
            'minProvideSize': '1.0', 
            'last': '0.7114', 
            'bid': '0.7111', 
            'ask': '0.7118', 
            'price': '0.7114', 
            'type': 'future', 
            'futureType': 'perpetual', 
            'baseCurrency': None, 
            'isEtfMarket': False, 
            'quoteCurrency': None, 
            'underlying': '1INCH', 
            'restricted': False, 
            'highLeverageFeeExempt': False, 
            'largeOrderThreshold': '500.0', 
            'change1h': '0.013968072976054732', 
            'change24h': '0.12296764009471192', 
            'changeBod': '0.02095292766934558', 
            'quoteVolume24h': '19991438.5128', 
            'volumeUsd24h': '19991438.5128', 
            'priceHigh24h': '0.7345', 
            'priceLow24h': '0.632'}, 
            'percentage': True, 
            'tierBased': True, 
            'maker': 0.0002, 
            'taker': 0.0007, 
            'tiers': {
                'taker': [[0.0, 0.0007], [2000000.0, 0.0006], [5000000.0, 0.00055], [10000000.0, 0.0005], [25000000.0, 0.0045], [50000000.0, 0.0004]], 
                'maker': [[0.0, 0.0002], [2000000.0, 0.00015], [5000000.0, 0.0001], [10000000.0, 5e-05], [25000000.0, 0.0], [50000000.0, 0.0]]
            }
            }
        } 
        """
    except:
        print('[get_markets]: FTX ERROR to load markets. Check the FTX API settings.')
        exit(1)
    if len(all_markets) < 3:
        print('[get_markets]: FTX warning: Less then 3 objects')
    return all_markets

def build_tc_pairs_list(pairs):
    tc_pairs = {}
    for key in markets:
        if "PERP" in markets[key]["id"] and not any(blackperp in markets[key]["id"] for blackperp in config.PAIRS_BLACKLIST):
            tc_pairs[markets[key]["id"]] = ""
    return tc_pairs

def get_min_order_price(markets):
    limits = {}
    for key in markets:
        if "PERP" in markets[key]["id"] and not any(blackperp in markets[key]["id"] for blackperp in config.PAIRS_BLACKLIST):
            if "minProvideSize" in markets[key]["info"]:
                limits[markets[key]["id"]] = math.ceil(float(markets[key]["info"]["minProvideSize"]) * float(markets[key]["info"]["price"]))
    return limits

def generate_long_bots(pairs, minprice):
    bot_list = {}
    bot_error = []
    for key in pairs:
        if config.BASE_ORDER_SIZE > minprice[key] and config.SAFETY_ORDER_SIZE > minprice[key]:
            try:
                error, data = p3cw.request(
                    entity='bots',
                    action='create_bot', # https://github.com/3commas-io/3commas-official-api-docs/blob/master/bots_api.md
                    payload={
                    "name": config.LONG_PREFIX + key,
                    "account_id": config.TC_ACCOUNT_ID,
                    "pairs": "USD_" + key,
                    "base_order_volume": config.BASE_ORDER_SIZE,
                    "base_order_volume_type": "quote_currency",
                    "take_profit": config.TAKE_PROFIT,
                    "safety_order_volume": config.SAFETY_ORDER_SIZE,
                    "safety_order_volume_type": "quote_currency",
                    "martingale_volume_coefficient": config.SAFETY_ORDER_VOLUME_SCALE,
                    "martingale_step_coefficient": config.SAFETY_ORDER_STEP_SCALE,
                    "max_safety_orders": config.MAX_SAFETY_ORDERS_COUNT,
                    "active_safety_orders_count": config.MAX_ACTIVE_SAFETY_ORDERS_COUNT,
                    "safety_order_step_percentage": config.SAFETY_ORDER_STEP_PERCENTAGE,
                    "take_profit_type": "total",
                    "strategy_list": [{"strategy":"nonstop"}],
                    "leverage_type": "cross",
                    "leverage_custom_value": config.LEVERAGE_CUSTOM_VALUE,
                    "start_order_type": "market",
                    "stop_loss_type": "stop_loss",
                    "strategy": "long"
                    }
                )
            except:
                print('[generate_long_bots]: 3COMMAS ERROR to create bot. Check the 3Commas account setttings.')
                exit(1)
            if len(error) > 0:
                print(f'[generate_long_bots]: {key} 3COMMAS ERROR: {error}')
                bot_error.append(key)
                continue
            bot_list[key] = data["id"]
            print(f'{key}  > {bot_list[key]}')
            time.sleep(0.1)
            f = open(config.LIST_LONGBOTS, "a")
            f.write(f'{key}:{bot_list[key]}\n')
            f.close()
        else:
            print(f'[generate_long_bots]: Order volume too low for {key}, bot not created')
            bot_error.append(key)
    print(f'The following long pairs had issues: {bot_error}')
    file = open(config.LIST_ERRORBOTS, "a")
    for element in bot_error:
        file.write("LongBot: " + element + "\n")
    file.close()
    return bot_list, bot_error

def generate_short_bots(pairs, minprice):
    bot_list = {}
    bot_error = []
    for key in pairs:
        if config.BASE_ORDER_SIZE > minprice[key] and config.SAFETY_ORDER_SIZE > minprice[key]:
            try:
                error, data = p3cw.request( 
                    entity='bots',
                    action='create_bot', # https://github.com/3commas-io/3commas-official-api-docs/blob/master/bots_api.md
                    payload={
                    "name": config.SHORT_PREFIX + key,
                    "account_id": config.TC_ACCOUNT_ID,
                    "pairs": "USD_" + key,
                    "base_order_volume": config.BASE_ORDER_SIZE,
                    "base_order_volume_type": "quote_currency",
                    "take_profit": config.TAKE_PROFIT,
                    "safety_order_volume": config.SAFETY_ORDER_SIZE,
                    "safety_order_volume_type": "quote_currency",
                    "martingale_volume_coefficient": config.SAFETY_ORDER_VOLUME_SCALE,
                    "martingale_step_coefficient": config.SAFETY_ORDER_STEP_SCALE,
                    "max_safety_orders": config.MAX_SAFETY_ORDERS_COUNT,
                    "active_safety_orders_count": config.MAX_ACTIVE_SAFETY_ORDERS_COUNT,
                    "safety_order_step_percentage": config.SAFETY_ORDER_STEP_PERCENTAGE,
                    "take_profit_type": "total",
                    "strategy_list": [{"strategy":"nonstop"}],
                    "leverage_type": "cross",
                    "leverage_custom_value": config.LEVERAGE_CUSTOM_VALUE,
                    "start_order_type": "market",
                    "stop_loss_type": "stop_loss",
                    "strategy": "short"
                    }
                )
            except:
                print('[generate_short_bots]: 3COMMAS ERROR to create bot. Check the 3Commas account setttings.')
                exit(1)
            if len(error) > 0:
                print(f'[generate_long_bots]: {key} 3COMMAS ERROR: {error}')
                bot_error.append(key)
                continue
            bot_list[key] = data["id"]
            print(f'{key}  > {bot_list[key]}')
            time.sleep(0.1)
            f = open(config.LIST_SHORTBOTS, "a")
            f.write(f'{key}:{bot_list[key]}\n')
            f.close()
        else:
            print(f'[generate_short_bots]: Order volume too low for {key}, bot not created')
            bot_error.append(key)
    print(f'The following short pairs had issues: {bot_error}')
    file = open(config.LIST_ERRORBOTS, "a")
    for element in bot_error:
        file.write("ShortBot: " + element + "\n")
    file.close()
    return bot_list, bot_error

def build_bots():
    global markets
    markets = get_markets()
    pairs_list = build_tc_pairs_list(markets)
    min_price = get_min_order_price(markets)
    longbot_list, no_long_bots = generate_long_bots(pairs_list, min_price)
    shortbot_list, no_short_bots = generate_short_bots(pairs_list, min_price)
    #add list of too low order value pairs to a file.
    print(f'{len(longbot_list)} long bots created.')
    print(f'{len(no_long_bots)} long pairs ignored')
    print(f'{len(shortbot_list)} short bots created.')
    print(f'{len(no_short_bots)} short pairs ignored')
    print(f"Ignored pairs can be found in {config.LIST_ERRORBOTS}")

#############################################################

longbots_file = Path(config.LIST_LONGBOTS)
shortbots_file = Path(config.LIST_SHORTBOTS)
errorbots_file = Path(config.LIST_ERRORBOTS)
if longbots_file.is_file() or shortbots_file.is_file():
    print("An existing bot ID list was found. Using this option will over-write this list. Are you sure? y/n")
    x = input()
    if x != "y":
        print("Bye!")
    else:
        print("over-writing in progress...")
        try:
            if longbots_file.is_file(): os.remove(config.LIST_LONGBOTS)
            if shortbots_file.is_file(): os.remove(config.LIST_SHORTBOTS)
            if errorbots_file.is_file(): os.remove(config.LIST_ERRORBOTS)
        except:
            pass
        build_bots()

else:
    #print("no existing bot ID files found, proceeding....")
    build_bots()

print("All done, have a nice day!")
