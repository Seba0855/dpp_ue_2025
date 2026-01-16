#!/usr/bin/env python3
"""
Queue Manager - narzędzie do zarządzania kolejką i consumerami
"""

import csv
import os
import subprocess
import sys
import time
from datetime import datetime

QUEUE_FILE = "queue.csv"
FIELDNAMES = ["id", "task_name", "status", "created_at", "started_at", "completed_at"]

def read_queue():
    """Odczytuje kolejkę"""
    if not os.path.exists(QUEUE_FILE):
        return []
    
    with open(QUEUE_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def show_stats():
    """Wyświetla statystyki kolejki"""
    tasks = read_queue()
    
    if not tasks:
        print("📭 Kolejka jest pusta")
        return
    
    pending = [t for t in tasks if t['status'] == 'pending']
    in_progress = [t for t in tasks if t['status'] == 'in_progress']
    done = [t for t in tasks if t['status'] == 'done']
    
    print("\n" + "=" * 70)
    print("📊 STATYSTYKI KOLEJKI")
    print("=" * 70)
    print(f"Łącznie zadań:        {len(tasks)}")
    print(f"Oczekujące (pending): {len(pending)}")
    print(f"W trakcie (in_progress): {len(in_progress)}")
    print(f"Wykonane (done):      {len(done)}")
    print(f"Postęp:               {len(done)}/{len(tasks)} ({len(done)/len(tasks)*100:.1f}%)")
    print("=" * 70)
    
    if pending:
        print(f"\n⏳ Pierwsze 5 oczekujących zadań:")
        for task in pending[:5]:
            print(f"   - {task['id']}: {task['task_name']}")
    
    if in_progress:
        print(f"\n🔄 Zadania w trakcie wykonywania:")
        for task in in_progress:
            print(f"   - {task['id']}: {task['task_name']} (od {task['started_at']})")

def clear_queue():
    """Czyści kolejkę"""
    if os.path.exists(QUEUE_FILE):
        os.remove(QUEUE_FILE)
        print("🗑️  Wyczyszczono kolejkę")
    else:
        print("ℹ️  Kolejka już jest pusta")

def reset_stuck_tasks():
    """Resetuje zadania 'in_progress' do 'pending'"""
    tasks = read_queue()
    
    if not tasks:
        print("📭 Kolejka jest pusta")
        return
    
    reset_count = 0
    for task in tasks:
        if task['status'] == 'in_progress':
            task['status'] = 'pending'
            task['started_at'] = ''
            reset_count += 1
    
    if reset_count > 0:
        with open(QUEUE_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(tasks)
        
        print(f"🔄 Zresetowano {reset_count} zadań do statusu 'pending'")
    else:
        print("ℹ️  Brak zadań do zresetowania")

def start_consumers(count):
    """Uruchamia wiele consumerów w osobnych oknach"""
    print(f"🚀 Uruchamianie {count} consumerów...")
    
    for i in range(1, count + 1):
        consumer_id = f"C{i:03d}"
        
        # Windows
        if sys.platform == "win32":
            cmd = f'start cmd /k "python consumer.py --id {consumer_id}"'
            subprocess.Popen(cmd, shell=True)
        # Linux/Mac
        else:
            cmd = f'gnome-terminal -- python3 consumer.py --id {consumer_id}'
            try:
                subprocess.Popen(cmd, shell=True)
            except:
                # Fallback dla systemów bez gnome-terminal
                cmd = f'xterm -e python3 consumer.py --id {consumer_id} &'
                subprocess.Popen(cmd, shell=True)
        
        time.sleep(0.5)  # Małe opóźnienie między uruchomieniami
    
    print(f"✅ Uruchomiono {count} consumerów")

def show_menu():
    """Wyświetla menu"""
    print("\n" + "=" * 70)
    print("🎛️  QUEUE MANAGER - Menu")
    print("=" * 70)
    print("1. Wyświetl statystyki kolejki")
    print("2. Dodaj zadania do kolejki")
    print("3. Uruchom consumerów")
    print("4. Resetuj zadania 'in_progress' do 'pending'")
    print("5. Wyczyść kolejkę")
    print("6. Monitoruj kolejkę (odświeżanie co 5s)")
    print("0. Wyjście")
    print("=" * 70)

def monitor_queue():
    """Monitoruje kolejkę w czasie rzeczywistym"""
    print("\n📡 Monitorowanie kolejki (Ctrl+C aby zatrzymać)...\n")
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"🕐 Ostatnia aktualizacja: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            show_stats()
            print("\n(Odświeżanie co 5 sekund, Ctrl+C aby zatrzymać)")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n✋ Zatrzymano monitorowanie")

def main():
    """Główna funkcja menu"""
    while True:
        show_menu()
        choice = input("\nWybierz opcję: ").strip()
        
        if choice == "1":
            show_stats()
        
        elif choice == "2":
            count = input("Ile zadań dodać? (domyślnie: 100): ").strip()
            count = int(count) if count else 100
            
            print(f"\n🚀 Dodawanie {count} zadań...")
            subprocess.run([sys.executable, "producer.py", "--count", str(count)])
            print("\n✅ Zadania dodane!")
        
        elif choice == "3":
            count = input("Ile consumerów uruchomić? (domyślnie: 3): ").strip()
            count = int(count) if count else 3
            start_consumers(count)
        
        elif choice == "4":
            reset_stuck_tasks()
        
        elif choice == "5":
            confirm = input("Czy na pewno chcesz wyczyścić kolejkę? (tak/nie): ").strip().lower()
            if confirm in ['tak', 'yes', 't', 'y']:
                clear_queue()
        
        elif choice == "6":
            monitor_queue()
        
        elif choice == "0":
            print("\n👋 Do widzenia!")
            break
        
        else:
            print("\n❌ Nieprawidłowa opcja!")
        
        input("\nNaciśnij Enter aby kontynuować...")

if __name__ == "__main__":
    main()