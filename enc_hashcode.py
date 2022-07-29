from rubika.client import Bot,clients
from colorama import Fore
from random import randint
from json import loads, dumps
from requests import post,get
from pathlib import Path
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


bot = Bot("app_name",auth="hnbegvqoujaojlmapkqgpdtckpzjpsva",displayWelcome=False)
target = "g0BpV6y00799e70887c8fb64420c39d8"

path = "/storage/emulated/0/Music/Macan Band - Ba To.mp3"

key = bytearray("a"*32, "UTF-8")
iv = bytearray.fromhex('00000000000000000000000000000000')

def encrypt(text):
    raw = pad(text.encode('UTF-8'), AES.block_size)
    aes = AES.new(key, AES.MODE_CBC, iv)
    enc = aes.encrypt(raw)
    result = base64.b64encode(enc).decode('UTF-8')
    return result

def requestSendFile(file):
    while True:
        try:
            return loads(bot.enc.decrypt(post(json={"api_version":"5","auth": bot.auth,"data_enc":bot.enc.encrypt(dumps({
                "method":"requestSendFile",
                "input":{
                    "file_name": str(file.split("/")[-1]),
                    "mime": file.split(".")[-1],
                    "size": str(499999)
                },
                "client": clients.web
            }))},url=Bot._getURL()).json()["data_enc"]))["data"]
            break
        except: continue


def uploadFile(file):
    frequest = requestSendFile(file)
    bytef = open(file,"rb").read()

    hash_send = frequest["access_hash_send"]
    file_id = frequest["id"]
    url = frequest["upload_url"]

    header = {
        'auth':bot.auth,
        'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
        'chunk-size':str(Path(file).stat().st_size),
        'file-id':str(file_id),
        'access-hash-send':hash_send,
        "content-type": "application/octet-stream",
        "content-length": str(Path(file).stat().st_size),
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.1"
    }

    if len(bytef) <= 131072:
        header["part-number"], header["total-part"] = "1","1"

        while True:
            try:
                j = post(data=bytef,url=url,headers=header).text
                j = loads(j)['data']['access_hash_rec']
                break
            except Exception as e:
                continue

        return [frequest, j]
    else:
        t = round(len(bytef) / 1310720)
        f = round(len(bytef) / t + 1)
        for i in range(1,t+1):
            if i != t:
                k = i - 1
                k = k * f
                while True:
                    try:
                        header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
                        o = post(data=bytef[k:k + f],url=url,headers=header).text
                        print(f"{Fore.RED}● part:{Fore.GREEN}{i}{Fore.WHITE} / {Fore.CYAN}{t}{Fore.WHITE} / {Fore.CYAN} Status: {Fore.GREEN} OK")
                        o = loads(o)['data']
                        break
                    except Exception as e:
                        continue
            else:
                k = i - 1
                k = k * f
                while True:
                    try:
                        header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
                        p = post(data=bytef[k:k + f],url=url,headers=header).text
                        print(f"{Fore.RED}● part:{Fore.GREEN}{i}{Fore.WHITE} / {Fore.CYAN}{t}{Fore.WHITE} / {Fore.CYAN} Status: {Fore.GREEN} OK")
                        p = loads(p)['data']['access_hash_rec']
                        break
                    except Exception as e:
                        continue
                return [frequest, p]

def sendDocument(chat_id, file, caption=None, message_id=None):
    uresponse = uploadFile(file)

    file_id = str(uresponse[0]["id"])
    mime = file.split(".")[-1]
    dc_id = uresponse[0]["dc_id"]
    access_hash_rec = uresponse[1]
    file_name = file.split("_")[-1]
    size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

    inData = {
        "method":"sendMessage",
        "input":{
            "object_guid":chat_id,
            "reply_to_message_id":message_id,
            "rnd":f"{randint(100000,999999999)}",
            "file_inline":{
                "dc_id":str(dc_id),
                "file_id":str(file_id),
                "type":"File",
                "file_name":file_name,
                "size":size,
                "mime":mime,
                "access_hash_rec":access_hash_rec
            }
        },
        "client": clients.web
    }

    if caption != None: inData["input"]["text"] = caption

    data = {
        "api_version":"5",
        "auth":bot.auth,
        "data_enc":bot.enc.encrypt(dumps(inData))
    }

    while True:
        try:
            return loads(bot.enc.decrypt(loads(post(json=data,url=Bot._getURL()).text)['data_enc']))
            break
        except: continue

print(encrypt(dumps(sendDocument(target,path)["data"]["message_update"])))

    

    

