from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializace databáze
def init_db():
    conn = sqlite3.connect('fridge.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manufacture_date TEXT,
            purchase_date TEXT NOT NULL,
            min_durability_date TEXT NOT NULL,
            consumption_date TEXT,
            photo TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('fridge.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    errors = []
    now = datetime.now()
    edit_item = None

    # Načtení položky pro editaci
    if 'edit' in request.args:
        item_id = request.args.get('edit')
        edit_item = conn.execute('SELECT * FROM food_items WHERE id = ?', (item_id,)).fetchone()

    # Zpracování formuláře
    if request.method == 'POST':
        data = {
            'id': request.form.get('id'),
            'name': request.form.get('name', '').strip(),
            'purchase_date': request.form.get('purchase_date'),
            'min_durability_date': request.form.get('min_durability_date'),
            'manufacture_date': request.form.get('manufacture_date') or None,
            'consumption_date': request.form.get('consumption_date') or None,
            'photo': edit_item['photo'] if edit_item else None
        }

        # Validace povinných polí
        if not data['name']:
            errors.append("Název je povinný.")
        if not data['purchase_date']:
            errors.append("Datum nákupu je povinné.")
        if not data['min_durability_date']:
            errors.append("Datum minimální trvanlivosti je povinné.")

        # Validace datových vztahů
        if data['manufacture_date'] and data['purchase_date']:
            dv = datetime.fromisoformat(data['manufacture_date'])
            dn = datetime.fromisoformat(data['purchase_date'])
            if dn < dv:
                errors.append("Datum nákupu nesmí být dřívější než datum výroby.")

        # Nahrání fotky
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data['photo'] = filename

        if not errors:
            try:
                if data['id']:
                    conn.execute('''
                        UPDATE food_items SET
                        name=?, manufacture_date=?, purchase_date=?,
                        min_durability_date=?, consumption_date=?, photo=?
                        WHERE id=?
                    ''', (
                        data['name'], data['manufacture_date'], data['purchase_date'],
                        data['min_durability_date'], data['consumption_date'], data['photo'], data['id']
                    ))
                else:
                    conn.execute('''
                        INSERT INTO food_items 
                        (name, manufacture_date, purchase_date, min_durability_date, consumption_date, photo)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        data['name'], data['manufacture_date'], data['purchase_date'],
                        data['min_durability_date'], data['consumption_date'], data['photo']
                    ))
                conn.commit()
                return redirect(url_for('index'))
            except Exception as e:
                errors.append(f"Chyba databáze: {str(e)}")

    # Smazání záznamu
    if 'delete' in request.args:
        conn.execute('DELETE FROM food_items WHERE id=?', (request.args.get('id'),))
        conn.commit()
        return redirect(url_for('index'))

    # Načtení a výpočet PS
    items = conn.execute('''
        SELECT *, 
        COALESCE(consumption_date, min_durability_date) AS end_date,
        COALESCE(manufacture_date, purchase_date) AS start_date
        FROM food_items
    ''').fetchall()

    # Přidání PS
    items = [
        {
            **dict(item),
            'ps': (
                datetime.fromisoformat(item['start_date']) + 
                (datetime.fromisoformat(item['end_date']) - datetime.fromisoformat(item['start_date'])) / 2
            ).date().isoformat()
        }
        for item in items
    ]

    # Řazení
    items.sort(key=lambda x: (
        datetime.fromisoformat(x['end_date']) < now,
        datetime.fromisoformat(x['ps'])
    ))

    conn.close()
    return render_template(
        'index.html',
        items=items,
        errors=errors,
        edit_item=edit_item,
        now=now,
        datetime=datetime
    )

if __name__ == '__main__':
    app.run(debug=True)
