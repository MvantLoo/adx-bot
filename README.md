# 3Commas FTX ADX Trigger Script
 
This script creates a set of trading bots on [3Commas.io](https://3commas.io/?c=tc954485) based on available perpetual futures on [FTX.com](https://ftx.com/referrals#a=mvantloo), and automatically provides triggers for those bots to start deals.

- [Original blog about this script](https://onepercent.blog/2022/01/16/35-percent-roi-in-15-days-new-automated-trading-script/)
- [Original blog about Google Cloud VM](https://onepercent.blog/2022/01/11/run-python-trading-bots-on-google-vm-cloud/)

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
  1. `sudo apt-get -y update`
  1. `sudo apt-get -y install build-essential wget unzip tmux python3 python3-pip`
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

## Setup FTX and 3Commas

- x
- y

## Configure and run the adx-bot

- x
- y

