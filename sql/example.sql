-- Synthetic example schema. No real data.
CREATE TABLE IF NOT EXISTS run_records (
    id uuid PRIMARY KEY,
    started_at timestamptz NOT NULL,
    outcome text NOT NULL,
    cost_usd numeric(10, 4) NOT NULL DEFAULT 0
);

SELECT
    outcome,
    count(*) AS runs,
    sum(cost_usd) AS total_cost_usd
FROM run_records
GROUP BY outcome
ORDER BY outcome;
