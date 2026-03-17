
# ExamenIIParcialArquitectura
Examen II parcial usando Django, psutil, python, docker

INTEGRANTES: 
Victor Raul Martinez Salazar 202310010415
Carlos Dario Garcia Villalvir 202210011005

=======
--Monitor de Sistema

Aplicacion Django que muestra en tiempo real el estado del sistema (CPU, RAM y disco) usando la librería externa psutil

--Instalacion de dependencias para ejecutar de manera local

1. Crear y activar un entorno virtual. el proyecto se llama "monitor", para activar el entorno virtual ejecutar el comando en la terminal "python -m venv venv" y luego venv\Scripts\Activate
2. Ejecutar "pip install -r requirements.txt" para instalar Django y "psutil".

-- Ejecución local

1. Asegurarse de estar en la carpeta raíz del proyecto "Monitor".
2. Ejecuta "python manage.py migrate" 
3. Levanta el servidor con "python manage.py runserver"
4. Accede a "http://127.0.0.1:8000" para ver los datos del sistema.

-- si ya esta docker instalado en nuestra compu, clonar el repositorio y ejecutar el comando docker-compose up --build, luego entrar a la url http://127.0.0.1:8000 para ver el sistema ejecutandose

