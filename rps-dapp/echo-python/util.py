
def str2hex(str):
    # encode a string as a hex
    return "0x" + str.encode('utf-8').hex()

def hex2str(hex):
    # decode a hex as a string
    return bytes.fromhex(hex[2:]).decode('utf-8')