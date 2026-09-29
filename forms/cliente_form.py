from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    cedula = StringField(
        "Cédula",
        validators=[
            DataRequired(message="La cédula es obligatoria."),
            Length(
                min=10,
                max=20,
                message="La cédula debe tener entre 10 y 20 caracteres."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            Length(
                max=20,
                message="El teléfono no puede superar los 20 caracteres."
            )
        ]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    submit = SubmitField(
        "Registrar cliente"
    )