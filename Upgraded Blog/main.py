from flask import Flask, render_template, request
import requests
import smtplib
import os

Email = os.environ["email"]
password = os.environ["password"]
app = Flask(__name__)

response = requests.get("https://api.npoint.io/482bcced3b581f5942f0")
response.raise_for_status()
data = response.json()

@app.route('/')
def get_all_posts():
    return render_template("index.html", data=data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in data:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/contact", methods=["POST", "GET"])
def use_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        send_mail(name, email, phone, message)
        return f'<h1>Successfully sent the email</h1>'
    else:
        return render_template('contact.html')

# msg=f"Subject:Someone contacted you through your blog.\n\nName:{name}\nEmail:{email}\nPhone:{phone}\nMessage:{message}"
def send_mail(name, email, phone, message):
    connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
    connection.starttls()
    connection.login(user=Email, password=password)
    connection.sendmail(
        from_addr=Email,
        to_addrs=Email,
        msg=f"Subject:Someone contacted you through your blog.\n\nName:{name}\nEmail:{email}\nPhone:{phone}\nMessage:{message}"
    )
    connection.quit()


if __name__ == "__main__":
    app.run(debug=True)