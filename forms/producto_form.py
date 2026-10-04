from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(
                min=5,
                max=300,
                message="La descripción debe tener entre 5 y 300 caracteres."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        places=2,
        validators=[
            InputRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(message="Debe seleccionar un proveedor.")
        ]
    )

    disponible = BooleanField(
        "Producto disponible"
    )

    submit = SubmitField(
        "Registrar producto"
    )