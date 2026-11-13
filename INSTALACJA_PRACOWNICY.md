# Hurtownia danych Modna Kiecka w Claude Code - instalacja krok po kroku (dla pracowników)

Ta instrukcja prowadzi od komputera z samym Claude Code do pierwszego raportu z hurtowni danych Modnej Kiecki.
Większość pracy wykona za Ciebie Claude Code - Ty tylko zatwierdzasz kolejne kroki.

- **Czas:** ok. 30-40 minut (z czego większość to czekanie na instalację).
- **Komputer:** Windows 10/11 albo macOS.
- **Wiedza:** nie musisz znać programowania ani SQL. Wystarczy umieć skopiować i wkleić tekst.

---

## Zanim zaczniesz

1. **Konto Claude** z planem Pro, Max albo Team/Enterprise (darmowy plan nie obejmuje Claude Code).
   Zapytaj administratora, którym kontem masz się logować.
   Jeśli to Twoje prywatne konto (Pro/Max): na claude.ai wejdź w **Ustawienia > Prywatność** i wyłącz
   **„Pomóż ulepszać Claude”** - będziesz pracować na danych firmy.
2. **Numer konta (1, 2, 3, 4 albo „biuro”) i plik klucza** od administratora albo kierownika zespołu.
3. **Prawo do instalowania programów** na komputerze. Na komputerze służbowym bez tych praw poproś o pomoc dział IT.
4. Potrzebujesz **Claude Code w oknie poleceń** (terminalu). Aplikacja Claude na komputer ani rozszerzenie do
   VS Code nie wystarczą.

## Twój klucz i Twoje konto

Każda osoba dostaje **własne konto serwisowe** (Service Account) i **własny plik klucza**. Klucz działa jak hasło
do hurtowni: daje dostęp tylko do odczytu danych, ale i tak nie wolno go nikomu przekazywać ani wysyłać.

| Nr | Konto serwisowe (nazwa) | Adres konta | Plik klucza |
|---|---|---|---|
| 1 | Modna Kiecka 1 | `modna-kiecka-1@bq-modnakiecka.iam.gserviceaccount.com` | `modna-kiecka-1.json` |
| 2 | Modna Kiecka 2 | `modna-kiecka-2@bq-modnakiecka.iam.gserviceaccount.com` | `modna-kiecka-2.json` |
| 3 | Modna Kiecka 3 | `modna-kiecka-3@bq-modnakiecka.iam.gserviceaccount.com` | `modna-kiecka-3.json` |
| 4 | Modna Kiecka 4 | `modna-kiecka-4@bq-modnakiecka.iam.gserviceaccount.com` | `modna-kiecka-4.json` |
| biuro | Biuro Modna Kiecka | `modna-kiecka-biuro@bq-modnakiecka.iam.gserviceaccount.com` | `modna-kiecka-biuro.json` |

Administrator albo kierownik zespołu powie Ci, **który numer jest Twój**, i przekaże plik klucza osobno,
innym kanałem niż e-mail. W całej instrukcji `N` oznacza Twój numer konta (1, 2, 3, 4 albo `biuro`).

Wszystkie konta mają te same uprawnienia: **odczyt danych BigQuery + uruchamianie zapytań** w projekcie
`bq-modnakiecka`. Nie mogą niczego zmienić ani usunąć.

---

## CZĘŚĆ 0 - co robisz sam (ok. 10 minut)

### 0.1. Otwórz okno poleceń

- **Windows:** naciśnij klawisz Windows, wpisz `PowerShell`, kliknij **Windows PowerShell**
  (nie „ISE”, nie „(x86)”, bez „Uruchom jako administrator”). Linia w oknie zaczyna się od `PS C:\Users\...>`.
  Jeśli nie ma `PS` na początku, to jest inne okno (cmd) - zamknij je i otwórz PowerShell.
- **macOS:** naciśnij `Cmd` + `Spacja`, wpisz `Terminal`, naciśnij Enter.

Polecenia z tej instrukcji kopiujesz w całości i wklejasz do tego okna (Windows: `Ctrl+V` albo prawy przycisk
myszy, macOS: `Cmd+V`), a potem naciskasz Enter.

### 0.2. Windows: sprawdź Git (na macOS pomiń)

Wpisz:

```powershell
git --version
```

Jeśli widzisz numer wersji - dalej. Jeśli błąd: wejdź na https://git-scm.com/downloads/win, pobierz
„64-bit Git for Windows Setup”, uruchom i klikaj **Next** do końca (domyślne ustawienia są dobre). Jeśli instalator
prosi o hasło administratora, którego nie masz - poproś dział IT. Potem zamknij i otwórz okno PowerShell.

### 0.3. Zainstaluj Claude Code (jeśli jeszcze go nie masz)

Sprawdź, czy już jest:

```bash
claude --version
```

Jeśli widzisz numer wersji (np. `2.1.x`), przejdź do kroku 0.4. Jeśli błąd („nie rozpoznano” / „command not found”):

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

(Jeśli widzisz „irm is not recognized” - jesteś w cmd, nie w PowerShell. Wróć do 0.1.)

**macOS (Terminal):**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Zamknij okno poleceń, otwórz je ponownie i wpisz `claude --version`. Jeśli nadal jest błąd, a instalator na
końcu pisał coś o „PATH” (np. „is not in your PATH”), wklej jedno polecenie, zamknij okno, otwórz nowe i sprawdź jeszcze raz:

- **Windows (PowerShell):**

  ```powershell
  [Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH','User') + ";$env:USERPROFILE\.local\bin", 'User')
  ```

