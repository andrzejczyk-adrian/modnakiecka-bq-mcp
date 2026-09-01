# Table: aio_main

Fundament modelu AIO — kompletne, zunifikowane źródło danych (~230 kolumn), na którym
zbudowane są wszystkie datamarty `aio_*`. **Brak oficjalnej dokumentacji dla tej
tabeli** (stan również w oryginalnej platformie).

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
- 🚨 **Okno zdublowanych zamówień 2026-06-28 … 2026-08-02**: wiersze `Ecommerce`
  występują podwójnie — z `MK shoper` ORAZ z równoległego feedu
  `MK Custom Ecommerce` (te same zamówienia; feed wygaszony na początku sierpnia
  2026). Sumy przychodu/zamówień w tym oknie są ~2× zawyżone bez filtra
  `data_source_name = 'MK shoper'` (albo deduplikacji po `ecomm_order_id`).
  Szczegóły: `aio/tables/aio_ecommerce_orders`.
- `report_currency` = waluta zunifikowana; pola `original_*` = waluta źródła.
- Do typowych analiz preferuj dedykowane datamarty (`aio_ad_systems`,
  `aio_ecommerce_orders`, `aio_ga4_sessions`...) — `aio_main` tylko gdy potrzebujesz
  przekroju niedostępnego w datamartach.
