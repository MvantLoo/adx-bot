import ccxt
import time
import math
import config
import sys
from time import gmtime, strftime
from py3cw.request import Py3CW
from pathlib import Path
from datetime import timezone
import datetime
import numpy as np
import pandas as pd
import pandas_ta as ta
import operator
import json


# Setup
p3cw = Py3CW(
    key=config.TC_API_KEY,
    secret=config.TC_API_SECRET,
    request_options={
        'request_timeout': 30,
        'nr_of_retries': 5,
        'retry_status_codes': [500, 502, 503, 504]
    }
)

ftx = ccxt.ftx({
    'apiKey': config.FTX_API_KEY,
    'secret': config.FTX_SECRET_KEY,
    'headers': {'FTX-SUBACCOUNT': config.FTX_SUBACCOUNT}
})

#ftx.verbose = True

def get_tradeable_balance():
    trycnt = 4
    while trycnt > 0:
        try:
            account_balances = ftx.fetch_balance()
            balance = account_balances["total"]["USD"]
            print(f'Balance: {balance}')
            trycnt = 0
        except Exception as e:
            print(e)
            f = open(config.LOGFILE, "a")
            f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - FTX connection error: {e}\n')
            f.close()
            trycnt -= 1
            if trycnt == 3:
                print(f'Connection error, trying again... (count down: {trycnt})')
                time.sleep(5)
            elif trycnt == 2:
                print(f'Connection error, trying again... (count down: {trycnt})')
                time.sleep(15)
            elif trycnt == 1:
                print(f'Connection error, trying again... (count down: {trycnt})')
                time.sleep(45)
            elif trycnt == 0:
                print('Giving up....')
                exit()
        else:
            return balance

def get_max_bot_usage(balance):
    if config.SAFETY_ORDER_VOLUME_SCALE == 1.0:
        max_bot_usage = (config.BASE_ORDER_SIZE + (config.SAFETY_ORDER_SIZE*config.MAX_SAFETY_ORDERS_COUNT)) / config.LEVERAGE_CUSTOM_VALUE
    else:
        max_bot_usage = (config.BASE_ORDER_SIZE + (config.SAFETY_ORDER_SIZE*(config.SAFETY_ORDER_VOLUME_SCALE**config.MAX_SAFETY_ORDERS_COUNT - 1) / (config.SAFETY_ORDER_VOLUME_SCALE - 1))) / config.LEVERAGE_CUSTOM_VALUE
    return max_bot_usage


