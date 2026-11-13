# Hurtownia danych Modna Kiecka - zasady pracy dla Claude

Ten plik leży w folderze roboczym pracownika (`~/ModnaKiecka/CLAUDE.md`). Claude Code czyta go na starcie
każdej sesji uruchomionej w tym folderze. Kopia wzorcowa: repo `modnakiecka-bq-mcp`, plik `pracownicy/CLAUDE.md`.

## Kim jest użytkownik i jak z nim rozmawiać

- Pracownik Modnej Kiecki, zwykle bez doświadczenia w SQL i BigQuery. Mów po polsku, prosto, bez żargonu.
  Gdy używasz pojęcia (MER, przychód brutto, partycja), wyjaśnij je jednym zdaniem.
- Zanim policzysz coś nowego, powiedz w 1-2 zdaniach, skąd weźmiesz dane i za jaki okres.
- Wynik podawaj z okresem, źródłem i zastrzeżeniami (np. „ostatnie dni mogą jeszcze się zmienić”).
- Jeśli instalacja nie jest zakończona (brak serwera `modnakiecka-bq` w `/mcp`), wróć do instrukcji
  `~/ModnaKiecka/modnakiecka-bq-mcp/INSTALACJA_PRACOWNICY.md` (gdy jej nie ma - pobierz ją poleceniem
  `curl -fsSL https://raw.githubusercontent.com/andrzejczyk-adrian/modnakiecka-bq-mcp/main/INSTALACJA_PRACOWNICY.md -o INSTALACJA_PRACOWNICY.md`
  i przeczytaj w całości).

## Dostęp

- Serwer MCP `modnakiecka-bq` (narzędzia: `load_project`, `list_tables`, `get_table_schema`, `describe_columns`,
  `run_query`, `list_documents`, `read_document`). Tylko odczyt (SELECT/WITH), maks. 4 GB skanu na zapytanie.
- Projekt Google Cloud: `bq-modnakiecka`, region EU. Konto serwisowe pracownika: `modna-kiecka-N` (tylko odczyt).
- **Plik klucza `~/.modnakiecka/modna-kiecka-N.json` to sekret.** Nigdy go nie czytaj, nie wyświetlaj, nie przeszukuj
  (Read, Grep, cat, type) i nie kopiuj. Do danych używaj serwera MCP albo skryptów z `modnakiecka-bq-mcp/pracownicy/`,
  które dostają tylko ścieżkę do klucza.
- `run_query` przyjmuje pełne nazwy tabel z dowolnego zbioru projektu, np.
  `bq-modnakiecka.zamowieniamodnakiecka.orders` - nie tylko tabele z `list_tables`.

## Źródła prawdy - z czego liczyć (to ma pierwszeństwo przed dokumentami serwera MCP)

Dokument `read_document("introduction")` serwera MCP opisuje procedurę (fazy PHASE 1-3, najpierw pytania,
SQL tylko według dokumentów) i tabele `aio_*` jako główne. W tym folderze ta procedura nie obowiązuje -
obowiązuje ten plik i zapytania wzorcowe.

| Co liczysz | Źródło | Zasada |
|---|---|---|
| Zamówienia, przychód, średnia wartość zamówienia | `zamowieniamodnakiecka.orders` (ERP) | zawsze `order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')` - drugi status to nieopłacone przelewy (ok. 4-5% świeżych zamówień), które sklep anuluje po ok. 14 dniach; przychód brutto = `total_revenue_incl_tax` (produkty po rabacie + dostawa, z VAT, przed zwrotami); dzień = `DATE(order_date, 'Europe/Warsaw')` |
| Kanał sprzedaży | `orders.order_source_system` | `'Shoper'` = www, `'Sklep'` = **aplikacja mobilna** (nie sklep stacjonarny!), `'Biuro'` = biuro/telefon |
| Sprzedane sztuki i produkty | `zamowieniamodnakiecka.order_products` + `orders` (status) | model = pierwsza liczba z `product_code` (`14212` z `14212 (288) A#42`); wartość pozycji `quantity * unit_price_incl_tax` jest przed rabatem zamówienia |
| Koszt reklam Meta i Google Ads | `analityka.aio_products` | suma `cost` = pełny koszt kont (z konstrukcji tabeli; sprawdzone 13.11.2026 co do grosza); `platform` = `meta` / `google_ads`; `id_level` mówi, czy znamy kolor (`wariant`), tylko model (`model`), czy nic (`not set`); koszt za wczoraj jest po ok. 8:00 (latem 9:00) |
| MER (efektywność marketingu) | przychód brutto ERP / koszt z `aio_products` | tylko Meta + Google - innych kanałów płatnych hurtownia nie ma |
| Ruch na stronie, źródła wejść (GA4) | `analytics_291537403.events_*` (surowy eksport) | zawsze `_TABLE_SUFFIX BETWEEN 'RRRRMMDD' AND 'RRRRMMDD'`; pomijaj ostatnie 3 dni; to analiza zaawansowana - najpierw zapytaj o cel |

