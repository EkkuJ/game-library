from hashlib import md5
from django.conf import settings
# from .models import Payment
import random
sid = settings.PAYMENT_SID
secret = settings.PAYMENT_SECRET

# Function to get the Checksum to be sent to the service
def getChecksum(pid, sid, amount):
    checksumstr = f"pid={pid:s}&sid={sid:s}&amount={amount:.2f}&token={secret:s}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    return checksum


# pid max len 64. implemented so that player id is first and then game_id.
# Will be good until the sum of players and games is more than 10^64
# the ':' divides player id and game id so we can later use only the data coming from payment service
# to decide which game is linked to which player in the ownedgame relation
# after the /-sign comes a random part so that we wont get the exception of 
def getPid(player, game):
    rand = random.getrandbits(32)
    pid = str(player.id) + ':' + str(game.id) + '/' + str(rand)
    # print(pid)
    return pid


def getSid():
    return sid

# checking the checksum coming from the payment service
def getIncomingChecksum(pid, ref, result):
    checksumstr = f"pid={pid:s}&ref={ref:s}&result={result:s}&token={secret:s}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    return checksum
