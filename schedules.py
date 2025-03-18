import sqlite3
import time

def connect_db():
    return sqlite3.connect('assistant.db')

def create_tables(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todo_lists (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL
                        );''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            list_id INTEGER,
                            description TEXT NOT NULL,
                            is_done BOOLEAN DEFAULT 0,
                            FOREIGN KEY (list_id) REFERENCES todo_lists (id)
                        );''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS meetings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            start_time TEXT NOT NULL,
                            end_time TEXT NOT NULL
                        );''')

        conn.execute('''CREATE TABLE IF NOT EXISTS reminders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            message TEXT,
                            time TEXT NOT NULL,
                            is_alarm BOOLEAN DEFAULT 0
                        );''')

def add_todo_list(conn, name):
    with conn:
        conn.execute('INSERT INTO todo_lists (name) VALUES (?)', (name,))

def add_task(conn, list_id, description):
    with conn:
        conn.execute('INSERT INTO tasks (list_id, description) VALUES (?, ?)', (list_id, description))

def get_todo_lists(conn):
    return conn.execute('SELECT * FROM todo_lists').fetchall()

def get_tasks(conn, list_id):
    return conn.execute('SELECT * FROM tasks WHERE list_id = ?', (list_id,)).fetchall()

def mark_task_done(conn, task_id):
    with conn:
        conn.execute('UPDATE tasks SET is_done = 1 WHERE id = ?', (task_id,))

def mark_task_undone(conn, task_id):
    with conn:
        conn.execute('UPDATE tasks SET is_done = 0 WHERE id = ?', (task_id,))

def delete_task(conn, task_id):
    with conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

def add_meeting(conn, title, description, start_time, end_time):
    with conn:
        conn.execute('''INSERT INTO meetings (title, description, start_time, end_time)
                        VALUES (?, ?, ?, ?)''', (title, description, start_time, end_time))

def get_meetings(conn):
    return conn.execute('SELECT * FROM meetings').fetchall()

def update_meeting(conn, meeting_id, title, description, start_time, end_time):
    with conn:
        conn.execute('''UPDATE meetings
                        SET title = ?, description = ?, start_time = ?, end_time = ?
                        WHERE id = ?''', (title, description, start_time, end_time, meeting_id))

def delete_meeting(conn, meeting_id):
    with conn:
        conn.execute('DELETE FROM meetings WHERE id = ?', (meeting_id,))

def add_reminder(conn, title, message, time, is_alarm=False):
    with conn:
        conn.execute('''INSERT INTO reminders (title, message, time, is_alarm)
                        VALUES (?, ?, ?, ?)''', (title, message, time, is_alarm))

def get_reminders(conn):
    return conn.execute('SELECT * FROM reminders').fetchall()

def update_reminder(conn, reminder_id, title, message, time, is_alarm):
    with conn:
        conn.execute('''UPDATE reminders
                        SET title = ?, message = ?, time = ?, is_alarm = ?
                        WHERE id = ?''', (title, message, time, is_alarm, reminder_id))

def delete_reminder(conn, reminder_id):
    with conn:
        conn.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))

def stopwatch():
    print("Press ENTER to start the stopwatch and press ENTER again to stop it.")
    input()
    start_time = time.time()
    print("Stopwatch started...")
    input()
    elapsed_time = time.time() - start_time
    print(f"Stopwatch stopped. Elapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")

def timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")