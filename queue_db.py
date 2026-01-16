#!/usr/bin/env python3
"""
Queue Database - model bazy danych SQLite dla systemu kolejkowania
"""

import sqlite3
import threading
from datetime import datetime
from typing import List, Dict, Optional
import uuid

# Globalne połączenie i lock dla thread-safety
_db_lock = threading.Lock()
DB_FILE = "queue.db"

class QueueDB:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Inicjalizuje bazę danych i tworzy tabelę zadań"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT
                )
            ''')
            
            # Indeksy dla lepszej wydajności
            conn.execute('CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON tasks(created_at)')
            
            conn.commit()
            conn.close()
    
    def add_task(self, task_name: str) -> str:
        """Dodaje nowe zadanie do kolejki"""
        task_id = str(uuid.uuid4())[:8]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            conn.execute('''
                INSERT INTO tasks (id, task_name, status, created_at)
                VALUES (?, ?, 'pending', ?)
            ''', (task_id, task_name, created_at))
            conn.commit()
            conn.close()
        
        return task_id
    
    def get_all_tasks(self) -> List[Dict]:
        """Pobiera wszystkie zadania z kolejki"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM tasks 
                ORDER BY created_at ASC
            ''')
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
        
        return tasks
    
    def get_pending_task(self) -> Optional[Dict]:
        """Pobiera pierwsze dostępne zadanie ze statusem 'pending'"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM tasks 
                WHERE status = 'pending' 
                ORDER BY created_at ASC 
                LIMIT 1
            ''')
            task = cursor.fetchone()
            conn.close()
        
        return dict(task) if task else None
    
    def claim_task(self, task_id: str) -> bool:
        """Zmienia status zadania na 'in_progress' i ustawia started_at"""
        started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute('''
                UPDATE tasks 
                SET status = 'in_progress', started_at = ?
                WHERE id = ? AND status = 'pending'
            ''', (started_at, task_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
        
        return rows_affected > 0
    
    def complete_task(self, task_id: str) -> bool:
        """Oznacza zadanie jako wykonane"""
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute('''
                UPDATE tasks 
                SET status = 'done', completed_at = ?
                WHERE id = ? AND status = 'in_progress'
            ''', (completed_at, task_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
        
        return rows_affected > 0
    
    def get_stats(self) -> Dict[str, int]:
        """Zwraca statystyki kolejki"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute('''
                SELECT 
                    status,
                    COUNT(*) as count
                FROM tasks 
                GROUP BY status
            ''')
            
            stats_raw = cursor.fetchall()
            
            # Pobierz też łączną liczbę
            cursor = conn.execute('SELECT COUNT(*) FROM tasks')
            total = cursor.fetchone()[0]
            
            conn.close()
        
        # Przygotuj statystyki
        stats = {'pending': 0, 'in_progress': 0, 'done': 0, 'total': total}
        
        for status, count in stats_raw:
            stats[status] = count
        
        return stats
    
    def reset_in_progress_tasks(self) -> int:
        """Resetuje zadania 'in_progress' do 'pending'"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute('''
                UPDATE tasks 
                SET status = 'pending', started_at = NULL
                WHERE status = 'in_progress'
            ''')
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
        
        return rows_affected
    
    def clear_all_tasks(self) -> int:
        """Usuwa wszystkie zadania z kolejki"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute('DELETE FROM tasks')
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
        
        return rows_affected
    
    def get_tasks_by_status(self, status: str, limit: int = None) -> List[Dict]:
        """Pobiera zadania o określonym statusie"""
        with _db_lock:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            
            query = 'SELECT * FROM tasks WHERE status = ? ORDER BY created_at ASC'
            params = [status]
            
            if limit:
                query += ' LIMIT ?'
                params.append(limit)
            
            cursor = conn.execute(query, params)
            tasks = [dict(row) for row in cursor.fetchall()]
            conn.close()
        
        return tasks

# Globalna instancja bazy danych
queue_db = QueueDB()