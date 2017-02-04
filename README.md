# Tournament Results

## Introduction

A smarter tournament system in which players are paired with those of similar skill level and everyone competes in every round. More fair than an elimination bracket and more efficient than a round-robin tournament.

A PostgreSQL database stores match results, and a Python module queries the database to rank and pair players. When two players have the same win record, ties are broken by summing the win record of each player's previous opponents.

## Documentation

To read more about the concept and details of the implementation visit
  [Concept.md](CONCEPT.md "Documentation").

## Requirements

* Python: Make sure you have python installed. You can check if it is installed by running `python --version`
* Virtualbox and Vagrant: You can check if it is installed by running `vagrant -v`

## Installation

1. Clone the github project with `git clone https://github.com/sonnenfeld269/swiss-tournament-db.git`
2. Go inside the folder with `cd swiss-tournament-db`
3. If you already have psql installed then go to step 4, otherwise use `vagrant up` and then `vagrant ssh` to start the virtual machine.
4. Use `psql` command start psql the console and connect to the tournament database with `\c tournament`.
5. Now you can use any sql commands like `SELECT * FROM players;` to browse tables or
you can play with the db-api in python by changing queries inside `tournament.py`

## References
https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL
