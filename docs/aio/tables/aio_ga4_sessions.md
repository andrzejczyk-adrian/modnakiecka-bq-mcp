# All In One - traffic and marketing cost data (GA4 + Ad Systems)

## Purpose and Main Use Case 🎯

The table aio_ga_sessions is the central point for **analyzing traffic on your website combined with marketing cost data**. Its main goal is to enable the evaluation of the effectiveness of various marketing channels by comparing data on sessions, user behavior, and conversions (from Google Analytics 4) with advertising spend (from ad systems).

It is an ideal tool for creating so-called **"blended reports"**, where in a single view you can calculate key indicators such as **ROAS (Return On Ad Spend)** and **CPA (Cost Per Acquisition)** for individual sources, mediums, or campaigns, even if directly joining the data (JOIN) is hindered due to inconsistencies in tagging.

## Included Source Systems 🔌

This table combines data from two main categories to provide a complete picture of traffic effectiveness:

- **Session and Behavior Data (User Behaviour):**
    - **Google Analytics 4 BigQuery:** Session-level data (Google Analytics 4 BigQuery - Sessions - GA4).
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{id-projektu}.aio_ga_sessions`

## Data Structure and Granularity 🧱

The table has a UNION-based structure, which means that **one row represents one of two events**:

1. **Aggregated session data from a given day for a specific combination of dimensions** (e.g., source, medium, campaign) from Google Analytics 4.
2. **Aggregated daily marketing cost** from a given advertising system.

This architecture allows flexible grouping of data in BI tools (e.g., Looker Studio) to create unified marketing channels (e.g., "Paid Social", "Paid Search") and calculate efficiency metrics for them.

**Main field groups:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **GA4 Session Dimensions:** ga_session_source, ga_session_medium, ga_session_campaign, ga_country, etc.
- **GA4 Session Metrics:** ga_totals_sessions, ga_totals_engagement, ga_totals_revenue, ga_totals_purchase, etc.
- **Marketing Dimensions and Metrics:** ad_system_campaign_name, ad_system_cost, ad_system_clicks, ad_system_impressions.

## Common Analytical Questions Answered by This Table 🤔

- Which overall marketing channel (e.g., Paid Search, Paid Social, Organic) generated the highest ROAS in the last quarter?
- What are the most and least efficient campaigns in terms of Cost per Session across all paid sources?
- How do engagement rate and e-commerce conversion rate differ between paid and free traffic?
- What is the daily relationship between total marketing cost and revenue recorded in Google Analytics?

## Full Column Definitions 📋

| Field Name                                      | Business Description                                             | Availability (Source Type) |
| ----------------------------------------------- | ---------------------------------------------------------------- | -------------------------- |
| data_source_collect_id                          | Technical identifier of the connector that retrieved the data.   | All                        |
| data_source_last_mod_time                       | Timestamp of the last modification of data in the source system. | All                        |
| data_source_type                                | Main type of data source (e.g., 'Ad Systems', 'User Behaviour'). | All                        |
| data_source_subtype                             | Detailed data subtype (e.g., 'GA4 BigQuery – Sessions').         | All                        |
| data_source_category                            | Source category (e.g., 'Google Ads', 'GA4 BigQuery').            | All                        |
| data_source_name                                | Name of the specific data source in the platform.                | All                        |
| date                                            | Event date (reporting).                                          | All                        |
| event_timestamp_utc                             | Exact event timestamp (UTC).                                     | User Behaviour             |
| currency                                        | Original currency.                                               | All                        |
| report_currency                                 | Reporting currency.                                              | All                        |
| ga_session_id                                   | Unique GA4 session identifier.                                   | User Behaviour             |
| ga_session_source                               | Session source (e.g., 'google', 'facebook.com').                 | User Behaviour             |
| ga_session_medium                               | Session medium (e.g., 'cpc', 'organic').                         | User Behaviour             |
| ga_session_campaign                             | Campaign name assigned to the session by GA4.                    | User Behaviour             |
| ga_session_ad_content                           | Ad content assigned to the session (GA4).                        | User Behaviour             |
| ga_session_keyword                              | Keyword assigned to the session (GA4).                           | User Behaviour             |
| ga_landing_page                                 | Session landing page.                                            | User Behaviour             |
| ga_platform                                     | Platform (e.g., 'WEB', 'ANDROID').                               | User Behaviour             |
| ga_country                                      | User country.                                                    | User Behaviour             |
| ga_city                                         | User city.                                                       | User Behaviour             |
| ad_system_account_id                            | Google Ads account ID linked to the session (from GA4).          | User Behaviour             |
| ad_system_account_name                          | Google Ads account name linked to the session (from GA4).        | User Behaviour             |
| ad_system_campaign_id                           | Google Ads campaign ID linked to the session (from GA4).         | User Behaviour             |
| ad_system_campaign_name                         | Google Ads campaign name linked to the session (from GA4).       | User Behaviour             |
| ad_system_adgroup_id                            | Google Ads ad group ID linked to the session (from GA4).         | User Behaviour             |
| ad_system_adgroup_name                          | Google Ads ad group name linked to the session (from GA4).       | User Behaviour             |
| ad_system_placement                             | Google Ads placement (from GA4).                                 | User Behaviour             |
| ga_totals_sessions                              | Number of sessions.                                              | User Behaviour             |
| ga_totals_engagement                            | Number of engaged sessions.                                      | User Behaviour             |
| ga_totals_engagement_time_seconds               | Total engagement time (sec.).                                    | User Behaviour             |
| ga_totals_page_view                             | Total page views.                                                | User Behaviour             |
| ga_totals_unique_page_view                      | Total unique page views.                                         | User Behaviour             |
| ga_totals_screen_view                           | Total screen views (apps).                                       | User Behaviour             |
| ga_totals_unique_screen_view                    | Total unique screen views.                                       | User Behaviour             |
| ga_totals_first_visit                           | Sessions that were the user's first visit.                       | User Behaviour             |
| ga_totals_visit_duration                        | Total visit duration.                                            | User Behaviour             |
| ga_totals_event                                 | Total events.                                                    | User Behaviour             |
| ga_totals_event_count                           | Counts of individual events (aggregate).                         | User Behaviour             |
| ga_totals_event_value                           | Values of individual events (aggregate).                         | User Behaviour             |
| ga_totals_view_item                             | Product view events (view_item).                                 | User Behaviour             |
| ga_totals_add_to_cart                           | Add-to-cart events.                                              | User Behaviour             |
| ga_totals_begin_checkout                        | Checkout start events.                                           | User Behaviour             |
| ga_totals_add_shipping_info                     | Add shipping info events.                                        | User Behaviour             |
| ga_totals_add_payment_info                      | Add payment info events.                                         | User Behaviour             |
| ga_totals_purchase                              | Purchase events (purchase).                                      | User Behaviour             |
| ga_totals_revenue                               | Purchase revenue (GA4 property currency).                        | User Behaviour             |
| ga_totals_original_revenue                      | Technical field (identical to revenue).                          | User Behaviour             |
| ga_totals_purchase_revenue_in_property_currency | Purchase revenue in property currency.                           | User Behaviour             |
| ga_totals_shipping_value_in_property_currency   | Shipping revenue (property currency).                            | User Behaviour             |
| ga_totals_tax_value_in_property_currency        | Tax (property currency).                                         | User Behaviour             |
| ga_totals_refund_value_in_property_currency     | Refunds (property currency).                                     | User Behaviour             |
| ga_totals_abandoned_cart_sessions               | Sessions with abandoned carts.                                   | User Behaviour             |
| ga_totals_is_first_purchase_sessions            | Sessions with first purchase.                                    | User Behaviour             |
| ad_system_cost                                  | Cost in reporting currency.                                      | Ad Systems                 |
| ad_system_clicks                                | Total clicks.                                                    | Ad Systems                 |
| ad_system_impressions                           | Total impressions.                                               | Ad Systems                 |
| ad_system_conversions                           | Total conversions (from the advertising system).                 | Ad Systems                 |
| ad_system_account_name (cost)                   | Ad account name (from cost data).                                | Ad Systems                 |
| ad_system_campaign_name (cost)                  | Campaign name (from cost data).                                  | Ad Systems                 |
| channel_grouping1                               | Custom grouping level 1 (user-defined, e.g., marketing channel or market). | All                        |
| channel_grouping2                               | Custom grouping level 2 (user-defined, e.g., channel subcategory). | All                        |
| channel_grouping3                               | Custom grouping level 3 (user-defined, e.g., specific channel).   | All                        |
| channel_grouping4                               | Custom grouping level 4 (user-defined, e.g., campaign type).      | All                        |
| channel_grouping5                               | Custom grouping level 5 (user-defined, e.g., market segment).     | All                        |

## Important Notes and Limitations ⚠️

- **Key rule for date filtering:** The table is partitioned. To keep your queries fast and inexpensive, **always filter data using the \_PARTITIONTIME pseudo-column**.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with marketing data (data_source_type = 'Ad Systems') will not include GA4 metrics (e.g., ga_totals_sessions will be NULL), and vice versa. Combining these data into coherent channels is done through grouping in the BI tool.
- **Tagging consistency:** The effectiveness of analysis in this table strongly depends on the quality of UTM tagging in your campaigns. Consistent naming of utm_campaign, utm_source, and utm_medium allows for precise linking of costs to sessions.
- **Uwaga (doświadczenie praktyczne):** `ga_totals_event_count` to STRING w formacie `NAZWA:LICZBA||,` — parsuj przez `REGEXP_EXTRACT`. Metryki eventów liczą tylko eventy przypisane do sesji (`ga_session_id`); eventy bez sesji nie są ujęte, więc sumy mogą być niższe niż w surowym eksporcie GA4.

## Example SQL Queries

### Basic traffic and cost metrics for the "google / cpc" channel yesterday

```sql
SELECT
  -- GA4 metrics
  SUM(ga_totals_sessions) AS sessions,
  SUM(ga_totals_revenue)  AS ga_revenue,
  -- Cost metrics
  SUM(ad_system_cost)      AS cost,
  SUM(ad_system_clicks)    AS clicks,
  SUM(ad_system_impressions) AS impressions,
  -- KPI
  SAFE_DIVIDE(SUM(ad_system_cost), SUM(ga_totals_sessions)) AS cost_per_session
FROM
  `witcloud_{id-projektu}.aio_ga_sessions`
WHERE
  _PARTITIONTIME = TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
  AND (
    (ga_session_source = 'google' AND ga_session_medium = 'cpc')
    OR
    (data_source_category = 'Google Ads' AND data_source_subtype NOT LIKE '%Shopping%')
  );
```

### Campaign performance based on GA4 and cost data in the current month

```sql
SELECT
  COALESCE(ga_session_campaign, ad_system_campaign_name) AS campaign_name,
  SUM(ad_system_cost)        AS total_cost,
  SUM(ga_totals_sessions)    AS total_sessions,
  SUM(ga_totals_purchase)    AS total_purchases,
  SUM(ga_totals_revenue)     AS total_revenue,
  SAFE_DIVIDE(SUM(ga_totals_revenue), SUM(ad_system_cost)) AS roas
FROM
  `witcloud_{id-projektu}.aio_ga_sessions`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
GROUP BY
  campaign_name
HAVING
  total_cost > 0 OR total_sessions > 0
ORDER BY
  total_cost DESC;
```
