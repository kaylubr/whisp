import base64

def encode_id(unique_id):
    return base64.urlsafe_b64encode(str(unique_id).encode('utf-8')).decode('utf-8').rstrip('=')

def decode_id(encoded_id):
    return base64.urlsafe_b64decode(encoded_id + '=' * (-len(encoded_id) % 4)).decode('utf-8')