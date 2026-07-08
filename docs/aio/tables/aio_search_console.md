# Table: Search Console

WIP — dokumentacja tej tabeli w platformie WitBee ma status "work in progress"
(stan identyczny w oryginalnym MCP WitCloud).

Praktyczne uwagi z pracy z tą tabelą:

- Zawiera dane Google Search Console (kliknięcia, wyświetlenia) per query/page/data.
- **Brak kolumny średniej pozycji** — CTR licz ręcznie: `SUM(clicks)/SUM(impressions)`.
- Jak wszystkie tabele AIO: filtruj `_PARTITIONTIME`, nazwa fizyczna z sufiksem
  (`aio_search_console_szdsp`).
- Schemat sprawdź przez `get_table_schema(tableId="aio_search_console_szdsp")`.
