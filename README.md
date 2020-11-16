## Cumplo Demo
Construir una aplicación web que permita obtener el valor de la UDIS y el dólar, asi tambien presentar un demo con los lideres técnicos

### Módulos incluidos
 - Una vista web para filtar valores historicos del dolares o udis por rango de fechas,
 valores minimo, maximo, promedio y una grafica de los mismo.
 - Comando para obtener valores historicos del dolar y udis


### Requerimientos
 - Python 3.8
 - Virtualenv
 - MySQL 8.0.22
 - Baxico [Documentacion API](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/consultaDatosSerieRango)  
 - Token Banxico [Obtener token](https://www.banxico.org.mx/SieAPIRest/service/v1/;jsessionid=5fa4f900baccc38cd60cb4f38981)
 - Formateador Black [Black](https://github.com/psf/black) 
 

### Installation

Clonación del proyecto
```sh
git clone https://github.com/jdht1992/cumplo.git
```

Crear y activar virtualenv
```sh
python3 -m venv env_cumplo
source env_cumplo/bin/activate
```
Instalacion de paquetes
```
cd cumplo
pip install -r requirements.txt
```

### Ejecutar proyecto 

Se aplican las migraciones y se corre el proyecto
```sh
python manage.py migrate
python manage.py runserver
```

#### Comando para obtener los valores de dollar y udis
```sh
python manage.py get_currency_values --kind "DOLLAR" --date_start "2020-11-01" --date_end "2020-11-16"
python manage.py get_currency_values --kind "UDIS" --date_start "2020-11-01" --date_end "2020-11-16"

```

### Mejoras
Para mejorar este proyecto recomiendo las siguientes acciones
 - Integracion de Docker y docker-compose para mejorar la compatibilidad.
 - Manejar el command mediante un crontab para automatizar.
 - Agregar Pruebas Unitarias y pytest
 - Preteger las credenciales usando [Django-environ](https://github.com/joke2k/django-environ)
 - Agregar un logging
    