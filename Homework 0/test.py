def interpretMessage(message):
    if b'@' in message and b'.' in message:
        name = message.split(b'@')[0].split(b'.')
        return name[0].capitalize() + b' ' + name[1].capitalize()
    else:
        return message

print("%s" % interpretMessage(b'hello.adad@adad'))
