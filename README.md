# 3Commas FTX ADX Trigger Script
 
This script creates a set of trading bots on [3Commas.io](https://3commas.io/?c=tc954485) based on available perpetual futures on [FTX.com](https://ftx.com/referrals#a=mvantloo), and automatically provides triggers for those bots to start deals.

- [Original blog about this script](https://onepercent.blog/2022/01/16/35-percent-roi-in-15-days-new-automated-trading-script/)
- [Original blog about Google Cloud VM](https://onepercent.blog/2022/01/11/run-python-trading-bots-on-google-vm-cloud/)

## Setup FTX and 3Commas

- x
- y

## Setup Google Cloud VM

- Go to https://cloud.google.com/
- Select at Compute Engine: `VM instances`
- Press at `Create Instance` (Enable API if needed)
  - Name: `vm-pybot`
  - Region: `us-east1 (South Carolina)`
  - Machine type: `e2-micro (2 vCPU, 1 GB memory`
  - CREATE
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
