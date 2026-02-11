# Pedidos Muchavista App

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-black.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange.svg)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-green.svg)

Una aplicación web robusta y modular desarrollada con Flask para la gestión integral de un negocio. Facilita el control de inventario, productos, movimientos de stock y la administración de proveedores, garantizando una operación eficiente y organizada.

## Características Principales

*   **Gestión de Productos:** Añade, edita y visualiza tu catálogo de productos.
*   **Control de Inventario:** Mantén un seguimiento preciso de las existencias disponibles.
*   **Registro de Movimientos:** Registra entradas y salidas de productos para un historial completo.
*   **Administración de Proveedores:** Gestiona la información de tus proveedores de manera centralizada.
*   **Base de Datos Relacional:** Utiliza SQLAlchemy para una interacción potente y flexible con la base de datos.
*   **Migraciones de Base de Datos:** Gestión del esquema de la base de datos mediante Alembic.

## Tecnologías Utilizadas

*   **Backend:**
    *   [Python](https://www.python.org/)
    *   [Flask](https://flask.palletsprojects.com/) - Microframework web.
    *   [SQLAlchemy](https://www.sqlalchemy.org/) - Toolkit y ORM para bases de datos.
    *   [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Alembic) - Extension para migraciones de DB.
*   **Frontend:**
    *   [Jinja2](https://jinja.palletsprojects.com/) - Motor de plantillas.
    *   HTML, CSS, JavaScript (con posibles librerías adicionales en `static/js/scripts.js`).
*   **Base de Datos:**
    *   SQLite (en `instance/inventario.db`) - Ideal para desarrollo y pruebas.

## Configuración y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/pedidos_muchavista_app.git
    cd pedidos_muchavista_app
    ```

2.  **Crear y Activar un Entorno Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate    # En Windows
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno (Opcional pero recomendado):**
    Puedes crear un archivo `.env` o establecer las variables de entorno necesarias para tu aplicación (ej. `SECRET_KEY`, `DATABASE_URL` si no usas SQLite por defecto).

5.  **Inicializar y Migrar la Base de Datos:**
    ```bash
    flask db upgrade
    ```
    Si es la primera vez que inicializas las migraciones, puede que necesites:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6.  **Poblar la Base de Datos (Opcional):**
    Si tienes un script para datos de prueba:
    ```bash
    python seed.py
    ```

7.  **Ejecutar la Aplicación:**
    ```bash
    python run.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000` (o el puerto configurado).

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar su mantenimiento y escalabilidad:

```
├───README.md
├───requirements.txt
├───run.py
├───seed.py
├───vercel.json
├───app/
│   ├───__init__.py           # Inicialización de la app Flask
│   ├───config.py             # Configuración de la aplicación
│   ├───extensions.py         # Inicialización de extensiones de Flask
│   ├───models.py             # Modelos de base de datos (SQLAlchemy)
│   ├───routes.py             # Rutas/Vistas principales
│   ├───inventario/           # Blueprint para la gestión de inventario
│   ├───movimientos/          # Blueprint para el registro de movimientos
│   ├───productos/            # Blueprint para la gestión de productos
│   ├───proveedores/          # Blueprint para la gestión de proveedores
│   ├───services/             # Módulos de servicios
│   ├───static/               # Archivos estáticos (CSS, JS, imágenes)
│   └───templates/            # Plantillas HTML (Jinja2)
├───instance/                 # Archivos de instancia (ej. base de datos SQLite)
└───migrations/               # Scripts de migración de base de datos (Alembic)
```

## Despliegue

Este proyecto incluye un archivo `vercel.json` para facilitar su despliegue en la plataforma [Vercel](https://vercel.com/).

---