- **macOS (Terminal):**

  ```bash
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
  ```

**Pierwsze uruchomienie:** wpisz `claude`. Wybierz motyw kolorów (Enter). Przy sposobie logowania wybierz
**Claude account with subscription**. Otworzy się przeglądarka - zaloguj się i zatwierdź (jeśli się nie otworzy,
naciśnij `c`, żeby skopiować link, i wklej go do przeglądarki). Wróć do okna i naciskaj Enter na kolejnych ekranach.
Po zalogowaniu wpisz `/exit`, żeby wyjść.

### 0.4. Zapisz plik klucza

Plik `modna-kiecka-N.json` od administratora zapisz w folderze **Pobrane** (Downloads). **Nie zmieniaj jego nazwy
i nie otwieraj go** - Claude sam go znajdzie i przeniesie w bezpieczne miejsce.

### 0.5. Utwórz folder roboczy i uruchom w nim Claude Code

**Windows (PowerShell):**

```powershell
mkdir $HOME\ModnaKiecka -Force; cd $HOME\ModnaKiecka; claude
```

**macOS (Terminal):**

```bash
mkdir -p ~/ModnaKiecka && cd ~/ModnaKiecka && claude
```

Claude może zapytać, czy ufasz temu folderowi („Do you trust the files in this folder?”) - wybierz **Yes**.

### 0.6. Wklej polecenie startowe

Skopiuj cały tekst i wklej do Claude Code, potem Enter:

```text
Jestem pracownikiem Modnej Kiecki i instaluję dostęp do hurtowni danych.
Pobierz instrukcję poleceniem curl -fsSL https://raw.githubusercontent.com/andrzejczyk-adrian/modnakiecka-bq-mcp/main/INSTALACJA_PRACOWNICY.md -o INSTALACJA_PRACOWNICY.md
(nie przez WebFetch), przeczytaj cały plik i wykonaj go dla mnie od CZĘŚCI 1, krok po kroku.
Mów po polsku i prosto, przed każdą instalacją powiedz, co instalujesz i po co, i poczekaj na moją zgodę.
Najpierw zapytaj mnie o numer konta.
```

### Jak zatwierdzać kroki

Claude będzie pytał o zgodę na uruchomienie poleceń (np. „Do you want to proceed?”). Jeśli polecenie zgadza się
z tym, co Claude właśnie zapowiedział - wybierz **Yes** (strzałki + Enter). Jeśli czegoś nie rozumiesz, napisz
„co to robi?”. W każdej chwili możesz przerwać klawiszem `Esc`.

---

> **Od tego miejsca instrukcja jest napisana dla Claude Code.** Ty tylko czytasz komunikaty i zatwierdzasz kroki.

## CZĘŚĆ 1 - audyt środowiska (wykonuje Claude)

### Zasady dla Claude na całą instalację

- Mów po polsku, prostym językiem. Jeden krok naraz. Po każdej części pokaż krótkie podsumowanie (✅ / ❌).
- **Przed każdą instalacją** powiedz, co i po co instalujesz, i poczekaj na zgodę użytkownika.
- **Klucz to sekret:** nigdy nie wyświetlaj zawartości pliku klucza (żadnego `cat`, `type`, `Get-Content`, `Read`,
  `Grep`). Wolno odczytać z niego tylko jawne pola `type`, `project_id` i `client_email` poleceniem z punktu 1.6.
  Nie kopiuj klucza do żadnego repozytorium, nie wysyłaj go nigdzie, nie wklejaj do czatu.
- Nie zmieniaj ustawień komputera poza opisanymi tu krokami. Nie wyłączaj zabezpieczeń, antywirusa ani zapory.
- Jeśli krok nie udaje się dwa razy z rzędu - zatrzymaj się, pokaż użytkownikowi komunikat błędu i sprawdź tabelę
  „Rozwiązywanie problemów” na końcu instrukcji. Nie wymyślaj obejść.
- **Windows:** wszystkie polecenia z części 1-3 uruchamiaj narzędziem **Bash** (Git Bash), NIE narzędziem PowerShell,
  nawet jeśli PowerShell jest dostępny - polecenia są w składni bash (`$(...)`, `< /dev/null`, `grep`, `cygpath`).
  Ścieżki mają postać `/c/Users/...`. Jeśli narzędzia Bash nie ma (brak Git for Windows) - zatrzymaj się i poproś
  użytkownika o krok 0.2 z tej instrukcji.
- Polecenia uruchamiaj w osobnych wywołaniach. Zmienne powłoki nie przechodzą między wywołaniami - dlatego
  w instrukcji są pełne ścieżki. Wyjątek: blok Windows w kroku 2.8 uruchom w całości jednym wywołaniem.
- Folder roboczy: `~/ModnaKiecka` (Windows: `C:\Users\<nazwa>\ModnaKiecka`). Klucz trafi do `~/.modnakiecka/`
  (poza folderem roboczym, żeby nie był przypadkiem czytany).
- `N` w poleceniach zastępuj numerem konta, który podał użytkownik (1, 2, 3, 4 albo `biuro` - wtedy plik to
  `modna-kiecka-biuro.json`, a konto `modna-kiecka-biuro@...`).

### Audyt - sprawdź i zanotuj wynik każdego punktu

Uruchom sprawdzenia (bez instalowania czegokolwiek) i pokaż użytkownikowi tabelę wyników.

