# 3Commas account setttings
TC_ACCOUNT_ID = ''
TC_API_KEY = ''
TC_API_SECRET = ''
TC_BASE_URL = 'https://api.3commas.io'

# FTX account settings
FTX_API_KEY = ''
FTX_SECRET_KEY = ''
FTX_SUBACCOUNT = ''


PAIRS_BLACKLIST = ['STEP-PERP', 'DMG-PERP', 'BRZ-PERP', 'PERP/USD', 'SRN-PERP', 'PRIV-PERP', 'SHIB-PERP', 'CUSDT-PERP']
MAX_OPEN_POSITIONS = 100
FUNDS_USAGE = 0.8

# ADX settings
TF = 15 # 15 Timeframe - always in minutes - minimum: 5, less than 1 day.
ADX_LENGTH = 14
EMA_LENGTH = 20
EMA_SMOOTHING = 3
DEAL_BOT_RATIO_WARNING = 0.75 # Warn when ratio of open-positions-without-enabled-bot is high. (between 0 and 1)
CLOSE_DEALS_WITH_BOT = False  # WARNING: Will close all open positions (deals) with no equivalent enabled bots.
EARLY_CLOSE = False # line 124, unknown what/why
CLOSE_DEALS = False # Allow bot to close deals on opposite signals. Use False to manually rescue red bags.

# 3Commas Bot Settings - Example settings use max 15 USD per deal
LONG_PREFIX = 'LongADX_'
SHORT_PREFIX = 'ShortADX_'
TAKE_PROFIT = 2 # %
BASE_ORDER_SIZE   = 5 # In USD
SAFETY_ORDER_SIZE = 2 # In USD
MAX_SAFETY_ORDERS_COUNT = 5
MAX_ACTIVE_SAFETY_ORDERS_COUNT = 2
SAFETY_ORDER_VOLUME_SCALE = 1
SAFETY_ORDER_STEP_SCALE = 1
SAFETY_ORDER_STEP_PERCENTAGE = 3 # Price deviation to open safety orders
LEVERAGE_CUSTOM_VALUE = 1

# Used When Updating Bot Settings
STOP_LOSS_TYPE = 'stop_loss_and_disable_bot'  # or stop_loss
STOP_LOSS_PERCENTAGE = 0
STOP_LOSS_TIMEOUT_ENABLED = False
STOP_LOSS_TIMEOUT_IN_SECONDS = 300
START_ORDER_TYPE = 'market'
#MIN_VOLUME = 150

# Script settings - DO NOT EDIT
LIST_LONGBOTS = 'list_longbots.txt'
LIST_SHORTBOTS = 'list_shortbots.txt'
LIST_ERRORBOTS = 'list_bots_not_created.txt'
LOGFILE = 'adx_bot.log'