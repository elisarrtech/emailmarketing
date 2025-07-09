from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/send')
def send_message():
    return render_template('send_message.html')

@app.route('/contacts')
def manage_contacts():
    return render_template('manage_contacts.html')

@app.route('/history')
def view_history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)

