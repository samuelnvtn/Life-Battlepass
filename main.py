from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import sqlite3


app = Flask(__name__)
DATABASE = '/Users/samuelnovotny/Desktop/dev/projekty/life battlepass/Life-Battlepass/identifier.sqlite'


# Funkce pro připojení k databázi
def get_db_connection():
    conn = sqlite3.connect(DATABASE,  timeout=10)
    conn.row_factory = sqlite3.Row  # Umožní přístup k datům jako slovníku
    return conn


# Hlavní stránka - seznam úkolů
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM task ORDER BY completed ASC, completed_date DESC, due_date ASC').fetchall()
    operations = conn.execute('SELECT * FROM operation ORDER BY end_date ASC').fetchall()
    rewards = conn.execute('SELECT * FROM battlepass_reward').fetchall()

    # Fetch total XP from the user
    user = conn.execute('SELECT total_xp FROM user WHERE user_id = 1').fetchone()
    total_xp = user['total_xp'] if user else 0

    conn.close()

#novinka
    operation_data = []
    today = datetime.today()
    task_data = []

   # TODO: odpocet hodin pokud mene jak 24h

    task_data = []
    for task in tasks:
        due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
        remaining_days = max((due_date - today).days, 0)  # Nastavte na 0, pokud je datum v minulosti

        task_data.append({
            'id': task['id'],
            'name': task['name'],
            'description': task['description'],
            'created_date': task['created_date'],
            'due_date': task['due_date'],
            'xp_reward': task['xp_reward'],
            'task_type': task['task_type'],
            'remaining_days': remaining_days,
            'completed': task['completed'],
            'operation_id': task['operation_id']
        })

    for operation in operations:
        end_date = datetime.strptime(operation['end_date'], '%Y-%m-%d')
        remaining_days = max((end_date - today).days, 0)  # Záporné hodnoty nastavíme na 0
        completed = operation['current_xp'] >= operation['xp_goal']  # Kontrola, zda je operace dokončena

        operation_data.append({
            'id': operation['id'],
            'name': operation['name'],
            'description': operation['description'],
            'current_xp': operation['current_xp'],
            'current_level': operation['current_xp'] // 1000,
            'max_level': operation['xp_goal'] // 1000,
            'remaining_days': remaining_days,
            'completed': completed,
            'image_url': operation['image_url'],
            'icon_url': operation['icon_url'],
        })
#konec novinky

    # Optionally fetch details for a specific operation (e.g., from a query parameter or session)
    operation = None
    if 'operation_id' in request.args:
        operation_id = request.args['operation_id']
        conn = get_db_connection()
        operation = conn.execute('SELECT * FROM operation WHERE id = ?', (operation_id,)).fetchone()
        conn.close()

    return render_template('index.html', tasks=task_data, operations=operation_data, operation=operation, rewards=rewards, total_xp=total_xp)


# Stránka pro přidání úkolu
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Handle the POST request (form submission)
        name = request.form['name']
        description = request.form['description']
        xp_reward = request.form['xp_reward']
        due_date = request.form['due_date']
        task_type = request.form['task_type']
        operation_id = request.form['operation_id']

        if task_type not in ['Daily', 'Weekly']:
            return redirect('/add_task')

        created_date = datetime.now().strftime('%Y-%m-%d')

        # Insert data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO task (name, description, xp_reward, created_date, due_date, task_type, operation_id, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (name, description, xp_reward, created_date, due_date, task_type, operation_id, 0))
        conn.commit()
        conn.close()

        return redirect('/')  # Redirect back to the main page after adding a task

    # If GET request, render the form page
    conn = get_db_connection()
    operations = conn.execute('SELECT * FROM operation').fetchall()  # Get all operations
    conn.close()

    return render_template('add_task.html', operations=operations)  # Render form for adding task




@app.route('/operations')
def operations():
    conn = get_db_connection()
    operations = conn.execute('SELECT * FROM operation').fetchall()
    conn.close()
    return render_template('index.html', operations=operations)



@app.route('/add_operation', methods=['GET', 'POST'])
def add_operation():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        xp_goal = int(request.form['xp_goal'])  # Převod na celé číslo
        description = request.form['description']
        image_url = request.form['image_url']
        icon_url = request.form['icon_url']

        max_level = xp_goal // 1000

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO operation (name, start_date, end_date, xp_goal, description, image_url, current_xp, icon_url, max_level, current_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (name, start_date, end_date, xp_goal, description, image_url, 0, icon_url, max_level, 0))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_operation.html')

