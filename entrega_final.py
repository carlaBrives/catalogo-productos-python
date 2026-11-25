import os
from pathlib import Path

import dataset


ARCHIVO_BASE_DATOS = (
    Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    / "talento_ba"
    / "datos.db"
)


def conectar_base_datos():
    ARCHIVO_BASE_DATOS.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite:///{ARCHIVO_BASE_DATOS.as_posix()}"
    return dataset.connect(url)


def crear_tabla(base_datos):
    base_datos.query(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio INTEGER NOT NULL
        )
        """
    )


def listar_productos(base_datos):
    return list(base_datos["productos"].find(order_by="id"))


def agregar_producto(base_datos):
    nombre = input("Nombre del producto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del producto: ").strip()

    categoria = input("Categoría del producto: ").strip()
    while categoria == "":
        print("La categoría no puede estar vacía.")
        categoria = input("Categoría del producto: ").strip()

    while True:
        precio_ingresado = input("Precio sin centavos: $").strip()
        if precio_ingresado.isdigit() and int(precio_ingresado) > 0:
            precio = int(precio_ingresado)
            break
        print("Ingresá un precio entero mayor a cero, sin centavos.")

    base_datos["productos"].insert(
        {
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
        }
    )
    print(f"Se agregó el producto '{nombre}'.")


def mostrar_productos(base_datos):
    productos = listar_productos(base_datos)
    if not productos:
        print("No hay productos registrados.")
        return

    print("\nProductos registrados:")
    for indice, producto in enumerate(productos, start=1):
        print(
            f"{indice}. {producto['nombre']} | "
            f"Categoría: {producto['categoria']} | "
            f"Precio: ${producto['precio']}"
        )


def buscar_productos(base_datos):
    nombre_buscar = input("Ingresá el nombre o parte del nombre: ").strip()
    while nombre_buscar == "":
        print("La búsqueda no puede estar vacía.")
        nombre_buscar = input("Ingresá el nombre o parte del nombre: ").strip()

    encontrados = base_datos.query(
        """
        SELECT nombre, categoria, precio
        FROM productos
        WHERE nombre LIKE :busqueda COLLATE NOCASE
        ORDER BY id
        """,
        busqueda=f"%{nombre_buscar}%",
    )
    encontrados = list(encontrados)

    if not encontrados:
        print("No se encontraron productos con ese nombre.")
        return

    for producto in encontrados:
        print(
            f"{producto['nombre']} | Categoría: {producto['categoria']} | "
            f"Precio: ${producto['precio']}"
        )


def eliminar_producto(base_datos):
    productos = listar_productos(base_datos)
    if not productos:
        print("No hay productos para eliminar.")
        return

    print("\nProductos registrados:")
    for indice, producto in enumerate(productos, start=1):
        print(
            f"{indice}. {producto['nombre']} | "
            f"Categoría: {producto['categoria']} | "
            f"Precio: ${producto['precio']}"
        )

    while True:
        posicion_ingresada = input(
            "Ingresá el número del producto que querés eliminar "
            "(0 para cancelar): "
        ).strip()

        if posicion_ingresada.isdigit():
            posicion = int(posicion_ingresada)
            if posicion == 0:
                print("Eliminación cancelada.")
                return
            if 1 <= posicion <= len(productos):
                producto = productos[posicion - 1]
                base_datos["productos"].delete(id=producto["id"])
                print(f"Se eliminó '{producto['nombre']}'.")
                return
            print("No hay un producto con ese número.")
        else:
            print("Ingresá un número entero válido.")


def main():
    print("Sistema de gestión básica de productos")

    base_datos = conectar_base_datos()
    try:
        crear_tabla(base_datos)
        while True:
            print("\n--- Menú ---")
            print("1. Agregar producto")
            print("2. Mostrar productos")
            print("3. Buscar productos por nombre")
            print("4. Eliminar producto por número")
            print("5. Salir")

            opcion = input("Elegí una opción (1-5): ").strip()

            if opcion == "1":
                agregar_producto(base_datos)
            elif opcion == "2":
                mostrar_productos(base_datos)
            elif opcion == "3":
                buscar_productos(base_datos)
            elif opcion == "4":
                eliminar_producto(base_datos)
            elif opcion == "5":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción incorrecta. Ingresá un número del 1 al 5.")
    finally:
        base_datos.close()


if __name__ == "__main__":
    main()
