# All In One - order data and marketing costs

## Purpose and Main Use Cases 🎯

The table aio_ecommerce_orders is your hub for analyzing business profitability. Its unique feature is the **combination, in one place, of "hard" sales data from your e-commerce platforms and marketplaces with aggregated, daily costs from all advertising systems**.

The main goal of this datamart is to enable you to answer the fundamental question: "How much do we earn and how much do we spend?". It allows for instant calculation of global profitability indicators such as **ROAS (Return On Ad Spend)** and **ERS (effective revenue share)**, cohort analysis of customers (new vs. returning), and monitoring the overall financial health of your sales and marketing activities.

## Included Source Systems 🔌

This table combines data from two main categories to provide a complete picture:

- **Order Data (Ecommerce & Marketplace):**
    - **E-commerce Platforms:** BaseLinker, IdoSell, Magento, PrestaShop, Shoper, WooCommerce.
    - **Marketplace:** Allegro.
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{project-id}.aio_ecommerce_orders`

## Data Structure and Granularity 🧱

The table has a unique UNION-based structure, which means that **one row represents one of two events**:

1. **Single order**: A row originating from an Ecommerce or Marketplace source.
2. **Aggregated daily marketing cost**: A row originating from an Ad Systems source.

This design allows for very simple daily aggregations to compare revenue and costs.

**Key groups of fields:**

- **Data Source Dimensions:** data_source_type, data_source_name, etc.
- **Order Dimensions:** order_id, order_status, order_payment_name, etc.
- **Customer Dimensions:** customer_hash, customer_is_new, etc.
- **Financial Metrics:** item_revenue_incl_tax, shipping_revenue_incl_tax, ad_system_cost, etc.

## Typical Analytical Questions this table answers 🤔

- What was our total **order revenue** and **total marketing cost** last month?
- What is our overall **ROAS (revenue/cost)** or **ERS (cost/revenue)** in the current quarter?
- How many **new customers** did we acquire last week and what sales did they generate?
- Which **shipping methods** are most frequently chosen by customers?

## Full Column Definitions 📋

| Field Name                          | Business Description                                                          | Availability (Source Type) |
| ----------------------------------- | ----------------------------------------------------------------------------- | -------------------------- |
| data_source_collect_id              | Technical identifier of the connector that retrieved the data.                | All                        |
| data_source_last_mod_time           | Timestamp of the last modification of data in the source system.              | All                        |
| data_source_type                    | Main type of data source (e.g., 'Ad Systems', 'Ecommerce').                   | All                        |
| data_source_subtype                 | Detailed subtype of data defining its granularity (e.g., 'Magento - Orders'). | All                        |
| data_source_category                | Source category (e.g., 'Magento', 'Allegro').                                 | All                        |
| data_source_name                    | Name of the specific data source defined on the platform (e.g., store name).  | All                        |
| date                                | Event date (order placement or cost incurred).                                | All                        |
| event_timestamp_utc                 | Exact timestamp (UTC) of order placement.                                     | Ecommerce, Marketplace     |
| currency                            | Currency in which values are expressed (e.g., PLN, EUR).                      | All                        |
| order_id                            | Unique order identifier from the store/marketplace system.                    | Ecommerce, Marketplace     |
| order_status                        | Order status (e.g., "fulfilled", "canceled").                                 | Ecommerce, Marketplace     |
| order_city                          | City of order delivery.                                                       | Ecommerce, Marketplace     |
| order_country                       | Country of order delivery.                                                    | Ecommerce, Marketplace     |
| order_region                        | Region/province/postal code of delivery.                                      | Ecommerce, Marketplace     |
| order_delivery_name                 | Name of the selected delivery method.                                         | Ecommerce, Marketplace     |
| order_payment_name                  | Name of the selected payment method.                                          | Ecommerce, Marketplace     |
| shop_id                             | Identifier of the store or order source.                                      | Ecommerce, Marketplace     |
| shop_name                           | Name of the store or order source.                                            | Ecommerce, Marketplace     |
| customer_id                         | Internal customer identifier from the source system.                          | Ecommerce                  |
| customer_hash                       | Hashed (SHA256) customer email address for cross-platform analysis.           | Ecommerce, Marketplace     |
| customer_is_new                     | Flag (true/false) indicating whether this is the customer's first order.      | Ecommerce                  |
| customer_first_order_timestamp      | Timestamp of the customer's first-ever order.                                 | Ecommerce                  |
| item_revenue_incl_tax               | Sum of product values in the order (including tax).                           | Ecommerce, Marketplace     |
| item_revenue_excl_tax               | Sum of product values (excluding tax).                                        | Ecommerce, Marketplace     |
| shipping_revenue_incl_tax           | Shipping revenue (including tax).                                             | Ecommerce, Marketplace     |
| shipping_revenue_excl_tax           | Shipping revenue (excluding tax).                                             | Ecommerce, Marketplace     |
| discount_value_incl_tax             | Value of applied discounts (including tax).                                   | Ecommerce                  |
| discount_value_excl_tax             | Value of applied discounts (excluding tax).                                   | Ecommerce                  |
| item_quantity                       | Number of product units in the order.                                         | Ecommerce, Marketplace     |
| ad_system_campaign_name             | Advertising campaign name.                                                    | Ad Systems                 |
| ad_system_account_name              | Advertising account name.                                                     | Ad Systems                 |
| ad_system_cost                      | Cost in the reporting currency.                                               | Ad Systems                 |
| ad_system_clicks                    | Total clicks.                                                                 | Ad Systems                 |
| ad_system_impressions               | Total impressions.                                                            | Ad Systems                 |
| ad_system_conversions               | Total conversions.                                                            | Ad Systems                 |
| ad_system_conversions_value         | Conversion value in the reporting currency.                                   | Ad Systems                 |
| original_discount_value_excl_tax    | Original discount value (excluding tax) in the source currency.               | Ecommerce                  |
| original_discount_value_incl_tax    | Original discount value (including tax) in the source currency.               | Ecommerce                  |
| original_shipping_revenue_excl_tax  | Original shipping revenue (excluding tax) in the source currency.             | Ecommerce                  |
| original_shipping_revenue_incl_tax  | Original shipping revenue (including tax) in the source currency.             | Ecommerce                  |
| ad_system_original_cost             | Total cost in the original currency of the advertising system.                | Ad Systems                 |
| ad_system_original_conversion_value | Total conversion value in the original currency of the advertising system.    | Ad Systems                 |
| channel_grouping1                   | Custom grouping level 1 (user-defined, e.g., marketing channel or market).    | All                        |
| channel_grouping2                   | Custom grouping level 2 (user-defined, e.g., channel subcategory).            | All                        |
| channel_grouping3                   | Custom grouping level 3 (user-defined, e.g., specific channel).               | All                        |
| channel_grouping4                   | Custom grouping level 4 (user-defined, e.g., campaign type).                  | All                        |
| channel_grouping5                   | Custom grouping level 5 (user-defined, e.g., market segment).                 | All                        |

## Important Notes and Limitations ⚠️

- 🚨 **Duplicate-orders window 2026-06-28 … 2026-08-02 (Modna Kiecka):** in this
  period orders exist TWICE — from `MK shoper` AND from the parallel feed
  `MK Custom Ecommerce` (99.8% identical `order_id`s; feed switched off in early
  August 2026). Revenue/order sums over that window are ~2× inflated unless you
  filter `data_source_name = 'MK shoper'` or deduplicate by `order_id`. The same
  duplication affects `aio_ecommerce_order_products` and the Ecommerce rows of
  `aio_main`. The retired feed was also the only source of mobile-app orders
  (`order_id` range 300,000,xxx) — from 2026-08-03 app orders are missing from
  the warehouse (audit 2026-09-01).
- **Key rule for date filtering:** The table is partitioned by data ingestion time. To keep your queries fast and inexpensive, **always filter data using the pseudo-column \_PARTITIONTIME**, not the date column.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with data_source_type = 'Ad Systems' will not include order details (e.g., order_id will be NULL), and vice versa. When summing metrics, you don't need to worry about this, but when filtering, it's worth keeping in mind.
- **Customer analysis:** The customer_is_new field is extremely useful for segmentation and analysis of customer lifetime value (LTV).

## Example SQL Queries

### Daily sales vs. marketing cost and ROAS & ERS indicators in the current month

```sql
SELECT
  date,
  SUM(item_revenue_incl_tax) AS total_revenue,
  SUM(ad_system_cost) AS total_cost,
  -- ROAS = Revenue / Cost
  SAFE_DIVIDE(SUM(item_revenue_incl_tax), SUM(ad_system_cost)) AS roas,
  -- ERS = Cost / Revenue
  SAFE_DIVIDE(SUM(ad_system_cost), SUM(item_revenue_incl_tax)) AS ers
FROM
  `witcloud_{project-id}.aio_ecommerce_orders`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
GROUP BY
  date
ORDER BY
  date DESC;
```

### Number of orders from new and returning customers yesterday

```sql
SELECT
  customer_is_new,
  COUNT(DISTINCT order_id) AS number_of_orders,
  SUM(item_revenue_incl_tax) AS revenue
FROM
  `witcloud_{project-id}.aio_ecommerce_orders`
WHERE
  _PARTITIONTIME = TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY))
  AND data_source_type = 'Ecommerce'
GROUP BY
  customer_is_new;
```

### Sales by payment method in the current month

```sql
SELECT
  order_payment_name,
  SUM(item_revenue_incl_tax) AS total_revenue
FROM
  `witcloud_{project-id}.aio_ecommerce_orders`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND order_payment_name IS NOT NULL
GROUP BY
  order_payment_name
ORDER BY
  total_revenue DESC;
```