| # | Co sprawdzić | macOS | Windows (narzędzie Bash) | Wymagane |
|---|---|---|---|---|
| 1.1 | System | `sw_vers; uname -m` | `uname -s -r; echo $PROCESSOR_ARCHITECTURE` | Windows 10/11 albo macOS; zanotuj ARM64 |
| 1.2 | Claude Code | `claude --version` | `claude --version` | jest |
| 1.3 | Git | `xcode-select -p >/dev/null 2>&1 && git --version \|\| echo "brak git"` | `git --version` | jest (macOS: jeśli brak - krok 2.1) |
| 1.4 | uv (instalator Pythona) | `~/.local/bin/uv --version` | `~/.local/bin/uv.exe --version` | jeśli brak - krok 2.2 (nawet gdy działa samo `uv` z innego miejsca) |
| 1.5 | Internet | `curl -sS -o /dev/null -w "%{http_code}\n" https://github.com` i to samo dla `https://bigquery.googleapis.com` | to samo | dowolny kod HTTP (200/301/404 = połączenie działa) |
| 1.6 | Plik klucza | polecenie `find` poniżej | to samo | dokładnie jeden plik dla numeru N |
| 1.7 | Bieżący folder | `pwd` | `pwd` | `~/ModnaKiecka` |
| 1.8 | Serwery MCP | `claude mcp list` | `claude mcp list` | informacyjnie: czy `modnakiecka-bq` już jest |

Punkt 1.6 - znajdź plik klucza (nazwa może mieć dopisek, np. `modna-kiecka-2 (1).json`; dla konta biuro `N` = `biuro`):

```bash
find ~/Downloads ~/Desktop ~/ModnaKiecka ~/.modnakiecka ~/OneDrive* -maxdepth 3 -iname 'modna-kiecka-N*.json' 2>/dev/null
```

- macOS może pokazać okno „Terminal chce uzyskać dostęp do plików w folderze Pobrane” - poproś użytkownika
  o kliknięcie **OK / Pozwól**. Jeśli wynik to „Operation not permitted” - patrz „Rozwiązywanie problemów”.
- Sprawdź znaleziony plik **bez wyświetlania sekretu** (`grep` wypisze tylko trzy jawne pola):

```bash
grep -oE '"(type|project_id|client_email)": *"[^"]*"' "<ścieżka do znalezionego pliku>"
```

Poprawny wynik to trzy linie: `"type": "service_account"`, `"project_id": "bq-modnakiecka"` i
`"client_email": "modna-kiecka-N@bq-modnakiecka.iam.gserviceaccount.com"`, gdzie `N` zgadza się z numerem
użytkownika. Jeśli numer się nie zgadza albo plików jest kilka - zatrzymaj się i zapytaj użytkownika.

Wynik audytu pokaż jako tabelę: co jest ✅, czego brakuje ❌ i co zainstalujesz w części 2. Zapytaj o zgodę na instalację.

---

## CZĘŚĆ 2 - instalacja (wykonuje Claude, za zgodą użytkownika)

Pomiń kroki, które audyt oznaczył jako ✅.

### 2.1. Git (tylko jeśli brak)

- **macOS:** uruchom `xcode-select --install`. Pojawi się okno systemowe - poproś użytkownika, żeby kliknął
  **Zainstaluj** (może poprosić o hasło do komputera) i poczekał do końca (kilka minut). Potem `git --version`.
- **Windows:** poproś użytkownika o krok 0.2 tej instrukcji (instalacja Git for Windows), potem `/exit`,
  zamknięcie i otwarcie PowerShell, `cd $HOME\ModnaKiecka; claude` i polecenie startowe jeszcze raz.

### 2.2. uv - instalator Pythona (tylko jeśli brak `~/.local/bin/uv`)

uv instaluje odpowiednią wersję Pythona osobno, nie ruszając niczego w systemie.

- **macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Sprawdź: `~/.local/bin/uv --version` (Windows: `~/.local/bin/uv.exe --version`). W dalszych krokach wywołuj uv
pełną ścieżką, bo nowa ścieżka systemowa zadziała dopiero w nowym oknie poleceń.

### 2.3. Pobierz serwer MCP hurtowni

```bash
cd ~/ModnaKiecka && git clone https://github.com/andrzejczyk-adrian/modnakiecka-bq-mcp.git
```

Jeśli folder `modnakiecka-bq-mcp` już istnieje: `cd ~/ModnaKiecka/modnakiecka-bq-mcp && git pull`.
Plik `INSTALACJA_PRACOWNICY.md` pobrany w kroku 0.6 do `~/ModnaKiecka` możesz teraz usunąć - ta sama instrukcja
jest w `~/ModnaKiecka/modnakiecka-bq-mcp/`.

### 2.4. Środowisko Pythona i biblioteki

macOS:

```bash
cd ~/ModnaKiecka/modnakiecka-bq-mcp && ~/.local/bin/uv venv --python 3.12 --allow-existing && ~/.local/bin/uv pip install --python .venv -r requirements.txt
```

Windows:

```bash
cd ~/ModnaKiecka/modnakiecka-bq-mcp && ~/.local/bin/uv.exe venv --python 3.12 --allow-existing && ~/.local/bin/uv.exe pip install --python .venv -r requirements.txt
```

- Windows z procesorem ARM64 (audyt 1.1): zamiast `--python 3.12` użyj `--python cpython-3.12-windows-x86_64-none`
  (część bibliotek nie ma wersji ARM64; Python x64 działa w emulacji).
- uv sam pobierze Pythona 3.12 (ok. 25 MB) i zainstaluje biblioteki w folderze `.venv`.

Sprawdzenie (musi wypisać `biblioteki OK`):

