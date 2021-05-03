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


# Opplasting til kark.uit.no

Opplasting til kark kan gjøres via git. 

Først må du koble deg til kark med ssh (husk vpn).

Når du er tilkoblet kark kan du opprette `flask_prosjekt` mappen om du ikke har gjort det allerede.

```shell
mkdir -p public_html/flask_prosjekt/flask_prosjekt
```

Etter dette må du endre arbeidsmappe til den du nettop laget:

```shell
cd public_html/flask_prosjekt/flask_prosjekt
```

For å hente ned koden fra coderefinery kjører du følgende kommando:

```shell
git clone https://source.coderefinery.org/dte-2509-prosjekt-1/blog.git .
```

Du vil nå bli bedt om brukernavn og passord til coderefinery.

Når koden er ferdig klonet må du opprette ett nytt virtual environment:

```shell
python3.6 -m virtualenv venv
```

Deretter må dette aktiveres:

```shell
source venv/bin/activate
```

Når det virtuelle miljøet er aktivert kan du installere alle pakkene som trengs:

```shell
pip install -r requirements.txt
```

Når denne prosessen er ferdig må du opprette en `.env` fil med alle instillinger for prosjektet:

```shell
nano .env
```

Filen bør inneholde det følgende nøkler:

```shell
SECRET_KEY=super-secret
DATABASE_NAME=stud_v21_ytterdal
DATABASE_USER=stud_v21_ytterdal
DATABASE_PASSWORD=super-secret
URL_PREFIX=/~tyt005/flask_prosjekt
```

Nå kan du kjøre kommandoen for å sette opp databasen:

```bash
FLASK_APP=commands.py flask db init
```

Applikasjonen er nå ferdig opplastet til kark. 

For fremtidige endringer kan du koble til med ssh og kjøre `git pull`.