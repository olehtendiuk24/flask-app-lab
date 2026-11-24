import logging
from flask import request, render_template, redirect, url_for, flash, current_app as app
from app.forms import ContactForm

contact_logger = logging.getLogger('contact_logger')
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    file_handler = logging.FileHandler('contact_messages.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    contact_logger.addHandler(file_handler)


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

        contact_logger.info(
            f"Нове повідомлення | Name: {name} | Email: {email} | Phone: {phone} | Subject: {subject} | Message: {message}"
        )

        flash(f"Дякуємо, {name}! Ваше повідомлення успішно відправлено та збережено.", "success")
        return redirect(url_for('contacts'))
    elif request.method == 'POST':
        flash("Будь ласка, виправте помилки у формі та спробуйте ще раз.", "danger")

    return render_template('contacts.html', title='Контакти', form=form)