- macOS: `~/ModnaKiecka/modnakiecka-bq-mcp/.venv/bin/python -c "from mcp.server.fastmcp import FastMCP; import google.cloud.bigquery; print('biblioteki OK')"`
- Windows: `~/ModnaKiecka/modnakiecka-bq-mcp/.venv/Scripts/python.exe -c "from mcp.server.fastmcp import FastMCP; import google.cloud.bigquery; print('biblioteki OK')"`

Python serwera to dalej: macOS `~/ModnaKiecka/modnakiecka-bq-mcp/.venv/bin/python`,
Windows `~/ModnaKiecka/modnakiecka-bq-mcp/.venv/Scripts/python.exe`.

### 2.5. Klucz w bezpiecznym miejscu

Przenieś (nie kopiuj) plik klucza znaleziony w audycie do `~/.modnakiecka/` pod docelową nazwą:

```bash
mkdir -p ~/.modnakiecka && mv "<ścieżka do znalezionego pliku>" ~/.modnakiecka/modna-kiecka-N.json
```

- macOS: dodatkowo `chmod 700 ~/.modnakiecka && chmod 600 ~/.modnakiecka/modna-kiecka-N.json`
  (tylko ten użytkownik komputera może go czytać).
- Powiedz użytkownikowi: „Klucz jest teraz w ukrytym folderze .modnakiecka w Twoim katalogu domowym. Nie wysyłaj
  go nikomu. Jeśli zgubisz komputer albo klucz trafi w niepowołane ręce, od razu powiedz administratorowi - wyłączy go.
  Warto też usunąć wiadomość/załącznik, którym klucz do Ciebie przyszedł.”

### 2.6. Zasady pracy, ochrona klucza i folder na raporty

Zasady (`CLAUDE.md` Claude czyta automatycznie przy każdym uruchomieniu w folderze `ModnaKiecka`):

```bash
if [ -f ~/ModnaKiecka/CLAUDE.md ]; then diff ~/ModnaKiecka/CLAUDE.md ~/ModnaKiecka/modnakiecka-bq-mcp/pracownicy/CLAUDE.md && echo "CLAUDE.md aktualny"; else cp ~/ModnaKiecka/modnakiecka-bq-mcp/pracownicy/CLAUDE.md ~/ModnaKiecka/CLAUDE.md && echo "CLAUDE.md skopiowany"; fi
```

Jeśli `diff` pokazał różnice - pokaż je użytkownikowi i zapytaj, czy nadpisać (`cp` jak wyżej).

Blokada czytania klucza przez Claude w tym folderze i folder na raporty:

```bash
mkdir -p ~/ModnaKiecka/.claude ~/ModnaKiecka/raporty && [ -f ~/ModnaKiecka/.claude/settings.json ] || cp ~/ModnaKiecka/modnakiecka-bq-mcp/pracownicy/settings.json ~/ModnaKiecka/.claude/settings.json
```

(Jeśli `~/ModnaKiecka/.claude/settings.json` już istniał - pokaż go użytkownikowi i dopisz reguły `deny` z
`pracownicy/settings.json`, nie usuwając istniejących.)

### 2.7. Test połączenia bez MCP

macOS:

```bash
cd ~/ModnaKiecka/modnakiecka-bq-mcp && .venv/bin/python pracownicy/sprawdz_polaczenie.py ~/.modnakiecka/modna-kiecka-N.json
```

Windows:

```bash
cd ~/ModnaKiecka/modnakiecka-bq-mcp && .venv/Scripts/python.exe pracownicy/sprawdz_polaczenie.py ~/.modnakiecka/modna-kiecka-N.json
```

Oczekiwany wynik: adres konta `modna-kiecka-N@...`, trzy linie `OK` i na końcu „Wszystko działa”.
`UWAGA` (zamiast `OK`) przy koszcie reklam przed ok. 8:00 rano jest normalne - dane za wczoraj jeszcze się ładują.
`BŁĄD` - patrz „Rozwiązywanie problemów”.

### 2.8. Rejestracja serwera MCP w Claude Code

Serwer rejestrujemy dla użytkownika (będzie dostępny w każdej sesji). Najpierw `claude mcp list` - jeśli
`modnakiecka-bq` już istnieje (np. ze starej instalacji), pokaż jego konfigurację (`claude mcp get modnakiecka-bq`),
zapytaj użytkownika i dopiero wtedy usuń: `claude mcp remove modnakiecka-bq --scope user`.

**macOS:**

```bash
claude mcp add --scope user modnakiecka-bq --env GOOGLE_APPLICATION_CREDENTIALS="$HOME/.modnakiecka/modna-kiecka-N.json" -- "$HOME/ModnaKiecka/modnakiecka-bq-mcp/.venv/bin/python" "$HOME/ModnaKiecka/modnakiecka-bq-mcp/server.py"
```

**Windows** (ścieżki muszą być w formacie Windows, stąd `cygpath -w`; uruchom cały blok jednym wywołaniem):

```bash
KLUCZ_W=$(cygpath -w "$HOME/.modnakiecka/modna-kiecka-N.json")
PY_W=$(cygpath -w "$HOME/ModnaKiecka/modnakiecka-bq-mcp/.venv/Scripts/python.exe")
SRV_W=$(cygpath -w "$HOME/ModnaKiecka/modnakiecka-bq-mcp/server.py")
claude mcp add --scope user modnakiecka-bq --env GOOGLE_APPLICATION_CREDENTIALS="$KLUCZ_W" -- "$PY_W" "$SRV_W"
```

Sprawdzenie, w dwóch częściach:

1. `claude mcp list` - przy `modnakiecka-bq` powinno być **Connected**. To potwierdza tylko, że Python i serwer
   startują - **klucza ten status nie sprawdza**.
