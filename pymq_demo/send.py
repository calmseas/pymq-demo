"""Send Message with Stomp.py

Usage:
  send.py <url> <username> <password> [queue|topic] <dest> [message|file] <data>
  send.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import stomp
import base64
import os
from urllib.parse import urlparse

if __name__ == '__main__':
    arguments = docopt(__doc__, version='send.py 0.1')

    r = urlparse(arguments['<url>'])
    if r.scheme == 'failover':
        brokers = [urlparse(x) for x in r.path[1:-1].split(',')]
        hosts = [(x.hostname, int(x.port)) for x in brokers]
    else:
        hosts = [(r.hostname, r.port)]

    conn = stomp.Connection(hosts)
    conn.set_ssl(hosts)
    conn.connect(username=arguments['<username>'], passcode=arguments['<password>'])

    content_type = 'text/plain'
    data = arguments['<data>']
    if arguments['file']:
        if '.json' in arguments['<data>']:
            content_type = 'application/json'
        elif '.xml' in arguments['<data>']:
            content_type = 'application/xml'
        with open(arguments['<data>'], mode="rb") as f:
            s = f.read()
        data = base64.b64encode(s).decode()

    if arguments['queue']:
        dest = '/queue/' + arguments['<dest>']
    elif arguments['topic']:
        dest = '/topic/' + arguments['<dest>']

    if arguments['message']:
        conn.send('/queue/' + arguments['<dest>'], data, content_type)
    elif arguments['file']:
        conn.send('/queue/' + arguments['<dest>'], data,
                  filename=os.path.basename(arguments['<data>']),
                  content_type=content_type)
    print("message sent")


