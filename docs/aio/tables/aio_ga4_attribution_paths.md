# All In One - conversion paths and attribution models (GA4)

## Purpose and Main Use Cases 🎯

The table aio_ga_attribution_paths is an advanced tool for **analyzing the paths users take before converting**. Unlike other tables that focus on last click, this datamart lets you see the full sequence of interactions (e.g., google/organic > facebook/cpc > google/cpc) that led to a purchase or other goal.

The main goal is to understand how different marketing channels work together, which ones most often start and which ones end the paths, and how long the average journey to conversion is. Thanks to the presence of a **transaction ID**, it is possible to enrich this analysis with hard sales data from your e‑commerce system, which opens the door to very advanced attribution models. The table also contains **aggregated marketing costs** for comparative analyses.

## Included Source Systems 🔌

This table combines data from two main categories:

- **Conversion Path Data (User Behaviour):**
    - **Google Analytics 4 BigQuery:** Attribution path data (Google Analytics 4 BigQuery - Attribution Orders - GA4).
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{project-id}.aio_ga_attribution_paths`

## Data Structure and Granularity 🧱

The table has a UNION-based structure, which means that **one row represents one of two events**:

1. **A single, complete conversion path** for a given event (e.g., purchase).
2. **Aggregated daily marketing cost** from a given advertising system.

**Key groups of fields:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **Path Dimensions:** journey_id, path_length, path_length_days, source_medium_path.
- **Conversion Dimensions:** transaction_id, event_name, date.
- **Conversion Metrics:** event_value, conversions (always 1 for rows with a path).
- **Marketing Dimensions and Metrics:** ad_system_campaign_name, ad_system_cost, etc.

## Typical Analytical Questions Answered by This Table 🤔

- What are the most common sequences of channels leading to a purchase?
- Which channels most often appear at the beginning, and which at the end of the conversion path?
- On average, how many days and touchpoints does a user need to convert?
- Which paths generate transactions with the highest value?

## Full Column Definitions 📋

| Field Name                          | Business Description                                             | Availability (Source Type) |
| ----------------------------------- | ---------------------------------------------------------------- | -------------------------- |
| data_source_collect_id              | Technical identifier of the connector that retrieved the data.   | All                        |
| data_source_last_mod_time           | Timestamp of the last modification of data in the source system. | All                        |
| data_source_type                    | Main data source type (e.g., 'Ad Systems', 'User Behaviour').    | All                        |
| data_source_subtype                 | Detailed data subtype.                                           | All                        |
| data_source_category                | Source category (platform name).                                 | All                        |
| data_source_name                    | Name of the specific data source in the platform.                | All                        |
| date                                | Event date (conversion or cost). Reporting.                      | All                        |
| report_currency                     | Reporting currency.                                              | All                        |
| journey_id                          | Unique conversion path identifier.                               | User Behaviour             |
| timespan                            | Attribution window set in GA4 (e.g., '30_days').                 | User Behaviour             |
| path_length                         | Path length in number of touchpoints.                            | User Behaviour             |
| path_length_days                    | Path length in days (from first touch to conversion).            | User Behaviour             |
| source_medium_path                  | Full `source/medium > ...` path.                                 | User Behaviour             |
| campaign_path                       | Full `campaign > ...` path.                                      | User Behaviour             |
| first_source_medium_path            | First channel (`source/medium`) in the path.                     | User Behaviour             |
| last_source_medium_path             | Last (non-direct) channel (`source/medium`).                     | User Behaviour             |
| first_campaign_path                 | First campaign in the path.                                      | User Behaviour             |
| last_campaign_path                  | Last campaign in the path.                                       | User Behaviour             |
| transaction_id                      | Transaction ID (for purchase). Key for JOIN with backend.        | User Behaviour             |
| transaction_timestamp_utc           | Exact conversion timestamp for purchase.                         | User Behaviour             |
| event_name                          | Conversion event name (e.g., 'purchase').                        | User Behaviour             |
| ga_attribution_direct               | Attribution type (usually filtered to non_direct).               | User Behaviour             |
| event_value                         | Event value in reporting currency.                               | User Behaviour             |
| conversions                         | Number of conversions (for paths = 1).                           | User Behaviour             |
| ad_system_account_id                | Advertising account ID.                                          | Ad Systems                 |
| ad_system_account_name              | Advertising account name.                                        | Ad Systems                 |
| ad_system_campaign_id               | Campaign ID.                                                     | Ad Systems                 |
| ad_system_campaign_name             | Campaign name.                                                   | Ad Systems                 |
| ad_system_adgroup_id                | Ad group ID.                                                     | Ad Systems                 |
| ad_system_adgroup_name              | Ad group name.                                                   | Ad Systems                 |
| ad_system_placement                 | Ad placement.                                                    | Ad Systems                 |
| ad_system_publisher_id              | Publisher ID (affiliates).                                       | Ad Systems                 |
| ad_system_publisher_name            | Publisher name (affiliates).                                     | Ad Systems                 |
| ad_system_order_id                  | Order ID (affiliates).                                           | Ad Systems                 |
| ad_system_cost                      | Cost in reporting currency.                                      | Ad Systems                 |
| ad_system_clicks                    | Total clicks.                                                    | Ad Systems                 |
| ad_system_impressions               | Total impressions.                                               | Ad Systems                 |
| ad_system_conversions               | Total conversions from the advertising system.                   | Ad Systems                 |
| ad_system_conversions_value         | Conversion value from the advertising system.                    | Ad Systems                 |
| ad_system_item_cost                 | Product-level cost (usually 0 in this table).                    | Ad Systems                 |
| ad_system_item_clicks               | Product-level clicks (usually 0).                                | Ad Systems                 |
| ad_system_item_impressions          | Product-level impressions (usually 0).                           | Ad Systems                 |
| ad_system_item_conversions          | Product-level conversions (usually 0).                           | Ad Systems                 |
| ad_system_original_cost             | Cost in the system's original currency.                          | Ad Systems                 |
| ad_system_original_conversion_value | Conversion value in the original currency.                       | Ad Systems                 |
| currency                            | Original cost data currency.                                     | Ad Systems                 |
| channel_grouping1                   | Custom grouping level 1 (user-defined, e.g., marketing channel or market). | All                        |
| channel_grouping2                   | Custom grouping level 2 (user-defined, e.g., channel subcategory). | All                        |
| channel_grouping3                   | Custom grouping level 3 (user-defined, e.g., specific channel).   | All                        |
| channel_grouping4                   | Custom grouping level 4 (user-defined, e.g., campaign type).      | All                        |
| channel_grouping5                   | Custom grouping level 5 (user-defined, e.g., market segment).     | All                        |

## Important Notes and Limitations ⚠️

- **Key rule for date filtering:** The table is partitioned. To keep your queries fast and inexpensive, **always filter data using the \_PARTITIONTIME pseudo-column**.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with marketing data (data_source_type = 'Ad Systems') will not include path details (e.g., journey_id will be NULL), and vice versa.
- **Joining with backend data:** You will get the most value from this table by joining (JOIN) it with the aio_ecommerce_orders or aio_ecommerce_order_products table using the transaction_id field. This will enrich path analysis with real margin, order status, or customer information.

## Example SQL Queries

### Most frequent paths leading to purchase in the current month

```sql
SELECT
  source_medium_path,
  COUNT(journey_id) AS number_of_conversions,
  SUM(event_value)  AS total_conversion_value
FROM
  `witcloud_{project-id}.aio_ga_attribution_paths`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND event_name = 'purchase'
GROUP BY
  source_medium_path
ORDER BY
  number_of_conversions DESC
LIMIT 20;
```

### Average path length (in days and steps) for transactions

```sql
SELECT
  AVG(path_length)      AS avg_path_length_in_steps,
  AVG(path_length_days) AS avg_path_length_in_days
FROM
  `witcloud_{project-id}.aio_ga_attribution_paths`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND event_name = 'purchase';
```

### Channels that most often start conversion paths

```sql
SELECT
  first_source_medium_path,
  COUNT(journey_id) AS initiated_paths
FROM
  `witcloud_{project-id}.aio_ga_attribution_paths`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND event_name = 'purchase'
GROUP BY
  first_source_medium_path
ORDER BY
  initiated_paths DESC;
```
