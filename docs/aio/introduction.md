# All In One - marketing and sales analytics in one place

All your marketing and sales data in one consistent model.

## 📘 Introduction - What is "All In One"?

### 🎯 Module goal - why was "All In One" created?

In today's world of marketing and e-commerce, data comes from dozens of different
sources: advertising systems, analytics platforms, e-commerce systems (CRM), and
marketplaces. The platform, through the **'Collect'** modules, collects raw data from
all these systems, then transforms dozens of raw tables into consistent, ready-to-use
reporting sets.

Answering a simple question such as "What was our real marketing ROI last quarter?"
requires specialist knowledge to combine, clean, and aggregate data – a tedious,
time-consuming, and error-prone process.

**The "All In One" module solves this problem.**

It automatically retrieves, cleans, and most importantly, **unifies** the data into
one consistent analytical model — a single, reliable source of truth.

### ⚙️ How does it work? (Architecture overview)

1. **Data Collection:** Connection to all key data sources.
2. **Unification and Processing:** Algorithms standardize metric and dimension names,
   combine data into a consistent structure, and prepare it for analysis.
   > Example: *Spend* from Facebook Ads and *Cost* from Google Ads become a single
   > metric – `ad_system_cost`.
3. **Analysis Access:** A series of ready-to-use, specialized tables (datamarts),
   optimized for specific business questions.

### 📊 Where can you use this data?

The data model is available in **Google BigQuery** and is fully compatible with:

- **Looker Studio:** native BigQuery connector for interactive dashboards.
- **Microsoft Power BI / Tableau:** advanced analyses and detailed reports.
- **Google Sheets:** "Connected Sheets" add-on.
- **Direct SQL Queries:** directly in the BigQuery console or via this MCP server.
- **AI and Machine Learning Tools:** clean, structured data as fuel for models.

### 🔗 Integrated systems and levels of granularity

#### 🧩 Advertising systems (Ad Systems)
- **Awin** – transaction and commission data
- **Bing Ads** – campaign performance data
- **Ceneo** – click and cost data
- **Criteo Ads** – aggregated campaign statistics
- **Domodi & Allani** – category-level statistics
- **Facebook Ads** – segmented data for:
  - Facebook Ads (aggregated)
  - Conversions Segments
  - Product Conversions
  - Shopping (product level)
  - Reach (account / campaign / ad set)
- **Google Ads** – segmented data for:
  - Google Ads (aggregated)
  - Conversions Segments
  - Shopping (product level)
- **Optimise**, **RTB House**, **TikTok**, **Tradedoubler** – conversions, commissions,
  campaign statistics.

#### 📈 Analytics (User Behaviour)
- **Google Analytics 4 BigQuery**:
  - Sessions
  - Orders
  - Products
  - Attribution Orders (attribution paths)

#### 🛒 E-commerce
- **BaseLinker**, **IdoSell**, **Magento**, **PrestaShop**, **Shoper**, **WooCommerce**:
  - Orders
  - Products in orders

#### 🏬 Marketplace
- **Allegro**:
  - Orders
  - Products in orders

> Uwaga: powyższa lista to pełen katalog integracji platformy. To, które źródła są
> realnie podpięte w projekcie Modna Kiecka, sprawdzisz w danych:
> `SELECT DISTINCT data_source_category, data_source_subtype FROM aio_main` (z filtrem
> `_PARTITIONTIME`).

### 🧮 Overview of ready-to-use analytical datamarts

Detailed documentation for each table: `read_document("aio/tables/<baseTableName>")`.

* **aio_ad_systems** — aggregates only data from advertising systems. The ideal place
  to analyze costs, clicks, impressions, and conversions from multiple platforms in
  one consistent view, without sales data from the CRM.
* **aio_ecommerce_orders** — a key datamart for profitability analysis. It combines
  "hard" sales data from your e-commerce system with aggregated marketing costs
  (global ERS/ROAS, new vs. returning customers).
* **aio_ecommerce_order_products** — a detailed view of sales at the individual
  product level (which products sell best, revenue by product, trends over time).
  It does not include general order data such as shipping cost.
* **aio_ga4_sessions** — an integrated table for website traffic analysis. GA4
  sessions, users and events combined with costs from advertising systems — for
  "blended metrics" per channel (e.g. ROAS for total paid traffic).
* **aio_ga4_orders** — an alternative to aio_ecommerce_orders, based on transaction
  data recorded by Google Analytics 4.
* **aio_ga4_products** — product-level GA4 transaction data (SKU analysis with full
  session context).
* **aio_ga4_attribution_paths** — detailed, multi-channel conversion paths with a
  transaction ID that can be joined to CRM data for deep attribution analysis.
* **aio_ga4_attribution_summary** — an aggregated view for analyzing and comparing
  channel performance across attribution models (Last-Click, First-Click, Linear,
  Position Based, Time Decay).
* **aio_main** — the complete unified data source (foundation for all datamarts
  above; ~230 columns, advanced users only; no official docs — use get_table_schema).
* **aio_search_console** — Search Console data (WIP in the platform docs).

### 📚 How to use this documentation?

Detailed information about each of the above tables, including **full column
definitions** and **example SQL queries**, is available via
`read_document("aio/tables/<baseTableName>")`.
