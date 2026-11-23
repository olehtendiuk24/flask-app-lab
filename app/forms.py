from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message="Ім'я є обов'язковим"),
            Length(min=4, max=10, message="Довжина імені повинна бути від 4 до 10 символів")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email є обов'язковим"),
            Email(message="Введіть коректну адресу електронної пошти")
        ]
    )
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(message="Телефон є обов'язковим"),
            Regexp(r'^\+380\d{9}$', message="Формат телефону має бути: +380XXXXXXXXX")
        ]
    )
    subject = SelectField(
        'Subject',
        choices=[
            ('general', 'Загальне питання'),
            ('support', 'Технічна підтримка'),
            ('cooperation', 'Співпраця'),
            ('other', 'Інше')
        ],
        validators=[DataRequired()]
    )
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Повідомлення не може бути порожнім"),
            Length(max=500, message="Максимальна довжина повідомлення — 500 символів")
        ]
    )
    submit = SubmitField('Send Message')