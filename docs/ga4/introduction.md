# GA4 data — raw events & aggregated API reports (Modna Kiecka)

Beyond the AIO data source, this project has **two GA4 datasets** in the same
BigQuery project (`bq-modnakiecka`, location EU). They are NOT part of the AIO
dataset and behave differently. Read this document before writing any GA4 SQL.

> ⚠️ **Tool scope.** `list_tables`, `get_table_schema` and `describe_columns` are
> hard-scoped to the AIO dataset (`witcloud_qfmdjgmqib6ghnpoimik`) and will NOT
> see the GA4 datasets. For GA4 you must use `run_query` with fully qualified
> names. That works — only SELECT/WITH is enforced, not the dataset.

---

## The one rule that matters most

🚨 **The raw GA4 export has a 23-day hole: `2026-06-16` … `2026-07-08` (inclusive).**

It was caused by **re-connecting the GA4 connector** — reconnecting wipes the
export dataset and starts it fresh. The historical shards were restored from a
backup, but those 23 days were never exported by anyone and are **permanently
lost from the raw data**.

**Never treat this window as a traffic drop.** Any day-over-day, month-over-month
or year-over-year analysis touching June–July 2026 MUST exclude it, or it will
report a catastrophic fake decline. Either filter the range out, or — better —
use `GA4_API` for that period (it has those days; see below).

---

## Dataset 1 — `analytics_291537403` (raw, event-level)

Standard GA4 BigQuery export: **date-sharded**, one table per day, nested schema.

| | |
|---|---|
| Tables | `events_YYYYMMDD` (476), `pseudonymous_users_YYYYMMDD` (480) |
| Range | `2025-03-09` … `2026-07-20` |
| Rows | ~240.6M events |
| Granularity | one row per event, `event_params` / `items` / `user_properties` nested |
| **Hole** | **`2026-06-16` … `2026-07-08` (23 days) — exclude** |

**Query with the wildcard + `_TABLE_SUFFIX`** (this is the partition pruning
mechanism here — filtering on `event_date` scans everything and costs real money):

```sql
SELECT
  PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) AS dzien,
  COUNT(*) AS eventy,
  COUNT(DISTINCT user_pseudo_id) AS uzytkownicy,
  COUNTIF(event_name = 'purchase') AS zakupy
FROM `bq-modnakiecka.analytics_291537403.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20260601' AND '20260720'
  -- MANDATORY: drop the connector hole
  AND _TABLE_SUFFIX NOT BETWEEN '20260616' AND '20260708'
GROUP BY dzien
ORDER BY dzien
```

Notes specific to this dataset:

- **No `events_intraday_*` tables exist here, deliberately.** The wildcard
  `events_*` also matches `events_intraday_*`, so keeping them would double-count
  days that already have a daily shard. Do not restore them.
- **`event_original_occurrence_timestamp` may be invisible via the wildcard.**
  BigQuery takes the wildcard schema from the *most recently created* matching
  table; the restored historical shards are newer (created 2026-07-22) than the
  connector's tables, so this one field (present only in new shards, and empty
  anyway) can raise `Unrecognized name`. It resolves itself once the connector
  writes another day. Query the specific table directly if you truly need it.
- `pseudonymous_users_*` is a separate user-level export — do not join it to
  events by date expecting 1:1 rows.

---

## Dataset 2 — `GA4_API` (aggregated, Data Transfer Service)

Pre-aggregated GA4 reports (the same numbers the GA4 UI shows), delivered by the
GA4 → BigQuery Data Transfer Service. **Not** event-level.

| | |
|---|---|
| Tables | 10 × `p_ga4_<Report>_291537403` (query these) |
| Views | 10 × `ga4_<Report>_291537403` (thin wrappers) |
| Range | `2026-01-01` … `2026-07-20` (139 days with data) |
| Partitioning | **ingestion-time → filter on `_PARTITIONDATE`** (there is no date column!) |
| **Own hole** | **`2026-03-31` … `2026-05-31` (62 days)** |

Available reports: `Audiences`, `DemographicDetails`, `EcommercePurchases`,
`Events`, `LandingPage`, `PagesAndScreens`, `Promotions`, `TechDetails`,
`TrafficAcquisition`, `UserAcquisition`.

These tables carry **no `event_date` / `date` column** — the date lives only in
the partition pseudo-column. Filtering by `_PARTITIONDATE` is mandatory:

```sql
SELECT
  _PARTITIONDATE AS dzien,
  SUM(screenPageViews) AS odslony,
  SUM(activeUsers)     AS uzytkownicy,
  SUM(totalRevenue)    AS przychod
FROM `bq-modnakiecka.GA4_API.p_ga4_PagesAndScreens_291537403`
WHERE _PARTITIONDATE BETWEEN '2026-06-16' AND '2026-07-08'  -- the raw hole, covered here
GROUP BY dzien
ORDER BY dzien
```

---

## Which dataset to use

The two are **complementary — each one covers the other's hole**:

| Period | raw `events_*` | `GA4_API` | Use |
|---|---|---|---|
| 2025-03-09 … 2025-12-31 | ✅ | ❌ (starts 2026-01-01) | raw |
| 2026-01-01 … 2026-03-30 | ✅ | ✅ | either |
| **2026-03-31 … 2026-05-31** | ✅ | ❌ hole | **raw** |
| 2026-06-01 … 2026-06-15 | ✅ | ✅ | either |
| **2026-06-16 … 2026-07-08** | ❌ hole | ✅ | **`GA4_API`** |
| 2026-07-09 → now | ✅ | ✅ | either |

Rules of thumb:

- **Event-level questions** (funnels, sequences, custom parameters, user paths,
  cohorts) → raw `events_*`. Only it has that granularity.
- **Standard reporting metrics** (sessions, pageviews, traffic sources,
  demographics, revenue by day) → `GA4_API` is cheaper and already aggregated,
  and it matches the GA4 UI numbers.
- **Any analysis spanning 2026-06-16 … 2026-07-08** → take that window from
  `GA4_API`, or exclude it and say so explicitly in the output.
- **Do not blindly UNION the two.** Different granularity and different metric
  definitions (GA4's modelled/aggregated metrics ≠ raw event counts); totals will
  not reconcile exactly. Pick one per metric, or clearly label a stitched series.

Always state in the answer which dataset a number came from, and flag whenever a
requested range overlaps either hole.

---

## Cost & safety

- `run_query` is read-only (SELECT/WITH only) and capped at 4 GB scanned per query.
- Raw `events_*` is ~0.94 TB — an unfiltered wildcard query will hit the cap and
  fail. Always constrain `_TABLE_SUFFIX`.
- `GA4_API` is small; still filter `_PARTITIONDATE` to keep scans predictable.
- `analytics_291537403_backup` is a **cold backup of the raw export — do not
  query it for analysis and do not delete it.** It is the only copy of the
  history if the connector is reconnected again.
