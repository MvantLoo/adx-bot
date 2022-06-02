# 3Commas FTX ADX Trigger Script
 
This script creates a set of trading bots on [3Commas.io](https://3commas.io/?c=tc954485) based on available perpetual futures on [FTX.com](https://ftx.com/referrals#a=mvantloo), and automatically provides triggers for those bots to start deals.

- [Original blog about this script](https://onepercent.blog/2022/01/16/35-percent-roi-in-15-days-new-automated-trading-script/)
- [Original blog about Google Cloud VM](https://onepercent.blog/2022/01/11/run-python-trading-bots-on-google-vm-cloud/)

## Setup FTX and 3Commas

#### Create and setup FTX
- Create an FTX account
  - Go to [FTX.com](https://ftx.com/referrals#a=mvantloo)
  - Follow the registration process
- Logon and deposit tokens of your choice.
  - Go to https://ftx.com/wallet and `CONVERT` the tokens to `USD (USD)` as this script __only__ works with USD.
- Go to the Subaccounts page: https://ftx.com/profile#Subaccounts
  - Press `CREATE SUBACCOUNT`, call this `PyBot1`
  - At `Select Account`, choose `PyBot1`, see at the right-top that you see the name of this sub-account.
  - At `Transfer Funds Between Subaccounts` choose `USD (USD)`, Source Account: `Main Account`, Destination Account: `PyBot1` and the amount of USD that you want to use for this script.
  - Go to the Wallet at https://ftx.com/wallet, look at the right-top to see if you are at subaccount `PyBot1` and see if you see your USD's.
- Click at your name in the right-top and select `API`: https://ftx.com/settings/api
  - Press `Create API Key for PyBot1`
  - Copy `API key` and `API Secret` to a text-file for later usage

#### Create and setup 3Commas
- Create a free 3Commas account
  - Go to [3Commas.io](https://3commas.io/?c=tc954485) 
  - Press `Try It Free`
  - Follow the registration process
- Logon, click on the round icon at the right-top and select `API`
- Press `+ New API access token`
  - Name: pybot
  - Select: `Bots read`, `Bots write` and `Accounts read`
  - Copy `API key` and `API Secret` to a text-file for later usage
- Connect 3Commas with FTX
  - Go to `My Exchanges`: https://3commas.io/accounts
  - Press `+ Connect a new exchange`
  - Select `API Connect`
  - Name: `FTX`
  - Sub-accoun Name: `PyBot1`
  - API Key: Use the FTX API Key
  - API Secret: Use the FTX API Secret

## Setup Google Cloud VM

- Go to https://cloud.google.com/
- Select at Compute Engine: `VM instances`
- Press at `Create Instance` (Enable API if needed)
  - Name: `vm-pybot`
  - Region: `us-east1 (South Carolina)`
  - Machine type: `e2-micro (2 vCPU, 1 GB memory`
  - `CREATE`
- When the VM is created
  - Go to https://console.cloud.google.com/compute/instances
  - Press under Connect at `SSH`. An commandline interface should pop-up in a new window.
- Execute the following commands
  1. ```
     sudo apt-get -y update
     ```
  1. ```
     sudo apt-get -y install build-essential wget unzip tmux python3 python3-pip
     ```
  1. ```
     pip3 install --upgrade setuptools
     pip3 install TA-lib pandas_ta ccxt py3cw
     ```
  1. ```
     sudo wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
     tar -xzf ta-lib-0.4.0-src.tar.gz
     cd ta-lib/
     ./configure --prefix=/usr
     make
     sudo make install
     cd ..
     ```
  1. ```
     git clone https://github.com/MvantLoo/adx-bot
     ```


## Configure and run the adx-bot

- Execute the following commands
  1. ```
     cd adx-bot
	 cp example.config.py config.py
	 ```
  1. ```
     nano config.py
	 ```
- Update the following lines:
  1. `TC_ACCOUNT_ID = ''` 3Commas Account ID
  1. `TC_API_KEY = ''` 3Commas API Key
  1. `TC_API_SECRET = ''` 3Commas API Secret

  1. `API_KEY = ''` FTX API Key
  1. `SECRET_KEY = ''` FTX Secret Key
  1. `SUB_ACCOUNT = ''` FTX Sub-account
- Save the file and exit nano with `Ctrl-X`, confirm the filename.
- Start a new Tmux session
  ```
  tmux new -s pybot1
  ```
- Create the bots
  ```
  python3 Py3c_create.py
  ```
- Run the script
  ```
  python3 adx_bot.py
  ```
- Sit back and enjoy

### Reopen the running script

If for whatever reason you loose access to the SSH window, you can open a new window and reopen the running session.

- Go to https://console.cloud.google.com/compute/instances
- Press under Connect at `SSH`. An commandline interface should pop-up in a new window.
- List the running Tmux sessions
  ```
  tmux ls
  ```
- Attach to the running `pybot1` session
  ```
  tmux a -t pybot1
  ```
