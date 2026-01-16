#!/usr/bin/env python3
"""
Producer SQLite - odpowiedzialny za dodawanie zadań do kolejki w bazie SQLite
Każde uruchomienie dodaje jedno lub więcej zadań do bazy danych
"""

import time
import argparse
from queue_db import queue_db

def add_task_to_queue(task_name):
    """Dodaje zadanie do kolejki"""
    task_id = queue_db.add_task(task_name)
    print(f"📝 Dodano zadanie: {task_id} - {task_name}")
    return task_id

def add_multiple_tasks(count):
    """Dodaje wiele zadań do kolejki"""
    print(f"🚀 Dodawanie {count} zadań do kolejki...")
    
    for i in range(1, count + 1):
        task_name = f"Rozmowa telefoniczna #{i}"
        add_task_to_queue(task_name)
        
        # Małe opóźnienie żeby nie przeciążyć systemu
        if i % 10 == 0:
            print(f"   Dodano {i}/{count} zadań...")
            time.sleep(0.1)
    
    print(f"✅ Dodano wszystkie {count} zadań do kolejki!")

def main():
    parser = argparse.ArgumentParser(description="Producer SQLite - dodaje zadania do kolejki")
    parser.add_argument("--count", "-c", type=int, default=1, 
                       help="Liczba zadań do dodania (domyślnie: 1)")
    parser.add_argument("--task", "-t", type=str, 
                       help="Nazwa zadania (domyślnie: generowana automatycznie)")
    
    args = parser.parse_args()
    
    # Inicjalizuj bazę danych (zostanie utworzona jeśli nie istnieje)
    print("🔧 Inicjalizacja bazy danych...")
    
    if args.count == 1 and args.task:
        # Dodaj pojedyncze zadanie z niestandardową nazwą
        add_task_to_queue(args.task)
    elif args.count == 1:
        # Dodaj pojedyncze zadanie z domyślną nazwą
        task_name = f"Rozmowa telefoniczna #{int(time.time())}"
        add_task_to_queue(task_name)
    else:
        # Dodaj wiele zadań
        add_multiple_tasks(args.count)
    
    # Pokaż statystyki
    stats = queue_db.get_stats()
    print(f"\n📊 Aktualne statystyki kolejki:")
    print(f"   Łącznie zadań: {stats['total']}")
    print(f"   Oczekujące: {stats['pending']}")
    print(f"   W trakcie: {stats['in_progress']}")
    print(f"   Wykonane: {stats['done']}")

if __name__ == "__main__":
    main()