#!/usr/bin/env python3
"""
Producer - odpowiedzialny za dodawanie zadań do kolejki
Każde uruchomienie dodaje jedno zadanie do pliku queue.csv
"""

import csv
import os
import time
from datetime import datetime
import uuid
import argparse

QUEUE_FILE = "queue.csv"
FIELDNAMES = ["id", "task_name", "status", "created_at", "started_at", "completed_at"]

def initialize_queue_file():
    """Inicjalizuje plik kolejki z nagłówkami jeśli nie istnieje"""
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"✅ Utworzono plik kolejki: {QUEUE_FILE}")

def add_task_to_queue(task_name):
    """Dodaje zadanie do kolejki"""
    task = {
        "id": str(uuid.uuid4())[:8],
        "task_name": task_name,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "started_at": "",
        "completed_at": ""
    }
    
    with open(QUEUE_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(task)
    
    print(f"📝 Dodano zadanie: {task['id']} - {task_name}")
    return task['id']

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
    parser = argparse.ArgumentParser(description="Producer - dodaje zadania do kolejki")
    parser.add_argument("--count", "-c", type=int, default=1, 
                       help="Liczba zadań do dodania (domyślnie: 1)")
    parser.add_argument("--task", "-t", type=str, 
                       help="Nazwa zadania (domyślnie: generowana automatycznie)")
    
    args = parser.parse_args()
    
    # Inicjalizuj plik kolejki
    initialize_queue_file()
    
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

if __name__ == "__main__":
    main()