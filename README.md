# C2-Application/Rat 
# White Trash

White Trash is an open-source remote access tool (RAT) project built around client/server communication. The current version supports basic messaging and connection checks; it does not provide general remote device control.

## Features

- Server listens on `127.0.0.1:5555` by default
- Named clients can connect and send messages
- Server commands: `PING`, `STATUS`, and `DISCONNECT`
- Messages use newline-delimited JSON

## Run

Start the server:

```bash
python3 Server.py
```

In another terminal, start a client:

```bash
python3 client.py
```

Use these commands in the server terminal:

```text
clients
ping <client id>
status <client id>
disconnect <client id>
quit
```

Type `exit` in the client to disconnect.

## Security

The default address allows connections from the same computer only. The prototype has no encryption or authentication. Use it only on systems you own or are authorized to manage.
