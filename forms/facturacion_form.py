from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange, Length


class FacturacionForm(FlaskForm):

    cliente = SelectField(
        "Cliente",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message="Seleccione un cliente.")
        ]
    )

    direccion = StringField(
        "Dirección",
        validators=[
            DataRequired(message="La dirección es obligatoria."),
            Length(
                max=200,
                message="La dirección no puede superar los 200 caracteres."
            )
        ]
    )

    producto = SelectField(
        "Producto",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message="Seleccione un producto.")
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor que 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Pagada", "Pagada")
        ],
        validators=[
            DataRequired(message="Seleccione un estado.")
        ]
    )

    submit = SubmitField(
        "Registrar factura"
    )