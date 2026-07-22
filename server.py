"""
Modna Kiecka BigQuery MCP Server
================================
Wierna kopia serwera MCP platformy danych AIO dla JEDNEGO projektu:
hurtownia AIO w BigQuery klienta Modna Kiecka.

Roznice vs oryginalna platforma:
- brak multi-projektowosci (list_projects) — serwer jest przypisany do projektu
  Modna Kiecka; load_project nie przyjmuje argumentow,
- dokumentacja AIO jest wbudowana lokalnie w docs/ (kopia 1:1),
  a sciezki tabel w przykladach SQL sa podmieniane w locie na fizyczne
  nazwy z sufiksem projektu,
- brak business contexts / context log (funkcje platformy zrodlowej).

Konfiguracja przez zmienne srodowiskowe:
  GOOGLE_APPLICATION_CREDENTIALS  sciezka do klucza JSON service account
  BQ_MAX_BYTES_BILLED             limit skanu na zapytanie (domyslnie 4 GB)
"""

import json
import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

GCP_PROJECT_ID = "bq-modnakiecka"
DATASET_ID = "witcloud_qfmdjgmqib6ghnpoimik"
AIO_SUFFIX = "_szdsp"
MAX_BYTES_BILLED = int(os.environ.get("BQ_MAX_BYTES_BILLED", str(4 * 1024**3)))
DOCS_DIR = Path(__file__).parent / "docs"

# Nazwy logiczne uzywane w dokumentacji AIO -> fizyczne tabele w BQ.
# Dokumentacja historycznie uzywa nazw bez "4" i z "orders_products".
DOC_TABLE_MAP = {
    "aio_ad_systems": "aio_ad_systems" + AIO_SUFFIX,
    "aio_ecommerce_orders": "aio_ecommerce_orders" + AIO_SUFFIX,
    "aio_ecommerce_orders_products": "aio_ecommerce_order_products" + AIO_SUFFIX,
    "aio_ecommerce_order_products": "aio_ecommerce_order_products" + AIO_SUFFIX,
    "aio_ga_sessions": "aio_ga4_sessions" + AIO_SUFFIX,
    "aio_ga4_sessions": "aio_ga4_sessions" + AIO_SUFFIX,
    "aio_ga_orders": "aio_ga4_orders" + AIO_SUFFIX,
    "aio_ga4_orders": "aio_ga4_orders" + AIO_SUFFIX,
    "aio_ga_products": "aio_ga4_products" + AIO_SUFFIX,
    "aio_ga4_products": "aio_ga4_products" + AIO_SUFFIX,
    "aio_ga_attribution_paths": "aio_ga4_attribution_paths" + AIO_SUFFIX,
    "aio_ga4_attribution_paths": "aio_ga4_attribution_paths" + AIO_SUFFIX,
    "aio_ga_attribution_summary": "aio_ga4_attribution_summary" + AIO_SUFFIX,
    "aio_ga4_attribution_summary": "aio_ga4_attribution_summary" + AIO_SUFFIX,
    "aio_main": "aio_main" + AIO_SUFFIX,
    "aio_search_console": "aio_search_console" + AIO_SUFFIX,
}

mcp = FastMCP("modnakiecka-bq")

_bq_client = None


def _client():
    global _bq_client
    if _bq_client is None:
        from google.cloud import bigquery
        _bq_client = bigquery.Client(project=GCP_PROJECT_ID)
    return _bq_client


_FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|CREATE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|CALL|EXPORT)\b",
    re.IGNORECASE,
)
_DOC_PATH_RE = re.compile(r"witcloud_\{[^}]+\}\.(aio_[a-z0-9_]+)")


def _strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    return sql.strip()


def _localize_doc(content: str) -> str:
    """Podmienia placeholdery `witcloud_{project-id}.aio_x` z dokumentacji AIO
    na pelne fizyczne sciezki tego projektu."""

    def repl(m):
        logical = m.group(1)
        physical = DOC_TABLE_MAP.get(logical, logical + AIO_SUFFIX)
        return f"{GCP_PROJECT_ID}.{DATASET_ID}.{physical}"

    return _DOC_PATH_RE.sub(repl, content)


def _base_table_name(table_id: str) -> str | None:
    if table_id.endswith(AIO_SUFFIX):
        return table_id[: -len(AIO_SUFFIX)]
    return None


