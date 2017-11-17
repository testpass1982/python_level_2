import json

def send_message(s, text):
    sending = convert_message_to_bytes(text)
    s.send(sending)

def convert_message_to_bytes(text):
    json_message = json.dumps(text)
    byte_message = json_message.encode('utf-8')
    return byte_message

def convert_bytes_to_message(bytes):
    json_message = bytes.decode('utf-8')
    message = json.loads(json_message)
    return message