-- Parameter: session_start = '2023-01-04', session_counter = 7
-- Nur Sessions ab dem Stichtag; mehr als 7 Sessions im selben Zeitraum.
WITH filtered_sessions AS (
    SELECT *
    FROM sessions
    WHERE session_start >= %(session_start)s
),
active_users AS (
    SELECT user_id
    FROM filtered_sessions
    GROUP BY user_id
    HAVING COUNT(*) > %(session_counter)s
)
-- Stammdaten der Nutzer aus der Kohorte.
SELECT u.*
FROM users AS u
WHERE u.user_id IN (SELECT user_id FROM active_users);
