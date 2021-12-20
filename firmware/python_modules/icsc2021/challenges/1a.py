import upysh, flags, easydraw

for name in dir(upysh):
    globals()[name] = getattr(upysh, name)

_message = 'Connect to the device via USB at baud 115200. You\'re now in a Python shell with "upysh" commandline-like functions.\n' + \
      'Type "man" to see what you can do, and hunt for a file called flag.txt.\n\n' + \
      'You can submit the flag by calling flags.submit_flag("CTF{xxxx}").'

print(_message)
easydraw.messageCentered('Scriptkiddie\n\n\n' + _message)