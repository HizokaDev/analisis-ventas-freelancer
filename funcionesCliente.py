import pandas as pd

import unicodedata

import matplotlib.pyplot as plt
import os

def leer_archivo(ruta_archivo):
    """
    Intenta leer un archivo CSV y devuelve un DataFrame.
    Si hay error, muestra mensaje y devuelve None.
    """
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no fue encontrado.")
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
    return None

def calcular_total_ventas(ruta_archivo):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return  # Sale si no pudo cargar el archivo

    df["total_venta"] = df["PrecioUnitario"] * df["Cantidad"]
    total = df["total_venta"].sum()
    print(f"El total de ventas registradas es: ${total:.2f}")

def producto_mas_vendido(ruta_archivo):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    if "Producto" not in df.columns or "Cantidad" not in df.columns:
        print("Error: El archivo no contiene las columnas necesarias 'Producto' y 'Cantidad'.")
        return

    ventas_por_producto = df.groupby("Producto")["Cantidad"].sum()
    
    if ventas_por_producto.empty:
        print("No hay datos de ventas para mostrar.")
        return
    
    producto_top = ventas_por_producto.idxmax()
    cantidad_top = ventas_por_producto.max()
    
    print(f"El producto más vendido es: {producto_top} con un total de {cantidad_top} unidades.")
    
def cliente_con_mas_compras(ruta_archivo):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    if "Cliente" not in df.columns or "Cantidad" not in df.columns:
        print("Error: El archivo no contiene las columnas necesarias 'Cliente' y 'Cantidad'.")
        return

    ventas_por_cliente = df.groupby("Cliente")["Cantidad"].sum()
    
    if ventas_por_cliente.empty:
        print("No hay datos de ventas para mostrar.")
        return
    
    cliente_top = ventas_por_cliente.idxmax()
    cantidad_top = ventas_por_cliente.max()
    
    print(f"El cliente con más compras es: {cliente_top} con un total de {cantidad_top} unidades.")
    
def ventas_por_dia(ruta_archivo):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    if "Fecha" not in df.columns or "Cantidad" not in df.columns:
        print("Error: El archivo no contiene las columnas necesarias 'Fecha' y 'Cantidad'.")
        return

    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors='coerce')
    df = df.dropna(subset=["Fecha"])

    ventas_dia = df.groupby("Fecha")["Cantidad"].sum()

    if ventas_dia.empty:
        print("No hay datos de ventas para mostrar.")
        return

    print("Ventas por día:")
    for fecha, cantidad in ventas_dia.items():
        print(f"{fecha.date()}: {cantidad} unidades vendidas")
        
def filtrar_cliente(ruta_archivo, cliente):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    if "Cliente" not in df.columns:
        print("Error: El archivo no contiene la columna 'Cliente'.")
        return

    cliente_normalizado = normalizar(cliente)
    df["Cliente_normalizado"] = df["Cliente"].apply(normalizar)

    ventas_cliente = df[df["Cliente_normalizado"] == cliente_normalizado]

    if ventas_cliente.empty:
        print(f"No se encontraron ventas para el cliente '{cliente}'.")
    else:
        print(f"Ventas para el cliente '{cliente}':")
        print(ventas_cliente.drop(columns=["Cliente_normalizado"]))
        
def filtrar_producto(ruta_archivo, producto):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    if "Producto" not in df.columns:
        print("Error: El archivo no contiene la columna 'Producto'.")
        return

    producto_normalizado = normalizar(producto)
    df["Producto_normalizado"] = df["Producto"].apply(normalizar)

    ventas_producto = df[df["Producto_normalizado"] == producto_normalizado]

    if ventas_producto.empty:
        print(f"No se encontraron ventas para el producto '{producto}'.")
    else:
        print(f"Ventas para el producto '{producto}':")
        print(ventas_producto.drop(columns=["Producto_normalizado"]))

def graf_prod(ruta_archivo):
    print("Probando gráfico productos")

    df = pd.read_csv(ruta_archivo)
    ventas = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    ventas.plot(kind="bar", color="skyblue")
    plt.title("Productos más vendidos")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad vendida")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    ruta = os.path.join("ventas-análisis", "Imagenes", "productos.png")
    # Crear carpeta si no existe
    os.makedirs("ventas-análisis/Imagenes", exist_ok=True)
    plt.savefig(ruta)
    print(f"Gráfico guardado en {ruta}")
    plt.close()

def graf_dia(ruta_archivo):
    print("Probando gráfico días")

    df = pd.read_csv(ruta_archivo)
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors='coerce')
    df = df.dropna(subset=["Fecha"])
    df["Total"] = df["PrecioUnitario"] * df["Cantidad"]
    ventas = df.groupby("Fecha")["Total"].sum()

    plt.figure(figsize=(10, 6))
    ventas.plot(kind="line", marker="o", linestyle="-", color="green")
    plt.title("Ventas por día")
    plt.xlabel("Fecha")
    plt.ylabel("Total ($)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    ruta = os.path.join("ventas-análisis", "Imagenes", "dias.png")
    # Crear carpeta si no existe
    os.makedirs("ventas-análisis/Imagenes", exist_ok=True)
    plt.savefig(ruta)
    print(f"Gráfico guardado en {ruta}")
    plt.close()