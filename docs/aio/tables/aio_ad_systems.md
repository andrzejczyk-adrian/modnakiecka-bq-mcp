# All In One - data from advertising systems

## Purpose and Main Use🎯

The aio_ad_systems table is your command center for marketing performance. It was created to collect, in one place and in a consistent way, all key metrics from connected advertising systems. Its main goal is to enable **analysis and comparison of costs, clicks, impressions, and conversions across different platforms** (e.g., Google Ads, Facebook Ads, TikTok) without the need to switch between their dashboards.

Thanks to this table, you can easily monitor expenses, calculate indicators such as **CPC** (cost per click) or **CPA** (cost per conversion), and evaluate which campaigns or platforms deliver the best results.

## Included Source Systems🔌

The table below contains data **only from the Ad Systems category**. It includes the following sources and levels of detail (subtypes):

- **Awin** – transaction and commission data
- **Bing Ads** – campaign performance data
- **Ceneo** – click and cost data
- **Convertiser** – conversion and cost data
- **Criteo Ads** – aggregated campaign statistics
- **Domodi & Allani** – category-level statistics
- **Facebook Ads**
    - Facebook Ads (aggregated data)
    - Facebook Ads – Conversions Segments (conversion goal data)
    - Facebook Ads – Product Conversions (product-level conversions)
    - Facebook Ads – Shopping (product-level statistics)
    - Facebook Ads – Reach (reach data)
- **Google Ads**
    - Google Ads (aggregated data)
    - Google Ads – Conversions Segments (conversion goal data)
    - Google Ads – Shopping (product-level statistics)
- **Optimise** – conversion and commission data
- **RTB House** – aggregated campaign statistics
- **TikTok** – ad group performance data
- **Tradedoubler** – transaction, commission, and campaign statistics

## Table Location in BigQuery 📍

The table is located in BigQuery under the path:
`witcloud_{project-id}.aio_ad_systems`

## Data Structure and Granularity 🧱

Each row in this table represents **aggregated daily data** from a specific advertising system for a defined set of dimensions. The data granularity depends on the subtype (Data Source Subtype):

- **General data** (e.g., Google Ads, Facebook Ads): Aggregation at the campaign or ad group level.
- **Shopping data**: Aggregation at the **product (SKU)** level. Data at this level is available only for **Google Ads and Facebook Ads**.
- **Conversions Segments data**: Data at the level of **individual conversion goals**. Raw conversion data (often in key:value array format) has been flattened and split into separate rows. This allows cost analysis for specific conversion actions you've selected.

**Key field groups:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **Campaign Dimensions:** date, account_name, campaign_name, adgroup_name, etc.
- **Product Dimensions:** item_id, item_name, item_brand, etc.
- **Performance Metrics:** cost, clicks, impressions, conversions, conversions_value, etc.

## Typical Analytical Questions Answered by This Table 🤔

- What was our total marketing cost across all channels last week?
- How much did we spend on Google Ads campaigns that generated "Add to cart" conversions?
- What's the comparison of average CPC between Facebook Ads and TikTok Ads?
- What is the cost and number of clicks for a specific product in Google Shopping campaigns?

## Full Column Definition 📋

