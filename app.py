import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for cross-origin requests
CORS(app, resources={r"/*": {"origins": "https://your-frontend-domain.vercel.app"}})

# Configure mail server settings
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    messages = []
    try:
        with open('messages.txt', 'r') as f:
            content = f.read()
            messages = content.split('---\n')[:-1]
    except FileNotFoundError:
        pass

    return render_template('admin.html', messages=messages)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_email = request.form["email"]
        user_message = request.form["message"]

        try:
            # Save message to file
            with open('messages.txt', 'a') as f:
                f.write(f"Sender: {user_email}\nMessage: {user_message}\n---\n")

            # Send message to your email
            message_to_me = Message(
                "New Message from Contact Form",
                sender=app.config['MAIL_USERNAME'],
                recipients=["your-email@zoho.com"]
            )
            message_to_me.body = f"Sender: {user_email}\n\nMessage: {user_message}"
            mail.send(message_to_me)

            # Send auto-reply
            message_to_user = Message(
                "Thank you for reaching out!",
                sender=app.config['MAIL_USERNAME'],
                recipients=[user_email]
            )
            message_to_user.body = "Thank you for your message! I'll get back to you soon."
            mail.send(message_to_user)

            return render_template("contact.html", thank_you=True)
        except Exception as e:
            print(f"Error: {e}")
            return render_template("contact.html", error="Failed to send your message. Please try again later.")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
