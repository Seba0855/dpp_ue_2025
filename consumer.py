#!/usr/bin/env python3
"""
Consumer - odpowiedzialny za wykonywanie zadań z kolejki
Działa w pętli, sprawdza co 5s czy są zadania do wykonania
"""

import csv
import os
import time
from datetime import datetime
import argparse
import threading
import random

QUEUE_FILE = "queue.csv"
FIELDNAMES = ["id", "task_name", "status", "created_at", "started_at", "completed_at"]
CHECK_INTERVAL = 5  # Sprawdzaj kolejkę co 5 sekund
TASK_DURATION = 30  # Każde zadanie trwa 30 sekund

# Lock do synchronizacji dostępu do pliku
file_lock = threading.Lock()

class Consumer:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.tasks_completed = 0
        self.running = True
    
    def read_queue(self):
        """Odczytuje wszystkie zadania z kolejki"""
        if not os.path.exists(QUEUE_FILE):
            return []
        
        with file_lock:
            with open(QUEUE_FILE, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
    
    def write_queue(self, tasks):
        """Zapisuje wszystkie zadania do kolejki"""
        with file_lock:
            with open(QUEUE_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerows(tasks)
    
    def find_and_claim_task(self):
        """Znajduje zadanie 'pending' i zmienia jego status na 'in_progress'"""
        tasks = self.read_queue()
        
        for task in tasks:
            if task['status'] == 'pending':
                # Znaleziono zadanie - zmień status
                task['status'] = 'in_progress'
                task['started_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Zapisz zmiany
                self.write_queue(tasks)
                
                return task
        
        return None
    
    def complete_task(self, task_id):
        """Oznacza zadanie jako wykonane"""
        tasks = self.read_queue()
        
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = 'done'
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.write_queue(tasks)
    
    def execute_task(self, task):
        """Wykonuje zadanie (symulacja 30-sekundowej pracy)"""
        print(f"[Consumer-{self.consumer_id}] 🔄 Rozpoczynam: {task['id']} - {task['task_name']}")
        
        # Symulacja pracy - 30 sekund z wizualizacją postępu
        for i in range(TASK_DURATION):
            time.sleep(1)
            if (i + 1) % 10 == 0:
                print(f"[Consumer-{self.consumer_id}]    Postęp: {i + 1}/{TASK_DURATION}s...")
        
        # Oznacz jako wykonane
        self.complete_task(task['id'])
        self.tasks_completed += 1
        
        print(f"[Consumer-{self.consumer_id}] ✅ Zakończono: {task['id']} - {task['task_name']}")
    
    def get_queue_stats(self):
        """Zwraca statystyki kolejki"""
        tasks = self.read_queue()
        
        pending = sum(1 for t in tasks if t['status'] == 'pending')
        in_progress = sum(1 for t in tasks if t['status'] == 'in_progress')
        done = sum(1 for t in tasks if t['status'] == 'done')
        
        return {
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'total': len(tasks)
        }
    
    def run(self):
        """Główna pętla consumera"""
        print(f"[Consumer-{self.consumer_id}] 🚀 Uruchomiono consumera")
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
    parser = argparse.ArgumentParser(description="Consumer - wykonuje zadania z kolejki")
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