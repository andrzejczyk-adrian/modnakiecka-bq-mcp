"""Pierwszy raport: sprzedaż (ERP) i koszt reklam (Meta + Google) - plik HTML z wykresami, tabelą i wnioskami.

Użycie (z folderu modnakiecka-bq-mcp, Pythonem z .venv):
  macOS:   .venv/bin/python pracownicy/pierwszy_raport.py ~/.modnakiecka/modna-kiecka-1.json
  Windows: .venv\\Scripts\\python.exe pracownicy\\pierwszy_raport.py %USERPROFILE%\\.modnakiecka\\modna-kiecka-1.json
Opcjonalnie: --folder <gdzie zapisać> (domyślnie ~/ModnaKiecka/raporty), --tygodnie N (domyślnie 8).

Źródła (sprawdzone, te same co w pracownicy/zapytania_wzorcowe.sql):
  - przychód i zamówienia: ERP `zamowieniamodnakiecka.orders`, bez statusów 'Anulowane' i 'Oczekujące na wpłatę'
    (nieopłacone przelewy, sklep anuluje je po ok. 14 dniach), dzień w czasie warszawskim;
  - koszt reklam: `analityka.aio_products` (suma = pełny koszt kont Meta i Google Ads, zgodne co do grosza - sprawdzone 13.11.2026).
Uruchamiaj po ok. 8:00 (latem 9:00) - wcześniej nie ma jeszcze kosztu reklam za wczoraj.
Plik raportu zawiera dane firmy - nie wysyłaj go poza firmę i nie wrzucaj do publicznych miejsc.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

PROJEKT = "bq-modnakiecka"
CHART_JS = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"

SQL_DZIENNIE = """
WITH okno AS (
  SELECT DATE_SUB(DATE_TRUNC(CURRENT_DATE('Europe/Warsaw'), ISOWEEK), INTERVAL @tygodnie WEEK) AS d0,
         DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY) AS d1),
s AS (
  SELECT DATE(order_date, 'Europe/Warsaw') AS dzien,
    COUNT(*) AS zamowienia,
    SUM(total_revenue_incl_tax) AS przychod,
    SUM(IF(order_source_system = 'Shoper', total_revenue_incl_tax, 0)) AS przychod_www,
    SUM(IF(order_source_system = 'Sklep', total_revenue_incl_tax, 0)) AS przychod_aplikacja,
    SUM(IF(order_source_system = 'Biuro', total_revenue_incl_tax, 0)) AS przychod_biuro,
    COUNTIF(order_source_system = 'Sklep') AS zam_aplikacja
  FROM `bq-modnakiecka.zamowieniamodnakiecka.orders`, okno
  WHERE order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę') AND DATE(order_date, 'Europe/Warsaw') BETWEEN okno.d0 AND okno.d1
  GROUP BY 1),
k AS (
  SELECT date AS dzien, SUM(IF(platform = 'meta', cost, 0)) AS koszt_meta,
    SUM(IF(platform = 'google_ads', cost, 0)) AS koszt_google
  FROM `bq-modnakiecka.analityka.aio_products`, okno
  WHERE date BETWEEN okno.d0 AND okno.d1
  GROUP BY 1)
