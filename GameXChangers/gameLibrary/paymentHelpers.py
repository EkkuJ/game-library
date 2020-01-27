from hashlib import md5


sid = "UBN1CUdhbWVYQ2hhbmdlcnM="
secret = "tySaeUTMVu8yVBoURQ3kUo4gzqwA"


def getChecksum(pid, sid, amount):
    secret = "tySaeUTMVu8yVBoURQ3kUo4gzqwA"
    checksumstr = f"pid={pid:s}&sid={sid:s}&amount={amount:.2f}&token={secret:s}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    return checksum


# pid max len 64. implemented so that player id is first and then game_id.
# Will be good until there are more players than 10^32 or games than 10^32
def getPid(player, game_id):
    pid = str(player.id) + str(game_id)
    # print(pid)
    return pid


def getSid():
    return sid
