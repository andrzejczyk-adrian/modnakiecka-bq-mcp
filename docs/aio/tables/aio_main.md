# Table: aio_main

Fundament modelu AIO — kompletne, zunifikowane źródło danych (~230 kolumn), na którym
zbudowane są wszystkie datamarty `aio_*`. **Brak oficjalnej dokumentacji WitBee dla tej
tabeli** (stan również w oryginalnym MCP WitCloud).

Jak z niej korzystać:

1. `get_table_schema(tableId="aio_main_szdsp")` — pełna lista pól i typów.
2. `describe_columns` — opisy z metadanych BQ (mogą być puste).
3. Konwencje nazewnicze są spójne z datamartami: pola `ga_*` (GA4), `ad_system_*`
   (systemy reklamowe), `data_source_*` (klasyfikacja źródła), `item_*` / `order_*`
   (e-commerce), `channel_grouping1..5` (własne grupowania).

Żelazne zasady (jak we wszystkich tabelach AIO):

- **UNION long-format**: wiersze `User Behaviour` / `Ecommerce` / `Marketplace` vs
  `Ad Systems` (koszty). Metryki łącz przez GROUP BY + COALESCE po wymiarach,
  **nie przez JOIN** (ryzyko fanout).
- **Zawsze filtruj `_PARTITIONTIME`**, nie kolumnę `date`.
- `report_currency` = waluta zunifikowana; pola `original_*` = waluta źródła.
- Do typowych analiz preferuj dedykowane datamarty (`aio_ad_systems`,
  `aio_ecommerce_orders`, `aio_ga4_sessions`...) — `aio_main` tylko gdy potrzebujesz
  przekroju niedostępnego w datamartach.
