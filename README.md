# Prosjektoppgave - Blog

## Gruppe 1
Thomas Melchior Ytterdal, Hanstein Rommerud, Jan Erik Skaiå Bisseth, Carlos Reiakvam.

## Konfigurasjon
Applikasjonen kan konfigureres ved å sette kjøremiljø variabler som hentes inn av applikasjonen.

Den letteste måten å sette disse på er å opprette en `.env` fil lokalt. I denne filen kan du sette verdier for 
kjøremiljø variablene og de vil automatisk bli fanget opp av Flask (siden vi har python-dotenv installert).

Eksemper på en `.env` fil:

```bash
SECRET_KEY=super-secret
DATABASE_HOST=127.0.0.1
DATABASE_NAME=blog
DATABASE_USER=user
DATABASE_PASSWORD=super-secret
```

Bytt ut verdiene med verdier som stemmer for ditt miljø.

## Opprette database tabeller
Det er opprettet en Flask CLI kommando for å opprette tabellene som applikasjonen bruker.

Kommandoen er som følger:

```bash
flask db init
```
For at denne kommandoen skal fungere må variablene for ditt kjøremiljø være satt som vist over, og  `FLASK_APP` 
må være satt til `commands.py`. 

På Mac / linux kan dette gjøres samtidig som kommandoen kjøres:

```bash
FLASK_APP=commands.py flask db init
```

På windows kan dette settes i `.env`:

```bash
FLASK_APP=commands.py
```

## Slette og reinitiallisere tabller

Kommandoen `flask db reset` vil slette tabellene for applikasjonen og opprette de på nytt med eksempel data. 
Denne kommandoen kjøres på samme måte som `flask db init`.
