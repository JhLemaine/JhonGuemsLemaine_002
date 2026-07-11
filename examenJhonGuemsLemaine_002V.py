def mostrar_menu():
    print("""
========== MENÚ PRINCIPAL ==========
1. Unidades por categoría
2. Búsqueda de productos por rango de precio
3. Actualizar precio de producto
4. Agregar producto
5. Eliminar producto
6. Salir
=====================================
""")
    
def leer_opcion():
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")

def validar_texto(valor):
    return valor.strip() != ""

def validar_peso(peso):
    return peso > 0

def validar_sn(valor):
    return valor.strip().lower() in ("s", "n")

def validar_precio(precio):
    return precio > 0

def validar_unidades(unidades):
    return unidades >= 0

def buscar_codigo(codigo, stock):
    return codigo.upper() in stock

def unidades_categoria(categoria, productos, stock):
    total = 0
    
    for codigo, datos in productos.items():
        if datos[1].lower() == categoria.lower():
            total += stock[codigo][1]
    print(f"El total de unidades disponibles es: {total}")

def busqueda_precio(p_min, p_max, productos, stock):
    encontrados = []
    
    for codigo, datos in stock.items():
        precio = datos[0]
        unidades = datos[1]
        if p_min <= precio <= p_max and unidades != 0:
            nombre = productos[codigo][0]
            encontrados.append(f"{nombre}--{codigo}")

    if encontrados:
        encontrados.sort()
        print(f"Los productos encontrados son: {encontrados}")
    else:
        print("No hay productos en ese rango de precios.")

def actualizar_precio(codigo, nuevo_precio, stock):
    if buscar_codigo(codigo, stock):
        stock[codigo.upper()][0] = nuevo_precio
        return True
    return False

def agregar_producto(codigo, nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro, precio, unidades, productos, stock):
    codigo = codigo.upper()
    if buscar_codigo(codigo, stock):
        return False
    productos[codigo] = [nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro]
    stock[codigo] = [precio, unidades]
    return True

def eliminar_producto(codigo, productos, stock):
    
    if buscar_codigo(codigo, stock):
        codigo = codigo.upper()
        del productos[codigo]
        del stock[codigo]
        return True
    return False

def main():
    
    productos = {}
    stock = {}

    activo = True
    while activo:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            categoria = input("Ingrese categoría a consultar: ")
            
            unidades_categoria(categoria, productos, stock)

        elif opcion == 2:
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min < 0 or p_max < 0 or p_min > p_max:
                        print("Debe ingresar valores enteros")
                        continue
                    break
                
                except ValueError:
                    print("Debe ingresar valores enteros")
                    
            busqueda_precio(p_min, p_max, productos, stock)

        elif opcion == 3:
            repetir = "s"
            while repetir == "s":
                codigo = input("Ingrese código del producto: ")
        
                try:
                    nuevo_precio = int(input("Ingrese nuevo precio: "))
                    if not validar_precio(nuevo_precio):
                        print("El precio debe ser un entero mayor que cero")
                    else:
                        actualizado = actualizar_precio(codigo, nuevo_precio, stock)
                        if actualizado:
                            print("Precio actualizado")
                        else:
                            print("El código no existe")
                except ValueError:
                    print("Debe ingresar un valor entero")

                repetir = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()

        elif opcion == 4:
            codigo = input("Ingrese código del producto: ")
            nombre = input("Ingrese nombre: ")
            categoria = input("Ingrese categoría: ")
            marca = input("Ingrese marca: ")

            datos_validos = True

            if not validar_texto(codigo) or buscar_codigo(codigo, stock):
                print("El código no es válido o ya existe")
                datos_validos = False

            if datos_validos and not validar_texto(nombre):
                print("El nombre no es válido")
                datos_validos = False

            if datos_validos and not validar_texto(categoria):
                print("La categoría no es válida")
                datos_validos = False

            if datos_validos and not validar_texto(marca):
                print("La marca no es válida")
                datos_validos = False

            peso_kg = None
            if datos_validos:
                try:
                    peso_kg = float(input("Ingrese peso (kg): "))
                    if not validar_peso(peso_kg):
                        print("El peso debe ser un número mayor que cero")
                        datos_validos = False
                except ValueError:
                    print("El peso debe ser un numero válido")
                    datos_validos = False

            es_importado = None
            if datos_validos:
                resp_importado = input("¿Es importado? (s/n): ")
                if not validar_sn(resp_importado):
                    print("Debe ingresar 's' o 'n'")
                    datos_validos = False
                else:
                    es_importado = resp_importado.strip().lower() == "s"

            es_para_cachorro = None
            if datos_validos:
                resp_cachorro = input("¿Es para cachorro? (s/n): ")
                if not validar_sn(resp_cachorro):
                    print("Debe ingresar 's' o 'n'")
                    datos_validos = False
                else:
                    es_para_cachorro = resp_cachorro.strip().lower() == "s"

            precio = None
            if datos_validos:
                try:
                    precio = int(input("Ingrese precio: "))
                    if not validar_precio(precio):
                        print("El precio debe ser un entero mayor que cero")
                        datos_validos = False
                except ValueError:
                    print("El precio debe ser un entero válido")
                    datos_validos = False

            unidades = None
            if datos_validos:
                try:
                    unidades = int(input("Ingrese unidades: "))
                    if not validar_unidades(unidades):
                        print("Las unidades deben ser un entero mayor o igual a cero")
                        datos_validos = False
                except ValueError:
                    print("Las unidades deben ser un entero válido ")
                    datos_validos = False

            if datos_validos:
                agregado = agregar_producto(codigo, nombre, categoria, marca, peso_kg, es_importado, es_para_cachorro, precio, unidades, productos, stock)
                if agregado:
                    print("Producto agregado")
                else:
                    print("El código ya existe")

        elif opcion == 5:
            codigo = input("Ingrese código del producto: ")
            eliminado = eliminar_producto(codigo, productos, stock)
            if eliminado:
                print("Producto eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            activo = False
            print("Programa finalizado.")

main()