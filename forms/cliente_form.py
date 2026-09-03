from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField
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

    correo = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    tipo_cliente = SelectField(
        "Tipo de cliente",
        choices=[
            ("Nuevo", "Nuevo"),
            ("Frecuente", "Frecuente")
        ],
        validators=[
            DataRequired(message="Seleccione un tipo de cliente.")
        ]
    )

    submit = SubmitField(
        "Registrar cliente"
    )