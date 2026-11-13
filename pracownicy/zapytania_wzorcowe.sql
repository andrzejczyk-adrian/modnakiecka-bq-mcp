-- =====================================================================================
-- Zapytania wzorcowe - hurtownia Modna Kiecka (projekt bq-modnakiecka)
-- Sprawdzone 13.11.2026 kontem pracownika (modna-kiecka-1) i niezależnie innymi źródłami (zgodność 100%).
-- Zamówienia: zawsze bez 'Anulowane' i 'Oczekujące na wpłatę' (nieopłacone przelewy - sklep anuluje je po ok. 14 dniach).
-- Używaj ich jako punktu wyjścia - zmieniaj okres, grupowanie, filtry, ale NIE źródła danych.
-- Wszystkie daty w czasie warszawskim, okres kończy się na wczoraj (dzisiejszy dzień jest niepełny).
-- =====================================================================================

-- P1. Sprzedaż dzienna z ERP: zamówienia i przychód brutto (bez anulowanych i nieopłaconych), www / aplikacja / biuro
SELECT
  DATE(order_date, 'Europe/Warsaw') AS dzien,
  CASE order_source_system WHEN 'Shoper' THEN 'www' WHEN 'Sklep' THEN 'aplikacja' WHEN 'Biuro' THEN 'biuro' ELSE order_source_system END AS kanal,
  COUNT(*) AS zamowienia,
  ROUND(SUM(total_revenue_incl_tax), 2) AS przychod_brutto_zl
FROM `bq-modnakiecka.zamowieniamodnakiecka.orders`
WHERE order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')
  AND DATE(order_date, 'Europe/Warsaw') BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY)
                                            AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)
GROUP BY dzien, kanal
ORDER BY dzien, kanal
;

-- P2. Koszt reklam dziennie: Meta i Google Ads (suma = pełny koszt kont)
SELECT date AS dzien, platform AS platforma, ROUND(SUM(cost), 2) AS koszt_zl
FROM `bq-modnakiecka.analityka.aio_products`
WHERE date BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY)
               AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)
GROUP BY dzien, platforma
ORDER BY dzien, platforma
;

-- P3. MER tygodniowo = przychód brutto ERP / koszt Meta + Google (pełne tygodnie pon-niedz., ostatnie 8)
WITH s AS (
  SELECT DATE_TRUNC(DATE(order_date, 'Europe/Warsaw'), ISOWEEK) AS tydzien,
    COUNT(*) AS zamowienia, SUM(total_revenue_incl_tax) AS przychod,
    COUNTIF(order_source_system = 'Sklep') AS zam_aplikacja
  FROM `bq-modnakiecka.zamowieniamodnakiecka.orders`
  WHERE order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')
    AND DATE(order_date, 'Europe/Warsaw') >= DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Warsaw'), ISOWEEK), INTERVAL 8 WEEK)
    AND DATE(order_date, 'Europe/Warsaw') <  DATE_TRUNC(CURRENT_DATE('Europe/Warsaw'), ISOWEEK)
  GROUP BY 1),
k AS (
  SELECT DATE_TRUNC(date, ISOWEEK) AS tydzien, COUNT(DISTINCT date) AS dni_kosztu, SUM(cost) AS koszt,
    SUM(IF(platform = 'meta', cost, 0)) AS koszt_meta, SUM(IF(platform = 'google_ads', cost, 0)) AS koszt_google
  FROM `bq-modnakiecka.analityka.aio_products`
  WHERE date >= DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Warsaw'), ISOWEEK), INTERVAL 8 WEEK)
    AND date <  DATE_TRUNC(CURRENT_DATE('Europe/Warsaw'), ISOWEEK)
  GROUP BY 1)
SELECT s.tydzien, s.zamowienia, ROUND(s.przychod) AS przychod_brutto_zl,
  ROUND(100 * s.zam_aplikacja / s.zamowienia, 1) AS udzial_aplikacji_proc,
  ROUND(s.przychod / s.zamowienia, 2) AS srednia_wartosc_zamowienia_zl,
  ROUND(k.koszt_meta) AS koszt_meta_zl, ROUND(k.koszt_google) AS koszt_google_zl,
  ROUND(s.przychod / k.koszt, 2) AS mer
FROM s JOIN k USING (tydzien)
WHERE k.dni_kosztu = 7   -- koszt za wczoraj pojawia się ok. 8:00 (latem 9:00), bez kompletu tydzień byłby zaniżony
ORDER BY tydzien
;

-- P4. Średnia wartość zamówienia i liczba sztuk w zamówieniu: www vs aplikacja (ostatnie 28 pełnych dni)
WITH o AS (
  SELECT order_id, order_source_system, total_revenue_incl_tax
  FROM `bq-modnakiecka.zamowieniamodnakiecka.orders`
  WHERE order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')
    AND DATE(order_date, 'Europe/Warsaw') BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 28 DAY)
                                              AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)),
