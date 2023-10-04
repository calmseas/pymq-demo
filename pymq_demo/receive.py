"""Send Message with Stomp.py

Usage:
  send.py <url> <username> <password> [queue|topic] <dest> [--loop]
  send.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import base64
import os
import time
import stomp
from stomp.listener import ConnectionListener
from urllib.parse import urlparse

class MessageListener(ConnectionListener):
    def on_message(self, frame):
        if "filename" in frame.headers:
            content = base64.b64decode(frame.body.encode())
            if os.path.exists(frame.headers["filename"]):
                fname = "%s.%s" % (frame.headers["filename"], int(time.time()))
            else:
                fname = frame.headers["filename"]
            with open(fname, "wb") as f:
                f.write(content)
            frame.body = "Saved file: %s" % fname
        print("MESSAGE", frame)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='receive.py 0.1')

    r = urlparse(arguments['<url>'])
    if r.scheme == 'failover':
        brokers = [urlparse(x) for x in r.path[1:-1].split(',')]
        hosts = [(x.hostname, int(x.port)) for x in brokers]
    else:
        hosts = [(r.hostname, r.port)]

    conn = stomp.Connection(hosts)
    conn.set_ssl(hosts)
    conn.set_listener('print', MessageListener())
    conn.connect(username=arguments['<username>'], passcode=arguments['<password>'])

    # this is a very naive implementation, ideally it would just be a loop
    # listening for sigint
    if arguments['queue']:
        conn.subscribe('/queue/' + arguments['<dest>'], 1)
        # small sleep to receive messages that are already on queue
        time.sleep(2)

    if arguments['topic']:
        conn.subscribe('/topic/' + arguments['<dest>'], 1)
        # topic notifications are only received if you are subscribed when they are published
        # so longer sleep here
        time.sleep(10)

    conn.unsubscribe(1)
    conn.disconnect()


