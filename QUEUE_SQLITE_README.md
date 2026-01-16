# System Kolejkowania SQLite - Symulacja Infolinii

System kolejkowania oparty na bazie danych SQLite, symulujący pracę infolinii z operatorami.

## Pliki systemu

### Wersja SQLite (zalecana)
- `producer_sqlite.py` - Dodaje zadania do kolejki w bazie SQLite
- `consumer_sqlite.py` - Wykonuje zadania z kolejki z bazy SQLite  
- `queue_manager_sqlite.py` - Narzędzie do zarządzania kolejką SQLite
- `queue_db.py` - Model bazy danych i operacje na SQLite
- `queue.db` - Plik bazy danych SQLite (tworzony automatycznie)

### Wersja CSV (legacy)
- `producer.py` - Wersja z plikami CSV
- `consumer.py` - Wersja z plikami CSV
- `queue_manager.py` - Wersja z plikami CSV

## Zalety wersji SQLite

✅ **Thread-safe** - Bezpieczne współbieżne operacje  
✅ **ACID** - Atomowość, spójność, izolacja, trwałość  
✅ **Wydajność** - Indeksy i optymalizacje zapytań  
✅ **Skalowność** - Lepsze zarządzanie dużą liczbą zadań  
✅ **Integralność** - Kontrola spójności danych  
✅ **Zapytania** - Zaawansowane filtrowanie i sortowanie  

## Statusy zadań

- `pending` - Zadanie czeka na wykonanie
- `in_progress` - Zadanie jest wykonywane przez consumera
- `done` - Zadanie zostało wykonane

## Szybki start

### 1. Dodaj 100 zadań do kolejki
```bash
python producer_sqlite.py --count 100
```

### 2. Uruchom consumerów (każdy w osobnym terminalu)
```bash
# Terminal 1
python consumer_sqlite.py --id Operator1

# Terminal 2  
python consumer_sqlite.py --id Operator2

# Terminal 3
python consumer_sqlite.py --id Operator3
```

### 3. Lub użyj Queue Managera (zalecane)
```bash
python queue_manager_sqlite.py
```

## Szczegółowe instrukcje

### Producer SQLite (producer_sqlite.py)

**Dodanie pojedynczego zadania:**
```bash
python producer_sqlite.py
python producer_sqlite.py --task "Rozmowa z klientem VIP"
```

**Dodanie wielu zadań:**
```bash
python producer_sqlite.py --count 50
python producer_sqlite.py -c 100
```

### Consumer SQLite (consumer_sqlite.py)

**Uruchomienie consumera:**
```bash
python consumer_sqlite.py
python consumer_sqlite.py --id MójOperator
```

**Jak działa consumer:**
- Sprawdza kolejkę co 5 sekund
- Pobiera pierwsze dostępne zadanie (`pending`)
- Atomowo zmienia status na `in_progress`
- Wykonuje zadanie przez 30 sekund
- Atomowo zmienia status na `done`

### Queue Manager SQLite (queue_manager_sqlite.py)

Interaktywne narzędzie z rozszerzonym menu:

```bash
python queue_manager_sqlite.py
```

**Funkcje:**
1. **Statystyki** - Wyświetla stan kolejki
2. **Dodaj zadania** - Dodaje zadania przez producera
3. **Uruchom consumerów** - Uruchamia wielu consumerów w osobnych oknach
4. **Reset zadań** - Resetuje zadania `in_progress` do `pending`
5. **Wyczyść kolejkę** - Usuwa wszystkie zadania
6. **Monitorowanie** - Wyświetla statystyki w czasie rzeczywistym
7. **Lista zadań** - Szczegółowa lista wszystkich zadań
8. **Eksport CSV** - Eksportuje zadania do pliku CSV

## Struktura bazy danych

### Tabela `tasks`

```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,           -- Unikalny identyfikator zadania
    task_name TEXT NOT NULL,       -- Nazwa zadania
    status TEXT NOT NULL DEFAULT 'pending',  -- Status: pending/in_progress/done
    created_at TEXT NOT NULL,      -- Data utworzenia
    started_at TEXT,               -- Data rozpoczęcia (nullable)
    completed_at TEXT              -- Data zakończenia (nullable)
);

-- Indeksy dla wydajności
CREATE INDEX idx_status ON tasks(status);
CREATE INDEX idx_created_at ON tasks(created_at);
```

## Przykładowy scenariusz testowy

### Krok 1: Przygotowanie
```bash
# Uruchom Queue Manager SQLite
python queue_manager_sqlite.py

# W menu wybierz opcję 2 i dodaj 100 zadań
```

