from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, filters, ContextTypes, MessageHandler,CallbackContext
import random
import logging
import requests

# Configurar el registro de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7240801167:AAElezmbVvapp1alYWMlMfUoGPflFVTQfaA'
API_KEY = '25339eefe03c957d71e0ac825205db46'

# Base de conocimiento estado de animo----------------------------------------------------------------
estado_animo_opciones = {
    "Feliz": [
        "¡Qué bueno que estés feliz! Recuerda que la felicidad es un estado de ánimo que se puede cultivar.",
        "La felicidad es un derecho, no un privilegio. ¡Disfruta de cada momento!",
        "La sonrisa es el mejor maquillaje. ¡No te olvides de sonreír!"
    ],
    "Triste": [
        "Lo siento que estés triste. Recuerda que la tristeza es un estado de ánimo que puede cambiar.",
        "No te rindas. La vida es un ciclo y la tristeza es solo una parte de él.",
        "Habla con alguien de confianza. A veces, solo necesitamos alguien que nos escuche."
    ],
    "Enojado": [
        "Entiendo que estés enojado. Recuerda que el enojo es un estado de ánimo que puede ser manejado.",
        "No dejes que el enojo te consuma. Toma un respiro y piensa en lo que puedes hacer para cambiar la situación.",
        "El enojo es un sentimiento natural, pero no tiene que controlarte. ¡Tú eres el dueño de tus emociones!"
    ],
    "Ansioso": [
        "Lo siento que estés ansioso. Recuerda que la ansiedad es un estado de ánimo que puede ser manejado.",
        "No te preocupes por el futuro. El presente es lo que importa.",
        "Toma un respiro y enfócate en el momento. La ansiedad no puede controlarte si no le das permiso."
    ]
}

