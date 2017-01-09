DROP TABLE players CASCADE;
DROP TABLE matches CASCADE;

CREATE TABLE players (id SERIAL primary key, name TEXT);
CREATE TABLE matches (id SERIAL primary key,
                      winner INTEGER REFERENCES players (id),
                      loser INTEGER REFERENCES players (id));

/* This is the View for counting the matches won */
CREATE VIEW v_matchesWon as
SELECT players.id, players.name, count(matches.winner) as matches_won
FROM players LEFT JOIN matches
ON players.id = matches.winner
GROUP BY players.id,players.name;

/* This is the View for counting the matches played */
CREATE VIEW v_matchesPlayed as
SELECT players.id, players.name, count(matches.id) as matches_played
FROM players LEFT JOIN matches
ON players.id = matches.winner or players.id = matches.loser
GROUP BY players.id,players.name;

/*

    Alternative Solution

    CREATE VIEW v_playerstandings as
    SELECT players.id, players.name,
    (SELECT count(*) FROM matches WHERE matches.winner = players.id) as matches_won,
    (SELECT count(*) FROM matches WHERE players.id = matches.winner or players.id = matches.loser) as matches_played
    FROM players
    GROUP BY players.id, players.name;


*/