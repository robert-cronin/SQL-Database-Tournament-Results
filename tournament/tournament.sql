-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DROP DATABASE IF EXISTS tournament;
-- CREATE DATABASE tournament;
-- \c tournament


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE Players
(
PlayerID SERIAL,
FullName varchar(200),
PRIMARY KEY (PlayerID)
);

CREATE TABLE Matches
(
MatchID SERIAL PRIMARY KEY,
WinnerID int REFERENCES Players(PlayerID),
LoserID int REFERENCES Players(PlayerID)
);

CREATE TABLE Rounds
(
RoundID SERIAL,
RoundName text,
PRIMARY KEY (RoundID)
);

CREATE TABLE PlayerStanding
(
RoundID SERIAL,
PlayerID SERIAL REFERENCES Players(PlayerID),
Wins int,
MatchesPlayed int
);

CREATE TABLE SwissPairings
(
RoundID int,
MatchID SERIAL,
ID1 int,
name1 varchar(200),
ID2 int,
name2 varchar(200)
);
