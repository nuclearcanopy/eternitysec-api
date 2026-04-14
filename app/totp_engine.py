import hmac, hashlib, base64, time, struct

def generate_totp(secret: str):
    counter = int(time.time() // 30)
    h = hmac.new(base64.b32decode(secret), struct.pack(">Q", counter), hashlib.sha1)

    result = h.digest()

    offset = result[-1] & 0x0F
    
    int.from_bytes(result[offset:offset+4], byteorder='big') & 0x7FFFFFFF
