# Places Finder App

Una aplicación Flask para buscar los mejores lugares en una ciudad según Google Maps Places API.

## 🚀 Cómo usar

1. Clona o descomprime este repositorio.
2. Instala dependencias:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Crea cuenta de google maps y genera una API key para utilizar en la aplicación:
https://developers.google.com/maps/documentation/places/web-service/get-api-key
4. Almacena la variable de entorno que contiene la APIKEY para google maps:
```bash
export PLACES_API_TOKEN="yor_amazing_api_key"
```
5. Ejecuta la app:

```bash
python app.py
```

:warning: Al ejecutar las queries, esperar a que el programa ejecute, puede tardar un buen rato.

. Visita `http://localhost:5000` en tu navegador.


---
