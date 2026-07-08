# Instalacja od zera — nowy komputer + Claude Code + hurtownia Modna Kiecka (MCP)

Instrukcja dla projektu GCP **`bq-modnakiecka`** (hurtownia WitBee AIO w BigQuery).
Czas: ~15 minut. Wymagania wstępne: konto Claude (Pro/Max lub Console) oraz **klucz
service account (`sa-key.json`)** otrzymany od administratora hurtowni.

---

## CZĘŚĆ A — przygotowanie komputera

### Krok 1. Zainstaluj Claude Code

**Windows** (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**macOS / Linux** (Terminal):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Po instalacji uruchom w terminalu `claude` i zaloguj się (otworzy się przeglądarka).

### Krok 2. Zainstaluj Git i Python

- **Git:** https://git-scm.com/downloads (Windows: domyślne opcje instalatora).
- **Python 3.10+:** https://www.python.org/downloads/
  ⚠️ **Windows: zaznacz „Add python.exe to PATH"** na pierwszym ekranie instalatora.

Weryfikacja (nowe okno terminala):

```bash
git --version
python --version
```

### Krok 3. Pobierz projekt i zainstaluj zależności

```bash
git clone https://github.com/andrzejczyk-adrian/modnakiecka-bq-mcp.git
cd modnakiecka-bq-mcp
pip install -r requirements.txt
```

### Krok 4. Wgraj klucz dostępowy

Otrzymany plik klucza zapisz jako **`sa-key.json`** bezpośrednio w folderze
`modnakiecka-bq-mcp` (obok `server.py`).

⚠️ Klucza nie wysyłaj mailem w postaci jawnej, nie commituj do gita (jest w
`.gitignore`), nie udostępniaj osobom trzecim.

### Krok 5. Uruchom Claude Code w folderze projektu

```bash
cd modnakiecka-bq-mcp
claude
```

Claude Code wykryje plik `.mcp.json` i zapyta o zgodę na uruchomienie serwera
**modnakiecka-bq** — zatwierdź. Gotowe.

### Krok 6. Test połączenia

Wpisz w Claude Code:

> Załaduj projekt (load_project), przeczytaj dokument "introduction" i przedstaw mi
> dostępne dane. Potem pokaż dzienne przychody i koszty marketingu z ostatnich 14 dni
> wraz z ROAS.

Jeśli dostaniesz tabelkę z przychodami i kosztami — wszystko działa.

---

## CZĘŚĆ B — prompt do wklejenia w Claude Code (automatyczna instalacja)

Jeżeli masz już zainstalowane Claude Code, Git i Pythona (kroki 1–2), **cała reszta
może zrobić się sama**. Uruchom `claude` w dowolnym folderze roboczym i wklej:

```text
Skonfiguruj mi dostęp do hurtowni danych Modna Kiecka (model WitBee AIO w BigQuery,
projekt GCP bq-modnakiecka) przez MCP:

1. Sklonuj repo https://github.com/andrzejczyk-adrian/modnakiecka-bq-mcp.git do
   bieżącego folderu i wejdź do niego.
2. Zainstaluj zależności: pip install -r requirements.txt (jeśli pip nie działa,
   spróbuj python -m pip).
3. Sprawdź, czy w folderze jest plik sa-key.json. Jeśli go nie ma — zatrzymaj się
   i poproś mnie o wskazanie ścieżki do otrzymanego klucza service account,
   po czym skopiuj go do folderu repo jako sa-key.json.
4. Serwer MCP jest zdefiniowany w .mcp.json (project scope). Dodatkowo zarejestruj go
   globalnie, żeby działał z każdego folderu:
   claude mcp add --scope user modnakiecka-bq --env GOOGLE_APPLICATION_CREDENTIALS=
   <PEŁNA ŚCIEŻKA DO sa-key.json> -- python <PEŁNA ŚCIEŻKA DO server.py>
5. Przetestuj połączenie: wywołaj load_project, przeczytaj dokument "introduction",
   wylistuj tabele (list_tables) i policz dzienne przychody vs koszty marketingu
   z ostatnich 14 dni (aio_ecommerce_orders, filtr _PARTITIONTIME).
6. Na koniec pokaż mi wynik testu i krótką ściągę: 5 przykładowych pytań
   analitycznych, które mogę zadawać o dane Modnej Kiecki (ROAS/ERS, produkty,
   kanały, atrybucja, nowi vs powracający klienci).

Pamiętaj: hurtownia jest tylko do odczytu (SELECT), zawsze filtruj _PARTITIONTIME
(nigdy po kolumnie date), tabele mają sufiks _szdsp.
```

Po ponownym uruchomieniu `claude` serwer **modnakiecka-bq** będzie dostępny w każdej
sesji.

---

## CZĘŚĆ C — dla administratora: wygenerowanie klucza dla klienta

W projekcie `bq-modnakiecka` (Console → IAM & Admin → Service Accounts):

1. Utwórz service account, np. `claude-mcp-reader@bq-modnakiecka.iam.gserviceaccount.com`.
2. Nadaj MU wyłącznie role: **BigQuery Data Viewer** + **BigQuery Job User**
   (poziom projektu). Bez ról Editor/Owner/Storage.
3. Zakładka Keys → Add key → JSON → pobierz plik i przekaż klientowi bezpiecznym
   kanałem (np. menedżer haseł, link wygasający). Plik u klienta nazywa się `sa-key.json`.
4. Rotacja: usuń stary klucz w konsoli, wygeneruj nowy, podmień plik u klienta.

Wariant `gcloud`:

```bash
gcloud iam service-accounts create claude-mcp-reader \
  --project=bq-modnakiecka --display-name="Claude MCP reader (read-only BQ)"

gcloud projects add-iam-policy-binding bq-modnakiecka \
  --member="serviceAccount:claude-mcp-reader@bq-modnakiecka.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding bq-modnakiecka \
  --member="serviceAccount:claude-mcp-reader@bq-modnakiecka.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

gcloud iam service-accounts keys create sa-key.json \
  --iam-account=claude-mcp-reader@bq-modnakiecka.iam.gserviceaccount.com
```

---

## Rozwiązywanie problemów

| Objaw | Przyczyna / rozwiązanie |
|---|---|
| `python` nie znaleziony (Windows) | Reinstalacja Pythona z zaznaczonym „Add to PATH", nowe okno terminala |
| Serwer MCP nie widoczny w Claude Code | Uruchom `claude` w folderze repo (tam gdzie `.mcp.json`) albo sprawdź `claude mcp list` |
| `DefaultCredentialsError` | Brak `sa-key.json` w folderze repo lub zła ścieżka w env |
| `Access Denied: BigQuery` | Service account nie ma ról Data Viewer + Job User w projekcie `bq-modnakiecka` |
| `Query exceeded limit for bytes billed` | Brak filtra `_PARTITIONTIME` — zawęź zakres dat |
| Zapytanie odrzucone „tylko SELECT" | Serwer celowo blokuje DML/DDL — hurtownia jest read-only |
| Tabela nie istnieje | Użyj pełnej nazwy z sufiksem `_szdsp` (z `list_tables`), np. `aio_main_szdsp` |