szt AS (SELECT order_id, SUM(quantity) AS sztuki FROM `bq-modnakiecka.zamowieniamodnakiecka.order_products` GROUP BY 1)
SELECT CASE o.order_source_system WHEN 'Shoper' THEN 'www' WHEN 'Sklep' THEN 'aplikacja' WHEN 'Biuro' THEN 'biuro' END AS kanal,
  COUNT(*) AS zamowienia, ROUND(SUM(o.total_revenue_incl_tax)) AS przychod_brutto_zl,
  ROUND(AVG(o.total_revenue_incl_tax), 2) AS srednia_wartosc_zl, ROUND(AVG(szt.sztuki), 2) AS srednio_sztuk
FROM o LEFT JOIN szt USING (order_id)
GROUP BY kanal ORDER BY zamowienia DESC
;

-- P5. Top 10 modeli wg sprzedanych sztuk (ostatnie 30 pełnych dni, bez anulowanych i nieopłaconych), model = pierwsza liczba kodu produktu
WITH op AS (
  SELECT REGEXP_EXTRACT(op.product_code, r'^\s*(\d+)') AS model, op.product_name, op.quantity,
    op.quantity * op.unit_price_incl_tax AS wartosc
  FROM `bq-modnakiecka.zamowieniamodnakiecka.order_products` op
  JOIN `bq-modnakiecka.zamowieniamodnakiecka.orders` o USING (order_id)
  WHERE o.order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')
    AND DATE(o.order_date, 'Europe/Warsaw') BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY)
                                                AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY))
SELECT model,
  ANY_VALUE(TRIM(REGEXP_REPLACE(product_name, r'\s*\d{3,5}-\w{1,4}(-[A-ZŁ]\d?)?\s*$', ''))) AS przykladowa_nazwa,
  SUM(quantity) AS sztuki, ROUND(SUM(wartosc)) AS wartosc_przed_rabatem_zl
FROM op WHERE model IS NOT NULL
GROUP BY model ORDER BY sztuki DESC LIMIT 10
;

-- P6. Top 10 modeli wg kosztu reklam (Meta + Google, ostatnie 30 pełnych dni) i ich sprzedaż z ERP
WITH k AS (
  SELECT sku_model AS model, SUM(cost) AS koszt,
    SUM(IF(platform = 'meta', cost, 0)) AS koszt_meta, SUM(IF(platform = 'google_ads', cost, 0)) AS koszt_google
  FROM `bq-modnakiecka.analityka.aio_products`
  WHERE sku_model != 'not set'
    AND date BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY) AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)
  GROUP BY 1),
s AS (
  SELECT REGEXP_EXTRACT(op.product_code, r'^\s*(\d+)') AS model, SUM(op.quantity) AS sztuki,
    SUM(op.quantity * op.unit_price_incl_tax) AS wartosc
  FROM `bq-modnakiecka.zamowieniamodnakiecka.order_products` op
  JOIN `bq-modnakiecka.zamowieniamodnakiecka.orders` o USING (order_id)
  WHERE o.order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę')
    AND DATE(o.order_date, 'Europe/Warsaw') BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY) AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)
  GROUP BY 1)
SELECT k.model, ROUND(k.koszt) AS koszt_reklam_zl, ROUND(k.koszt_meta) AS meta_zl, ROUND(k.koszt_google) AS google_zl,
  IFNULL(s.sztuki, 0) AS sprzedane_sztuki, ROUND(IFNULL(s.wartosc, 0)) AS wartosc_przed_rabatem_zl,
  ROUND(SAFE_DIVIDE(k.koszt, s.sztuki), 2) AS koszt_reklam_na_sztuke_zl,
  ROUND(100 * SAFE_DIVIDE(k.koszt, s.wartosc), 1) AS koszt_do_wartosci_proc
FROM k LEFT JOIN s USING (model)
ORDER BY k.koszt DESC LIMIT 10
;

-- P7. Do jakiego poziomu produktu znamy koszt reklam (ostatnie 30 pełnych dni): kolor / tylko model / brak produktu
SELECT platform AS platforma,
  CASE id_level WHEN 'wariant' THEN '1. znany kolor (wariant)' WHEN 'model' THEN '2. tylko model' ELSE '3. bez produktu' END AS poziom,
  ROUND(SUM(cost)) AS koszt_zl,
  ROUND(100 * SUM(cost) / SUM(SUM(cost)) OVER (PARTITION BY platform), 1) AS udzial_proc
FROM `bq-modnakiecka.analityka.aio_products`
WHERE date BETWEEN DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 30 DAY) AND DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)
GROUP BY platforma, poziom ORDER BY platforma, poziom
;

