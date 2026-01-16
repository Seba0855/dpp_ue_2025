#!/usr/bin/env python3
"""
Queue Manager SQLite - narzędzie do zarządzania kolejką i consumerami w bazie SQLite
"""

import os
import subprocess
import sys
import time
from datetime import datetime
from queue_db import queue_db

def show_stats():
    """Wyświetla statystyki kolejki"""
    stats = queue_db.get_stats()
    
    if stats['total'] == 0:
        print("📭 Kolejka jest pusta")
        return
    
    print("\n" + "=" * 70)
    print("📊 STATYSTYKI KOLEJKI (SQLite)")
    print("=" * 70)
    print(f"Łącznie zadań:        {stats['total']}")
    print(f"Oczekujące (pending): {stats['pending']}")
    print(f"W trakcie (in_progress): {stats['in_progress']}")
    print(f"Wykonane (done):      {stats['done']}")
    
    if stats['total'] > 0:
        progress = stats['done'] / stats['total'] * 100
        print(f"Postęp:               {stats['done']}/{stats['total']} ({progress:.1f}%)")
    
    print("=" * 70)
    
    # Pokaż przykładowe zadania
    pending_tasks = queue_db.get_tasks_by_status('pending', limit=5)
    if pending_tasks:
        print(f"\n⏳ Pierwsze 5 oczekujących zadań:")
        for task in pending_tasks:
            print(f"   - {task['id']}: {task['task_name']}")
    
    in_progress_tasks = queue_db.get_tasks_by_status('in_progress')
    if in_progress_tasks:
        print(f"\n🔄 Zadania w trakcie wykonywania:")
        for task in in_progress_tasks:
            print(f"   - {task['id']}: {task['task_name']} (od {task['started_at']})")

def clear_queue():
    """Czyści kolejkę"""
    count = queue_db.clear_all_tasks()
    if count > 0:
        print(f"🗑️  Usunięto {count} zadań z kolejki")
    else:
        print("ℹ️  Kolejka już jest pusta")

def reset_stuck_tasks():
    """Resetuje zadania 'in_progress' do 'pending'"""
    count = queue_db.reset_in_progress_tasks()
    
    if count > 0:
        print(f"🔄 Zresetowano {count} zadań do statusu 'pending'")
    else:
        print("ℹ️  Brak zadań do zresetowania")

def start_consumers(count):
    """Uruchamia wiele consumerów w osobnych oknach"""
    print(f"🚀 Uruchamianie {count} consumerów SQLite...")
    
    for i in range(1, count + 1):
        consumer_id = f"C{i:03d}"
        
        # Windows
        if sys.platform == "win32":
            cmd = f'start cmd /k "python consumer_sqlite.py --id {consumer_id}"'
            subprocess.Popen(cmd, shell=True)
        # Linux/Mac
        else:
            cmd = f'gnome-terminal -- python3 consumer_sqlite.py --id {consumer_id}'
            try:
                subprocess.Popen(cmd, shell=True)
            except:
                # Fallback dla systemów bez gnome-terminal
                cmd = f'xterm -e python3 consumer_sqlite.py --id {consumer_id} &'
                subprocess.Popen(cmd, shell=True)
        
        time.sleep(0.5)  # Małe opóźnienie między uruchomieniami
    
    print(f"✅ Uruchomiono {count} consumerów SQLite")

def show_detailed_tasks():
    """Wyświetla szczegółową listę zadań"""
    tasks = queue_db.get_all_tasks()
    
    if not tasks:
        print("📭 Brak zadań w kolejce")
        return
    
    print("\n" + "=" * 100)
    print("📋 SZCZEGÓŁOWA LISTA ZADAŃ")
    print("=" * 100)
    print(f"{'ID':<10} {'Nazwa':<30} {'Status':<12} {'Utworzono':<20} {'Rozpoczęto':<20} {'Zakończono':<20}")
    print("-" * 100)
    
    for task in tasks[:20]:  # Pokaż tylko pierwsze 20
        started = task['started_at'] or '-'
        completed = task['completed_at'] or '-'
        
        print(f"{task['id']:<10} {task['task_name'][:29]:<30} {task['status']:<12} "
              f"{task['created_at']:<20} {started:<20} {completed:<20}")
    
    if len(tasks) > 20:
        print(f"\n... i {len(tasks) - 20} więcej zadań")

def export_to_csv():
    """Eksportuje zadania do pliku CSV"""
    import csv
    
    tasks = queue_db.get_all_tasks()
    
    if not tasks:
        print("📭 Brak zadań do eksportu")
        return
    
    filename = f"queue_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'task_name', 'status', 'created_at', 'started_at', 'completed_at']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
    
    print(f"📄 Wyeksportowano {len(tasks)} zadań do pliku: {filename}")

def show_menu():
    """Wyświetla menu"""
    print("\n" + "=" * 70)
    print("🎛️  QUEUE MANAGER SQLite - Menu")
    print("=" * 70)
    print("1. Wyświetl statystyki kolejki")
    print("2. Dodaj zadania do kolejki")
    print("3. Uruchom consumerów")
    print("4. Resetuj zadania 'in_progress' do 'pending'")
    print("5. Wyczyść kolejkę")
    print("6. Monitoruj kolejkę (odświeżanie co 5s)")
    print("7. Pokaż szczegółową listę zadań")
    print("8. Eksportuj zadania do CSV")
    print("0. Wyjście")
    print("=" * 70)

def monitor_queue():
    """Monitoruje kolejkę w czasie rzeczywistym"""
    print("\n📡 Monitorowanie kolejki SQLite (Ctrl+C aby zatrzymać)...\n")
    
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
    print("🔧 Inicjalizacja bazy danych SQLite...")
    
    while True:
        show_menu()
        choice = input("\nWybierz opcję: ").strip()
        
        if choice == "1":
            show_stats()
        
        elif choice == "2":
            count = input("Ile zadań dodać? (domyślnie: 100): ").strip()
            count = int(count) if count else 100
            
            print(f"\n🚀 Dodawanie {count} zadań...")
            subprocess.run([sys.executable, "producer_sqlite.py", "--count", str(count)])
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
        
        elif choice == "7":
            show_detailed_tasks()
        
        elif choice == "8":
            export_to_csv()
        
        elif choice == "0":
            print("\n👋 Do widzenia!")
            break
        
        else:
            print("\n❌ Nieprawidłowa opcja!")
        
        input("\nNaciśnij Enter aby kontynuować...")

if __name__ == "__main__":
    main()