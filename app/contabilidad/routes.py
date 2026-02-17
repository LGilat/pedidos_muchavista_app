from flask import render_template, request, flash, redirect, url_for, jsonify
from . import bp
from ..extensions import db
from ..models import Transaccion, CategoriaTransaccion
from datetime import datetime, timedelta
from sqlalchemy import func, extract

@bp.route("/categorias", methods=["GET"])
def list_transaction_categories():
    categorias = CategoriaTransaccion.query.order_by(CategoriaTransaccion.tipo, CategoriaTransaccion.nombre).all()
    return render_template("contabilidad/lista_categorias_transaccion.html", categorias=categorias)

@bp.route("/categorias/nueva", methods=["GET", "POST"])
def new_transaction_category():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo")

        if not nombre or not tipo:
            flash("Debe proporcionar un nombre y un tipo para la categoría.", "danger")
            return redirect(url_for("contabilidad.new_transaction_category"))

        if tipo not in ["ingreso", "gasto"]:
            flash("Tipo de categoría inválido. Debe ser 'ingreso' o 'gasto'.", "danger")
            return redirect(url_for("contabilidad.new_transaction_category"))

        existing_category = CategoriaTransaccion.query.filter_by(nombre=nombre, tipo=tipo).first()
        if existing_category:
            flash(f"Ya existe una categoría '{nombre}' de tipo '{tipo}'.", "danger")
            return redirect(url_for("contabilidad.new_transaction_category"))

        new_category = CategoriaTransaccion(nombre=nombre, tipo=tipo)
        db.session.add(new_category)
        try:
            db.session.commit()
            flash(f"Categoría '{nombre}' de tipo '{tipo}' creada exitosamente.", "success")
            return redirect(url_for("contabilidad.list_transaction_categories"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la categoría: {str(e)}", "danger")
            return redirect(url_for("contabilidad.new_transaction_category"))
    
    return render_template("contabilidad/nueva_categoria_transaccion.html")


@bp.route("/transacciones", methods=["GET"])
def list_transactions():
    transacciones = Transaccion.query.order_by(Transaccion.fecha.desc()).all()
    return render_template("contabilidad/lista_transacciones.html", transacciones=transacciones)

@bp.route("/transacciones/nueva", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        cantidad_str = request.form.get("cantidad")
        fecha_str = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        categoria_id = request.form.get("categoria_id")

        if not all([tipo, cantidad_str, fecha_str, categoria_id]):
            flash("Faltan datos obligatorios para la transacción.", "danger")
            return redirect(url_for("contabilidad.add_transaction"))
        
        if tipo not in ["ingreso", "gasto"]:
            flash("Tipo de transacción inválido. Debe ser 'ingreso' o 'gasto'.", "danger")
            return redirect(url_for("contabilidad.add_transaction"))

        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                flash("La cantidad debe ser un valor positivo.", "danger")
                return redirect(url_for("contabilidad.add_transaction"))
        except ValueError:
            flash("La cantidad debe ser un número válido.", "danger")
            return redirect(url_for("contabilidad.add_transaction"))

        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            flash("Formato de fecha inválido. Use AAAA-MM-DD.", "danger")
            return redirect(url_for("contabilidad.add_transaction"))
        
        categoria = CategoriaTransaccion.query.get(categoria_id)
        if not categoria:
            flash("Categoría no encontrada.", "danger")
            return redirect(url_for("contabilidad.add_transaction"))

        new_transaction = Transaccion(
            tipo=tipo,
            cantidad=cantidad,
            fecha=fecha,
            descripcion=descripcion,
            categoria_id=categoria_id
        )
        db.session.add(new_transaction)
        try:
            db.session.commit()
            flash(f"Transacción de {tipo} por {cantidad:.2f}€ registrada exitosamente.", "success")
            return redirect(url_for("contabilidad.list_transactions"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar la transacción: {str(e)}", "danger")
            return redirect(url_for("contabilidad.add_transaction"))

    categorias = CategoriaTransaccion.query.all()
    today_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("contabilidad/nuevo_transaccion.html", categorias=categorias, today_date=today_date)


@bp.route("/informe", methods=["GET"])
def financial_report():
    periodo_tipo = request.args.get("periodo_tipo", "mes")
    fecha_inicio_str = request.args.get("fecha_inicio")
    fecha_fin_str = request.args.get("fecha_fin")

    # Default to current month/week/year if dates are not provided
    today = datetime.now()
    if not fecha_inicio_str or not fecha_fin_str:
        if periodo_tipo == "mes":
            fecha_inicio = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = today.replace(day=28) + timedelta(days=4)  # advance 4 days to get to next month
            fecha_fin = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
        elif periodo_tipo == "semana":
            fecha_inicio = today - timedelta(days=today.weekday()) # Monday of current week
            fecha_fin = fecha_inicio + timedelta(days=6, hours=23, minutes=59, seconds=59) # Sunday of current week
        elif periodo_tipo == "anyo":
            fecha_inicio = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else: # Default to month if invalid
            periodo_tipo = "mes"
            fecha_inicio = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = today.replace(day=28) + timedelta(days=4)
            fecha_fin = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)
    else:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            # Adjust fecha_fin to include the entire day
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            flash("Formato de fecha inválido. Usando período actual.", "warning")
            return redirect(url_for("contabilidad.financial_report")) # Redirect to default filter

    # Query transactions within the date range
    transacciones_filtradas = Transaccion.query.filter(
        Transaccion.fecha >= fecha_inicio,
        Transaccion.fecha <= fecha_fin
    ).all()

    total_ingresos = sum(t.cantidad for t in transacciones_filtradas if t.tipo == "ingreso")
    total_gastos = sum(t.cantidad for t in transacciones_filtradas if t.tipo == "gasto")
    balance_neto = total_ingresos - total_gastos

    ingresos_por_categoria = {}
    gastos_por_categoria = {}

    for t in transacciones_filtradas:
        categoria_nombre = t.categoria.nombre if t.categoria else "Sin Categoría"
        if t.tipo == "ingreso":
            ingresos_por_categoria[categoria_nombre] = ingresos_por_categoria.get(categoria_nombre, 0.0) + t.cantidad
        else:
            gastos_por_categoria[categoria_nombre] = gastos_por_categoria.get(categoria_nombre, 0.0) + t.cantidad
    
    reporte = {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "balance_neto": balance_neto,
        "ingresos_por_categoria": ingresos_por_categoria,
        "gastos_por_categoria": gastos_por_categoria,
    }

    return render_template(
        "contabilidad/informe_financiero.html",
        reporte=reporte,
        periodo_tipo=periodo_tipo,
        fecha_inicio_str=fecha_inicio.strftime("%Y-%m-%d"),
        fecha_fin_str=fecha_fin.strftime("%Y-%m-%d")
    )

