#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection

    Args:
        database_name: name of the database

    Returns:
        db: connection object
        cursor: a cursor for executing psql queries
    """
    try:
        connection = psycopg2.connect("dbname=%s" % database_name)
        cursor = connection.cursor()
        return connection, cursor
    except:
        print("Could not connect to database.")


def deleteMatches():
    """Remove all the match records from the database."""
    connection, db_cursor = connect()
    query = "TRUNCATE TABLE matches CASCADE;"
    db_cursor.execute(query)
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all player records from the database."""
    connection, db_cursor = connect()
    query = "TRUNCATE TABLE players CASCADE;"
    db_cursor.execute(query)
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection, db_cursor = connect()
    query = "SELECT count(*) FROM players;"
    db_cursor.execute(query)
    num_players = db_cursor.fetchall()[0][0]
    connection.commit()
    connection.close()
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    For details check the SQL database schema @tournament.sql

    Args:
      name: the player's full name(need not be unique).
    """
    connection, db_cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    params = (name,)  # use parameters to prevent sql injection
    db_cursor.execute(query, params)
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains(id, name, wins, matches):
        id: the player's unique id(assigned by the database)
        name: the player's full name(as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection, db_cursor = connect()
    query = "SELECT * FROM v_playerstandings;"
    db_cursor.execute(query)
    standings = db_cursor.fetchall()
    connection.commit()
    connection.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, db_cursor = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s,%s);"
    params = (winner, loser)  # use parameters to prevent sql injection
    db_cursor.execute(query, params)
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly - equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains(id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    all_standings = playerStandings()
    if countPlayers() % 2 == 0:
        # this for loop is equivalent to for(i=0,i<all_standings.length,i=i+2)
        for i in range(0, len(all_standings) - 1, 2):
            pairings.append(all_standings[i][0:2] + all_standings[i + 1][0:2])
    return pairings
