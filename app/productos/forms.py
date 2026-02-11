from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    unidad = StringField("Unidad (ej: bolsas, piezas)", validators=[DataRequired()])
    categoria = StringField("Categoría")
    ubicacion = StringField("Ubicación")
    submit = SubmitField("Guardar")
