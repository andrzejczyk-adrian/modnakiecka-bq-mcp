# All In One - summary of attribution models and channel effectiveness (GA4)

## Purpose and Main Use Cases 🎯

The table aio_ga_attribution_summary is a key tool for **strategic analysis of marketing channel effectiveness across different attribution models**. Unlike aio_ga_attribution_paths, which shows entire paths, this table provides an **aggregated, ready-to-use view** that assigns fractional shares of conversions and their values to individual channels (steps on the path).

The main goal of this datamart is to enable comparison of how different attribution models (e.g., **First Click, Last Click, Linear**) assess the contribution of a given channel (source/medium) or campaign. This allows you to make more informed budget allocation decisions by identifying channels that are undervalued in simpler models (e.g., Last Click) but play a key role at earlier stages of the customer journey. The table also contains **aggregated marketing costs**, which allows you to calculate ROAS for each channel in each attribution model.

## Included Source Systems 🔌

This table combines data from two main categories:

- **Attribution Data (User Behaviour):**
    - **Google Analytics 4 BigQuery:** Conversion share data from the attribution model (Google Analytics 4 BigQuery - Attribution Orders - GA4).
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{id-projektu}.aio_ga_attribution_summary`

## Data Structure and Granularity 🧱

The table has a UNION-based structure, which means that **one row represents one of two events**:

1. **Aggregated, daily share of a given channel/campaign in conversions** according to various attribution models.
2. **Aggregated daily marketing cost** from a given advertising system.

**Key groups of fields:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **Attribution Dimensions (step on the path):** ga_source, ga_medium, ga_campaign, event_name.
- **Attribution Metrics:** first_click_conversion, last_click_conversion_value, linear_conversion, etc.
- **Marketing Dimensions and Metrics:** ad_system_campaign_name, ad_system_cost, etc.

## Typical Analytical Questions Answered by This Table 🤔

- How do conversion share and ROAS for the channel facebook / cpc change depending on the attribution model used (First Click vs. Last Click)?
- Which channels are most important in initiating paths (high share in the First Click model), and which in closing them (high share in Last Click)?
- Comparing the Linear model, which marketing channel has the highest assigned conversion revenue?
- What is the ROAS for google / cpc in the Position Based model compared to the costs from the same day?

## Full Column Definitions 📋

| Field Name                          | Business Description                                                  | Availability (Source Type) |
| ----------------------------------- | ---------------------------------------------------------------------- | -------------------------- |
| data_source_collect_id              | Technical identifier of the connector that retrieved the data.        | All                        |
| data_source_last_mod_time           | Timestamp of the last modification of data in the source system.      | All                        |
| data_source_type                    | Main data source type (e.g., 'Ad Systems', 'User Behaviour').         | All                        |
| data_source_subtype                 | Detailed data subtype.                                                | All                        |
| data_source_category                | Source category (platform name).                                      | All                        |
| data_source_name                    | Name of the specific data source defined on the platform.             | All                        |
| date                                | Event date (path step or cost). Reporting.                            | All                        |
| report_currency                     | Reporting currency.                                                   | All                        |
| ga_source                           | Source at a given step of the conversion path.                        | User Behaviour             |
| ga_medium                           | Medium at a given step of the conversion path.                        | User Behaviour             |
| ga_campaign                         | Campaign at a given step of the conversion path.                      | User Behaviour             |
| ga_campaign_id                      | Campaign ID at a given step of the conversion path.                   | User Behaviour             |
| ga_ad_content                       | Ad content at a given step of the conversion path.                    | User Behaviour             |
| ga_keyword                          | Keyword at a given step of the conversion path.                       | User Behaviour             |
| event_name                          | Conversion event to which the attribution applies (e.g., 'purchase'). | User Behaviour             |
| transaction_id                      | Transaction ID (if applicable); for counting unique conversions/JOIN. | User Behaviour             |
| first_click_conversion              | Fractional share in the conversion (First Click model).               | User Behaviour             |
| first_click_conversion_value        | Fractional conversion value (First Click).                            | User Behaviour             |
| last_click_conversion               | Fractional share in the conversion (Last Click).                      | User Behaviour             |
| last_click_conversion_value         | Fractional conversion value (Last Click).                             | User Behaviour             |
| linear_conversion                   | Fractional share in the conversion (Linear).                          | User Behaviour             |
| linear_conversion_value             | Fractional conversion value (Linear).                                 | User Behaviour             |
| position_based_conversion           | Fractional share in the conversion (Position Based).                  | User Behaviour             |
| position_based_conversion_value     | Fractional conversion value (Position Based).                         | User Behaviour             |
| timedecay_conversion                | Fractional share in the conversion (Time Decay).                      | User Behaviour             |
| timedecay_conversion_value          | Fractional conversion value (Time Decay).                             | User Behaviour             |
| ad_system_account_id                | Advertising account ID.                                               | Ad Systems                 |
| ad_system_account_name              | Advertising account name.                                             | Ad Systems                 |
| ad_system_campaign_id               | Campaign ID.                                                          | Ad Systems                 |
| ad_system_campaign_name             | Campaign name.                                                        | Ad Systems                 |
| ad_system_adgroup_id                | Ad group ID.                                                          | Ad Systems                 |
| ad_system_adgroup_name              | Ad group name.                                                        | Ad Systems                 |
| ad_system_placement                 | Ad placement.                                                         | Ad Systems                 |
| ad_system_publisher_id              | Publisher ID (affiliates).                                            | Ad Systems                 |
| ad_system_publisher_name            | Publisher name (affiliates).                                          | Ad Systems                 |
| ad_system_order_id                  | Order ID (affiliates).                                                | Ad Systems                 |
| ad_system_cost                      | Cost in reporting currency.                                           | Ad Systems                 |
| ad_system_clicks                    | Total clicks.                                                         | Ad Systems                 |
| ad_system_impressions               | Total impressions.                                                    | Ad Systems                 |
| ad_system_conversions               | Total conversions reported by the advertising system.                 | Ad Systems                 |
| ad_system_conversions_value         | Conversion value from the advertising system.                         | Ad Systems                 |
| ad_system_item_cost                 | Product-level cost (usually 0).                                       | Ad Systems                 |
| ad_system_item_clicks               | Product-level clicks (usually 0).                                     | Ad Systems                 |
| ad_system_item_impressions          | Product-level impressions (usually 0).                                | Ad Systems                 |
| ad_system_item_conversions          | Product-level conversions (usually 0).                                | Ad Systems                 |
| ad_system_original_cost             | Cost in the system's original currency.                               | Ad Systems                 |
| ad_system_original_conversion_value | Conversion value in the original currency.                            | Ad Systems                 |
| currency                            | Original cost data currency.                                          | Ad Systems                 |
| channel_grouping1                   | Custom grouping level 1 (user-defined, e.g., marketing channel or market). | All                        |
| channel_grouping2                   | Custom grouping level 2 (user-defined, e.g., channel subcategory).    | All                        |
| channel_grouping3                   | Custom grouping level 3 (user-defined, e.g., specific channel).       | All                        |
| channel_grouping4                   | Custom grouping level 4 (user-defined, e.g., campaign type).          | All                        |
| channel_grouping5                   | Custom grouping level 5 (user-defined, e.g., market segment).         | All                        |

## Important Notes and Limitations ⚠️

- **Key rule for date filtering:** The table is partitioned. To keep your queries fast and inexpensive, **always filter data using the \_PARTITIONTIME pseudo-column**.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with marketing data (data_source_type = 'Ad Systems') will not contain attribution metrics (e.g., first_click_conversion will be NULL), and vice versa.
- **Aggregation:** This table is already aggregated. Each User Behaviour row is the sum of fractional shares for a given channel (ga_source, ga_medium, etc.) on a given day.

## Example SQL Queries

### Comparison of the number of "purchase" conversions by attribution models (current month)

```sql
SELECT
  ga_source,
  ga_medium,
  SUM(first_click_conversion)      AS first_click_conversions,
  SUM(last_click_conversion)       AS last_click_conversions,
  SUM(linear_conversion)           AS linear_conversions,
  SUM(position_based_conversion)   AS position_based_conversions
FROM
  `witcloud_{id-projektu}.aio_ga_attribution_summary`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND event_name = 'purchase'
GROUP BY
  ga_source,
  ga_medium
ORDER BY
  last_click_conversions DESC;
```

### ROAS for the "google / cpc" channel across different attribution models

```sql
SELECT
  'google / cpc' AS channel,
  SAFE_DIVIDE(SUM(first_click_conversion_value), SUM(ad_system_cost)) AS roas_first_click,
  SAFE_DIVIDE(SUM(last_click_conversion_value),  SUM(ad_system_cost)) AS roas_last_click,
  SAFE_DIVIDE(SUM(linear_conversion_value),      SUM(ad_system_cost)) AS roas_linear
FROM
  `witcloud_{id-projektu}.aio_ga_attribution_summary`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND (
    (ga_source = 'google' AND ga_medium = 'cpc')
    OR
    (data_source_category = 'Google Ads')
  );
```