2. Ścieżka klucza: `claude mcp get modnakiecka-bq`, skopiuj ścieżkę z linii `GOOGLE_APPLICATION_CREDENTIALS`
   i sprawdź, że plik istnieje (`ls -l "<ta ścieżka>"`; na Windows zamień ją najpierw: `ls -l "$(cygpath -u '<ta ścieżka>')"`).
   W ścieżce nie może zostać litera `N` zamiast numeru.

Jeśli w punkcie 1 jest „Failed to connect”, uruchom serwer ręcznie, żeby zobaczyć błąd. Serwer od razu się zakończy,
bo nie dostanie poleceń - kod `0` bez komunikatu błędu oznacza, że Python i biblioteki działają:

- macOS: `cd ~/ModnaKiecka/modnakiecka-bq-mcp && .venv/bin/python server.py < /dev/null; echo "kod: $?"`
- Windows: `cd ~/ModnaKiecka/modnakiecka-bq-mcp && .venv/Scripts/python.exe server.py < /dev/null; echo "kod: $?"`

### 2.9. Ponowne uruchomienie Claude Code

Nowy serwer MCP będzie widoczny dopiero w nowej sesji. Powiedz użytkownikowi dokładnie:

1. Wpisz `/exit` i naciśnij Enter.
2. W tym samym oknie wpisz `claude` i naciśnij Enter (jesteś nadal w folderze ModnaKiecka; jeśli nie:
   Windows `cd $HOME\ModnaKiecka`, macOS `cd ~/ModnaKiecka`).
3. Wklej:

```text
Kontynuuj instalację hurtowni Modna Kiecka od CZĘŚCI 3 instrukcji z pliku
modnakiecka-bq-mcp/INSTALACJA_PRACOWNICY.md (przeczytaj go w całości). Mój numer konta to N.
```

(Przed wyjściem podstaw w tym tekście numer użytkownika, żeby mógł go skopiować bez zmian.)

---

## CZĘŚĆ 3 - sprawdzenie połączenia (wykonuje Claude, po ponownym uruchomieniu)

1. Poproś użytkownika, żeby wpisał `/mcp` - na liście powinien być `modnakiecka-bq` ze statusem connected
   (zamknięcie listy: `Esc`). Możesz też od razu wywołać narzędzie z punktu 2 - jeśli działa, serwer jest podłączony.
2. Wywołaj `load_project`, potem `read_document("introduction")`. Streść użytkownikowi w 3 zdaniach, co jest w hurtowni.
   **Uwaga:** dokument `introduction` każe po wczytaniu zadać użytkownikowi pytania i nie uruchamiać SQL (fazy PHASE 1-3).
   W trakcie instalacji pomiń to i przejdź od razu do punktu 3. Zdanie, że od 03.08.2026 w hurtowni nie ma zamówień
   z aplikacji, dotyczy tylko tabel `aio_*` - ERP (`zamowieniamodnakiecka.orders`, kanał `Sklep`) ma te zamówienia.
   Zasady z `CLAUDE.md` i zapytania wzorcowe mają pierwszeństwo przed dokumentami serwera.
3. Przez `run_query` uruchom test zgodności kosztu reklam z platformami (przedwczoraj, żeby dane były domknięte):

```sql
WITH d AS (SELECT DATE_SUB(CURRENT_DATE('Europe/Warsaw'), INTERVAL 2 DAY) AS dz)
SELECT
  (SELECT dz FROM d) AS dzien,
  (SELECT ROUND(SUM(cost), 2) FROM `bq-modnakiecka.analityka.aio_products`, d WHERE date = d.dz) AS koszt_w_tabeli,
  ROUND(
    (SELECT SUM(spend) FROM `bq-modnakiecka.witcloud_qfmdjgmqib6ghnpoimik.fb_ads_act_*`, d WHERE date_start = d.dz)
  + (SELECT SUM(Cost) / 1e6 FROM `bq-modnakiecka.witcloud_qfmdjgmqib6ghnpoimik.gads_campaign_stats_*`, d
       WHERE _PARTITIONTIME >= TIMESTAMP(DATE_SUB(d.dz, INTERVAL 40 DAY)) AND Date = d.dz), 2) AS koszt_z_platform
```

   Obie kwoty powinny być równe (różnica do 1% jest dopuszczalna, jeśli platforma poprawiła dane po porannym
   przeliczeniu tabeli). To dowód, że widzisz pełne i spójne dane.
4. Uruchom zapytanie **P3** z pliku `~/ModnaKiecka/modnakiecka-bq-mcp/pracownicy/zapytania_wzorcowe.sql`
   i pokaż wynik jako tabelę.
5. Podsumuj: „✅ Połączenie z hurtownią działa. Możesz zadawać pytania.”, pokaż sekcję „Jak wrócić do pracy”
   i CZĘŚĆ 5.

### Jak wrócić do pracy (każdego dnia)

1. Otwórz okno poleceń (krok 0.1).
2. Wpisz: **Windows** `cd $HOME\ModnaKiecka; claude`, **macOS** `cd ~/ModnaKiecka && claude`.
3. **Zawsze startuj w folderze ModnaKiecka** - tylko tam Claude zna zasady z `CLAUDE.md`. W innym folderze hurtownia
   też odpowie, ale Claude może policzyć sprzedaż ze złej tabeli. Nie uruchamiaj `claude` w folderze
   `modnakiecka-bq-mcp` (jest tam stara konfiguracja dla innego trybu - jeśli Claude zapyta o serwer z pliku
   `.mcp.json`, odmów).
