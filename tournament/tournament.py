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
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM Matches;")
    cur.execute("UPDATE PlayerStanding SET Wins = 0, MatchesPlayed = 0;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM PlayerStanding cascade;")
    cur.execute("DELETE FROM Players cascade;")
    cur.execute("ALTER SEQUENCE Players_PlayerID_seq RESTART WITH 1;")
    cur.execute("ALTER SEQUENCE PlayerStanding_PlayerID_seq RESTART WITH 1;")
    cur.execute("ALTER SEQUENCE PlayerStanding_RoundID_seq RESTART WITH 1;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) from Players;")
    return cur.fetchall()[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO Players (FullName) VALUES ('%s');"""%name.replace("'", "''"))
    cur.execute("INSERT INTO PlayerStanding (Wins, MatchesPlayed) VALUES (0, 0)")
    conn.commit()
    conn.close()


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
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT PlayerStanding.PlayerID, Players.FullName, PlayerStanding.Wins, PlayerStanding.MatchesPlayed FROM PlayerStanding INNER JOIN Players ON Players.PlayerID=PlayerStanding.PlayerID ORDER BY PlayerStanding.Wins desc;")
    standing = cur.fetchall()    
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Matches (WinnerID, LoserID) VALUES ('%s', '%s');"%(winner, loser))
    cur.execute("UPDATE PlayerStanding SET Wins=(SELECT Wins FROM PlayerStanding WHERE PlayerID=%s)+1 WHERE PlayerID = %s;"%(winner, winner))
    cur.execute("UPDATE PlayerStanding SET MatchesPlayed=(SELECT MatchesPlayed FROM PlayerStanding WHERE PlayerID=%s)+1 WHERE PlayerID = %s;"%(winner, winner))
    cur.execute("UPDATE PlayerStanding SET MatchesPlayed=(SELECT MatchesPlayed FROM PlayerStanding WHERE PlayerID=%s)+1 WHERE PlayerID = %s;"%(loser, loser))
    conn.commit()
    conn.close()

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
    conn = connect()
    cur = conn.cursor()
    standing = iter(playerStandings())
    for i in standing:
        i
        second = next(standing)
        cur.execute("INSERT INTO SwissPairings (ID1, name1, ID2, name2) VALUES ('%s', '%s', '%s', '%s');"%(i[0], i[1], second[0], second[1]))

    cur.execute("SELECT ID1, name1, ID2, name2 FROM SwissPairings;")
    pairings = cur.fetchall()
    return pairings
