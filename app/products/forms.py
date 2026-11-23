from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(message="Введіть назву товару"),
            Length(min=3, message="Назва товару має містити мінімум 3 символи")
        ]
    )
    content = TextAreaField(
        'Опис товару',
        validators=[DataRequired(message="Додайте опис товару")],
        render_kw={"rows": 5, "cols": 40}
    )
    price = DecimalField(
        'Ціна ($)',
        places=2,
        validators=[
            DataRequired(message="Введіть ціну"),
            NumberRange(min=0.01, message="Ціна має бути додатною")
        ]
    )
    category = SelectField(
        'Категорія',
        choices=[
            ('Laptops', 'Ноутбуки'),
            ('Smartphones', 'Смартфони'),
            ('PC', 'Настільні ПК'),
            ('Accessories', 'Аксесуари')
        ],
        validators=[DataRequired()]
    )
    quantity = IntegerField(
        'Кількість одиниць',
        validators=[
            DataRequired(message="Вкажіть кількість"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ]
    )
    image = FileField(
        'Зображення товару (PNG, JPG, JPEG)',
        validators=[
            FileAllowed(['png', 'jpg', 'jpeg'], message="Дозволені лише зображення форматів PNG, JPG або JPEG!")
        ]
    )
    submit = SubmitField('Зберегти товар')