SELECT s.*, IFNULL(k.koszt_meta, 0) AS koszt_meta, IFNULL(k.koszt_google, 0) AS koszt_google
FROM s LEFT JOIN k USING (dzien)
ORDER BY dzien
"""


def pobierz(klucz, tygodnie):
    from google.cloud import bigquery
    from google.oauth2.service_account import Credentials
    klient = bigquery.Client(project=PROJEKT, location="EU",
                             credentials=Credentials.from_service_account_file(str(klucz)))
    cfg = bigquery.QueryJobConfig(maximum_bytes_billed=4 * 10**9, query_parameters=[
        bigquery.ScalarQueryParameter("tygodnie", "INT64", tygodnie)])
    wiersze = []
    for r in klient.query(SQL_DZIENNIE, job_config=cfg).result():
        d = {k: (float(v) if k != "dzien" and v is not None else v) for k, v in dict(r).items()}
        d["dzien"] = r["dzien"]
        wiersze.append(d)
    return wiersze


def liczba(x, miejsca=0):
    """Polski zapis liczby: spacja tysięcy, przecinek dziesiętny."""
    t = f"{x:,.{miejsca}f}"
    return t.replace(",", " ").replace(".", ",")


def zl(x):
    return liczba(x) + " zł"


def proc(x):
    return ("+" if x >= 0 else "") + liczba(x, 1) + "%"


def tygodniowo(dni):
    tyg = {}
    for d in dni:
        t = d["dzien"] - dt.timedelta(days=d["dzien"].weekday())
        w = tyg.setdefault(t, {"tydzien": t, "dni": 0, "zamowienia": 0, "przychod": 0, "zam_aplikacja": 0,
                               "koszt_meta": 0, "koszt_google": 0})
        w["dni"] += 1
        for k in ("zamowienia", "przychod", "zam_aplikacja", "koszt_meta", "koszt_google"):
            w[k] += d[k]
    pelne = [w for w in tyg.values() if w["dni"] == 7]
    for w in pelne:
        w["koszt"] = w["koszt_meta"] + w["koszt_google"]
        w["mer"] = w["przychod"] / w["koszt"] if w["koszt"] else None
        w["aov"] = w["przychod"] / w["zamowienia"] if w["zamowienia"] else None
        w["udzial_app"] = 100 * w["zam_aplikacja"] / w["zamowienia"] if w["zamowienia"] else None
    return sorted(pelne, key=lambda w: w["tydzien"])


def wnioski(dni, tyg):
    out = []
    if len(tyg) >= 2:
        a, b = tyg[-1], tyg[-2]
        okres = f"{a['tydzien']:%d.%m}-{a['tydzien'] + dt.timedelta(days=6):%d.%m}"
        out.append(f"Ostatni pełny tydzień ({okres}): przychód {zl(a['przychod'])} "
                   f"({proc(100 * (a['przychod'] / b['przychod'] - 1))} tydzień do tygodnia), "
                   f"{liczba(a['zamowienia'])} zamówień ({proc(100 * (a['zamowienia'] / b['zamowienia'] - 1))}).")
    if len(tyg) >= 5:
        a = tyg[-1]
        poprz = tyg[-5:-1]
        mer4 = sum(w["przychod"] for w in poprz) / sum(w["koszt"] for w in poprz)
        k4 = sum(w["koszt"] for w in poprz) / 4
        out.append(f"MER (przychód / koszt Meta + Google) w ostatnim tygodniu: {liczba(a['mer'], 2)} wobec "
                   f"{liczba(mer4, 2)} średnio w 4 wcześniejszych tygodniach; koszt reklam {zl(a['koszt'])} "
                   f"({proc(100 * (a['koszt'] / k4 - 1))} wobec średniej).")
    if len(tyg) >= 2:
        out.append(f"Aplikacja: {liczba(tyg[-1]['udzial_app'], 1)}% zamówień w ostatnim tygodniu "
                   f"(w pierwszym tygodniu okresu {liczba(tyg[0]['udzial_app'], 1)}%).")
    if dni:
        top = max(dni, key=lambda d: d["przychod"])
        out.append(f"Najlepszy dzień okresu: {top['dzien']:%d.%m.%Y} - {zl(top['przychod'])} "
                   f"z {liczba(top['zamowienia'])} zamówień.")
    if len(tyg) >= 4:
        ost = tyg[-4:]
        aov = sum(w["przychod"] for w in ost) / sum(w["zamowienia"] for w in ost)
        out.append(f"Średnia wartość zamówienia w ostatnich 4 tygodniach: {liczba(aov, 2)} zł.")
    return out


def html(dni, tyg, wn, tygodnie):
    etykiety = [d["dzien"].strftime("%d.%m") for d in dni]

    def seria(k):
        return [round(d[k], 2) for d in dni]

    mer_d = [round(d["przychod"] / (d["koszt_meta"] + d["koszt_google"]), 2)
             if (d["koszt_meta"] + d["koszt_google"]) else None for d in dni]
    mer7 = []
    for i in range(len(dni)):
        okno = dni[max(0, i - 6): i + 1]
        k = sum(x["koszt_meta"] + x["koszt_google"] for x in okno)
        mer7.append(round(sum(x["przychod"] for x in okno) / k, 2) if k and len(okno) == 7 else None)
    wykresy = {
        "przychod": {"labels": etykiety, "datasets": [
            {"label": "www", "data": seria("przychod_www")},
            {"label": "aplikacja", "data": seria("przychod_aplikacja")},
            {"label": "biuro", "data": seria("przychod_biuro")}]},
        "koszt": {"labels": etykiety, "datasets": [
            {"label": "Meta", "data": seria("koszt_meta")},
            {"label": "Google Ads", "data": seria("koszt_google")}]},
        "mer": {"labels": etykiety, "datasets": [
            {"label": "MER dzienny", "data": mer_d},
            {"label": "MER 7 dni (średnia krocząca)", "data": mer7}]},
    }
    wiersze_tab = "".join(
        f"<tr><td>{w['tydzien']:%d.%m}-{w['tydzien'] + dt.timedelta(days=6):%d.%m}</td>"
        f"<td>{liczba(w['zamowienia'])}</td><td>{liczba(w['przychod'])}</td><td>{liczba(w['udzial_app'], 1)}%</td>"
        f"<td>{liczba(w['aov'], 2)}</td><td>{liczba(w['koszt_meta'])}</td><td>{liczba(w['koszt_google'])}</td>"
        f"<td><b>{liczba(w['mer'], 2)}</b></td></tr>" for w in tyg)
    lista_wn = "".join(f"<li>{x}</li>" for x in wn)
    dzis = dt.date.today()
    return f"""<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sprzedaż i koszt reklam - {dzis:%d.%m.%Y}</title>
