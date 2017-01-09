# Tournament Results

## Introduction

A smarter tournament system in which players are paired with those of similar skill level and everyone competes in every round. More fair than an elimination bracket and more efficient than a round-robin tournament.

A PostgreSQL database stores match results, and a Python module queries the database to rank and pair players. When two players have the same win record, ties are broken by summing the win record of each player's previous opponents.

The main parts of the app are:
  * **tournament_text.py** - containing our test cases
  * **tournament.py** - is our python-db api for initiating db queries
  * **tournament.sql** - contains our sql queries

## Requirements

* Python: Make sure you have python installed. You can check if it is installed by running `python --version`
* Virtualbox and Vagrant: You can check if it is installed by running `vagrant -v`

## Installation

1. Clone the github project with `git clone https://github.com/sonnenfeld269/swiss-tournament-db.git`
2. Go inside the folder with `cd swiss-tournament-db`

## References
https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
