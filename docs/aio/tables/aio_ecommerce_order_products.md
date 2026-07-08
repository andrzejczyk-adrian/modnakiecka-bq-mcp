# All In One - product data from orders (Ecommerce & Marketplace)

## Purpose and Main Use Cases 🎯

The table aio_ecommerce_orders_products is a tool for **in-depth analysis of sales at the level of individual products**. While the aio_ecommerce_orders table focuses on the entire order, this datamart lets you "drill down" and understand which specific items in your assortment generate the most value.

The main goal is to answer questions such as: "Which products sell best?", "What is the revenue from a given category or brand?" or "How many units of a specific SKU did we sell last month?". The table also includes **aggregated marketing costs**, allowing you to juxtapose daily product sales with daily advertising spend.

## Included Source Systems 🔌

This table combines data from two main categories to provide a complete picture:

- **Product Data in Orders (Ecommerce & Marketplace):**
    - **E-commerce Platforms:** BaseLinker, IdoSell, Magento, PrestaShop, Shoper, WooCommerce (at the - Products level).
    - **Marketplace:** Allegro (at the - Products level).
- **Marketing Cost Data (Ad Systems):**
    - Awin, Bing Ads, Ceneo, Convertiser, Criteo Ads, Domodi & Allani, Facebook Ads, Google Ads, Optimise, RTB House, TikTok, Tradedoubler.

## Table Location in BigQuery 📍

The table is located in BigQuery at the path:
`witcloud_{project-id}.aio_ecommerce_orders_products`

## Data Structure and Granularity 🧱

The table has a UNION-based structure, which means that **one row represents one of two events**:

1. **A single product within an order**: A row originating from an Ecommerce or Marketplace source.
2. **Aggregated daily marketing cost**: A row originating from an Ad Systems source.

**Important difference vs. aio_ecommerce_orders**: This table includes detailed product dimensions (item_id, item_name, item_category), but **does not aggregate metrics at the entire order level**.

**Key groups of fields:**

- **Data Source Dimensions:** `data_source_type`, `data_source_name`, etc.
- **Order Dimensions (inherited):** `order_id`, `order_status`, `order_payment_name`, etc.
- **Product Dimensions:** `item_id`, `item_name`, `item_brand`, `item_category`, etc.
- **Customer Dimensions (inherited):** `customer_hash`, `customer_is_new`, etc.
- **Financial and Marketing Metrics:** `item_revenue_incl_tax`, `item_quantity`, `ad_system_cost`, `ad_system_item_cost`, etc.

## Typical Analytical Questions this table answers 🤔

- What are our **top 10 best-selling products** by revenue this month?
- How many units of the product with **SKU `XYZ-123`** did we sell last quarter?
- Which **categories** of products generate the highest revenue?
- What does **daily product sales** look like compared to **daily marketing costs**?

## Full Column Definitions 📋

