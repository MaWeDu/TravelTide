-- Parameter: session_start = '2023-01-04', session_counter = 7
-- Alle Anweisungen in derselben Datenbankverbindung ausführen.

-- 1. Kohorte: mehr als 7 Sessions ab dem Stichtag.
DROP TABLE IF EXISTS tmp_active_users;

CREATE TEMP TABLE tmp_active_users AS
SELECT user_id
FROM sessions
WHERE session_start >= %(session_start)s
GROUP BY user_id
HAVING COUNT(*) > %(session_counter)s;

-- 2. Stammdaten der Kohorte.
SELECT u.*
FROM users AS u
JOIN tmp_active_users AS a ON u.user_id = a.user_id;

-- 3. Nur Sessions der Kohorte innerhalb des Analysezeitraums.
SELECT s.*
FROM sessions AS s
JOIN tmp_active_users AS a ON s.user_id = a.user_id
WHERE s.session_start >= %(session_start)s;

-- 4. Flugdaten zu Reisen aus Sessions im Analysezeitraum.
SELECT f.*
FROM flights AS f
WHERE f.trip_id IN (
    SELECT s.trip_id
    FROM sessions AS s
    JOIN tmp_active_users AS a ON s.user_id = a.user_id
    WHERE s.session_start >= %(session_start)s
);

-- 5. Hoteldaten zu Reisen aus Sessions im Analysezeitraum.
SELECT h.*
FROM hotels AS h
WHERE h.trip_id IN (
    SELECT s.trip_id
    FROM sessions AS s
    JOIN tmp_active_users AS a ON s.user_id = a.user_id
    WHERE s.session_start >= %(session_start)s
);
