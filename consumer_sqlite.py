#!/usr/bin/env python3
"""
Consumer SQLite - odpowiedzialny za wykonywanie zadań z kolejki w bazie SQLite
Działa w pętli, sprawdza co 5s czy są zadania do wykonania
"""

import time
import argparse
import random
from queue_db import queue_db

CHECK_INTERVAL = 5  # Sprawdzaj kolejkę co 5 sekund
TASK_DURATION = 30  # Każde zadanie trwa 30 sekund

class Consumer:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.tasks_completed = 0
        self.running = True
    
    def find_and_claim_task(self):
        """Znajduje zadanie 'pending' i zmienia jego status na 'in_progress'"""
        # Pobierz pierwsze dostępne zadanie
        task = queue_db.get_pending_task()
        
        if task:
            # Spróbuj je zarezerwować (może być race condition z innymi consumerami)
            if queue_db.claim_task(task['id']):
                # Pobierz zaktualizowane dane zadania
                tasks = queue_db.get_all_tasks()
                for t in tasks:
                    if t['id'] == task['id']:
                        return t
        
        return None
    
    def complete_task(self, task_id):
        """Oznacza zadanie jako wykonane"""
        return queue_db.complete_task(task_id)
    
    def execute_task(self, task):
        """Wykonuje zadanie (symulacja 30-sekundowej pracy)"""
        print(f"[Consumer-{self.consumer_id}] 🔄 Rozpoczynam: {task['id']} - {task['task_name']}")
        
        # Symulacja pracy - 30 sekund z wizualizacją postępu
        for i in range(TASK_DURATION):
            time.sleep(1)
            if (i + 1) % 10 == 0:
                print(f"[Consumer-{self.consumer_id}]    Postęp: {i + 1}/{TASK_DURATION}s...")
        
        # Oznacz jako wykonane
        success = self.complete_task(task['id'])
        self.tasks_completed += 1
        
        if success:
            print(f"[Consumer-{self.consumer_id}] ✅ Zakończono: {task['id']} - {task['task_name']}")
        else:
            print(f"[Consumer-{self.consumer_id}] ⚠️  Błąd przy kończeniu zadania: {task['id']}")
    
    def get_queue_stats(self):
        """Zwraca statystyki kolejki"""
        return queue_db.get_stats()
    
    def run(self):
        """Główna pętla consumera"""
        print(f"[Consumer-{self.consumer_id}] 🚀 Uruchomiono consumera (SQLite)")
        print(f"[Consumer-{self.consumer_id}] ⏱️  Sprawdzanie kolejki co {CHECK_INTERVAL}s")
        print(f"[Consumer-{self.consumer_id}] ⏳ Czas wykonania zadania: {TASK_DURATION}s")
        print("-" * 70)
        
        while self.running:
            try:
                # Sprawdź statystyki
                stats = self.get_queue_stats()
                
                if stats['total'] > 0:
                    print(f"[Consumer-{self.consumer_id}] 📊 Kolejka: "
                          f"Oczekujące={stats['pending']}, "
                          f"W trakcie={stats['in_progress']}, "
                          f"Wykonane={stats['done']}/{stats['total']}")
                
                # Spróbuj pobrać zadanie
                task = self.find_and_claim_task()
                
                if task:
                    # Wykonaj zadanie
                    self.execute_task(task)
                else:
                    # Brak zadań - czekaj
                    if stats['pending'] == 0 and stats['in_progress'] == 0 and stats['done'] > 0:
                        print(f"[Consumer-{self.consumer_id}] 🎉 Wszystkie zadania wykonane! "
                              f"(Wykonano: {self.tasks_completed})")
                    else:
                        print(f"[Consumer-{self.consumer_id}] 💤 Brak zadań, czekam {CHECK_INTERVAL}s...")
                    
                    time.sleep(CHECK_INTERVAL)
            
            except KeyboardInterrupt:
                print(f"\n[Consumer-{self.consumer_id}] 🛑 Zatrzymywanie...")
                self.running = False
                break
            except Exception as e:
                print(f"[Consumer-{self.consumer_id}] ❌ Błąd: {e}")
                time.sleep(CHECK_INTERVAL)
        
        print(f"[Consumer-{self.consumer_id}] 👋 Zakończono pracę. Wykonano zadań: {self.tasks_completed}")

def main():
    parser = argparse.ArgumentParser(description="Consumer SQLite - wykonuje zadania z kolejki")
    parser.add_argument("--id", type=str, default=None,
                       help="ID consumera (domyślnie: losowe)")
    
    args = parser.parse_args()
    
    # Wygeneruj ID consumera
    consumer_id = args.id if args.id else f"{random.randint(1000, 9999)}"
    
    # Utwórz i uruchom consumera
    consumer = Consumer(consumer_id)
    
    try:
        consumer.run()
    except KeyboardInterrupt:
        print(f"\n[Consumer-{consumer_id}] 🛑 Przerwano przez użytkownika")

if __name__ == "__main__":
    main()