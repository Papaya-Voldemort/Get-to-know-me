from flask import Flask, render_template, request

app = Flask(__name__)


# Homepage
@app.route('/')
def home():
    return render_template('home.html')


# About Me page
@app.route('/about')
def about():
    return render_template('about.html')


# Contact Me form (handles GET and POST requests)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form data (we'll print it for now)
        name = request.form.get('name')
        message = request.form.get('message')
        print(f"Message from {name}: {message}")
        return render_template('contact.html', thank_you=True)
    return render_template('contact.html', thank_you=False)


if __name__ == '__main__':
    app.run(debug=True)