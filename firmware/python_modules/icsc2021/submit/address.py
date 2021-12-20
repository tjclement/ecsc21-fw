import flags, easydraw, time

_message = 'Finally, our investigation would be exponentially sped up if we know where Zagan is located. Please help us find their city, street name, and house number. You can submit it to us here via the terminal.'

print(_message)
easydraw.messageCentered('Zagan\'s Bitcoin Wallet\n\n\n' + _message)

def check():
    while True:
        address = input('Address: ').lower()
        time.sleep(2)
        if 'camino' in address and 'hondo' in address and \
            ('52' in address or '51' in address or '50' in address or '49' in address or '32' in address):
            print('Another job well done, congratulations. We\'ll add a flag for you as a token of your efforts.')
            flags.submit_flag('CTF{%s}' % '066ac561e89ab7f2e12aa07a759b31f5a5d233aefebbc2dc')
            break
        elif '28.519615' in address or '16.319824' in address:
            print('Our analyst is not great with coordinates, they confuse him. Please send us a city, street name, and house number.')
        else:
            print('Our systems indicate that this address is invalid or not associated with the Sixth Circle.')

check()