4. Wyjście: `/exit`. Powrót do ostatniej rozmowy: `claude --continue`.

---

## CZĘŚĆ 4 - zasady w skrócie (dla Ciebie)

- **Hurtownia jest tylko do odczytu.** Nic nie zepsujesz - konto nie ma uprawnień do zmian.
- **Każde zapytanie kosztuje** (płaci firma za ilość przeczytanych danych). Serwer blokuje zapytania powyżej 4 GB.
  Zwykłe pytania o sprzedaż i koszty to ułamki grosza; uważaj na analizy ruchu GA4 za długie okresy.
- **Świeżość danych:** zamówienia z ERP są ładowane w nocy; koszty reklam za wczoraj są w hurtowni po ok. 8:00
  (latem po ok. 9:00) - wcześniej tabela kończy się na przedwczoraj. Dzisiejszy dzień jest zawsze niepełny -
  pytaj o okresy do wczoraj.
- **Nieopłacone zamówienia:** zamówienia ze statusem „Oczekujące na wpłatę” (przelew nieopłacony) nie są liczone
  w sprzedaży - sklep anuluje je po ok. 14 dniach.
- **Ostatnie dni się zmieniają:** platformy reklamowe poprawiają koszt do 30 dni wstecz.
- **Dane klientów:** nie proś o e-maile, telefony ani adresy klientów i nie wysyłaj surowych danych poza firmę.
- Pełne zasady dla Claude są w pliku `~/ModnaKiecka/CLAUDE.md`. Nie usuwaj go.

---

## CZĘŚĆ 5 - pierwsze pytania (sprawdzone)

Te pytania są sprawdzone: dane źródłowe są właściwe, a zapytania przetestowane 13.11.2026 kontem pracownika
i porównane z innymi źródłami (zgodność 100%). Wklejaj je do Claude Code tak, jak są. Gotowe zapytania SQL (P1-P7)
są w pliku `modnakiecka-bq-mcp/pracownicy/zapytania_wzorcowe.sql` - Claude z nich skorzysta.

| # | Pytanie do wklejenia | Co dostaniesz | Skąd dane |
|---|---|---|---|
| 1 | „Pokaż sprzedaż dzienną z ostatnich 30 dni: liczba zamówień i przychód brutto osobno dla www, aplikacji i biura (zapytanie P1).” | tabela dzień po dniu | ERP, bez anulowanych i nieopłaconych |
| 2 | „Ile wydaliśmy dziennie na reklamy w Mecie i Google Ads w ostatnich 30 dniach? (P2)” | koszt dzienny per platforma | koszt kont reklamowych |
| 3 | „Pokaż podsumowanie ostatnich 8 pełnych tygodni: zamówienia, przychód, udział aplikacji, średnie zamówienie, koszt Meta i Google, MER (P3).” | tabela tygodniowa | ERP + koszt reklam |
| 4 | „Porównaj www i aplikację z ostatnich 4 tygodni: średnia wartość zamówienia i liczba sztuk w zamówieniu (P4).” | 3 wiersze: www, aplikacja, biuro | ERP |
| 5 | „Które 10 modeli sprzedało się najlepiej w ostatnich 30 dniach (sztuki i wartość)? (P5)” | ranking modeli | ERP, pozycje zamówień |
| 6 | „Na które 10 modeli wydaliśmy najwięcej na reklamy w ostatnich 30 dniach i ile ich sprzedaliśmy? Pokaż koszt reklam na sprzedaną sztukę (P6).” | koszt vs sprzedaż per model | koszt reklam per produkt + ERP |
| 7 | „Jaką część kosztu reklam umiemy przypisać do konkretnego koloru, a jaką tylko do modelu albo do niczego? (P7)” | struktura kosztu Meta i Google | koszt reklam per produkt |

Jak czytać wyniki:

- **Przychód brutto** = wartość zamówień z VAT, po rabatach, z dostawą, przed zwrotami, bez zamówień anulowanych
  i nieopłaconych.
- **MER** = przychód / koszt reklam Meta + Google. Np. MER 10 = na każdą złotówkę reklam przypada 10 zł sprzedaży
  (ze wszystkich źródeł, nie tylko z reklam). Innych kanałów płatnych hurtownia nie ma.
- **Aplikacja** w danych nazywa się `Sklep` - to aplikacja mobilna, nie sklep stacjonarny.
- **Wartość w P5 i P6** jest przed rabatem zamówienia (rabat liczony jest dla całego zamówienia, nie dla pozycji),
  więc udział kosztu reklam w P6 jest lekko zaniżony.
- **Koszt na sprzedaną sztukę (P6)** jest przybliżony: część kosztu reklam znamy tylko na poziomie modelu albo wcale
  (to pokazuje pytanie 7), a sprzedaż modelu pochodzi ze wszystkich źródeł, nie tylko z reklam.

Gdy opanujesz te pytania, zadawaj własne - np. „porównaj ten tydzień z tym samym tygodniem rok temu” albo
„jak zmieniała się średnia wartość zamówienia w aplikacji miesiąc do miesiąca”. Claude sam dobierze zapytanie
według zasad z `CLAUDE.md`. Przy porównaniach rok do roku pamiętaj: w 2025 aplikacji jeszcze nie było.

---

## CZĘŚĆ 6 - pierwszy raport HTML

Raport pokazuje 8 ostatnich tygodni: wykres przychodu dziennego (www / aplikacja / biuro), wykres kosztu reklam
(Meta / Google), wykres MER (dzienny i średnia z 7 dni), tabelę tygodniową i automatyczne wnioski.
Uruchamiaj go po ok. 8:00 (latem 9:00), gdy w hurtowni jest już koszt reklam za wczoraj.

