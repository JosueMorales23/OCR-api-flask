# Proyecto de Prueba: Encriptar y Desencriptar Imágenes con Tesseract OCR

Este proyecto es un ejemplo de cómo cifrar y descifrar imágenes utilizando el algoritmo AES en modo CFB, y luego 
extraer texto de la imagen descifrada utilizando Tesseract OCR. Incluye un servidor Flask que maneja el proceso 
y un script de cliente para probarlo.

## Instalación

1. Clona este repositorio en tu máquina local:
````
git clone https://github.com/JosueMorales23/OCR-api-flask.git
cd OCR-api-flask
````

2. Instale las dependencias requeridas usando pip:
```
pip install -r requirements.txt
 ```

3. Ejecute el servidor Flask:
```
python app.py
 ```

4. Abra otra ventana de terminal y ejecute el script del cliente:
```
python client.py
```
Asegúrese de tener instalado Python 3.x.

## Requisitos

Puede encontrar los paquetes de Python necesarios en el archivo `requirements.txt`. Instálalos usando el siguiente
comando:
```
pip install -r requirements.txt
```

## Uso

1. Coloque la imagen que desea cifrar en el directorio raíz del repositorio.

2. Ejecute el servidor Flask usando `python app.py`.

3. Ejecute el script del cliente usando `python client.py`. El script enviará la imagen al servidor para el cifrado,
   descifrado y extracción de texto.

## Notas

- Asegúrate de reemplazar `'ruta_a_tu_imagen.jpg'` en el script `client.py` con la ruta real a la imagen que deseas
  usar.

- El servidor Flask asume que se está ejecutando en `http://localhost:5000/process_image`. Actualice la
  variable `server_url` en el script `client.py` si su servidor se ejecuta en una dirección diferente.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

