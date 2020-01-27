from hashlib import md5


sid = "UBN1CUdhbWVYQ2hhbmdlcnM="
secret = "tySaeUTMVu8yVBoURQ3kUo4gzqwA"


def getChecksum(pid, sid, amount):
    secret = "tySaeUTMVu8yVBoURQ3kUo4gzqwA"
    checksumstr = f"pid={pid:s}&sid={sid:s}&amount={amount:.2f}&token={secret:s}"
    checksum = md5(checksumstr.encode('utf-8')).hexdigest()
    return checksum


# pid max len 64, so we get somehow unique stuff here maybe?
def getPid(player, game_id):
    player.username
    return "1"


def getSid():
    return sid
