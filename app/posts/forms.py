from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length

CATEGORIES = [
    ('news', 'News'),
    ('publication', 'Publication'),
    ('tech', 'Tech'),
    ('other', 'Other')
]


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(message="Заголовок є обов'язковим"),
            Length(min=2, max=150, message="Довжина заголовка від 2 до 150 символів")
        ]
    )
    content = TextAreaField(
        'Content',
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired(message="Текст поста не може бути порожнім")]
    )
    is_active = BooleanField('Active Post', default=True)
    publish_date = DateTimeLocalField(
        'Publish Date',
        format="%Y-%m-%dT%H:%M",
        default=datetime.now
    )
    category = SelectField(
        'Category',
        choices=CATEGORIES,
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')