import imaplib
import email

imap_server = imaplib.IMAP4_SSL(host='imap.gmail.com')
imap_server.login('pingryquizbowl@gmail.com', # not putting the pw here lmaooooo)
imap_server.select()

responseInfoDict = {}

_, message_numbers_raw = imap_server.search(None, 'ALL')
for message_number in message_numbers_raw[0].split():
    _, msg = imap_server.fetch(message_number, '(RFC822)')

    message = email.message_from_bytes(msg[0][1])

    if message.is_multipart():
        multipart_payload = message.get_payload()
        for sub_message in multipart_payload:
            subMessage = sub_message.get_payload()[1:]

    responseInfoDict[message["from"]] = subMessage[14:subMessage.index("<")]

fo = open("infodict.txt", "w")
fo.write(str(responseInfoDict))
fo.close()
