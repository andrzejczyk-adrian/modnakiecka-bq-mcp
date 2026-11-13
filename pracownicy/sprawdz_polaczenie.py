"""Sprawdza dostęp do hurtowni Modna Kiecka kluczem konta serwisowego - bez Claude i bez MCP.

Użycie (z folderu modnakiecka-bq-mcp, Pythonem z .venv):
  macOS:   .venv/bin/python pracownicy/sprawdz_polaczenie.py ~/.modnakiecka/modna-kiecka-1.json
  Windows: .venv\\Scripts\\python.exe pracownicy\\sprawdz_polaczenie.py %USERPROFILE%\\.modnakiecka\\modna-kiecka-1.json

Wypisuje tylko nazwę konta i wyniki testów. NIGDY nie wypisuje zawartości klucza.
Kod wyjścia 0 = wszystko działa, 1 = coś nie działa (opis błędu na ekranie).
"""
import json
import sys
from pathlib import Path

PROJEKT = "bq-modnakiecka"

TESTY = [
    ("Zamówienia z ERP (wczoraj)",
     "SELECT COUNT(*) AS n FROM `bq-modnakiecka.zamowieniamodnakiecka.orders` "
     "WHERE order_status NOT IN ('Anulowane', 'Oczekujące na wpłatę') "
     "AND DATE(order_date, 'Europe/Warsaw') = DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)"),
    ("Koszt reklam Meta + Google (wczoraj)",
     "SELECT ROUND(SUM(cost), 2) AS n FROM `bq-modnakiecka.analityka.aio_products` "
     "WHERE date = DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 1 DAY)"),
    ("Hurtownia reklamowa (tabele AIO)",
     "SELECT COUNT(*) AS n FROM `bq-modnakiecka.witcloud_qfmdjgmqib6ghnpoimik.aio_main_szdsp` "
     "WHERE _PARTITIONTIME >= TIMESTAMP(DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 3 DAY))"),
]


def main():
    if len(sys.argv) != 2:
        print("Podaj ścieżkę do pliku klucza, np. ~/.modnakiecka/modna-kiecka-1.json")
        return 1
    klucz = Path(sys.argv[1]).expanduser()
    if not klucz.is_file():
        print(f"BŁĄD: nie ma pliku {klucz}")
        return 1
    try:
        dane = json.loads(klucz.read_text(encoding="utf-8"))
    except Exception:
        print("BŁĄD: plik klucza nie jest poprawnym JSON-em (uszkodzony albo to nie ten plik)")
        return 1
    if dane.get("type") != "service_account" or dane.get("project_id") != PROJEKT:
        print(f"BŁĄD: to nie jest klucz konta serwisowego projektu {PROJEKT}")
        return 1
    print(f"Konto: {dane.get('client_email')}")

    try:
        from google.cloud import bigquery
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("BŁĄD: brak biblioteki google-cloud-bigquery. Uruchom skrypt Pythonem z .venv "
              "(uv pip install -r requirements.txt)")
        return 1

    klient = bigquery.Client(project=PROJEKT, location="EU",
                             credentials=Credentials.from_service_account_file(str(klucz)))
    bledy = 0
    for opis, sql in TESTY:
        try:
            wynik = list(klient.query(sql, job_config=bigquery.QueryJobConfig(
                maximum_bytes_billed=2 * 10**9)).result())[0]["n"]
            if wynik in (None, 0):
                print(f"  UWAGA {opis}: brak danych za wczoraj - połączenie działa, ale dane mogą być "
                      f"jeszcze ładowane (koszty reklam ok. 8:00, latem ok. 9:00). Spróbuj później.")
            else:
                print(f"  OK   {opis}: {wynik}")
        except Exception as e:  # noqa: BLE001 - pokazujemy użytkownikowi krótki powód
            bledy += 1
            powod = str(e).splitlines()[0][:200]
            print(f"  BŁĄD {opis}: {powod}")
    if bledy:
        print("\nCoś nie działa - patrz sekcja 'Rozwiązywanie problemów' w INSTALACJA_PRACOWNICY.md")
        return 1
    print("\nWszystko działa: klucz jest poprawny i hurtownia odpowiada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