### Wariant A - jedno polecenie (najprostszy, zawsze działa)

Wklej do Claude Code (zamień `N`):

```text
Wygeneruj mój pierwszy raport: uruchom skrypt modnakiecka-bq-mcp/pracownicy/pierwszy_raport.py
Pythonem z .venv, z kluczem ~/.modnakiecka/modna-kiecka-N.json. Potem otwórz raport w przeglądarce
i dopisz mi w czacie 3 obserwacje z wykresów.
```

Skrypt zapisze plik `~/ModnaKiecka/raporty/raport_sprzedaz_koszty_RRRR-MM-DD.html`. Otwierasz go dwuklikiem.

### Wariant B - raport zbudowany przez Claude (nauka pracy z danymi)

```text
Przygotuj raport HTML „Sprzedaż i koszt reklam - ostatnie 8 tygodni” i zapisz go w ~/ModnaKiecka/raporty/.
Dane pobierz przez run_query według zasad z CLAUDE.md:
1. przychód brutto dziennie z ERP osobno dla www, aplikacji i biura (jak P1, ale za 8 pełnych tygodni do wczoraj),
2. koszt dzienny Meta i Google Ads z analityka.aio_products (jak P2),
3. tabela tygodniowa jak P3.
W raporcie: 3 wykresy liniowe (przychód, koszt, MER dzienny + średnia z 7 dni) w Chart.js z cdnjs
(wersja 4.4.1), tabela tygodniowa, 3-5 wniosków opartych wyłącznie na liczbach z raportu oraz sekcja
„Skąd dane i na co uważać”. Jeden plik HTML, polskie formatowanie liczb. Na koniec otwórz go w przeglądarce.
```

Sprawdzenie poprawności (zrób to przy pierwszym raporcie): liczby w tabeli tygodniowej z wariantu B powinny być
**takie same** jak w raporcie z wariantu A za te same tygodnie. Jeśli się różnią - Claude użył innego źródła;
poproś go, żeby porównał zapytania i trzymał się `CLAUDE.md`.

---

## Rozwiązywanie problemów

| Objaw | Przyczyna | Co zrobić |
|---|---|---|
| `claude` - „nie rozpoznano” / „command not found” | folder `.local/bin` nie jest w ścieżce systemowej albo okno otwarte przed instalacją | wykonaj polecenie PATH z kroku 0.3 i otwórz nowe okno; jeśli pliku `~/.local/bin/claude` (Windows `%USERPROFILE%\.local\bin\claude.exe`) w ogóle nie ma - zainstaluj ponownie (krok 0.3) |
| „irm is not recognized” | otwarte okno cmd zamiast PowerShell | krok 0.1 |
| Windows: Claude nie ma narzędzia Bash / prosi o Git Bash | brak Git for Windows | krok 0.2, potem nowe okno |
| macOS: „Operation not permitted” przy folderze Pobrane | Terminal nie dostał zgody na Pobrane | Ustawienia systemowe > Prywatność i ochrona > Pliki i foldery > Terminal > włącz Pobrane; potem `/exit` i `claude` |
| `uv` - „command not found” zaraz po instalacji | nowa ścieżka działa dopiero w nowym oknie | wywołuj pełną ścieżką `~/.local/bin/uv` (Windows `~/.local/bin/uv.exe`) |
| `uv venv` - „A virtual environment already exists” | zostało z poprzedniej próby | użyj `--allow-existing` (jest w poleceniu z kroku 2.4) |
| `uv venv` - błąd pobierania Pythona | firmowa sieć / proxy blokuje pobieranie | spróbuj z innej sieci albo zgłoś administratorowi |
| `No module named 'mcp.server.fastmcp'` | zainstalowała się biblioteka mcp 2.x (stara kopia repo) | `git pull` w `modnakiecka-bq-mcp`, potem ponownie krok 2.4 (requirements ma `mcp<2`) |
| Test 2.7: „nie ma pliku” | zła ścieżka do klucza | sprawdź `ls ~/.modnakiecka/` |
| Test 2.7: „to nie jest klucz konta serwisowego” | wybrany zły plik (np. inny JSON z Pobranych) | poszukaj pliku `modna-kiecka-N.json`; poproś administratora o ponowne przesłanie |
| `invalid_grant` / `Invalid JWT Signature` | klucz został wyłączony albo jest uszkodzony | poproś administratora o nowy klucz |
| `Access Denied` / `403` | konto nie ma uprawnień albo zła nazwa tabeli | sprawdź nazwę tabeli (pełna nazwa z `bq-modnakiecka.`); jeśli dotyczy wszystkich zapytań - zgłoś administratorowi |
| `Query exceeded limit for bytes billed` | zapytanie czyta za dużo danych (>4 GB) | zawęź okres; dla tabel `aio_*` filtr `_PARTITIONTIME`, dla GA4 `_TABLE_SUFFIX` |
| `claude mcp list`: „Failed to connect” | zła ścieżka do Pythona albo `server.py` w rejestracji albo brak bibliotek | ręczny test z kroku 2.8; `claude mcp get modnakiecka-bq`, porównaj ścieżki; usuń i dodaj ponownie (krok 2.8) |
| `run_query`/`list_tables`: „File ... was not found” | zła ścieżka do klucza w rejestracji MCP (np. zostało `N`) | `claude mcp remove modnakiecka-bq --scope user`, ponownie krok 2.8 z właściwym numerem, potem `/exit` i `claude` |
| Narzędzia `modnakiecka-bq` niewidoczne w Claude | sesja uruchomiona przed rejestracją | `/exit` i ponownie `claude` (krok 2.9) |
| Raport: „brak kosztu reklam za …” | uruchomiony przed ok. 8:00 (latem 9:00) | uruchom później |
| „Dozwolone są wyłącznie zapytania SELECT/WITH” | próba zmiany danych | hurtownia jest tylko do odczytu - to celowe |
| „tabela nie istnieje” dla tabel AIO | brak sufiksu w nazwie | użyj pełnej nazwy z `list_tables` (np. `aio_main_szdsp`) |
| Liczby inne niż w raporcie zespołu | inne źródło albo inna definicja (z anulowanymi, inny okres) | zapytaj Claude: „z jakiej tabeli i z jakimi filtrami to policzyłeś?” i porównaj z `CLAUDE.md` |

