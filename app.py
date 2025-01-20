import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure mail server settings using environment variables for security
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True  # Secure connection using SSL
app.config['MAIL_USERNAME'] = "admin@elinelson.me"  # Your Zoho email
app.config['MAIL_PASSWORD'] = "Elin2010!!"  # Your Zoho password or app password

mail = Mail(app)


# Homepage
@app.route('/')
def home():
    return render_template('home.html')


# About Me page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/admin')
def admin():
    messages = []
    try:
        with open('messages.txt', 'r') as f:
            content = f.read()
            messages = content.split('---\n')[:-1]  # Split messages by separator
    except FileNotFoundError:
        pass

    return render_template('admin.html', messages=messages)


# Contact Me form (handles GET and POST requests)
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_email = request.form["email"]  # Get the user's email from the form
        user_message = request.form["message"]  # Get the message they wrote

        # Send their message to your email
        message_to_me = Message("New Message from Contact Form",
                                sender=app.config['MAIL_USERNAME'],
                                recipients=["your-email@zoho.com"])  # Replace with yours
        message_to_me.body = f"Sender: {user_email}\n\nMessage: {user_message}"
        mail.send(message_to_me)

        # Send an automated reply to the user
        message_to_user = Message("Thank you for reaching out!",
                                  sender=app.config['MAIL_USERNAME'],
                                  recipients=[user_email])
        message_to_user.body = "Thank you for your message! I'll get back to you as soon as possible."
        mail.send(message_to_user)

        return "Message sent successfully!"

    return '''
    <form method="POST">
        Your email: <input type="email" name="email" required>
        <br>
        Your message: <textarea name="message" required></textarea>
        <br>
        <button type="submit">Send</button>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)