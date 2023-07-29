# Tictactoe using Socket Programming in Python

## Requirement

- Terminal / Powershell / Command Prompt
- Python 3
- Minimum 1 server & 2 clients

## How to play

1. Download ZIP file or clone this github repo

```
git clone https://github.com/mlintang20/tictactoe-socket-programming.git
```

2. Copy **serverconf.conf.example** file, then paste it with file name **serverconf.conf** or just do this in terminal/command prompt

```
cp serverconf.conf.example serverconf.conf
```

3. Open the **serverconf.conf** file and edit _host_ and _port_ with your IP Address and port

```
host=xx.xx.xx.xx
port=xxxx
```

4. Open terminal in root directory, then start the server with this command

```
python server.py
```

5. Open terminal in root directory (can be run on the same or different computers), then start the client with this command (minimum 2 client to play this game)

```
python client.py
```

6. Player 1 types the room number

7. Player 2 types the same room number as Player 1 because each room must have exactly 2 players

## Documentation

![ss1](./img/Screenshot%201.png)
![ss2](./img/Screenshot%209.png)