@app.route('/operation/<int:operation_id>')
def operation_details(operation_id):
    conn = get_db_connection()
    operation = conn.execute('SELECT * FROM operation WHERE id = ?', (operation_id,)).fetchone()
    tasks = conn.execute('SELECT * FROM task WHERE operation_id = ?', (operation_id,)).fetchall()
    rewards = conn.execute('SELECT * FROM battlepass_reward WHERE operation_id = ?', (operation_id,)).fetchall()  # Fetch rewards
    conn.close()
    return render_template('index.html', operation=operation, tasks=tasks, rewards=rewards)

@app.route('/add_reward', methods=['GET', 'POST'])
def add_reward():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        xp_required = request.form['xp_required']
        image_url = request.form['image_url']
        operation_id = request.form['operation_id']  # Get the selected operation ID

        # Insert data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO battlepass_reward (name, xp_required, image_path, operation_id) VALUES (?, ?, ?, ?)',
                     (name, xp_required, image_url, operation_id))
        conn.commit()
        conn.close()

        return redirect('/')  # Redirect to homepage after adding reward

    # If GET request, fetch operations and render the form
    conn = get_db_connection()
    operations = conn.execute('SELECT * FROM operation').fetchall()  # Get all operations
    conn.close()

    return render_template('add_reward.html', operations=operations)  # Pass operations to the template


@app.route('/mark_task_completed/<int:task_id>', methods=['POST'])
def mark_task_completed(task_id):
    conn = get_db_connection()

    # Fetch the task details
    task = conn.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()
    if not task or task['completed'] == 1:
        conn.close()
        return jsonify({'success': False, 'message': 'Task not found or already completed'}), 400

    xp_reward = task['xp_reward']
    operation_id = task['operation_id']

    # Fetch the operation details
    operation = conn.execute('SELECT * FROM operation WHERE id = ?', (operation_id,)).fetchone()
    if not operation:
        conn.close()
        return jsonify({'success': False, 'message': 'Operation not found'}), 400

    current_xp = operation['current_xp']
    xp_goal = operation['xp_goal']

    # Calculate how much XP can be added to current_xp without exceeding xp_goal
    xp_to_add_to_operation = min(xp_reward, max(0, xp_goal - current_xp))
    xp_to_add_to_total = xp_reward

    # Update current_xp in operation, but do not exceed xp_goal
    if xp_to_add_to_operation > 0:
        conn.execute('UPDATE operation SET current_xp = current_xp + ? WHERE id = ?',
                     (xp_to_add_to_operation, operation_id))
        conn.commit()

    # Always add all XP to total_xp
    conn.execute('UPDATE user SET total_xp = total_xp + ? WHERE user_id = 1', (xp_to_add_to_total,))
    conn.commit()

    # Update current_level based on current_xp
    updated_operation = conn.execute('SELECT current_xp, xp_goal FROM operation WHERE id = ?', (operation_id,)).fetchone()
    current_level = updated_operation['current_xp'] // 1000

    conn.execute('UPDATE operation SET current_level = ? WHERE id = ?', (current_level, operation_id))
    conn.commit()

    # Mark the task as completed and set the completed_date to the current date
    completed_date = datetime.now().strftime('%Y-%m-%d')
    conn.execute('UPDATE task SET completed = 1, completed_date = ? WHERE id = ?', (completed_date, task_id))
    conn.commit()

    # Fetch updated values
    updated_xp = updated_operation['current_xp']
    total_xp = conn.execute('SELECT total_xp FROM user WHERE user_id = 1').fetchone()['total_xp']
    max_level = updated_operation['xp_goal'] // 1000
    completed = updated_xp >= xp_goal

    conn.close()

    return jsonify({
        'success': True,
        'task_id': task_id,
        'xp_reward': xp_reward,
        'total_xp': total_xp,
        'operation_id': operation_id,
        'current_xp': updated_xp,
        'operation_xp_goal': xp_goal,
        'current_level': current_level,
        'max_level': max_level,
        'completed': completed  # Přidání atributu

    })




if __name__ == '__main__':
    app.run(debug=True, port=5000)