def perp_stats(perp):
    stats = []
    time_frame_mins = config.TF
    adx_length = config.ADX_LENGTH
    ema_length = config.EMA_LENGTH
    look_back = max(adx_length, ema_length)*4
    current_time = datetime.datetime.now()
    from_time = current_time - datetime.timedelta(minutes = time_frame_mins*look_back)
    from_time_stamp = int(from_time.timestamp() * 1000)
    if time_frame_mins < 60:
        time_frame = time_frame_mins
        time_frame_units = 'm'
    elif time_frame_mins >= 60:
        time_frame = int(time_frame_mins//60)
        time_frame_units = 'h'
    trycnt = 4
    while trycnt > 0:
        try:
            candles = ftx.fetch_ohlcv(perp, str(int(time_frame)) + time_frame_units, from_time_stamp)
            trycnt = 0
        except Exception as e:
            print("Connection error, trying again...")
            f = open(config.LOGFILE, "a")
            f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - FTX connection error.\n')
            f.close()
            trycnt -= 1
            if trycnt == 3:
                time.sleep(3)
            elif trycnt == 2:
                time.sleep(15)
            elif trycnt == 1:
                time.sleep(45)
        else:
            # Load data into a pandas dataframe
            df = pd.DataFrame(np.array(candles), columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            # Get ADX and DMI values
            df.ta.adx(close='Close', length=adx_length, append=True)
            # Get ADX Slope
            df['ADX_SLOPE'] = df['ADX_'+str(adx_length)].diff()
            # Get EMA Values 
            df.ta.ema(close='Close', length=ema_length, append=True)
            # Calculate normalized Slope of EMA values
            df['EMA_SLOPE'] = df['EMA_'+str(ema_length)].diff().abs() / df['EMA_'+str(ema_length)]
            # Calculate EMA(3) of slope values
            df['EMA_SMOOTH'] = df['EMA_SLOPE'].ewm(span=config.EMA_SMOOTHING).mean()
            #if df.loc[(df.shape[0]-2), 'ADX_SLOPE'] > 0:
            #    adx_direction = 1
            #elif df.loc[(df.shape[0]-2), 'ADX_SLOPE'] =< 0:
            #    adx_direction = -1

            if config.EARLY_CLOSE and df.loc[(df.shape[0]-2), 'ADX_SLOPE'] < df.loc[(df.shape[0]-3), 'ADX_SLOPE'] and df.loc[(df.shape[0]-3), 'ADX_SLOPE'] < df.loc[(df.shape[0]-4), 'ADX_SLOPE'] and df.loc[(df.shape[0]-4), 'ADX_SLOPE'] and df.loc[(df.shape[0]-5), 'ADX_SLOPE']:
                adx_direction = -1
            else:
                adx_direction = df.loc[(df.shape[0]-2), 'ADX_SLOPE']
            
            # Add values to a list
            stats.append(perp)
            stats.append(df.loc[(df.shape[0]-2), 'ADX_'+str(adx_length)])
            stats.append(adx_direction)
            stats.append(df.loc[(df.shape[0]-2), 'DMP_'+str(adx_length)])
            stats.append(df.loc[(df.shape[0]-2), 'DMN_'+str(adx_length)])
            stats.append(df.loc[(df.shape[0]-2), 'EMA_SMOOTH'])
            return stats

def get_positions():
    open_positions = {}
    all_positions = ftx.fetchPositions(None, {"showAvgPrice": True})
    try:
      if 'info' in all_positions[0]:
        for y in all_positions:
            x=y['info']
            future = (x["future"])
            size = (x["size"])
            side = (x["side"])
            cost = (x["cost"])
            recentAverageOpenPrice = (x["recentAverageOpenPrice"])
            if size != '0.0':
                open_positions[future] = size, side, cost, recentAverageOpenPrice
      else:
        for x in all_positions:
            future = (x["future"])
            size = (x["size"])
            side = (x["side"])
            cost = (x["cost"])
            recentAverageOpenPrice = (x["recentAverageOpenPrice"])
            if size != '0.0':
                open_positions[future] = size, side, cost, recentAverageOpenPrice
    except Exception as e:
      pass
    return open_positions


def get_markets():
    trycnt = 4
    while trycnt > 0:
        try:
            all_markets = ftx.load_markets(True)
            trycnt = 0
        except Exception as e:
            print("Connection error, trying again...")
            f = open(config.LOGFILE, "a")
            f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - FTX connection error\n')
            f.close()
            trycnt -= 1
            if trycnt == 3:
                time.sleep(3)
            elif trycnt == 2:
                time.sleep(15)
            elif trycnt == 1:
                time.sleep(45)
        else:
            return all_markets

def start_bot(pair, ids):
    bot_id = ids[pair]
    error, bot_trigger = p3cw.request(
        entity = 'bots',
        action = 'enable',
        action_id = bot_id
    )   
    print(f'Bot Enabled for {pair} - {bot_id}')
    f = open(config.LOGFILE, "a")
    f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - Enable bot for {pair}; id: {bot_id}\n')
    f.close()
    return bot_trigger

def disable_bot(pair, bot_id):
    error, data = p3cw.request(
        entity='bots',
        action='disable',
        action_id = str(bot_id),
    )
    print(f'Error: {error}')
    print(f'Bot Disabled for {pair} - {bot_id}')
    f = open(config.LOGFILE, "a")
    f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - Disable bot for {pair}; id: {bot_id}\n')
    f.close()

def close_deal(pair, bot_id):
    if type(bot_id) is not int:
        bot_id = bot_id[pair]
    error, deal_close = p3cw.request(
        entity = 'bots',
        action = 'panic_sell_all_deals',
        action_id = str(bot_id)
    )
    print(f'Panic Close - {pair}')
    f = open(config.LOGFILE, "a")
    f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - Panic Close {pair}; id: {bot_id}\n')
    f.close()
    time.sleep(5)
    return deal_close


def load_bot_ids(filename):
    d = {}
    with open(filename) as f:
        for line in f:
            (key, val) = line.split(':')
            d[key] = val.rstrip('\n')
    return d

def get_bot_info():
    data = []
    bot_info = []
    first_run = True
    base_offset = 100
    offset = 0
    while len(data) == 100 or first_run:
        first_run = False
        error, data = p3cw.request(
            entity='bots',
            action='',
            payload={
                "account_id": config.TC_ACCOUNT_ID,
                "limit": base_offset,
                "offset": offset,
            }
        )
        if type(data) is not list:
            print("Data from 3Commas is not a list.")
            print(data)
            data = []
        bot_info = bot_info + data
        offset += base_offset
    return bot_info

def get_enabled_bots():
    enabled_bots = {}
    bot_list = get_bot_info()
    for bot in bot_list:
        if bot["is_enabled"] == True:
            bot_id = bot["id"]
            bot_pair = bot["pairs"][0]
            bot_strategy = bot["strategy"]
            enabled_bots[bot_pair[4:]] = bot_id, bot_strategy
    return enabled_bots

#############################################################

open_positions = {}
enabled_bots = {}

# Check for existing list of bot id's and load into a dictionary
longbots_file = Path(config.LIST_LONGBOTS)
shortbots_file = Path(config.LIST_SHORTBOTS)
if not longbots_file.is_file() or not shortbots_file.is_file():
    print("No bot ID lists were found. Create bots and ID list before continuing.")
    print("Bye!")
    sys.exit()

# Load files into a dictionary
long_bot_ids = {}
short_bot_ids = {}
long_bot_ids = load_bot_ids(config.LIST_LONGBOTS)
short_bot_ids = load_bot_ids(config.LIST_SHORTBOTS)

# Check the balance at FTX
tradeable_balance = get_tradeable_balance()
# Calculate the costs of a bot
bot_usage = get_max_bot_usage(tradeable_balance) # Result is not precise !!                                     <<<<<<
print(f'Max bot usage: {bot_usage}')
# Calc max number of bots - constrained by bot usage
max_bots = math.floor((float(tradeable_balance) * config.FUNDS_USAGE) / bot_usage)
if max_bots < config.MAX_OPEN_POSITIONS:
    max_positions = max_bots
else:
    max_positions = config.MAX_OPEN_POSITIONS
print(f'Max positions: {max_positions}')
if max_positions < 1:
    print('ERROR: Not enough liquidity to start a bot')
    exit()
    
last_balance_check = strftime("%Y-%m-%d", gmtime())

f = open(config.LOGFILE, "a")
f.write(f"#### SCRIPT START {strftime('%Y-%m-%d %H:%M:%S', gmtime())} UTC ####\n")
f.write(f'Time-frame: {config.TF}\n')
f.write(f'Balance: {tradeable_balance}, Max Positions: {max_positions}\n')
f.close()

update_stats_time = True

##    <<<<<<<<<<<   START LOOP HERE     >>>>>>>>>>>>>>>>>

unsorted_tradable_perps = []
sorted_tradable_perps = []
tradable_perps = {}

while True:
    time.sleep(0.5) # Give the CPU a break.
    while update_stats_time:
        print('Getting perps OHLCV data...')
        for perp in long_bot_ids:
            unfiltered_stats = perp_stats(perp)
            ADX = unfiltered_stats[1]
            ADX_Slope = unfiltered_stats[2]
            DM_plus = unfiltered_stats[3]
            DM_minus = unfiltered_stats[4]
            if ADX > 15 and (ADX_Slope > 0 and ((DM_plus > DM_minus and ADX > DM_minus) or (ADX < DM_plus and ADX < DM_minus))) and DM_plus > DM_minus:
                unfiltered_stats.append("long")
                unsorted_tradable_perps.append(unfiltered_stats)
            elif ADX > 15 and (ADX_Slope > 0 and ((DM_plus < DM_minus and ADX > DM_plus) or (ADX < DM_plus and ADX < DM_minus))) and DM_plus < DM_minus:
                unfiltered_stats.append("short")
                unsorted_tradable_perps.append(unfiltered_stats)
            elif ADX_Slope < 0:
                unfiltered_stats.append("disable")
                unsorted_tradable_perps.append(unfiltered_stats)
            else:
                unfiltered_stats.append("ignore")
                unsorted_tradable_perps.append(unfiltered_stats)
            print(".", end =" ")

        # Sort the lists by EMA Slope
        sorted_tradable_perps = sorted(unsorted_tradable_perps, key=operator.itemgetter(5), reverse = True)

        # Convert list to dictionary
        number_of_perps = len(sorted_tradable_perps)
        i = 0
        for i in range(number_of_perps):
            tradable_perps[sorted_tradable_perps[i][0]] = sorted_tradable_perps[i][1], sorted_tradable_perps[i][2], sorted_tradable_perps[i][3], sorted_tradable_perps[i][4], sorted_tradable_perps[i][5], sorted_tradable_perps[i][6]
        
        # Show open positions
        open_positions = get_positions()
        print("Open Positions:")
        print(json.dumps(open_positions, indent=4, sort_keys=True))
        f = open(config.LOGFILE, "a")
        f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - Open Positions: {open_positions}\n')
        f.close()

        # Show enabled bots
        enabled_bots = get_enabled_bots()
        print("Enabled Bots:")
        print(enabled_bots)
        f = open(config.LOGFILE, "a")
        f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - Enabled Bots: {enabled_bots}\n')
        f.close()
        
        available_bots = max_positions - max(len(enabled_bots), len(open_positions))

        # Check for orphaned deals - Only useful for when CLOSE_DEALS_WITH_BOT = True
        for open_perp in open_positions:
            if open_perp not in enabled_bots and config.CLOSE_DEALS_WITH_BOT:
                if open_positions[open_perp][1] == "buy":
                    close_deal(open_perp, long_bot_ids)
                if open_positions[open_perp][1] == "sell":
                    close_deal(open_perp, short_bot_ids)

        # Handle Open positions without active/enabled bots.
        for disabled_perp in open_positions:
            if disabled_perp not in enabled_bots:
                if config.CLOSE_DEALS:
                    if tradable_perps[disabled_perp][2] > tradable_perps[disabled_perp][3] and open_positions[disabled_perp][1] == "sell":
                        close_deal(disabled_perp, short_bot_ids)
                    elif tradable_perps[disabled_perp][2] < tradable_perps[disabled_perp][3] and open_positions[disabled_perp][1] == "buy":
                        close_deal(disabled_perp, long_bot_ids)
                    elif tradable_perps[disabled_perp][0] < 15 and open_positions[disabled_perp][1] == "sell":
                        close_deal(disabled_perp, short_bot_ids)
                    elif tradable_perps[disabled_perp][0] < 15 and open_positions[disabled_perp][1] == "buy":
                        close_deal(disabled_perp, long_bot_ids)
       
        # Disable a bot if ADX slope goes negative.
        for adx_perp in enabled_bots:
            if adx_perp in tradable_perps:
                if tradable_perps[adx_perp][5] == "disable" or tradable_perps[adx_perp][5] == "ignore":
                    disable_bot(adx_perp, enabled_bots[adx_perp][0])
                    if config.CLOSE_DEALS_WITH_BOT:
                        close_deal(adx_perp, enabled_bots[adx_perp][0])

        time.sleep(10) # Small delay, closing positions above lag execution of following two lines.

        open_positions = get_positions()   # Refresh the open positions after previous actions
        enabled_bots = get_enabled_bots()  # Refresh the enabled bots after previous actions
        available_bots = max_positions - max(len(enabled_bots), len(open_positions)) # Refresh the amount of bots we could start

        if available_bots == 0 and ((len(open_positions) - len(enabled_bots))/max_positions) > config.DEAL_BOT_RATIO_WARNING:
            print("WARNING !! Too much active deals (open positions) without enabled bots !! Consider manually closing open positions.")
            f = open(config.LOGFILE, "a")
            f.write(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC - RATIO WARNING !! Too much active deals (open positions) without enabled bots; Max positions: {max_positions}; Open positions: {len(open_positions)}; Enabled bots: {len(enabled_bots)}\n')
            f.close()
        print(f'Max Positions: {max_positions}')
        print(f'Open positions: {len(open_positions)}')
        print(f'Enabled Bots: {len(enabled_bots)}')
        print(f'Available Bots: {available_bots}')
        
        # Start (enable) bots
        if tradable_perps and available_bots > 0:
            print("Getting ready to enable bots....")
            for trade_perp in tradable_perps:
                if trade_perp not in enabled_bots and available_bots > 0:
                    if tradable_perps[trade_perp][5] == "long":
                        start_bot(trade_perp, long_bot_ids)
                        available_bots -= 1
                    elif tradable_perps[trade_perp][5] == "short":
                        start_bot(trade_perp, short_bot_ids)
                        available_bots -= 1

        update_stats_time = False
        # write to file next expected checkin time.
        next_update = datetime.datetime.now() + datetime.timedelta(seconds=config.TF*60)
        #f = open(config.LOGFILE, "a")
        #f.write(str(next_update))
        #f.close()
        print("Waiting for next TF....")
        time.sleep(60)
        
    print("[debug] end update_stats_time")

    open_positions.clear()
    unsorted_tradable_perps.clear()
    sorted_tradable_perps.clear()
    tradable_perps.clear()
    enabled_bots.clear()


    #now = datetime.datetime.now()
    
    if strftime("%Y-%m-%d", gmtime()) > last_balance_check:
        tradeable_balance = get_tradeable_balance()
        bot_usage = get_max_bot_usage(tradeable_balance)
        if math.floor((float(tradeable_balance) * config.FUNDS_USAGE) / bot_usage) < config.MAX_OPEN_POSITIONS:
            max_positions = math.floor((float(tradeable_balance) * config.FUNDS_USAGE) / bot_usage)
        else:
            max_positions = config.MAX_OPEN_POSITIONS

        last_balance_check = strftime("%Y-%m-%d", gmtime())
        f = open(config.LOGFILE, "a")
        f.write(f'Updated Balance: {tradeable_balance}, Max Positions: {max_positions} at {strftime("%Y-%m-%d %H:%M:%S", gmtime())} UTC\n')
        f.write(">>>>\n")
        f.close()
        print(f'Updated Balance: {tradeable_balance}, Max Positions: {max_positions}')
        

    now = datetime.datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes = ((now - midnight).seconds) // 60
    
    if (minutes % config.TF) == 0 :
        time.sleep(5)
        update_stats_time = True
