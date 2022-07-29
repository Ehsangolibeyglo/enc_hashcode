from rubika.client import Bot
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from json import loads

bot = Bot("app_name",auth="AUTH",displayWelcome=False)

getkey = ""
enckey = bytearray("a"*32, "UTF-8")
hex = bytearray.fromhex('00000000000000000000000000000000')

def decrypt(text):
    aes = AES.new(enckey, AES.MODE_CBC, hex)
    dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
    result = unpad(dec, AES.block_size).decode('UTF-8')
    return result

encr = loads(decrypt(getkey))

bot.download(save=True,**encr)