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
