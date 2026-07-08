# All In One - product level data from Google Analytics 4

## Purpose and Main Use Cases 🎯

The table aio_ga_products provides the most detailed insight into the **sales performance of individual products based on transaction data from Google Analytics 4**. Each row in this table represents a unique product within a single transaction, allowing for in-depth assortment analysis.

The main goal of this datamart is the analysis of revenue, quantities sold, brands, and categories at the SKU level. The table also includes the full session context (source, medium, campaign) in which a given product was sold, as well as **aggregated marketing costs**, which enables linking product performance data with daily advertising spend.

## Included Source Systems 🔌

- **Product Data in Transactions (User Behaviour):**
    - **Google Analytics 4 BigQuery:** Product-level data (Google Analytics 4 BigQuery - Products - GA4).
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{project-id}.aio_ga_products`

## Data Structure and Granularity 🧱

The table has a UNION-based structure, which means that **one row represents one of two events**:

1. **A single product within a transaction** recorded by Google Analytics 4.
2. **Aggregated daily marketing cost** from a given advertising system.

**Key groups of fields:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **GA4 Product Dimensions:** ga_item_id, ga_item_name, ga_item_brand, ga_item_category, etc.
- **Session Dimensions (context):** ga_session_source, ga_session_medium, ga_transaction_id, etc.
- **GA4 Product Metrics:** ga_item_quantity, ga_item_revenue_excl_tax.
- **Marketing Dimensions and Metrics:** ad_system_campaign_name, ad_system_cost, etc.

## Typical Analytical Questions Answered by This Table 🤔

- What are our best-selling products (TOP 10 SKU) by revenue this month?
- Products of which brands generate the highest revenue?
- How many units of a specific product were sold in google / cpc campaigns?
- What does daily product sales look like compared to daily advertising costs?

## Full Column Definitions 📋

| Field Name                     | Business Description                                             | Availability (Source Type)    |
| ------------------------------ | ---------------------------------------------------------------- | ----------------------------- |
| data_source_collect_id         | Technical identifier of the connector that retrieved the data.   | All                           |
| data_source_last_mod_time      | Timestamp of the last modification of data in the source system. | All                           |
| data_source_type               | Main data source type (e.g., 'Ad Systems', 'User Behaviour').    | All                           |
| data_source_subtype            | Detailed subtype (e.g., 'GA4 BigQuery – Products').              | All                           |
| data_source_category           | Source category (e.g., platform).                                | All                           |
| data_source_name               | Name of the specific data source in the platform.                | All                           |
| date                           | Event date (reporting).                                          | All                           |
| event_timestamp_utc            | Exact transaction timestamp (UTC).                               | User Behaviour                |
| currency                       | Original currency.                                               | All                           |
| report_currency                | Reporting currency.                                              | All                           |
| ga_item_id                     | Product ID (SKU) in GA4.                                         | User Behaviour                |
| ga_item_name                   | Product name.                                                    | User Behaviour                |
| ga_item_brand                  | Product brand.                                                   | User Behaviour                |
| ga_item_category               | Product category.                                                | User Behaviour                |
| ga_item_variant                | Product variant.                                                 | User Behaviour                |
| ga_transaction_id              | Transaction ID in which the product was sold.                    | User Behaviour                |
| ga_session_id                  | Session ID in which the product was sold.                        | User Behaviour                |
| ga_session_source              | Session source (e.g., 'google').                                 | User Behaviour                |
| ga_session_medium              | Session medium (e.g., 'cpc', 'organic').                         | User Behaviour                |
| ga_session_campaign            | Campaign assigned to the session.                                | User Behaviour                |
| ga_session_ad_content          | Ad content assigned to the session.                              | User Behaviour                |
| ga_session_keyword             | Keyword assigned to the session.                                 | User Behaviour                |
| ga_landing_page                | Session landing page.                                            | User Behaviour                |
| ga_platform                    | Platform (e.g., 'WEB').                                          | User Behaviour                |
| ga_country                     | User country.                                                    | User Behaviour                |
| ga_city                        | User city.                                                       | User Behaviour                |
| ad_system_account_id           | Advertising account ID linked to the session (from GA4).         | User Behaviour                |
| ad_system_account_name         | Advertising account name linked to the session (from GA4).       | User Behaviour                |
| ad_system_campaign_id          | Campaign ID linked to the session (from GA4).                    | User Behaviour                |
| ad_system_campaign_name        | Campaign name linked to the session (from GA4).                  | User Behaviour                |
| ad_system_adgroup_id           | Ad group ID linked to the session (from GA4).                    | User Behaviour                |
| ad_system_adgroup_name         | Ad group name linked to the session (from GA4).                  | User Behaviour                |
| ad_system_placement            | Placement of the ad linked to the session (from GA4).            | User Behaviour                |
| ga_item_quantity               | Number of product units sold.                                    | User Behaviour                |
| ga_item_revenue_excl_tax       | Product revenue (excluding tax) in the reporting currency.       | User Behaviour                |
| ad_system_campaign_name (cost) | Campaign name (from the advertising system).                     | Ad Systems                    |
| ad_system_account_name (cost)  | Advertising account name (from the advertising system).          | Ad Systems                    |
| ad_system_cost                 | Cost in reporting currency (campaign/ad group).                  | Ad Systems                    |
| ad_system_item_cost            | Product-level cost (Shopping campaigns).                         | Ad Systems (Google, Facebook) |
| ad_system_clicks               | Total clicks.                                                    | Ad Systems                    |
| ad_system_impressions          | Total impressions.                                               | Ad Systems                    |
| ad_system_conversions          | Total conversions from the advertising system.                   | Ad Systems                    |
| channel_grouping1              | Custom grouping level 1 (user-defined, e.g., marketing channel or market). | All                           |
| channel_grouping2              | Custom grouping level 2 (user-defined, e.g., channel subcategory). | All                           |
| channel_grouping3              | Custom grouping level 3 (user-defined, e.g., specific channel).   | All                           |
| channel_grouping4              | Custom grouping level 4 (user-defined, e.g., campaign type).      | All                           |
| channel_grouping5              | Custom grouping level 5 (user-defined, e.g., market segment).     | All                           |

## Important Notes and Limitations ⚠️

- **Key rule for date filtering:** The table is partitioned. To keep your queries fast and inexpensive, **always filter data using the \_PARTITIONTIME pseudo-column**.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with marketing data (data_source_type = 'Ad Systems') will not include product details (e.g., ga_item_id will be NULL), and vice versa.
- **Source of product data:** The data in this table comes from the e-commerce data layer and is recorded by Google Analytics 4. Its completeness and accuracy depend on the correctness of the tracking implementation on your site.

## Example SQL Queries

### Top 10 best-selling products (by SKU) in the current month

```sql
SELECT
  ga_item_id,
  ANY_VALUE(ga_item_name) AS item_name,
  SUM(ga_item_quantity) AS total_quantity_sold,
  SUM(ga_item_revenue_excl_tax) AS total_revenue
FROM
  `witcloud_{project-id}.aio_ga_products`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND ga_item_id IS NOT NULL
GROUP BY
  ga_item_id
ORDER BY
  total_revenue DESC
LIMIT 10;
```

### Product revenue by channels (source/medium) in the last week

```sql
SELECT
  ga_session_source,
  ga_session_medium,
  SUM(ga_item_revenue_excl_tax) AS total_product_revenue
FROM
  `witcloud_{project-id}.aio_ga_products`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
  AND ga_item_id IS NOT NULL
GROUP BY
  ga_session_source,
  ga_session_medium
ORDER BY
  total_product_revenue DESC;
```

### Daily product sales vs. total marketing cost

```sql
SELECT
  date,
  SUM(ga_item_revenue_excl_tax) AS total_product_revenue,
  SUM(ad_system_cost) + SUM(ad_system_item_cost) AS total_marketing_cost
FROM
  `witcloud_{project-id}.aio_ga_products`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
GROUP BY
  date
ORDER BY
  date DESC;
```
