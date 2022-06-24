# Read config, set the defaults, do some basic tests

import config

try:    config.TC_ACCOUNT_ID = str(config.TC_ACCOUNT_ID)
except: config.TC_ACCOUNT_ID = ''
if not config.TC_ACCOUNT_ID.isnumeric():
    print("TC_ACCOUNT_ID is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.TC_API_KEY = str(config.TC_API_KEY)
except: config.TC_API_KEY = ''
if len(config.TC_API_KEY) != 64:
    print("TC_API_KEY is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.TC_API_SECRET = str(config.TC_API_SECRET)
except: config.TC_API_SECRET = ''
if len(config.TC_API_SECRET) != 200:
    print("TC_API_SECRET is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.TC_BASE_URL = str(config.TC_BASE_URL)
except: config.TC_BASE_URL = 'https://api.3commas.io'

try:    config.FTX_API_KEY = str(config.FTX_API_KEY)
except: config.FTX_API_KEY = ''
if len(config.FTX_API_KEY) != 40:
    print(len(config.FTX_API_KEY))
    print("FTX_API_KEY is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.FTX_SECRET_KEY = str(config.FTX_SECRET_KEY)
except: config.FTX_SECRET_KEY = ''
if len(config.FTX_SECRET_KEY) != 40:
    print("FTX_SECRET_KEY is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.FTX_SUBACCOUNT = str(config.FTX_SUBACCOUNT)
except: config.FTX_SUBACCOUNT = ''
if len(config.FTX_SUBACCOUNT) < 1:
    print("FTX_SUBACCOUNT is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.PAIRS_BLACKLIST
except: config.PAIRS_BLACKLIST = []

try:    config.MAX_OPEN_POSITIONS
except: config.MAX_OPEN_POSITIONS = 1
try:    config.MAX_OPEN_POSITIONS = int(config.MAX_OPEN_POSITIONS)
except: 
    print(type(config.MAX_OPEN_POSITIONS))
    print("MAX_OPEN_POSITIONS should be a number (integer).\nUpdate file `config.py`.")
    exit(1)
if config.MAX_OPEN_POSITIONS < 1:
    print("MAX_OPEN_POSITIONS should 1 or higher.\nUpdate file `config.py`.")
    exit(1)

try:    config.FUNDS_USAGE
except: config.FUNDS_USAGE = 0.75
try:    config.FUNDS_USAGE = float(config.FUNDS_USAGE)
except:
    print("FUNDS_USAGE should be a number.\nUpdate file `config.py`.")
    exit(1)
if config.FUNDS_USAGE <= 0:
    print("FUNDS_USAGE should be higher then 0 and lower or equal to 1. (1 = 100%)\nUpdate file `config.py`.")
    exit(1)
if config.FUNDS_USAGE > 1:
    print("FUNDS_USAGE should be equal or lower then 1. (1 = 100%)\nUpdate file `config.py`.")
    exit(1)

try:    config.TF
except: config.TF = 15
try:    config.TF = int(config.TF)
except:
    print("TF (TimeFrame in minutes) should be a number (integer) between 5 and 1439. \nUpdate file `config.py`.")
    exit(1)
if config.TF < 5 or config.TF > 1439:
    print("TF (TimeFrame in minutes) should be between 5 and 1439. \nUpdate file `config.py`.")
    exit(1)

try:    config.ADX_LENGTH
except: config.ADX_LENGTH = 14
try:    config.ADX_LENGTH = int(config.ADX_LENGTH)
except:
    print("ADX_LENGTH should be a number (integer). \nUpdate file `config.py`.")
    exit(1)

try:    config.EMA_LENGTH
except: config.EMA_LENGTH = 20
try:    config.EMA_LENGTH = int(config.EMA_LENGTH)
except:
    print("EMA_LENGTH should be a number (integer). \nUpdate file `config.py`.")
    exit(1)

try:    config.EMA_SMOOTHING
except: config.EMA_SMOOTHING = 3
try:    config.EMA_SMOOTHING = int(config.EMA_SMOOTHING)
except:
    print("EMA_SMOOTHING should be a number (integer). \nUpdate file `config.py`.")
    exit(1)

try:    config.DEAL_BOT_RATIO_WARNING
except: config.DEAL_BOT_RATIO_WARNING = 0.75
try:    config.DEAL_BOT_RATIO_WARNING = float(config.DEAL_BOT_RATIO_WARNING)
except:
    print("DEAL_BOT_RATIO_WARNING should be a number.\nUpdate file `config.py`.")
    exit(1)
if config.DEAL_BOT_RATIO_WARNING <= 0:
    print("DEAL_BOT_RATIO_WARNING should be higher then 0 and lower or equal to 1. (1 = 100%)\nUpdate file `config.py`.")
    exit(1)
if config.DEAL_BOT_RATIO_WARNING > 1:
    print("DEAL_BOT_RATIO_WARNING should be equal or lower then 1. (1 = 100%)\nUpdate file `config.py`.")
    exit(1)

try:    config.CLOSE_DEALS_WITH_BOT
except: config.CLOSE_DEALS_WITH_BOT = False

try:    config.EARLY_CLOSE
except: config.EARLY_CLOSE = False

try:    config.CLOSE_DEALS
except: config.CLOSE_DEALS = False

try:    config.LONG_PREFIX = str(config.LONG_PREFIX)
except: config.LONG_PREFIX = 'LongADX_'

try:    config.LONG_PREFIX = str(config.LONG_PREFIX)
except: config.LONG_PREFIX = 'ShortADX_'

try:    config.TAKE_PROFIT
except: config.TAKE_PROFIT = 2.0
try:    config.TAKE_PROFIT = float(config.TAKE_PROFIT)
except:
    print("TAKE_PROFIT should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.TAKE_PROFIT <= 0:
    print("TAKE_PROFIT should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.BASE_ORDER_SIZE
except: config.BASE_ORDER_SIZE = 5.0
try:    config.BASE_ORDER_SIZE = float(config.BASE_ORDER_SIZE)
except:
    print("BASE_ORDER_SIZE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.BASE_ORDER_SIZE <= 0:
    print("BASE_ORDER_SIZE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.SAFETY_ORDER_SIZE
except: config.SAFETY_ORDER_SIZE = 2.0
try:    config.SAFETY_ORDER_SIZE = float(config.SAFETY_ORDER_SIZE)
except:
    print("SAFETY_ORDER_SIZE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.SAFETY_ORDER_SIZE <= 0:
    print("SAFETY_ORDER_SIZE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.MAX_SAFETY_ORDERS_COUNT
except: config.MAX_SAFETY_ORDERS_COUNT = 5
try:    config.MAX_SAFETY_ORDERS_COUNT = int(config.MAX_SAFETY_ORDERS_COUNT)
except:
    print("MAX_SAFETY_ORDERS_COUNT should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.MAX_SAFETY_ORDERS_COUNT <= 0:
    print("MAX_SAFETY_ORDERS_COUNT should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.MAX_ACTIVE_SAFETY_ORDERS_COUNT
except: config.MAX_ACTIVE_SAFETY_ORDERS_COUNT = 2
try:    config.MAX_ACTIVE_SAFETY_ORDERS_COUNT = int(config.MAX_ACTIVE_SAFETY_ORDERS_COUNT)
except:
    print("MAX_ACTIVE_SAFETY_ORDERS_COUNT should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.MAX_ACTIVE_SAFETY_ORDERS_COUNT <= 0:
    print("MAX_ACTIVE_SAFETY_ORDERS_COUNT should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.SAFETY_ORDER_VOLUME_SCALE
except: config.SAFETY_ORDER_VOLUME_SCALE = 1.0
try:    config.SAFETY_ORDER_VOLUME_SCALE = float(config.SAFETY_ORDER_VOLUME_SCALE)
except:
    print("SAFETY_ORDER_VOLUME_SCALE should be a number. \nUpdate file `config.py`.")
    exit(1)
if config.SAFETY_ORDER_VOLUME_SCALE <= 0:
    print("SAFETY_ORDER_VOLUME_SCALE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.SAFETY_ORDER_STEP_SCALE
except: config.SAFETY_ORDER_STEP_SCALE = 1.0
try:    config.SAFETY_ORDER_STEP_SCALE = float(config.SAFETY_ORDER_STEP_SCALE)
except:
    print("SAFETY_ORDER_STEP_SCALE should be a number. \nUpdate file `config.py`.")
    exit(1)
if config.SAFETY_ORDER_STEP_SCALE <= 0:
    print("SAFETY_ORDER_STEP_SCALE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.SAFETY_ORDER_STEP_PERCENTAGE
except: config.SAFETY_ORDER_STEP_PERCENTAGE = 3.0
try:    config.SAFETY_ORDER_STEP_PERCENTAGE = float(config.SAFETY_ORDER_STEP_PERCENTAGE)
except:
    print("SAFETY_ORDER_STEP_PERCENTAGE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.SAFETY_ORDER_STEP_PERCENTAGE <= 0:
    print("SAFETY_ORDER_STEP_PERCENTAGE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.LEVERAGE_CUSTOM_VALUE
except: config.LEVERAGE_CUSTOM_VALUE = 1
try:    config.LEVERAGE_CUSTOM_VALUE = int(config.LEVERAGE_CUSTOM_VALUE)
except:
    print("LEVERAGE_CUSTOM_VALUE should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.LEVERAGE_CUSTOM_VALUE <= 0:
    print("LEVERAGE_CUSTOM_VALUE should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.START_CONDITION = str(config.START_CONDITION)
except: config.START_CONDITION = 'ASAP'
if len(config.START_CONDITION) < 4:
    print("START_CONDITION is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.STOP_LOSS_TYPE = str(config.STOP_LOSS_TYPE)
except: config.STOP_LOSS_TYPE = 'stop_loss_and_disable_bot'
if len(config.STOP_LOSS_TYPE) < 4:
    print("STOP_LOSS_TYPE is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.STOP_LOSS_PERCENTAGE
except: config.STOP_LOSS_PERCENTAGE = 0
try:    config.STOP_LOSS_PERCENTAGE = float(config.STOP_LOSS_PERCENTAGE)
except:
    print("STOP_LOSS_PERCENTAGE should be a number (float) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.STOP_LOSS_PERCENTAGE < 0 or config.STOP_LOSS_PERCENTAGE >= 100:
    print("STOP_LOSS_PERCENTAGE should be a number (float) higher or equal then 0 and lower then 100. \nUpdate file `config.py`.")
    exit(1)

try:    config.STOP_LOSS_TIMEOUT_ENABLED
except: config.STOP_LOSS_TIMEOUT_ENABLED = False

try:    config.STOP_LOSS_TIMEOUT_IN_SECONDS
except: config.STOP_LOSS_TIMEOUT_IN_SECONDS = 300
try:    config.STOP_LOSS_TIMEOUT_IN_SECONDS = int(config.STOP_LOSS_TIMEOUT_IN_SECONDS)
except:
    print("STOP_LOSS_TIMEOUT_IN_SECONDS should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)
if config.STOP_LOSS_TIMEOUT_IN_SECONDS <= 0:
    print("STOP_LOSS_TIMEOUT_IN_SECONDS should be a number (integer) higher then 0. \nUpdate file `config.py`.")
    exit(1)

try:    config.START_ORDER_TYPE = str(config.START_ORDER_TYPE)
except: config.START_ORDER_TYPE = 'market'
if len(config.START_ORDER_TYPE) < 4:
    print("START_ORDER_TYPE is missing, not filled in or contains errors.\nUpdate file `config.py`.")
    exit(1)

try:    config.LIST_LONGBOTS = str(config.LIST_LONGBOTS)
except: config.LIST_LONGBOTS = 'list_longbots.txt'

try:    config.LIST_SHORTBOTS = str(config.LIST_SHORTBOTS)
except: config.LIST_SHORTBOTS = 'list_shortbots.txt'

try:    config.LIST_ERRORBOTS = str(config.LIST_ERRORBOTS)
except: config.LIST_ERRORBOTS = 'list_bots_not_created.txt'

try:    config.LOGFILE = str(config.LOGFILE)
except: config.LOGFILE = 'adx_bot.log'
