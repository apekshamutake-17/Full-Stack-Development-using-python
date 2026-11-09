
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "shayarisafar_secret_key"


# Home Page
@app.route('/')
def home():
    return redirect(url_for('login'))


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or not email or not password:
            flash("All fields are required!")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        if len(password) < 8:
            flash("Password must be at least 8 characters!")
            return redirect(url_for('register'))

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            flash("Email already registered!")
        else:
            hashed_password = generate_password_hash(password)
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please login.")

        cur.close()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, password FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))

        flash("Invalid email or password!")

    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', name=session['user_name'])


# Quotes Page with Categories
@app.route('/quotes')
def quotes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    category = request.args.get('category')

    conn = get_db_connection()
    cur = conn.cursor()

    if category:
        cur.execute(
            "SELECT * FROM quotes WHERE category = %s ORDER BY id",
            (category,)
        )
    else:
        cur.execute("SELECT * FROM quotes ORDER BY id")

    all_quotes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('quotes.html', quotes=all_quotes, category=category)


# Add to Favourites
@app.route('/add_favourite/<int:quote_id>')
def add_favourite(quote_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO favourites (user_id, quote_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (session['user_id'], quote_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    flash("Quote added to Favourites!")
    return redirect(url_for('quotes'))


# My Favourites
@app.route('/favourites')
def favourites():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT quotes.* FROM quotes
        JOIN favourites ON quotes.id = favourites.quote_id
        WHERE favourites.user_id = %s
        ORDER BY quotes.id
    """, (session['user_id'],))

    my_favourites = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('favourites.html', quotes=my_favourites)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
