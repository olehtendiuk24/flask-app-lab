import logging
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)

contact_logger = logging.getLogger('contact_logger')
if not contact_logger.handlers:
    contact_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('contact_messages.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    contact_logger.addHandler(file_handler)


@main_bp.route('/')
@main_bp.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@main_bp.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)


@main_bp.route('/contacts', methods=['GET', 'POST'])
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
        return redirect(url_for('main.contacts'))
    elif request.method == 'POST':
        flash("Будь ласка, виправте помилки у формі та спробуйте ще раз.", "danger")

    return render_template('contacts.html', title='Контакти', form=form)