---

## CZĘŚĆ 7 - aktualizacja

Serwer hurtowni nie aktualizuje się sam. Nowe wersje są w repozytorium `modnakiecka-bq-mcp`:
kod serwera, wbudowana dokumentacja tabel (`docs/`), zasady pracy (`pracownicy/CLAUDE.md`), zapytania wzorcowe
i skrypty. Lista zmian: `pracownicy/ZMIANY.md`. Sam Claude Code aktualizuje się automatycznie (ręcznie: `claude update`).

**Kiedy:** gdy administrator albo kierownik zespołu da znać o zmianach, a poza tym raz w miesiącu.

**Jak:** uruchom Claude Code w folderze ModnaKiecka i wklej:

```text
Zaktualizuj dostęp do hurtowni Modna Kiecka według CZĘŚCI 7 instrukcji
modnakiecka-bq-mcp/INSTALACJA_PRACOWNICY.md. Mój numer konta to N.
```

**Kroki dla Claude:**

1. `cd ~/ModnaKiecka/modnakiecka-bq-mcp && git pull` - pokaż użytkownikowi nowe wpisy z `pracownicy/ZMIANY.md`.
   Jeśli `git pull` zgłasza konflikt (ktoś zmieniał pliki w tym folderze) - nie nadpisuj niczego, pokaż komunikat
   i poproś o kontakt z administratorem.
2. Biblioteki - krok 2.4 (to samo polecenie; jest bezpieczne do powtórzenia) i jego sprawdzenie (`biblioteki OK`).
3. Zasady: porównaj `~/ModnaKiecka/modnakiecka-bq-mcp/pracownicy/CLAUDE.md` z `~/ModnaKiecka/CLAUDE.md` (`diff`).
   Pokaż różnice i zapytaj, czy nadpisać. Tak samo `pracownicy/settings.json` z `~/ModnaKiecka/.claude/settings.json`
   (reguły `deny` dopisz, niczego nie usuwaj).
4. Test połączenia - krok 2.7.
5. Jeśli zmienił się `server.py`, `requirements.txt` albo `docs/` - powiedz użytkownikowi, żeby zrobił `/exit`
   i ponownie `claude` (serwer MCP wczyta się na nowo). Rejestracji MCP (krok 2.8) nie trzeba powtarzać.
6. Podsumuj: co się zmieniło i czy wszystko działa.

---

## Dla administratora

- Konta: `modna-kiecka-1` … `modna-kiecka-4` (nazwy wyświetlane „Modna Kiecka 1-4”) i `modna-kiecka-biuro`
  („Biuro Modna Kiecka”) w projekcie `bq-modnakiecka`, utworzone 13.11.2026. Role na poziomie projektu: `roles/bigquery.dataViewer` + `roles/bigquery.jobUser`
  (tak jak istniejące konto analityczne klienta). Zapis zablokowany (sprawdzone próbą `CREATE TABLE`).
- **Uwaga:** rola na poziomie projektu daje odczyt wszystkich zbiorów danych, w tym kolumn z danymi osobowymi
  (np. e-mail, telefon, adres w surowych tabelach). Zasada nr 6 w `CLAUDE.md` jest instrukcją dla Claude, nie blokadą.
  Węższy wariant: `dataViewer` tylko na zbiorach `analityka`, `zamowieniamodnakiecka`, `witcloud_qfmdjgmqib6ghnpoimik`,
  `analytics_291537403` (+ `jobUser` na projekcie), ewentualnie zabezpieczenie kolumn osobowych.
- Klucze JSON nie są w żadnym repozytorium. Przekazuj je bezpiecznym kanałem (menedżer haseł, link wygasający),
  nie zwykłym mailem. Przypisanie numerów do osób trzymaj poza tym (publicznym) repozytorium.
- Wyłączenie dostępu osoby (np. odejście z firmy) - najszybciej wyłączyć konto:

```bash
gcloud iam service-accounts disable modna-kiecka-N@bq-modnakiecka.iam.gserviceaccount.com --project=bq-modnakiecka
```

- Rotacja klucza (np. klucz trafił w niepowołane ręce) - nowy plik zapisuj poza jakimkolwiek repozytorium:

```bash
gcloud iam service-accounts keys list --iam-account=modna-kiecka-N@bq-modnakiecka.iam.gserviceaccount.com
gcloud iam service-accounts keys create <folder poza repo>/modna-kiecka-N.json --iam-account=modna-kiecka-N@bq-modnakiecka.iam.gserviceaccount.com
gcloud iam service-accounts keys delete <ID_STAREGO_KLUCZA> --iam-account=modna-kiecka-N@bq-modnakiecka.iam.gserviceaccount.com
```

- Koszt zapytań każdego konta widać w `region-eu.INFORMATION_SCHEMA.JOBS_BY_PROJECT` (kolumna `user_email`).
