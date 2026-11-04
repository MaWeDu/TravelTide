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
-- Hoteldaten zu Reisen aus Sessions der Kohorte im Analysezeitraum.
SELECT h.*
FROM hotels AS h
WHERE h.trip_id IN (
    SELECT s.trip_id
    FROM filtered_sessions AS s
    WHERE s.user_id IN (SELECT user_id FROM active_users)
);
