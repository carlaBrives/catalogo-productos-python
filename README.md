# Catálogo de productos

Programa de consola en Python para administrar productos y guardarlos de forma persistente en una base de datos SQLite.

## Funciones

- Agregar productos con nombre, categoría y precio.
- Listar los productos registrados.
- Buscar productos por nombre o parte del nombre.
- Eliminar productos por número.

## Requisitos

- Python 3.
- La librería `dataset` (SQLite ya viene incluido con Python).

## Instalación

Desde una terminal abierta en la carpeta donde están `entrega_final.py` y `requirements.txt`, instalá la dependencia:

```powershell
python -m pip install -r requirements.txt
```

Si el comando `python` no está disponible en Windows, probá `py -m pip install -r requirements.txt` o usá la ruta completa a `python.exe`.

## Ejecución

En la misma carpeta, ejecutá:

```powershell
python entrega_final.py
```

El programa muestra un menú para agregar, listar, buscar o eliminar productos. Elegí la opción `5` para salir.

## Datos

La base de datos SQLite se crea automáticamente en la carpeta de datos local del usuario (`%LOCALAPPDATA%\\talento_ba\\datos.db` en Windows). Los datos permanecen allí al cerrar el programa. Si otra persona ejecuta el programa en su computadora, tendrá su propia base de datos.
