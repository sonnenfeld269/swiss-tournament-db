#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    db_cursor = connection.cursor()
    query = "DELETE FROM matches;"
    db_cursor.execute(query)
    connection.commit()
    connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    db_cursor = connection.cursor()
    query = "DELETE FROM players;"
    db_cursor.execute(query)
    connection.commit()
    connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    db_cursor = connection.cursor()
    query = "SELECT count(*) FROM players;"
    db_cursor.execute(query)
    num_players = db_cursor.fetchall()[0][0]
    connection.commit()
    connection.close()
    return num_players

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    db_cursor = connection.cursor()
    query = "INSERT INTO players (name) VALUES ('%s');" % name
    db_cursor.execute(query)
    connection.commit()
    connection.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    db_cursor = connection.cursor()
    #query_matches_played = "SELECT players.id, players.name, count(matches.id) as matches_played FROM players, matches WHERE players.id = matches.winner or players.id = matches.loser GROUP BY players.id,players.name;"
    #query_matches_won = "SELECT players.id, players.name, count(matches.winner) as matches_won FROM players, matches WHERE players.id = matches.winner GROUP BY players.id,players.name;"
    query = """SELECT v_matcheswon.id, v_matcheswon.name,
                      v_matcheswon.matches_won, v_matchesplayed.matches_played
               FROM v_matcheswon LEFT JOIN v_matchesplayed
               ON v_matcheswon.id = v_matchesplayed.id
               AND v_matcheswon.name = v_matchesplayed.name
               ORDER BY v_matcheswon.matches_won DESC;"""
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
    connection = connect()
    db_cursor = connection.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s,%s);" % (winner, loser)
    db_cursor.execute(query)
    connection.commit()
    connection.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    if countPlayers() % 2 == 0:
        for item in playerStandings():
            print item
