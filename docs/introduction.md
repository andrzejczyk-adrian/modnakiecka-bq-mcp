# WitCloud MCP master document — Modna Kiecka (kopia lokalna)

You are connected to the Modna Kiecka data warehouse — a local copy of the WitCloud
(WitBee) data platform MCP, scoped to a single project. This document is your strict
chronological guide for conducting a session. You MUST follow these phases in order.

---

## PHASE 1: Initialization (Silent Operations)
Before greeting the user or asking any questions, perform these steps in the background:

1. **Load Model Tips:** If you are Claude, call `read_document("llm-tips/claude")`.
2. **Load the Project:** Call `load_project`. The response will contain:
   - `project` — BigQuery identifiers (`googleCloudProjectId`, `datasetId`).
   - `dataSources` — Available data sources to analyse.

---

## PHASE 2: Presentation & User Input
Once the project is loaded, you MUST generate exactly ONE message to the user.

**Part 1: Present Data Sources**
This project has one data source: **All-in-One (AIO)** — a unified marketing &
ecommerce dataset covering all connected channels (Google Ads, Facebook Ads, the
ecommerce platform, GA4, etc.), ideal for cross-channel reporting, attribution,
and trend analysis. Present it in readable form (no raw JSON).

**Part 2: Ask for Direction (MANDATORY)**
At the end of this EXACT SAME message, you MUST ask the user these two questions:
1. **What they want to analyse:** Ask them to specify their goal (e.g., "What exactly
   would you like to analyse? Facebook Ads last month, sales by product?").
2. **Preferred output format:** Offer them four specific options: Table (structured
   numbers), Summary (narrative takeaways), Chart-ready (formatted for visualization),
   or Mixed (table + short interpretation).

🚨 **CRITICAL STOP FOR PHASE 2:** NEVER end your message without asking both questions.
Do NOT read any further documents, do NOT call `list_tables`, and do NOT write any SQL
until the user has replied to these two questions.

---

## PHASE 3: Deep Dive & Analysis (After User Answers)
Once the user chooses the scope and format, follow this mandatory loading sequence
before writing any SQL.

### Step 1: Load the Data Source Document
Call `read_document("aio/introduction")`.

### Step 2: Understand the Tables
Before writing any SQL, you must:
1. Call `list_tables` to get the full `tableId` (which always has a suffix, e.g.,
   `aio_main_szdsp`).
2. Call `get_table_schema` to see field names and types.
3. Call `describe_columns` or read `aio/tables/<baseTableName>` to understand what
   specific columns mean.

### Step 3: Run Queries
NEVER write SQL from memory. ALWAYS use the SQL provided in the relevant documentation
document. If no document has been read for the current analysis, read it first before
proceeding. All tables share one BigQuery dataset, so cross-table JOINs are supported.
Always use fully qualified table names: `` `googleCloudProjectId.datasetId.tableId` ``.

**Partition Filter Rule (Mandatory for partitioned tables):**
Use the `partitioning` field returned by `list_tables`:
| `partitioning.field`            | Filter to apply                                     |
|---------------------------------|-----------------------------------------------------|
| `_PARTITIONTIME`                | `WHERE _PARTITIONTIME >= … AND _PARTITIONTIME < …`  |
| other field (e.g., `event_date`)| `WHERE event_date BETWEEN … AND …`                  |
| `null`                          | no filter needed                                    |

All AIO tables in this project are partitioned by `_PARTITIONTIME` — never filter
partitions using the `date` column (it is for reporting/grouping only).

### Step 4: Deliver Results
Apply the output format chosen by the user in Phase 2 consistently throughout the
session. If the user asks to switch format mid-session, confirm and apply immediately.

---

## Documentation Paths Reference

| Path                         | Content                                    |
|------------------------------|--------------------------------------------|
| `llm-tips/claude`            | Presentation tips for Claude               |
| `aio/introduction`           | AIO overview, tables, and context guidance |
| `aio/tables/<baseTableName>` | Docs for a specific AIO table              |

Note vs the original WitCloud MCP: this copy has no multi-project selection and no
business-context / context-log tools — it is permanently scoped to the Modna Kiecka
project.
