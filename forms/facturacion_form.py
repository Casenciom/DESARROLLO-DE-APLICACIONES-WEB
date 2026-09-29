from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

class FacturacionForm(FlaskForm):

    cliente = SelectField(
        "Cliente",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message="Seleccione un cliente.")
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
    
