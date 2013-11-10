Algorithm trading for Bitcoin
---
Use simple moving average as trading strategy.

Installation
---
sudo pip install requests pandas

sudo pip install git+git://github.com/kmadac/bitstamp-python-client.git

Use
---
First you need get access key and secret from Bitstamp.
Login Bitstamp and click on Account -> Security -> API Access.
Follow the instructions to get a new API key.  The followin permissions are required:
Account balance, User transactions, Open orders, Cancel order Buy limit order, Sell limit order.

Then create a file ~/.bitstamp.  The file contains 3 lines:

UserID

Key

Secret

With the file you can run
`./src/run.sh ~/.bitstamp`

Dependencies
---
* http://bitcoincharts.com/ Data source.