| Field Name                      | Business Description                                                      | Availability (Example Systems)                                      |
| ------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| data_source_collect_id          | Technical identifier of the connector that collected the data.            | All                                                                 |
| data_source_last_mod_time       | Timestamp of the last modification in the source system.                  | All                                                                 |
| data_source_type                | Main data source type; for this table always `Ad Systems`.                | All                                                                 |
| data_source_subtype             | Detailed data subtype (e.g., `Google Ads - Shopping`).                    | All                                                                 |
| data_source_category            | Source category (e.g., `Google Ads`, `Facebook Ads`).                     | All                                                                 |
| data_source_name                | Name of the source in the platform (e.g., account name).                  | All                                                                 |
| date                            | Metric date (UTC). For reporting, not for partition filtering.            | All                                                                 |
| account_id                      | Unique identifier of the ad account.                                      | Google Ads, Facebook Ads, Bing Ads, Criteo, RTB House, Tradedoubler |
| account_name                    | Name of the ad account.                                                   | ibid.                                                               |
| campaign_id                     | Unique campaign identifier.                                               | Google Ads, Facebook Ads, Bing Ads, Criteo, TikTok, Optimise        |
| campaign_name                   | Name of the ad campaign.                                                  | All                                                                 |
| adgroup_id                      | Unique ad group identifier.                                               | Google Ads, Facebook Ads, TikTok                                    |
| adgroup_name                    | Name of the ad group.                                                     | ibid.                                                               |
| ad_id                           | Unique ad identifier.                                                     | Tradedoubler, Optimise, Ceneo                                       |
| ad_name                         | Ad name.                                                                  | Tradedoubler, Optimise                                              |
| placement                       | Placement (e.g., search/display network).                                 | Google Ads, Facebook Ads, Bing Ads, Optimise                        |
| publisher_id                    | Publisher identifier (affiliates).                                        | Awin, Tradedoubler, Optimise                                        |
| publisher_name                  | Publisher name (affiliates).                                              | Awin, Tradedoubler, Optimise                                        |
| order_id                        | Order ID linked to conversion (affiliates).                               | Awin, Tradedoubler, Optimise, Convertiser                           |
| item_id                         | Product ID (SKU) – Shopping only.                                         | Google Ads Shopping, Facebook Ads Shopping                          |
| item_name                       | Product name – Shopping only.                                             | Google Ads Shopping, Facebook Ads Shopping                          |
| item_brand                      | Product brand – Shopping only.                                            | Google Ads Shopping                                                 |
| item_category                   | Product category – Shopping only.                                         | Google Ads Shopping                                                 |
| conversion_id                   | Conversion goal ID – Segments only.                                       | Google/Facebook – Conversions Segments                              |
| conversion_name                 | Conversion goal name – Segments only.                                     | Google/Facebook – Conversions Segments                              |
| reach                           | 7-day reach.                                                              | Facebook Ads – Reach                                                |
| currency                        | Reporting currency (e.g., PLN, EUR).                                      | All                                                                 |
| cost                            | Cost in reporting currency (main cost metric).                            | Most \*                                                             |
| clicks                          | Total clicks.                                                             | Most \*                                                             |
| impressions                     | Total impressions.                                                        | Most (affiliates sometimes 0/NULL)                                  |
| conversions                     | Total default conversions.                                                | All                                                                 |
| conversions_value               | Total value of default conversions (reporting currency).                  | All                                                                 |
| item_cost                       | Product-level cost.                                                       | Google/Facebook – Shopping                                          |
| item_clicks                     | Product-level clicks.                                                     | Google/Facebook – Shopping                                          |
| item_impressions                | Product-level impressions.                                                | Google/Facebook – Shopping                                          |
| item_conversions                | Product-level conversions.                                                | Google/Facebook – Shopping                                          |
| conversion_segments_conversions | Conversions for specific goal (per conversion_name).                      | Google/Facebook – Segments                                          |
| reach_period_7d_cost            | 7-day cost.                                                               | Facebook Ads – Reach                                                |
| reach_period_7d_clicks          | 7-day clicks.                                                             | Facebook Ads – Reach                                                |
| reach_period_7d_impressions     | 7-day impressions.                                                        | Facebook Ads – Reach                                                |
| original_cost                   | Cost in the system's original currency (audit/recalculation).             | All                                                                 |
| original_conversion_value       | Conversion value in original currency (audit/recalculation).              | All                                                                 |
| channel_grouping1               | Custom grouping level 1 (user-defined, e.g., marketing channel category). | All                                                                 |
| channel_grouping2               | Custom grouping level 2 (user-defined, e.g., channel subcategory).        | All                                                                 |
| channel_grouping3               | Custom grouping level 3 (user-defined, e.g., specific channel).           | All                                                                 |
| channel_grouping4               | Custom grouping level 4 (user-defined, e.g., campaign type).              | All                                                                 |
| channel_grouping5               | Custom grouping level 5 (user-defined, e.g., market segment).             | All                                                                 |

> 💡
> Rows of type **Shopping** and **Conversions Segments** may have empty main metrics (cost, clicks, impressions) to avoid double counting.

## Important Notes and Limitations ⚠️

- **Key date filtering rule:** The table is partitioned by data ingestion time. To keep your queries fast and cost-efficient, **always filter data using the pseudo-column \_PARTITIONTIME**, not the `date` column. The `date` column is for reporting (e.g., grouping in Looker Studio) but not for query optimization.
- **Conversion segment analysis:** **Conversion Segments** data exists in separate rows. These rows contain detailed data for specific conversion types, but main metrics (cost, clicks, impressions) are intentionally zeroed out to prevent double counting. To correctly analyze cost per specific conversion, sum cost from all campaign rows and compare it with the total of the selected conversion goal (as in SQL Example No. 3).
- **Metric availability:** Not all advertising systems provide the same metrics. For example, some affiliate networks may not report impressions, in which case the value in this column will be 0 or NULL.
- **Aggregation levels:** Remember that different subtypes live at different aggregation levels within a single table.

## Example SQL Queries

### Total daily cost across all advertising systems yesterday

```sql
SELECT
  date,
  SUM(cost) AS total_cost
FROM
  `witcloud_{project-id}.aio_ad_systems`
WHERE
  -- Correct partition filtering for optimization
  _PARTITIONTIME = TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
GROUP BY
  date
ORDER BY
  date DESC;
```

### Comparing Google Ads campaign performance in the current month

```sql
SELECT
  campaign_name,
  SUM(cost) AS total_cost,
  SUM(clicks) AS total_clicks,
  SUM(conversions) AS total_conversions,
  SAFE_DIVIDE(SUM(cost), SUM(clicks)) AS avg_cpc
FROM
  `witcloud_{project-id}.aio_ad_systems`
WHERE
  -- Partition filter covering the entire current month
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND account_name LIKE '%Google Ads%'  -- Example filter for Google Ads accounts
GROUP BY
  campaign_name
ORDER BY
  total_cost DESC;
```

### Google Ads cost vs. number of conversions for a specific goal ('Purchase') yesterday

```sql
SELECT
  campaign_name,
  SUM(cost) AS total_cost,
  SUM(IF(conversion_name = 'Purchase', conversion_segments_conversions, 0)) AS purchase_conversions
FROM
  `witcloud_{project-id}.aio_ad_systems`
WHERE
  _PARTITIONTIME = TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
  AND account_name LIKE '%Google Ads%'
GROUP BY
  campaign_name
HAVING
  purchase_conversions > 0
ORDER BY
  purchase_conversions DESC;
```
