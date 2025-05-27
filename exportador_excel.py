import pandas as pd
import os
from funcionesCliente import leer_archivo  # Asegurate de importar correctamente

def exportar_resumen_excel(ruta_archivo, ruta_salida):
    df = leer_archivo(ruta_archivo)
    if df is None:
        return

    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors='coerce')
    df = df.dropna(subset=["Fecha"])
    df["Total"] = df["PrecioUnitario"] * df["Cantidad"]

    ventas_por_producto = df.groupby("Producto")["Cantidad"].sum().reset_index()
    ventas_por_cliente = df.groupby("Cliente")["Cantidad"].sum().reset_index()
    ventas_por_dia = df.groupby("Fecha")["Total"].sum().reset_index()

    # Crear carpeta si no existe
    carpeta = os.path.dirname(ruta_salida)
    os.makedirs(carpeta, exist_ok=True)

    with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
        ventas_por_producto.to_excel(writer, sheet_name="Productos", index=False)
        ventas_por_cliente.to_excel(writer, sheet_name="Clientes", index=False)
        ventas_por_dia.to_excel(writer, sheet_name="Dias", index=False)
        df.to_excel(writer, sheet_name="Datos Completos", index=False)

    print(f"Resumen exportado a: {ruta_salida}")