| Field Name                     | Business Description                                             | Availability (Source Type)    |
| ------------------------------ | ---------------------------------------------------------------- | ----------------------------- |
| data_source_collect_id         | Technical identifier of the connector that retrieved the data.   | All                           |
| data_source_last_mod_time      | Timestamp of the last modification of data in the source system. | All                           |
| data_source_type               | Main type of data source (e.g., 'Ad Systems', 'Ecommerce').      | All                           |
| data_source_subtype            | Detailed data subtype (e.g., 'Magento - Products').              | All                           |
| data_source_category           | Source category (e.g., 'Magento', 'Allegro').                    | All                           |
| data_source_name               | Name of the specific data source defined on the platform.        | All                           |
| date                           | Event date. For reporting, not for partition filtering.          | All                           |
| event_timestamp_utc            | Exact timestamp (UTC) of order placement.                        | Ecommerce, Marketplace        |
| currency                       | Currency in which values are expressed (e.g., PLN, EUR).         | All                           |
| order_id                       | Identifier of the order in which the given product is included.  | Ecommerce, Marketplace        |
| order_status                   | Status of the order in which the given product is included.      | Ecommerce, Marketplace        |
| order_city                     | City of order delivery.                                          | Ecommerce, Marketplace        |
| order_country                  | Country of order delivery.                                       | Ecommerce, Marketplace        |
| order_region                   | Region / province / postal code of delivery.                     | Ecommerce, Marketplace        |
| order_delivery_name            | Name of the delivery method for the entire order.                | Ecommerce, Marketplace        |
| order_payment_name             | Name of the payment method for the entire order.                 | Ecommerce, Marketplace        |
| shop_id                        | Identifier of the store or order source.                         | Ecommerce, Marketplace        |
| shop_name                      | Name of the store or order source.                               | Ecommerce, Marketplace        |
| customer_id                    | Internal identifier of the customer who purchased the product.   | Ecommerce                     |
| customer_hash                  | Hashed (SHA256) customer email address.                          | Ecommerce, Marketplace        |
| customer_is_new                | Flag (true/false) whether this was the customer's first order.   | Ecommerce                     |
| customer_first_order_timestamp | Timestamp of the customer's first order.                         | Ecommerce                     |
| item_id                        | Product or variant identifier (SKU).                             | Ecommerce, Marketplace        |
| item_name                      | Product name.                                                    | Ecommerce, Marketplace        |
| item_code                      | Product code (SKU, EAN or other).                                | Ecommerce, Marketplace        |
| item_brand                     | Product brand.                                                   | Ecommerce                     |
| item_category                  | Product category.                                                | Ecommerce                     |
| item_option                    | Selected product variant or option.                              | Ecommerce                     |
| item_quantity                  | Number of units of the product sold within the order line.       | Ecommerce, Marketplace        |
| item_revenue_incl_tax          | Value of the sold units of the product (including tax).          | Ecommerce, Marketplace        |
| item_revenue_excl_tax          | Value of the sold units of the product (excluding tax).          | Ecommerce, Marketplace        |
| ad_system_campaign_name        | Advertising campaign name.                                       | Ad Systems                    |
| ad_system_account_name         | Advertising account name.                                        | Ad Systems                    |
| ad_system_cost                 | Cost in the reporting currency (campaign/ad group).              | Ad Systems                    |
| ad_system_item_cost            | Cost in the reporting currency at the product level (Shopping).  | Ad Systems (Google, Facebook) |
| ad_system_clicks               | Total clicks (campaign/ad group).                                | Ad Systems                    |
| ad_system_item_clicks          | Total clicks at the product level (Shopping).                    | Ad Systems (Google, Facebook) |
| ad_system_impressions          | Total impressions (campaign/ad group).                           | Ad Systems                    |
| ad_system_item_impressions     | Total impressions at the product level (Shopping).               | Ad Systems (Google, Facebook) |
| ad_system_conversions          | Total conversions (campaign/ad group).                           | Ad Systems                    |
| ad_system_item_conversions     | Total conversions at the product level (Shopping).               | Ad Systems (Google, Facebook) |
| channel_grouping1              | Custom grouping level 1 (user-defined, e.g., marketing channel or market). | All                           |
| channel_grouping2              | Custom grouping level 2 (user-defined, e.g., channel subcategory). | All                           |
| channel_grouping3              | Custom grouping level 3 (user-defined, e.g., specific channel).   | All                           |
| channel_grouping4              | Custom grouping level 4 (user-defined, e.g., campaign type).      | All                           |
| channel_grouping5              | Custom grouping level 5 (user-defined, e.g., market segment).     | All                           |

## Important Notes and Limitations ⚠️

- **Key rule for date filtering:** The table is partitioned. To keep your queries fast and inexpensive, **always filter data using the \_PARTITIONTIME pseudo-column**.
- **Two types of rows:** Remember that this table contains two kinds of data. Rows with marketing data (data_source_type = 'Ad Systems') will not include product details (e.g., item_id will be NULL), and vice versa.
- **No order-level metrics:** This table is optimized for product analysis. It is **not suitable for analyzing aggregate order-level values**, such as shipping costs or discounts for the entire cart. For that purpose, use the aio_ecommerce_orders table.

## Example SQL Queries

### Top 10 best-selling products by revenue in the current month

```sql
SELECT
  item_name,
  item_code,
  SUM(item_revenue_incl_tax) AS total_product_revenue,
  SUM(item_quantity) AS total_quantity_sold
FROM
  `witcloud_{project-id}.aio_ecommerce_orders_products`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
  AND item_name IS NOT NULL
GROUP BY
  item_name,
  item_code
ORDER BY
  total_product_revenue DESC
LIMIT 10;
```

### Daily product sales vs. marketing cost

```sql
SELECT
  date,
  SUM(item_revenue_incl_tax) AS total_product_revenue,
  SUM(ad_system_cost) + SUM(ad_system_item_cost) AS total_marketing_cost
FROM
  `witcloud_{project-id}.aio_ecommerce_orders_products`
WHERE
  _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
GROUP BY
  date
ORDER BY
  date DESC;
```

### Total quantity sold for a specific product (SKU)

```sql
SELECT
  item_name,
  SUM(item_quantity) AS total_quantity_sold
FROM
  `witcloud_{project-id}.aio_ecommerce_orders_products`
WHERE
  -- Add a partition filter for optimization
  _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY))
  AND item_code = 'YOUR-SKU-CODE'
GROUP BY
  item_name;
```