@mcp.tool()
def load_project() -> str:
    """Call this tool first. Loads the Modna Kiecka project. Returns BigQuery
    identifiers (googleCloudProjectId, datasetId), available data sources and
    documentation pointers. REQUIRED: immediately after calling this tool, call
    read_document with slug "introduction" — that document contains all
    instructions on how to guide the user through the session.
    For any GA4 analysis, also read "ga4/introduction" — the raw GA4 export has a
    permanent 23-day hole (2026-06-16..2026-07-08) that must never be reported as
    a traffic drop."""
    return json.dumps(
        {
            "project": {
                "name": "Modna Kiecka",
                "googleCloudProjectId": GCP_PROJECT_ID,
                "datasetId": DATASET_ID,
                "aioId": AIO_SUFFIX.lstrip("_"),
            },
            "businessContexts": [],
            "dataSources": [
                {
                    "id": "aio",
                    "kind": "aio",
                    "name": "All-in-One",
                    "summary": "Unified marketing & ecommerce data from connected sources.",
                    "rootDocumentPath": "aio/introduction",
                    "tablesCount": 10,
                }
            ],
            "nextStep": 'Call read_document with slug exactly "introduction" for full guidance on how to proceed.',
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def list_tables(search: str = "", dataSourceId: str = "") -> str:
    """List BigQuery tables in the project dataset with classification (which
    dataSource each table belongs to). Tables that cannot be classified (no AIO
    suffix) are hidden. Use this BEFORE run_query to discover the full tableId
    (which always includes a suffix) and partitioning info. Optional
    case-insensitive substring filter via `search`."""
    tables = []
    for t in _client().list_tables(f"{GCP_PROJECT_ID}.{DATASET_ID}"):
        base = _base_table_name(t.table_id)
        if base is None:
            continue  # nieklasyfikowane tabele sa ukrywane (zgodnie z modelem AIO)
        full = _client().get_table(f"{GCP_PROJECT_ID}.{DATASET_ID}.{t.table_id}")
        partitioning = None
        if full.time_partitioning:
            partitioning = {
                "type": "TIME",
                "field": full.time_partitioning.field or "_PARTITIONTIME",
            }
        tables.append(
            {
                "tableId": t.table_id,
                "baseTableName": base,
                "dataSourceId": "aio",
                "source": "aio",
                "partitioning": partitioning,
                "documentPath": f"aio/tables/{base}",
            }
        )

    if dataSourceId:
        tables = [x for x in tables if x["dataSourceId"] == dataSourceId]
    if search:
        s = search.lower()
        tables = [
            x for x in tables
            if s in x["tableId"].lower() or s in x["baseTableName"].lower()
        ]

    return json.dumps(
        {
            "googleCloudProjectId": GCP_PROJECT_ID,
            "datasetId": DATASET_ID,
            "tables": sorted(tables, key=lambda x: x["tableId"]),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def get_table_schema(tableId: str) -> str:
    """Return the BigQuery schema (fields, types, modes) for a specific tableId.
    Use the full tableId returned by list_tables (with suffix). Field descriptions
    are NOT included here to keep responses lean — call describe_columns for the
    columns you actually want to understand."""
    table = _client().get_table(f"{GCP_PROJECT_ID}.{DATASET_ID}.{tableId}")

    def field_to_dict(f):
        d = {"name": f.name, "type": f.field_type, "mode": f.mode}
        if f.field_type == "RECORD":
            d["fields"] = [field_to_dict(sf) for sf in f.fields]
        return d

    return json.dumps(
        {
            "table": f"{GCP_PROJECT_ID}.{DATASET_ID}.{tableId}",
            "num_rows": table.num_rows,
            "partitioning": str(table.time_partitioning) if table.time_partitioning else None,
            "schema": [field_to_dict(f) for f in table.schema],
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def describe_columns(tableId: str, columns: list[str] | None = None) -> str:
    """Return business descriptions for specific columns of a table. Use this
    AFTER get_table_schema when you need to understand what columns mean. Always
    pass only the columns you actually need. If BigQuery metadata has no
    description, check the table documentation (read_document
    'aio/tables/<baseTableName>') which contains full business definitions."""
    table = _client().get_table(f"{GCP_PROJECT_ID}.{DATASET_ID}.{tableId}")
    wanted = {c.lower() for c in columns} if columns else None
    out = []
    for f in table.schema:
        if wanted and f.name.lower() not in wanted:
            continue
        out.append({"name": f.name, "type": f.field_type, "description": f.description or None})
    return json.dumps({"table": tableId, "columns": out}, ensure_ascii=False, indent=2)


@mcp.tool()
def run_query(query: str, maxResults: int = 1000) -> str:
    """Execute a SELECT query against the project BigQuery dataset.
    PREREQUISITES: call list_tables and (when needed) get_table_schema /
    read_document for any table you query. RULES:
    - Use fully qualified names: `bq-modnakiecka.witcloud_qfmdjgmqib6ghnpoimik.tableId`
      (the full suffixed tableId from list_tables)
    - ALWAYS include a partition filter for any partitioned table to keep scans
      cheap. AIO tables use ingestion-time partitioning — filter on
      `_PARTITIONTIME` (or `_PARTITIONDATE`), NOT on the `date` column.
    - Only SELECT queries are allowed; DML keywords are rejected
    - Cross-table JOIN is supported because everything lives in one dataset
    - maxResults: default 1000, max 10000

    GA4 datasets (outside the AIO dataset, reachable only through this tool —
    list_tables/get_table_schema/describe_columns do NOT see them):
    - `bq-modnakiecka.analytics_291537403.events_*` — raw events, date-sharded,
      filter with `_TABLE_SUFFIX`. 🚨 PERMANENT HOLE 2026-06-16..2026-07-08
      (connector reconnect). NEVER report it as a traffic drop — exclude it with
      `AND _TABLE_SUFFIX NOT BETWEEN '20260616' AND '20260708'`, or take that
      window from GA4_API which does cover it.
    - `bq-modnakiecka.GA4_API.p_ga4_<Report>_291537403` — aggregated GA4 reports,
      NO date column, filter on `_PARTITIONDATE`. Own hole: 2026-03-31..2026-05-31.
    Read `ga4/introduction` before any GA4 analysis."""
    from google.cloud import bigquery

    cleaned = _strip_sql_comments(query)
    first = cleaned.split(None, 1)[0].upper() if cleaned else ""
    if first not in ("SELECT", "WITH"):
        return json.dumps({"error": "Dozwolone sa wylacznie zapytania SELECT/WITH."})
    if _FORBIDDEN_SQL.search(cleaned):
        return json.dumps({"error": "Zapytanie zawiera niedozwolone slowo kluczowe DML/DDL."})

    maxResults = min(max(1, maxResults), 10000)
    job_config = bigquery.QueryJobConfig(maximum_bytes_billed=MAX_BYTES_BILLED)
    try:
        job = _client().query(query, job_config=job_config)
        rows = [dict(r) for r in job.result(max_results=maxResults)]
    except Exception as e:  # noqa: BLE001 — blad BQ zwracamy modelowi
        return json.dumps({"error": str(e)}, ensure_ascii=False)

    return json.dumps(
        {
            "rows": rows,
            "row_count": len(rows),
            "total_bytes_processed": job.total_bytes_processed,
            "gb_processed": round((job.total_bytes_processed or 0) / 1024**3, 3),
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    )


@mcp.tool()
def list_documents(search: str = "", slugPrefix: str = "") -> str:
    """Generic listing of project documentation. Returns summaries (no content)
    so it is cheap on tokens. Filter by slug prefix or free-text search. Slugs
    are path-like, e.g. 'aio/tables/aio_ad_systems'."""
    out = []
    for p in sorted(DOCS_DIR.rglob("*.md")):
        slug = p.relative_to(DOCS_DIR).with_suffix("").as_posix()
        first_line = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        out.append({"slug": slug, "title": first_line})
    if slugPrefix:
        out = [o for o in out if o["slug"].startswith(slugPrefix)]
    if search:
        s = search.lower()
        out = [o for o in out if s in o["slug"].lower() or s in o["title"].lower()]
    return json.dumps({"count": len(out), "documents": out}, ensure_ascii=False, indent=2)


@mcp.tool()
def read_document(slug: str) -> str:
    """Read the full markdown content of a document by its slug. Slugs are
    path-like, e.g. 'aio/tables/aio_ad_systems'. Use list_documents to discover
    slugs first. SQL examples in the docs are already localized to this project's
    fully-qualified physical table names."""
    safe = slug.replace("\\", "/").strip("/")
    if ".." in safe.split("/"):
        return json.dumps({"error": "Nieprawidlowy slug."})
    path = (DOCS_DIR / safe).with_suffix(".md")
    if not path.exists():
        available = [
            p.relative_to(DOCS_DIR).with_suffix("").as_posix()
            for p in sorted(DOCS_DIR.rglob("*.md"))
        ]
        return json.dumps(
            {"found": False, "slug": slug, "available": available}, ensure_ascii=False
        )
    return _localize_doc(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    mcp.run()
