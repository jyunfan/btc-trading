
from exchange import Exchange

class Bitstamp(Exchange):
    def __init__(self, keyfile):
        f = open(keyfile)
        keys = f.readlines()
        f.close()
        if len(keys) != 3:
            logger.error("Incorrect key file")
            exit()

        [user, key, secret] = [keys[0].strip(), keys[1].strip(), keys[2].strip()]
        self.bs_client = bitstamp.client.trading(username=user, key=key, secret=secret)
        self.bs_client_public = bitstamp.client.public()

    def get_balance(self):
        balance = self.bs_client.account_balance()

        # Convert string to double
        for attr in balance:
            balance[attr] = float(balance[attr])
        return balance
