import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='Firuliru',
        tipo='Cliente', 
        nombre='Mario', 
        apellido='Linares', 
        correo=test_user_email if test_user_email else 'mois3sanchez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='322 cambruit, \nCalifornia \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/segun2.jpg')

    crear_usuario(
        username='encigon',
        tipo='Cliente', 
        nombre='Jessica', 
        apellido='Montiel', 
        correo=test_user_email if test_user_email else 'sanchmoichi@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='av concepcion 1220,  \nViña del mar \nChile', 
        subscrito=True, 
        imagen='perfiles/chic.jpg')

    crear_usuario(
        username='Mrmochi',
        tipo='Cliente', 
        nombre='Gabriel', 
        apellido='Garrido', 
        correo=test_user_email if test_user_email else 'lolapalosa92@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='Juan gomez de almagro  2850, \santiago \nChile', 
        subscrito=False, 
        imagen='perfiles/gabo.jpg')

    crear_usuario(
        username='Ellesteban',
        tipo='Cliente', 
        nombre='Esteban', 
        apellido='Cito', 
        correo=test_user_email if test_user_email else 'elleshugabnverga@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='el aveninn 231, \nconcepcion \nChile', 
        subscrito=False, 
        imagen='perfiles/chico.jpg')

    crear_usuario(
        username='mrnobody',
        tipo='Administrador', 
        nombre='Martin', 
        apellido='Santaelices', 
        correo=test_user_email if test_user_email else 'traba23jo@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='233 martin road, San Diego, \nFlorida 33100 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/brohold.jpg')
    
    crear_usuario(
        username='elleshuga',
        tipo='Administrador', 
        nombre='Moises', 
        apellido='Sanchez', 
        correo=test_user_email if test_user_email else 'mo.sanchez@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='23.648.469-6', 
        direccion='Sancho de escalona 2850, Conchali, \nSantiago 90000 \nChile', 
        subscrito=False, 
        imagen='perfiles/moises.jpg')

    crear_usuario(
        username='Superman',
        tipo='Superusuario',
        nombre='Denisse',
        apellido='Coilla',
        correo=test_user_email if test_user_email else 'de.coilla@duocuc.cl',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='1950 brasil, San joaquin, \Santiago 90001 \nChile',
        subscrito=False,
        imagen='perfiles/denisse.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Far Cry 6',
            'descripcion': 'Far Cry 6 te lleva a la isla tropical de Yara, un paraíso detenido en el tiempo. Juega como Dani Rojas, un guerrillero que lucha por la libertad contra el régimen opresivo de Antón Castillo. Con un mundo abierto expansivo y una jugabilidad llena de acción, Far Cry 6 ofrece una experiencia intensa y emocionante.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil Village',
            'descripcion': 'Resident Evil Village continúa la historia de Ethan Winters en su búsqueda para rescatar a su hija secuestrada. Explora una aldea misteriosa llena de criaturas aterradoras y enfrenta desafíos mortales en este juego de acción y supervivencia. Con gráficos impresionantes y una atmósfera aterradora, Resident Evil Village es un digno sucesor de la icónica serie.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000002.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'The Last of Us Part II',
            'descripcion': 'The Last of Us Part II es una emotiva historia de venganza y redención en un mundo postapocalíptico. Sigue a Ellie en su viaje a través de un Estados Unidos devastado mientras enfrenta desafíos físicos y emocionales. Con impresionantes gráficos y una narrativa cautivadora, este juego redefine el género de aventura.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000003.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Ghost of Tsushima',
            'descripcion': 'Ghost of Tsushima te sumerge en la era feudal de Japón como Jin Sakai, un samurái en una misión para proteger su hogar de la invasión mongola. Explora un vasto mundo abierto lleno de paisajes deslumbrantes, combate táctico y una historia conmovedora sobre honor y sacrificio.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Overwatch',
            'descripcion': 'Overwatch es un shooter en equipo desarrollado por Blizzard Entertainment. Elige entre una diversa gama de héroes, cada uno con habilidades únicas, y trabaja en equipo para cumplir objetivos en mapas variados. Con actualizaciones constantes y una vibrante comunidad, Overwatch ofrece acción y estrategia sin fin.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000005.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Persona 5',
            'descripcion': 'Persona 5 es un aclamado juego de rol japonés que sigue la historia de un grupo de estudiantes de secundaria que llevan una vida secreta como ladrones de corazones. Con una narrativa intrigante, personajes memorables y un sistema de combate por turnos único, Persona 5 es una experiencia inolvidable.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000006.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy es un juego de rol de acción de mundo abierto ambientado en el universo de Harry Potter. Juega como un estudiante de Hogwarts en el siglo XIX, explora el castillo y sus alrededores, aprende magia y descubre secretos ocultos. Con una historia original y una jugabilidad inmersiva, Hogwarts Legacy es un sueño hecho realidad para los fanáticos de Harry Potter.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000007.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Elden Ring',
            'descripcion': 'Elden Ring es un juego de rol de acción desarrollado por FromSoftware y dirigido por Hidetaka Miyazaki, con la colaboración de George R. R. Martin. Explora un vasto mundo abierto lleno de desafíos, enemigos formidables y secretos ocultos. Con su jugabilidad profunda y atmósfera oscura, Elden Ring ofrece una experiencia única y desafiante para los jugadores.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000008.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Minecraft',
            'descripcion': 'Minecraft es un juego de construcción y aventuras que permite a los jugadores explorar, recolectar recursos y construir estructuras en un mundo generado proceduralmente. Con modos de juego como supervivencia, creativo y multijugador, Minecraft fomenta la creatividad y la colaboración.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000009.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Kena: Bridge of Spirits',
            'descripcion': 'Kena: Bridge of Spirits es un juego de aventura y acción que sigue a Kena, una joven guía espiritual, mientras ayuda a espíritus atrapados a encontrar la paz. Con una jugabilidad fluida, gráficos hermosos y una narrativa emotiva, este juego ofrece una experiencia mágica y envolvente.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000010.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Ratchet & Clank: Rift Apart',
            'descripcion': 'Ratchet & Clank: Rift Apart es una aventura interdimensional que sigue a los héroes Ratchet y Clank mientras luchan contra un emperador malvado de otra realidad. Con gráficos de última generación, jugabilidad fluida y una historia llena de humor y acción, este juego es una excelente adición a la serie.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Ori and the Will of the Wisps',
            'descripcion': 'Ori and the Will of the Wisps es un hermoso juego de aventuras y plataformas que sigue a Ori en un viaje para descubrir su verdadero destino. Con una jugabilidad desafiante, gráficos impresionantes y una banda sonora emotiva, este juego ofrece una experiencia mágica y conmovedora.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000012.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Plants vs. Zombies: La batalla de Neighborville',
            'descripcion': 'Plants vs. Zombies: La batalla de Neighborville es un videojuego de disparos en tercera persona desarrollado por PopCap Games y publicado por Electronic Arts para Microsoft Windows, PlayStation 4, Xbox One y Nintendo Switch. Es la tercera entrega de la serie de videojuegos Plants vs. Zombies: Garden Warfare.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Total War: WARHAMMER III',
            'descripcion': 'El final cataclísmico de la trilogía de Total War™: WARHAMMER® ha llegado. Reagrupa a tus fuerzas y adéntrate en el Reino del Caos, una dimensión de terrores horripilantes en la que se decidirá el destino del mundo. ¿Conquistarás a tus demonios... o los dirigirás?',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Humankind',
            'descripcion': 'Humankind es un juego de estrategia por turnos donde los jugadores pueden reescribir la historia de la humanidad combinando culturas desde la antigüedad hasta la era moderna. Toma decisiones estratégicas, construye ciudades y expande tu civilización a través de la historia. Con una jugabilidad innovadora y una profundidad estratégica, Humankind ofrece una nueva y emocionante experiencia en el género de estrategia.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000015.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Crusader Kings III',
            'descripcion': 'Crusader Kings III es un juego de gran estrategia que te permite gobernar una dinastía medieval a lo largo de generaciones. Maneja relaciones diplomáticas, complots políticos y conflictos militares mientras expandes tu reino y aseguras la prosperidad de tu linaje. Con una jugabilidad profunda y una rica narrativa emergente, Crusader Kings III ofrece una experiencia única y compleja en el género de estrategia.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000016.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Stardew Valley',
            'descripcion': 'Acabas de heredar la vieja parcela agrícola de tu abuelo de Stardew Valley. Decides partir hacia una nueva vida con unas herramientas usadas y algunas monedas. ¿Te ves capaz de vivir de la tierra y convertir estos campos descuidados en un hogar próspero?',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000017.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Project Zomboid',
            'descripcion': 'Project Zomboid es un videojuego de supervivencia isométrico de mundo abierto desarrollado por el estudio independiente británico y canadiense The Indie Stone.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000018.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Hades',
            'descripcion': 'Desafía al dios de los muertos y protagoniza una salvaje fuga del Inframundo en este juego de exploración de mazmorras de los creadores de Bastion, Transistor y Pyre.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000019.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Dark Souls III',
            'descripcion': 'Dark Souls III es un videojuego de rol de acción desarrollado por FromSoftware y publicado por Bandai Namco Entertainment para PlayStation 4, Xbox One y Microsoft Windows. Es la tercera y última entrega en la saga Souls, ​ lanzándose en Japón el 24 de marzo de 2016, y de manera mundial en abril del mismo año.​​',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000020.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

