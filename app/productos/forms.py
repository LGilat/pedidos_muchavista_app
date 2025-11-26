from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    unidad = StringField("Unidad (ej: bolsas, piezas)", validators=[DataRequired()])
    cantidad = FloatField("Cantidad", default=0)
    categoria = StringField("Categoría")
    submit = SubmitField("Guardar")