# Base de conocimiento trivia emociones---------------------------------------------------------------
trivias = {
    'Feliz': [
        {"pregunta": "¿Cuál es el color que se asocia con la felicidad?",
         "opciones": ["Amarillo", "Rojo", "Verde"],
         "respuesta_correcta": "Amarillo"},
        {"pregunta": "¿Cuál es el animal que se considera símbolo de la felicidad?",
         "opciones": ["Perro", "Gato", "Pájaro"],
         "respuesta_correcta": "Perro"},
        {"pregunta": "¿Cuál es el tipo de música que se asocia con la felicidad?",
         "opciones": ["Clásica", "Rock", "Pop"],
         "respuesta_correcta": "Pop"}
    ],
    'Triste': [
        {"pregunta": "¿Cuál es el color que se asocia con la tristeza?",
         "opciones": ["Azul", "Rojo", "Verde"],
         "respuesta_correcta": "Azul"},
        {"pregunta": "¿Cuál es el animal que se considera símbolo de la tristeza?",
         "opciones": ["Tortuga", "Gato", "Pájaro"],
         "respuesta_correcta": "Tortuga"},
        {"pregunta": "¿Cuál es el tipo de música que se asocia con la tristeza?",
         "opciones": ["Clásica", "Rock", "Blues"],
         "respuesta_correcta": "Blues"}
    ],
    'Enojado': [
        {"pregunta": "¿Cuál es el color que se asocia con la ira?",
         "opciones": ["Rojo", "Amarillo", "Verde"],
         "respuesta_correcta": "Rojo"},
        {"pregunta": "¿Cuál es el animal que se considera símbolo de la ira?",
         "opciones": ["León", "Gato", "Pájaro"],
         "respuesta_correcta": "León"},
        {"pregunta": "¿Cuál es el tipo de música que se asocia con la ira?",
         "opciones": ["Rock", "Pop", "Heavy Metal"],
         "respuesta_correcta": "Heavy Metal"}
    ],
    'Ansioso': [
        {"pregunta": "¿Cuál es el color que se asocia con la ansiedad?",
         "opciones": ["Gris", "Azul", "Verde"],
         "respuesta_correcta": "Gris"},
        {"pregunta": "¿Cuál es el animal que se considera símbolo de la ansiedad?",
         "opciones": ["Rata", "Gato", "Pájaro"],
         "respuesta_correcta": "Rata"},
        {"pregunta": "¿Cuál es el tipo de música que se asocia con la ansiedad?",
         "opciones": ["Electrónica", "Rock", "Pop"],
         "respuesta_correcta": "Electrónica"}
    ]
}
#Base de conocimiento cultura general------------------------------------------------------------------
preguntas_cultura = [
    {"pregunta": "¿Cuál es la capital de Francia?", "respuesta_correcta": "París"},
    {"pregunta": "¿En qué año llegó el hombre a la Luna?", "respuesta_correcta": "1969"},
    {"pregunta": "¿Quién pintó la Mona Lisa?", "respuesta_correcta": "Leonardo da Vinci"},
    {"pregunta": "¿Cuál es el río más largo del mundo?", "respuesta_correcta": "Nilo"},
    {"pregunta": "¿Cuál es el idioma más hablado en el mundo?", "respuesta_correcta": "Chino Mandarín"}
]
#Productos--------------------------------------------------------------------------------------------
products = [
    {
        'name': 'Producto 1',
        'description': 'Descripción del Producto 1',
        'price': '$10.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
    {
        'name': 'Producto 2',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/z7B3b0X',
        'cantidad':'10',
        'CAD':'05/11/2030'
    },
    {
        'name': 'Producto 3',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/WtPf8yc',
        'cantidad':'10',
        'CAD':'05/11/2031'
    },
    {
        'name': 'Producto 4',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2026'
    },
    {
        'name': 'Producto 5',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
    {
        'name': 'Producto 6',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
]
#Base de conocimientos precios productos
products_list = [
    {"name": "Paletas", "price": 100},
    {"name": "Pantalla", "price": 200000},
    {"name": "Celular", "price": 5000},
    {"name": "Monitor", "price": 3000},
    {"name": "Teclado", "price": 1000},
]

# Menu principal--------------------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /Inicio command."""
    keyboard = [
        [
            InlineKeyboardButton("PSICOLOGO ", callback_data='1'),
            InlineKeyboardButton("INTERRACCION BOT", callback_data='2'),
            InlineKeyboardButton("VENTA", callback_data='3'),
            InlineKeyboardButton("CLIMA (API)", callback_data='4'),
            InlineKeyboardButton("CODIGO", callback_data='5'),
        ],
        [InlineKeyboardButton("Opción 6", callback_data='6')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("MENU PRINCIPAL\nSELECCIONA UNA OPCIÓN: ", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text("MENU PRINCIPAL\nSELECCIONA UNA OPCIÓN: ", reply_markup=reply_markup)

# BUTTON-------------------------------------------------------------------------------------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button press."""
    query = update.callback_query
    await query.answer()
    data = query.data
    #OPCION 1--------------------------------------------
    if data == '1':
        keyboard = [
            [
                InlineKeyboardButton("Estado de ánimo", callback_data='1.1'),
                InlineKeyboardButton("Trivia", callback_data='1.2')
            ],
            [InlineKeyboardButton("Regresar al menú Principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Seleccionaste la opción 1. Ahora selecciona una subopción:", reply_markup=reply_markup)
    elif data == '1.1':
        await estado_animo(update, context)
    elif data == '1.2':
        if 'estado_animo' not in context.user_data:
            await query.edit_message_text(text="Por favor, selecciona un estado de ánimo antes de continuar.")
        else:
            await trivia_estado_animo(update, context)
    elif data == 'main_menu':
        await start(update, context)
    elif data in ['estado_animo_feliz', 'estado_animo_triste', 'estado_animo_enojado', 'estado_animo_ansioso']:
        await estado_animo_seleccionado(update, context)
    elif data.startswith('trivia_'):
        await manejar_respuesta_trivia(update, context, data)
    
    #OPCION 2--------------------------------------------
    if query.data == '2':
        # Submenú para la Opción 2
        keyboard = [
            [InlineKeyboardButton("Interacción bot", callback_data='2.1')],
            [InlineKeyboardButton("Preguntas de Cultura", callback_data='2.2')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Seleccionaste la opción 2. Ahora selecciona una subopción:", reply_markup=reply_markup)
        return

    # Submenú I - Interacción
    elif query.data == '2.1':
        await interaccion(update, context)
        return
    
    # Submenú II - Preguntas de Cultura
    elif query.data == '2.2':
        await pregunta_cultura_aleatoria(update, context)
        return

    elif query.data == 'main_menu':
        await start(update, context)
        return
    #OPCION 3--------------------------------------------
    if query.data == '3':
        # Submenú para la Opción 2
        keyboard = [
            [InlineKeyboardButton("Productos", callback_data='3.1')],
            [InlineKeyboardButton("Suma de productos", callback_data='3.2')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Seleccionaste la opción 3. Ahora selecciona una subopción:", reply_markup=reply_markup)
        return

    elif query.data == '3.1':
        await show_products(update, context)
        return
    
    elif query.data == '3.2':
        await suma_productos(update, context)
        return

    elif query.data == 'main_menu':
        await start(update, context)
        return
    #OPCION 4
    if query.data == '4':
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Mexico City&appid={API_KEY}&units=metric"

        # Realiza la solicitud a la API
        response = requests.get(url)
        data = response.json()

        # Extrae la temperatura
        temperature = data['main']['temp']

        # Mensaje con la temperatura
        message = f"El clima en CDMX es {temperature}°C"

        # Envía el mensaje de vuelta al usuario
        await update.callback_query.message.reply_text(message)
        return
    #OPCION 5
    if query.data == '5':
         # Submenú para la Opción 2
        keyboard = [
            [InlineKeyboardButton("Descarga codigo", callback_data='5.1')],
            [InlineKeyboardButton("Salir del bot", callback_data='5.2')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Seleccionaste la opción 3. Ahora selecciona una subopción:", reply_markup=reply_markup)
        return

    elif query.data == '5.1':
        await descarga_codigo(update, context)
        return
    
    elif query.data == '5.2':
        await salir_bot(update, context)
        return

    elif query.data == 'main_menu':
        await start(update, context)
        return
# Estado de animo--------------------------------------------------------------------------------------------------------------------------
async def estado_animo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle estado de ánimo."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Feliz", callback_data='estado_animo_feliz'),
            InlineKeyboardButton("Triste", callback_data='estado_animo_triste')
        ],
        [
            InlineKeyboardButton("Enojado", callback_data='estado_animo_enojado'),
            InlineKeyboardButton("Ansioso", callback_data='estado_animo_ansioso')
        ],
        [InlineKeyboardButton("Regresar al menú Principal", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="¿Cuál es tu estado de ánimo?", reply_markup=reply_markup)

async def estado_animo_seleccionado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle estado de ánimo seleccionado."""
    query = update.callback_query
    await query.answer()
    data = query.data

    estado_animo_mapping = {
        'estado_animo_feliz': 'Feliz',
        'estado_animo_triste': 'Triste',
        'estado_animo_enojado': 'Enojado',
        'estado_animo_ansioso': 'Ansioso'
    }

    estado_animo = estado_animo_mapping.get(data)
    if estado_animo:
        context.user_data['estado_animo'] = estado_animo
        mensaje = random.choice(estado_animo_opciones[estado_animo])
        await query.edit_message_text(text=mensaje)

        # Regresar al submenú después de seleccionar el estado de ánimo
        keyboard = [
            [
                InlineKeyboardButton("Estado de ánimo", callback_data='1.1'),
                InlineKeyboardButton("Trivia", callback_data='1.2')
            ],
            [InlineKeyboardButton("Regresar al menú Principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Seleccionaste la opción 1. Ahora selecciona una subopción:", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text="Estado de ánimo no reconocido. Por favor, intenta nuevamente.")

# Trivia estado de animo-------------------------------------------------------------------------------------------------------------------
async def trivia_estado_animo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle trivia estado de ánimo."""
    query = update.callback_query
    await query.answer()

    # Obtener el estado de ánimo previamente seleccionado
    estado_animo = context.user_data.get('estado_animo')

    if estado_animo is None:
        await query.edit_message_text(text="No se ha seleccionado un estado de ánimo. Por favor, selecciona uno primero.")
        return

    # Seleccionar una trivia al azar según el estado de ánimo
    trivia = random.choice(trivias[estado_animo])
    context.user_data['trivia_actual'] = trivia  # Guardar la trivia actual para validar la respuesta posteriormente

    # Mostrar la trivia
    keyboard = [
        [InlineKeyboardButton(opcion, callback_data=f"trivia_respuesta_{opcion}") for opcion in trivia["opciones"]],
        [InlineKeyboardButton("Regresar", callback_data='1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Trivia de estado de ánimo ({estado_animo}): {trivia['pregunta']}", reply_markup=reply_markup)

async def manejar_respuesta_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    """Maneja la respuesta seleccionada en la trivia."""
    query = update.callback_query
    await query.answer()

    if 'trivia_actual' not in context.user_data:
        await query.edit_message_text(text="No hay una trivia en curso. Por favor, inicia una nueva trivia.")
        return

    trivia = context.user_data['trivia_actual']
    respuesta_usuario = data.replace('trivia_respuesta_', '')

    if respuesta_usuario == trivia['respuesta_correcta']:
        mensaje = "¡Correcto! 🎉"
    else:
        mensaje = f"Incorrecto. La respuesta correcta era: {trivia['respuesta_correcta']}."

    # Mostrar resultado y regresar al submenú
    await query.edit_message_text(text=mensaje)

    keyboard = [
        [
            InlineKeyboardButton("Estado de ánimo", callback_data='1.1'),
            InlineKeyboardButton("Trivia", callback_data='1.2')
        ],
        [InlineKeyboardButton("Regresar al menú Principal", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Selecciona una subopción:", reply_markup=reply_markup)

# Interaccion con bot-----------------------------------------------------------------------------------------------------------------------
async def interaccion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Interacción con el usuario."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="¿Cuál es tu nombre?")
    context.user_data['interaccion'] = 'nombre'

async def manejar_interaccion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar la interacción con el usuario."""
    if 'interaccion' in context.user_data:
        step = context.user_data['interaccion']
        text = update.message.text
        
        if step == 'nombre':
            context.user_data['nombre'] = text
            await update.message.reply_text(f"Tu nombre es {text}. ¿Cuál es tu edad?")
            context.user_data['interaccion'] = 'edad'
        
        elif step == 'edad':
            context.user_data['edad'] = text
            await update.message.reply_text(f"Tu edad es {text}. ¿Cuál es tu número de teléfono?")
            context.user_data['interaccion'] = 'telefono'
        
        elif step == 'telefono':
            context.user_data['telefono'] = text
            await update.message.reply_text(f"Tu número de teléfono es {text}. ¿Cuál es tu dirección?")
            context.user_data['interaccion'] = 'direccion'
        
        elif step == 'direccion':
            context.user_data['direccion'] = text
            await update.message.reply_text(f"Tu dirección es {text}. ¡Gracias por compartir tu información!")
            # Limpiar el estado de interacción
            context.user_data.pop('interaccion', None)
            await mostrar_opcion_2(update, context)


#Preguntas cultura general---------------------------------------------------------------------
async def pregunta_cultura_aleatoria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Seleccionar una pregunta aleatoria
    pregunta = random.choice(preguntas_cultura)
    
    # Mostrar la pregunta
    context.user_data['pregunta_correcta'] = pregunta['respuesta_correcta']
    await query.edit_message_text(text=pregunta['pregunta'])
    context.user_data['modo_cultura'] = True

async def verificar_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'modo_cultura' in context.user_data and context.user_data['modo_cultura']:
        respuesta = update.message.text
        respuesta_correcta = context.user_data['pregunta_correcta']
        
        if respuesta.lower() == respuesta_correcta.lower():
            await update.message.reply_text("¡Correcto!")
            context.user_data.pop('modo_cultura', None)
            context.user_data.pop('pregunta_correcta', None)
            await mostrar_opcion_2(update, context)
        else:
            await update.message.reply_text("Respuesta incorrecta. Intenta de nuevo.")
#Mostrar productos------------------------------------------------------------------------------------
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show products to the user."""
    context.user_data['modo_cultura'] = False
    context.user_data['modo_producto'] = True  # Agregué esta línea
    messages = []
    for product in products:
        message = (
            f"*{product['name']}*\n"
            f"{product['description']}\n"
            f"Price: {product['price']}\n"
            f"[Image]({product['image_url']})\n"
            f"Cantidad: {product['cantidad']}\n"
            f"CAD: {product['CAD']}"
        )
        messages.append(message)
    
    for message in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
    #Regresar al menu de ventas
    await mostrar_opcion_3(update, context)
    
#Suma de productos------------------------------------------------------------------------------
def suma_productos(update: Update, context: CallbackContext):
    # Preguntar por el precio del producto 1
    update.message.reply_text("Ingrese el precio del producto 1:")
    producto_1 = float(context.bot.get_updates()[-1].message.text)
    
    # Preguntar por el precio del producto 2
    update.message.reply_text("Ingrese el precio del producto 2:")
    producto_2 = float(context.bot.get_updates()[-1].message.text)
    
    # Calcular el total
    total = producto_1 + producto_2
    
    # Mostrar el total
    update.message.reply_text(f"El total es: {total}")
#Mostrar menu principal------------------------------------------------------------------------

#Mostrar menu opcion 2-------------------------------------------------------------------------
async def mostrar_opcion_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Interacción", callback_data='2.1')],
        [InlineKeyboardButton("Preguntas de Cultura", callback_data='2.2')],
        [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text("Seleccionaste la opción 2. Ahora selecciona una subopción:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text="Seleccionaste la opción 2. Ahora selecciona una subopción:", reply_markup=reply_markup)
#Mostrar menu opcion 3-------------------------------------------------------------------------
async def mostrar_opcion_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Productos", callback_data='3.1')],
        [InlineKeyboardButton("Suma de productos", callback_data='3.2')],
        [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text("Seleccionaste la opción 3. Ahora selecciona una subopción:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text="Seleccionaste la opción 3. Ahora selecciona una subopción:", reply_markup=reply_markup)
#API----------------------------------------------------------------------------------------------------------------------

#Descargar codigo---------------------------------------------------------------------------------------------------------
async def descarga_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the code download request."""
    # El archivo debe estar en el mismo directorio que el script o proporcionar una ruta correcta.
    file_path = 'botTelegramFinal.py'  # Nombre del archivo con el código del bot.
    
    try:
        with open(file_path, 'rb') as file:
            await update.callback_query.message.reply_document(
                document=InputFile(file, filename='bot_code.py'),
                caption="Aquí está el código del bot que solicitaste."
            )
    except FileNotFoundError:
        await update.callback_query.message.reply_text("No se pudo encontrar el archivo del código.")
    except Exception as e:
        await update.callback_query.message.reply_text(f"Ocurrió un error: {str(e)}")

async def salir_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle bot exit."""
    await update.callback_query.message.reply_text("¡Gracias por usar el bot! Hasta luego.")
    # Opcionalmente puedes agregar lógica para finalizar la interacción del usuario si es necesario.     
#--------------------------------------------------------------------------------------------------------------
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    
    if 'espera_ciudad' in user_data:
        city_name = update.message.text
       # weather_info = get_weather(city_name)
       # await update.message.reply_text(weather_info)
        user_data.pop('espera_ciudad', None)  # Limpia el estado de espera
    elif user_data.get('modo_cultura', False):
        await verificar_respuesta(update, context)
    elif user_data.get('modo_producto', False):
        if user_data.get('productos_vistos', False):
            # El usuario ha visto la lista de productos, no hacer nada
            pass
        else:
            await show_products(update, context)
    elif 'producto1' in user_data and 'producto2' in user_data:
        await suma_productos(update, context)
    else:
        await manejar_interaccion(update, context)

# Función principal
def main():
    """Inicia el bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('Inicio', start))
    application.add_handler(CommandHandler('start', start))  # Por si el usuario usa /start
    application.add_handler(CallbackQueryHandler(button))
   # application.add_handler(CommandHandler('clima', clima))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, suma_productos))
    application.run_polling()

if __name__ == '__main__':
    main()