### Krok 2: Uruchomienie consumerów
```bash
# W menu wybierz opcję 3 i uruchom 5 consumerów
```

### Krok 3: Monitorowanie
```bash
# W menu wybierz opcję 6 aby monitorować postęp
```

## API bazy danych (queue_db.py)

### Główne metody

```python
from queue_db import queue_db

# Dodaj zadanie
task_id = queue_db.add_task("Nazwa zadania")

# Pobierz statystyki
stats = queue_db.get_stats()
# Returns: {'pending': 10, 'in_progress': 2, 'done': 5, 'total': 17}

# Pobierz zadanie do wykonania
task = queue_db.get_pending_task()

# Zarezerwuj zadanie
success = queue_db.claim_task(task_id)

# Zakończ zadanie
success = queue_db.complete_task(task_id)

# Resetuj zadania w trakcie
count = queue_db.reset_in_progress_tasks()

# Wyczyść kolejkę
count = queue_db.clear_all_tasks()
```

## Porównanie z wersją CSV

| Funkcja | CSV | SQLite |
|---------|-----|--------|
| Thread-safety | ⚠️ Lock na plik | ✅ Natywne |
| Wydajność | ❌ O(n) | ✅ O(log n) |
| Atomowość | ❌ Ręczna | ✅ Transakcje |
| Zapytania | ❌ Ograniczone | ✅ SQL |
| Skalowność | ❌ Wolne | ✅ Szybkie |
| Integralność | ❌ Brak | ✅ Kontrola |

## Migracja z CSV do SQLite

Jeśli masz dane w formacie CSV, możesz je zaimportować:

```python
import csv
from queue_db import queue_db

# Wczytaj dane z CSV
with open('queue.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Dodaj zadanie z zachowaniem statusu
        task_id = queue_db.add_task(row['task_name'])
        # Opcjonalnie: zaktualizuj status i daty
```

## Rozszerzenia systemu

System SQLite można łatwo rozszerzyć o:

### 1. Priorytety zadań
```sql
ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 0;
CREATE INDEX idx_priority ON tasks(priority DESC, created_at ASC);
```

### 2. Typy zadań
```sql
ALTER TABLE tasks ADD COLUMN task_type TEXT DEFAULT 'call';
CREATE INDEX idx_task_type ON tasks(task_type);
```

### 3. Retry mechanizm
```sql
ALTER TABLE tasks ADD COLUMN retry_count INTEGER DEFAULT 0;
ALTER TABLE tasks ADD COLUMN max_retries INTEGER DEFAULT 3;
```

### 4. Metryki wydajności
```sql
CREATE TABLE task_metrics (
    task_id TEXT,
    consumer_id TEXT,
    execution_time INTEGER,
    created_at TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);
```

## Troubleshooting

**Problem:** Database is locked  
**Rozwiązanie:** SQLite automatycznie zarządza blokadami, poczekaj chwilę

**Problem:** Consumer nie widzi zadań  
**Rozwiązanie:** Sprawdź czy baza `queue.db` istnieje i zawiera zadania

**Problem:** Zadania "utknęły" w statusie `in_progress`  
**Rozwiązanie:** Użyj Queue Manager opcja 4 aby zresetować zadania

**Problem:** Błędy współbieżności  
**Rozwiązanie:** SQLite obsługuje to automatycznie przez transakcje

## Monitoring i analityka

### Zapytania analityczne

```sql
-- Średni czas wykonania zadań
SELECT AVG(
    (julianday(completed_at) - julianday(started_at)) * 24 * 60 * 60
) as avg_execution_time_seconds
FROM tasks 
WHERE status = 'done';

-- Zadania według statusu w czasie
SELECT 
    date(created_at) as date,
    status,
    COUNT(*) as count
FROM tasks 
GROUP BY date(created_at), status
ORDER BY date DESC;

-- Top najdłużej wykonywanych zadań
SELECT 
    id,
    task_name,
    (julianday(completed_at) - julianday(started_at)) * 24 * 60 * 60 as duration_seconds
FROM tasks 
WHERE status = 'done'
ORDER BY duration_seconds DESC
LIMIT 10;
```

## Backup i restore

### Backup
```bash
# Backup całej bazy
cp queue.db queue_backup_$(date +%Y%m%d_%H%M%S).db

# Lub eksport do SQL
sqlite3 queue.db .dump > queue_backup.sql
```

### Restore
```bash
# Z kopii bazy
cp queue_backup_20240117_123000.db queue.db

# Z pliku SQL
sqlite3 queue_new.db < queue_backup.sql
```