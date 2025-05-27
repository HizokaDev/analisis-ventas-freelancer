import funcionesCliente
import sys
import os
from exportador_excel import exportar_resumen_excel
ruta_archivo = os.path.join("Data", "ventas_clientes.csv")

def mostrar_menu():
    print("\n--- Menú de Análisis de Ventas ---")
    print("1. Ver total de ventas")
    print("2. Ver producto más vendido")
    print("3. Ver cliente con más compras")
    print("4. Ver ventas por día")
    print("5. Filtrar ventas por cliente")
    print("6. Filtrar ventas por producto")
    print("7. Ver gráfico de productos más vendidos")
    print("8. Ver gráfico de ventas por día")
    print("9. Exportar resumen a Excel")
    print("10. Salir")

def pedir_opcion():
    while True:
        opcion = input("Selecciona una opción (1-10): ").strip()
        if opcion in [str(i) for i in range(1,11)]:
            return opcion
        else:
            print("Opción no válida. Por favor, ingresa un número entre 1 y 10.")

def main():
    print("¡Bienvenido al sistema de análisis de ventas!\n")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'. Revisa la ruta.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        sys.exit(1)

    while True:
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion == "1":
            funcionesCliente.calcular_total_ventas(ruta_archivo)
        elif opcion == "2":
            funcionesCliente.producto_mas_vendido(ruta_archivo)
        elif opcion == "3":
            funcionesCliente.cliente_con_mas_compras(ruta_archivo)
        elif opcion == "4":
            funcionesCliente.ventas_por_dia(ruta_archivo)
        elif opcion == "5":
            cliente = pedir_texto_valido("cliente")
            funcionesCliente.filtrar_cliente(ruta_archivo, cliente)
        elif opcion == "6":
            producto = pedir_texto_valido("producto")
            funcionesCliente.filtrar_producto(ruta_archivo, producto)
        elif opcion == "7":
            funcionesCliente.graf_prod(ruta_archivo)
        elif opcion == "8":
            funcionesCliente.graf_dia(ruta_archivo)
        elif opcion == "9":
            ruta_entrada = ruta_archivo
            ruta_salida = "/storage/emulated/0/DojoHizoka/ventas-análisis/Reportes/resumen_ventas.xlsx"
            exportar_resumen_excel(ruta_entrada, ruta_salida)
        elif opcion == "10":
            print("¡Gracias por usar el sistema! ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()