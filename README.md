# PRUEBA BACKEND DEVELOPER

A continuación se muestra el proceso de ejecución del proyecto para que se pueda hacer uso del mismo:

Esta es una aplicación de backend que utiliza FastAPI, PostgreSQL, HubSpot y ClickUp para crear contactos, sincronizarlos y registrar llamadas a la API en una base de datos.

## Instalación

1. Asegúrate de tener Python 3.7 o una versión superior instalada en tu sistema.
    - Si no la tiene instalada dirigirse a https://www.python.org/downloads/ y descargarlo de acuerdo al sistema operativo

2. Clonar el repositorio en cualquier directorio del sistema.

3. Abrir la consla del sistema:
    - Windows: CMD
    - MacOS/Linux: Terminal

4. Navega hasta el directorio del proyecto:
```
cd ruta/al/directorio
```

4. Crea y activa un entorno virtual para aislar las dependencias del proyecto:
```
python -m venv env       # Crear el entorno virtual
source env/Scripts/activate   # Activar el entorno virtual en Windows/Linux/MacOS
```

5. Instala las dependencias del proyecto con pip:
```
pip install fastapi requests sqlalchemy psycopg2 uvicorn
```

6. Ejecuta el servidor de aplicación usando FastAPI:
```
uvicorn main:app --reload
```

## Validación

1. La aplicación ahora se ejecuta en el servidor local. por lo general se utiliza erl puerto 8000 para la aplicación `http://localhost:8000`.

## Uso

La aplicación proporciona los siguientes endpoints:

- `POST /create_contact`: Crea un nuevo contacto en HubSpot y sincronízalo con ClickUp.
    * El body de la petición debe ser la siguiente estructura
    ```
    {
        "email": "mail@email.io",
        "firstname": "firstname",
        "lastname": "lastname",
        "phone": "573214567890",
        "website": "domain.com"
    }
    ```

- `POST /sync_contacts`: Sincroniza los contactos existentes en HubSpot con ClickUp.

- Se puede hacer uso de Postman para el envío de las peticiones al API.

# Licencia

Aplicación desarrollada únicamente con el fin de demostrar conocimientos en el área, el uso del mismo es interno para pruebas y conocimiento de los servicios integrados.

Todos los datos, código y accesos establecidos fueron planeados y ejecutados por @jvillabonp. Para cualquier cambio o adición contactar mediante este medio.