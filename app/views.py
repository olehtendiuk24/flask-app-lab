import logging
from flask import request, render_template, redirect, url_for, flash
from app import app
from app.forms import ContactForm

logging.basicConfig(
    filename='contact_messages.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = dict(form.subject.choices).get(form.subject.data)
        message = form.message.data

        logging.info(f"Нове повідомлення | Name: {name} | Email: {email} | Phone: {phone} | Subject: {subject} | Message: {message}")

        flash(f"Дякуємо, {name}! Ваше повідомлення успішно відправлено та збережено.", "success")

        return redirect(url_for('contacts'))
    elif request.method == 'POST':
        flash("Будь ласка, виправте помилки у формі та спробуйте ще раз.", "danger")

    return render_template('contacts.html', title='Контакти', form=form)