Gotowe, sprawdzone zapytania: `modnakiecka-bq-mcp/pracownicy/zapytania_wzorcowe.sql` (P1-P7). Zaczynaj od nich.

## Czego NIE robić (każdy punkt to błąd, który już się zdarzył)

1. **Nie licz sprzedaży ani ROAS z tabel `aio_*`** (`aio_ecommerce_orders`, `aio_main` itp. z listy `list_tables`).
   Od 03.08.2026 w tabelach sprzedaży (`aio_ecommerce_*`, `aio_main`) nie ma zamówień z aplikacji (duża część
   sprzedaży), a `aio_ga4_orders` ma je tylko częściowo, z GA4; 03.07-02.08.2026 każde zamówienie jest dwa razy,
   a przychód jest przed rabatem. Dokumenty serwera MCP (`read_document`) opisują te tabele jako główne -
   do sprzedaży i ROAS i tak używaj ERP.
2. **Nie licz zamówień z GA4** (zdarzenia `purchase`, `złożenie_zamówienia`) - GA4 nie widzi wszystkich zamówień.
3. **Nie raportuj dziur w danych jako spadków.** GA4 (surowy eksport) nie ma danych 16.06-08.07.2026, a 09.07, 10.07
   i 14.07 są prawie puste - pełne dane od 15.07.2026. Historia reklam zaczyna się 23.06.2025. ERP jest kompletny
   od 07.03.2024.
4. **Nie oceniaj ostatnich dni jak dni zamkniętych:** koszt reklam za wczoraj pojawia się ok. 8:00 (latem 9:00) -
   wcześniej tabela kończy się na przedwczoraj, więc sprawdź, czy każdy dzień ma koszt; Meta i Google poprawiają
   koszt do ok. 30 dni wstecz; GA4 dosyła zdarzenia do 3 dni. Nieopłacone zamówienia wykluczamy od razu (statusy wyżej).
5. **Nie filtruj tabel AIO po kolumnie `date`** - tylko `_PARTITIONTIME`. Tabela `analityka.aio_products` jest
   wyjątkiem (partycje po `date`, filtr po `date` jest poprawny).
6. **Nie wyciągaj danych osobowych** (e-mail, telefon, adres klienta). Klienta identyfikuje `customer_email_hash`.
   Nie wysyłaj surowych danych poza firmę.
7. **Nie nazywaj dostawcy hurtowni** w raportach - pisz „hurtownia danych”.
8. **Nie pisz SQL z pamięci** do nowych tabel - najpierw `get_table_schema`.

## Raporty

- Zapisuj w `~/ModnaKiecka/raporty/` (jeden plik HTML, wykresy z Chart.js z cdnjs.cloudflare.com, wersja przypięta).
- Każdy raport kończy się sekcją „Skąd dane i na co uważać” (źródła, okres, zastrzeżenia).
- Wnioski tylko z liczb w raporcie - bez zgadywania przyczyn. Przyczynę podawaj jako hipotezę do sprawdzenia.
- Generator pierwszego raportu: `modnakiecka-bq-mcp/pracownicy/pierwszy_raport.py`.
