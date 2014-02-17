import pyspv
import time
import traceback

def main():
    spv = pyspv.pyspv('pyspv-simple-wallet', logging_level=pyspv.DEBUG, peer_goal=0, testnet=False) #listen=None

    total_confirmed = 0
    total_unconfirmed = 0

    for spend_hash in spv.wallet.spends:
        spend = spv.wallet.spends[spend_hash]['spend']
        confirmations = spv.txdb.get_tx_depth(spend.prevout.tx_hash)
        print('prevout={}:{} amount={} confirmations={}'.format(pyspv.bytes_to_hexstring(spend.prevout.tx_hash), spend.prevout.n, spend.amount, confirmations))
        if confirmations >= 6:
            total_confirmed += spend.amount
        else:
            total_unconfirmed += spend.amount

    print('confirmed={} unconfirmed={}'.format(total_confirmed, total_unconfirmed))

    spv.shutdown() # Async shutdown
    spv.join()     # Wait for shutdown to complete

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()

