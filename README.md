# Prosjekoppgave - Blog
## Gruppe 1

## Konfigurasjon

Applikasjonen kan konfigurers ved å sette kjøremiljø variabler som hentes inn av applikasjonen. 

Den letteste måten å sette disse på er å opprette en `.env` fil lokalt.
I denne filen kan du sette verdier for kjøremiljø variablene og de vil automatisk bli fanget opp av Flask.

Eksemper på en `.env` fil:

```bash
DATABASE_HOST=192.168.1.25
DATABASE_NAME=blog
DATABASE_USER=blog
DATABASE_PASSWORD=super-secret
```

Vytt ut verdiene med verdier som stemmer for ditt milø.


## Opprette database tabeller

Det er opprettet en Flask CLI kommando for å opprette tabellene som applikasjonen bruker.

Kommandoen er som følger:

```bash
FLASK_APP=commands.py flask db init
```

For at denne kommandoen skal fungere må variablene for ditt kjøremiljø være satt som vist over.