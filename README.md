# modnakiecka-bq-mcp

Serwer MCP (Model Context Protocol) łączący **Claude Code** z hurtownią danych
**WitBee AIO w BigQuery** klienta **Modna Kiecka** — projekt GCP **`bq-modnakiecka`**,
dataset `witcloud_qfmdjgmqib6ghnpoimik`.

To **wierna kopia MCP WitBee/WitCloud** zawężona do jednego projektu: te same
narzędzia, ten sam przepływ pracy (load_project → introduction → list_tables →
schema → SQL) i wbudowana kopia oficjalnej dokumentacji AIO. Klient nie potrzebuje
dostępu do platformy WitBee — wystarczy dostęp do własnego BigQuery.

## Możliwości (narzędzia MCP — 1:1 z WitBee)

| Narzędzie | Opis |
|---|---|
| `load_project` | identyfikatory BQ, źródła danych — punkt startowy sesji |
| `list_tables` | 10 tabel AIO z klasyfikacją, partycjonowaniem i wskaźnikiem dokumentacji |
| `get_table_schema` | schemat tabeli (pola, typy, tryby) |
| `describe_columns` | opisy biznesowe wybranych kolumn |
| `run_query` | **wyłącznie SELECT/WITH**, limit skanu 4 GB/zapytanie, max 10 000 wierszy |
| `list_documents` / `read_document` | wbudowana dokumentacja AIO (kopia z WitBee) |

Różnice vs oryginał WitBee: brak wyboru projektu (serwer na stałe wskazuje Modną
Kieckę), brak business contexts / context log (to funkcje platformy WitBee).
Przykłady SQL w dokumentacji są automatycznie lokalizowane do pełnych fizycznych
nazw tabel (`bq-modnakiecka.witcloud_qfmdjgmqib6ghnpoimik.aio_*_szdsp`).

## Tabele AIO w projekcie

`aio_main` (fundament, ~230 kol.), `aio_ad_systems`, `aio_ecommerce_orders`,
`aio_ecommerce_order_products`, `aio_ga4_sessions`, `aio_ga4_orders`,
`aio_ga4_products`, `aio_ga4_attribution_paths`, `aio_ga4_attribution_summary`,
`aio_search_console` — wszystkie partycjonowane po `_PARTITIONTIME`, fizyczne nazwy
z sufiksem `_szdsp`.

## Bezpieczeństwo

- Tylko odczyt: DML/DDL odrzucane po stronie serwera.
- `maximum_bytes_billed` = 4 GB na zapytanie (konfigurowalne przez `BQ_MAX_BYTES_BILLED`).
- Uwierzytelnianie: klucz JSON service account z rolami **BigQuery Data Viewer** +
  **BigQuery Job User** (nic więcej). Klucz nie jest częścią repo (`.gitignore`).

## Szybki start

Pełna instrukcja krok po kroku (nowy komputer, od zera): **[INSTALACJA.md](INSTALACJA.md)**.

```bash
git clone https://github.com/andrzejczyk-adrian/modnakiecka-bq-mcp.git
cd modnakiecka-bq-mcp
pip install -r requirements.txt
# wgraj otrzymany klucz jako sa-key.json do tego folderu
claude          # uruchom Claude Code w tym folderze i zatwierdź serwer MCP z .mcp.json
```

Test w Claude Code: `Załaduj projekt Modna Kiecka i pokaż dzienne przychody vs koszty marketingu z ostatnich 14 dni.`

## Struktura

```
server.py            serwer MCP (Python, FastMCP)
.mcp.json            rejestracja serwera dla Claude Code (project scope)
requirements.txt     zależności
docs/                kopia dokumentacji WitBee (master guide, AIO, 10 tabel)
  introduction.md    przewodnik sesji (fazy 1-3, reguły SQL)
  aio/...            dokumentacja modelu AIO i tabel
INSTALACJA.md        instrukcja instalacji od zera + prompt do wklejenia
```