<script src="{CHART_JS}"></script>
<style>
 body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background: #f6f7f9; color: #1d2433; }}
 main {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }}
 h1 {{ font-size: 24px; margin: 0 0 4px; }} .pod {{ color: #5b6475; margin: 0 0 24px; }}
 .karta {{ background: #fff; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
 h2 {{ font-size: 17px; margin: 0 0 12px; }} canvas {{ max-height: 320px; }}
 table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
 th, td {{ padding: 8px 10px; text-align: right; border-bottom: 1px solid #e6e8ec; }}
 th:first-child, td:first-child {{ text-align: left; }} th {{ background: #f0f2f5; }}
 li {{ margin-bottom: 8px; line-height: 1.45; }} .uwagi {{ font-size: 13px; color: #5b6475; }}
</style></head><body><main>
<h1>Sprzedaż i koszt reklam</h1>
<p class="pod">Modna Kiecka · ostatnie {tygodnie} tygodni do {dni[-1]['dzien']:%d.%m.%Y} · wygenerowano {dzis:%d.%m.%Y}</p>
<div class="karta"><h2>Wnioski</h2><ul>{lista_wn}</ul></div>
<div class="karta"><h2>Przychód brutto dziennie (zł)</h2><canvas id="przychod"></canvas></div>
<div class="karta"><h2>Koszt reklam dziennie (zł)</h2><canvas id="koszt"></canvas></div>
<div class="karta"><h2>MER = przychód / koszt Meta + Google</h2><canvas id="mer"></canvas></div>
<div class="karta"><h2>Podsumowanie tygodniowe (pełne tygodnie pon.-niedz.)</h2>
<table><thead><tr><th>Tydzień</th><th>Zamówienia</th><th>Przychód brutto (zł)</th><th>Udział aplikacji</th>
<th>Średnie zamówienie (zł)</th><th>Koszt Meta (zł)</th><th>Koszt Google (zł)</th><th>MER</th></tr></thead>
<tbody>{wiersze_tab}</tbody></table></div>
<div class="karta uwagi"><b>Skąd dane i na co uważać</b><br>
Przychód brutto = wartość zamówień z ERP (produkty po rabacie + dostawa, z VAT), przed zwrotami, bez zamówień anulowanych
i nieopłaconych (status „Oczekujące na wpłatę” - sklep anuluje je po ok. 14 dniach, więc od razu ich nie liczymy).
Koszt = Meta i Google Ads (pełny koszt kont); innych kanałów płatnych hurtownia nie ma, więc MER jest zawyżony względem całego marketingu.
Kanał: www = sklep internetowy, aplikacja = aplikacja mobilna, biuro = zamówienia telefoniczne/biurowe.</div>
</main>
<script>
const dane = {json.dumps(wykresy, ensure_ascii=False)};
const kolory = ["#2f6fdf", "#e0763b", "#7a8599"];
for (const [id, d] of Object.entries(dane)) {{
  d.datasets.forEach((s, i) => Object.assign(s, {{ borderColor: kolory[i], backgroundColor: kolory[i],
    borderWidth: 2, pointRadius: 0, tension: 0.25, spanGaps: true }}));
  new Chart(document.getElementById(id), {{ type: "line", data: d,
    options: {{ responsive: true, interaction: {{ mode: "index", intersect: false }},
      plugins: {{ legend: {{ position: "bottom" }} }},
      scales: {{ y: {{ beginAtZero: id !== "mer", ticks: {{ callback: v => v.toLocaleString("pl-PL") }} }} }} }} }});
}}
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Pierwszy raport HTML: sprzedaż i koszt reklam")
    ap.add_argument("klucz", help="ścieżka do pliku klucza modna-kiecka-N.json")
    ap.add_argument("--folder", default=str(Path.home() / "ModnaKiecka" / "raporty"))
    ap.add_argument("--tygodnie", type=int, default=8)
    a = ap.parse_args()
    klucz = Path(a.klucz).expanduser()
    if not klucz.is_file():
        print(f"BŁĄD: nie ma pliku {klucz}")
        return 1
    dni = pobierz(klucz, a.tygodnie)
    if not dni:
        print("BŁĄD: zapytanie nie zwróciło danych")
        return 1
    braki = [d["dzien"] for d in dni if d["koszt_meta"] + d["koszt_google"] == 0]
    if braki:
        print("UWAGA: brak kosztu reklam za " + ", ".join(f"{x:%d.%m}" for x in braki) + " - tabela kosztów "
              "przelicza się codziennie ok. 8:00 (latem ok. 9:00). Uruchom raport później.")
        return 1
    tyg = tygodniowo(dni)
    folder = Path(a.folder).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    plik = folder / f"raport_sprzedaz_koszty_{dt.date.today():%Y-%m-%d}.html"
    plik.write_text(html(dni, tyg, wnioski(dni, tyg), a.tygodnie), encoding="utf-8")
    print(f"Zapisano raport: {plik}")
    print(f"Dni: {len(dni)}, pełnych tygodni: {len(tyg)}. Otwórz plik w przeglądarce (dwuklik).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
