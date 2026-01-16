# System Kolejkowania - Symulacja Infolinii

System kolejkowania oparty na plikach CSV, symulujący pracę infolinii z operatorami.

## Pliki systemu

- `producer.py` - Dodaje zadania do kolejki
- `consumer.py` - Wykonuje zadania z kolejki  
- `queue_manager.py` - Narzędzie do zarządzania kolejką
- `queue.csv` - Plik kolejki (tworzony automatycznie)

## Statusy zadań

- `pending` - Zadanie czeka na wykonanie
- `in_progress` - Zadanie jest wykonywane przez consumera
- `done` - Zadanie zostało wykonane

## Szybki start

### 1. Dodaj 100 zadań do kolejki
```bash
python producer.py --count 100
```

### 2. Uruchom consumerów (każdy w osobnym terminalu)
```bash
# Terminal 1
python consumer.py --id Operator1

# Terminal 2  
python consumer.py --id Operator2

# Terminal 3
python consumer.py --id Operator3
```

### 3. Lub użyj Queue Managera (zalecane)
```bash
python queue_manager.py
```

## Szczegółowe instrukcje

### Producer (producer.py)

**Dodanie pojedynczego zadania:**
```bash
python producer.py
python producer.py --task "Rozmowa z klientem VIP"
```

**Dodanie wielu zadań:**
```bash
python producer.py --count 50
python producer.py -c 100
```

### Consumer (consumer.py)

**Uruchomienie consumera:**
```bash
python consumer.py
python consumer.py --id MójOperator
```

**Jak działa consumer:**
- Sprawdza kolejkę co 5 sekund
- Pobiera pierwsze dostępne zadanie (`pending`)
- Zmienia status na `in_progress`
- Wykonuje zadanie przez 30 sekund
- Zmienia status na `done`

### Queue Manager (queue_manager.py)

Interaktywne narzędzie z menu:

```bash
python queue_manager.py
```

**Funkcje:**
1. **Statystyki** - Wyświetla stan kolejki
2. **Dodaj zadania** - Dodaje zadania przez producera
3. **Uruchom consumerów** - Uruchamia wielu consumerów w osobnych oknach
4. **Reset zadań** - Resetuje zadania `in_progress` do `pending`
5. **Wyczyść kolejkę** - Usuwa wszystkie zadania
6. **Monitorowanie** - Wyświetla statystyki w czasie rzeczywistym

## Przykładowy scenariusz testowy

### Krok 1: Przygotowanie
```bash
# Uruchom Queue Manager
python queue_manager.py

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

## Format pliku kolejki (queue.csv)

```csv
id,task_name,status,created_at,started_at,completed_at
a1b2c3d4,Rozmowa telefoniczna #1,pending,2024-01-17 10:30:00,,
e5f6g7h8,Rozmowa telefoniczna #2,in_progress,2024-01-17 10:30:01,2024-01-17 10:30:15,
i9j0k1l2,Rozmowa telefoniczna #3,done,2024-01-17 10:30:02,2024-01-17 10:30:20,2024-01-17 10:30:50
```

## Zalety systemu

✅ **Skalowalne** - Można uruchomić dowolną liczbę consumerów  
✅ **Odporne na awarie** - Zadania są trwale zapisane w pliku  
✅ **Monitorowalne** - Pełne statystyki i historia zadań  
✅ **Priorytetyzowalne** - Można łatwo dodać system priorytetów  
✅ **Analityczne** - Wszystkie czasy są rejestrowane  

## Symulacja różnych scenariuszy

### Scenariusz 1: Przeciążenie systemu
```bash
# Dodaj dużo zadań
python producer.py --count 500

# Uruchom tylko 2 consumerów
python consumer.py --id Op1 &
python consumer.py --id Op2 &
```

### Scenariusz 2: Skalowanie w górę
```bash
# Podczas pracy dodaj więcej consumerów
python consumer.py --id Op3 &
python consumer.py --id Op4 &
python consumer.py --id Op5 &
```

### Scenariusz 3: Awaria i odzyskiwanie
```bash
# Zatrzymaj consumerów (Ctrl+C)
# Zadania 'in_progress' można zresetować przez Queue Manager (opcja 4)
# Uruchom consumerów ponownie
```

## Rozszerzenia systemu

System można łatwo rozszerzyć o:
- **Priorytety zadań** - Dodanie kolumny `priority`
- **Typy zadań** - Różne rodzaje operacji
- **Retry mechanizm** - Ponowne próby dla nieudanych zadań
- **Load balancing** - Inteligentne rozdzielanie zadań
- **Metryki** - Szczegółowe statystyki wydajności
- **Web UI** - Interfejs webowy do monitorowania

## Troubleshooting

**Problem:** Consumer nie widzi zadań  
**Rozwiązanie:** Sprawdź czy plik `queue.csv` istnieje i zawiera zadania ze statusem `pending`

**Problem:** Zadania "utknęły" w statusie `in_progress`  
**Rozwiązanie:** Użyj Queue Manager opcja 4 aby zresetować zadania

**Problem:** Błędy dostępu do pliku  
**Rozwiązanie:** Upewnij się że tylko jeden proces modyfikuje plik w danym momencie