# pymq-demo
Demo repo showing how to use stomp.py to send json messages on ActiveMQ

## Install Dependencies

First create a virtual environment so you don't pollute your main distro:

```shell
% python -m venv .venv
% source .venv/bin/activate
(.venv) %
```

This demo app uses stomp.py module to send and receive messages from Amazon MQ (ActiveMQ)

```shell
(.venv) % pip install -r requirements.txt
```

## Sending messages

```shell
> python -m pymq_demo.send
Usage:
  send.py <url> <username> <password> [queue|topic] <dest> [message|file] <data>
  send.py --version
```

- paste in the failover string from Amazon MQ console for stomp+ssl protocol (in quotes)
- specify whether this is posted to a queue or topic
- specify if this is a message or a base64 encoded file