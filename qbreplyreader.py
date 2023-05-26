import imaplib
import email

imap_server = imaplib.IMAP4_SSL(host='imap.gmail.com')
imap_server.login('pingryquizbowl@gmail.com', 'rsxieenaquhajgdr')
imap_server.select("Inbox")

responseInfoDict = {}

_, message_numbers_raw = imap_server.search(None, 'UNSEEN')
for message_number in message_numbers_raw[0].split():
    _, msg = imap_server.fetch(message_number, '(RFC822)')

    message = email.message_from_bytes(msg[0][1])

    if message.is_multipart():
        multipart_payload = message.get_payload()
        for sub_message in multipart_payload:
            subMessage = sub_message.get_payload()[1:]

    responseInfoDict[message["from"]] = subMessage[14:subMessage.index("<")]
    # print(responseInfoDict[message["from"]])

fo = open("infodict.txt", "w")
fo.write(str(responseInfoDict))
fo.close()
