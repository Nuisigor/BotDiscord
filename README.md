#  Discord Bot

This bot was made for my class discord so we can use to get the Google Meet's Links to the classes.

It uses a SQL database to keep informations from Aulas that can be register and showed in the server.

## To run the bot
### Instalation
To run the bot you need to install some python's libraries, so if you have [python](https://www.python.org/downloads/) installed you can run on your shell:

```pip install -r requirements.txt```

After this get your bot token on discord and make a file named ```token.0``` in the ```/libs/bot``` folder.
### Running the bot
```python launcher.py``` to see it working locally

## The functions of this bot are:
* +RegAula : Register a Aula in the database receiving a ID and a Google Meet Link
* +Aula or +Link : Show a Aula from the database showing its Links receiving the Aula's ID
* +DelAula : Delete a Aula from the database receiving the Aula's ID, but this one just can be called from the owner from the bot, so if you use this code remember change it


## Log
* **V0.2** = Made some changes so the bot can be used on repl.it or a host







>This bot was based in [Carberra Tutorials](https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg) videos of python discord bot.