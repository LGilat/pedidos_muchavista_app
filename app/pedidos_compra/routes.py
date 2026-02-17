from flask import render_template, request, flash, redirect, url_for, jsonify
from . import bp
from ..extensions import db
from ..models import PedidoCompra, LineaPedidoCompra, Product, Proveedor
from datetime import datetime

@bp.route("/nuevo", methods=["GET", "POST"])
def new_purchase_order():
    if request.method == "POST":
        proveedor_id = request.form.get("proveedor_id")
        referencia = request.form.get("referencia")
        fecha_recepcion_esperada_str = request.form.get("fecha_recepcion_esperada")
        observaciones_pedido = request.form.get("observaciones_pedido")

        if not proveedor_id:
            flash("Debe seleccionar un proveedor.", "danger")
            return redirect(url_for("pedidos_compra.new_purchase_order"))

        proveedor = Proveedor.query.get(proveedor_id)
        if not proveedor:
            flash("Proveedor no encontrado.", "danger")
            return redirect(url_for("pedidos_compra.new_purchase_order"))

        fecha_recepcion_esperada = None
        if fecha_recepcion_esperada_str:
            try:
                fecha_recepcion_esperada = datetime.strptime(fecha_recepcion_esperada_str, "%Y-%m-%d")
            except ValueError:
                flash("Formato de fecha de recepción esperada inválido. Use AAAA-MM-DD.", "danger")
                return redirect(url_for("pedidos_compra.new_purchase_order"))

        new_purchase_order = PedidoCompra(
            proveedor_id=proveedor_id,
            fecha_pedido=datetime.utcnow(),
            referencia=referencia,
            observaciones=observaciones_pedido,
            fecha_recepcion_esperada=fecha_recepcion_esperada,
            total_amount=0.0,  # Will be calculated
            estado="pendiente"
        )
        db.session.add(new_purchase_order)
        db.session.flush()  # To get new_purchase_order.id before commit

        total_order_amount = 0.0
        items_count = 0
        for key in request.form:
            if key.startswith("items[") and key.endswith("][product_id]"):
                index = key.split("[")[1].split("]")[0]
                product_id = request.form.get(f"items[{index}][product_id]")
                cantidad_recibida_str = request.form.get(f"items[{index}][cantidad_recibida]")
                precio_unitario_str = request.form.get(f"items[{index}][precio_unitario]")

                if not all([product_id, cantidad_recibida_str, precio_unitario_str]):
                    db.session.rollback()
                    flash("Faltan datos en una línea de producto.", "danger")
                    return redirect(url_for("pedidos_compra.new_purchase_order"))

                product = Product.query.get(product_id)
                if not product:
                    db.session.rollback()
                    flash(f"Producto con ID {product_id} no encontrado.", "danger")
                    return redirect(url_for("pedidos_compra.new_purchase_order"))

                try:
                    cantidad_recibida = float(cantidad_recibida_str)
                    precio_unitario = float(precio_unitario_str)
                    if cantidad_recibida <= 0 or precio_unitario <= 0:
                        db.session.rollback()
                        flash("La cantidad y el precio unitario deben ser valores positivos.", "danger")
                        return redirect(url_for("pedidos_compra.new_purchase_order"))
                except ValueError:
                    db.session.rollback()
                    flash("La cantidad y el precio unitario deben ser números válidos.", "danger")
                    return redirect(url_for("pedidos_compra.new_purchase_order"))

                subtotal = cantidad_recibida * precio_unitario
                total_order_amount += subtotal
                items_count += 1

                new_line_item = LineaPedidoCompra(
                    pedido_id=new_purchase_order.id,
                    product_id=product_id,
                    cantidad_pedida=cantidad_recibida, # Assuming cantidad_pedida == cantidad_recibida for initial record
                    cantidad_recibida=cantidad_recibida,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
                db.session.add(new_line_item)
        
        if items_count == 0:
            db.session.rollback()
            flash("El pedido debe contener al menos un producto.", "danger")
            return redirect(url_for("pedidos_compra.new_purchase_order"))

        new_purchase_order.total_amount = total_order_amount
        db.session.commit()
        flash("Pedido de compra registrado exitosamente.", "success")
        return redirect(url_for("productos.lista_productos"))
    else: # GET request
        proveedores = Proveedor.query.all()
        productos = Product.query.all()
        return render_template(
            "pedidos_compra/nuevo_pedido.html", proveedores=proveedores, productos=productos
        )


@bp.route("/lista", methods=["GET"])
def list_purchase_orders():
    pedidos_compra = PedidoCompra.query.order_by(PedidoCompra.fecha_pedido.desc()).all()
    return render_template("pedidos_compra/lista_pedidos.html", pedidos_compra=pedidos_compra)
