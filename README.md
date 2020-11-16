## Cumplo Demo
Construir una aplicación web que permita obtener el valor de la UDIS y el dólar. Y presentar un demo con los lideres técnicos

### Requerimientos
 - Python 3.8
 - Virtualenv
 - MySQL 8.0.22
 - Baxico [API](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/consultaDatosSerieRango)  
 - Token Banxico [Token](https://www.banxico.org.mx/SieAPIRest/service/v1/;jsessionid=5fa4f900baccc38cd60cb4f38981)
 

### Installation

Clonación del proyecto
```sh
git clone https://github.com/jdht1992/cumplo.git
```

Crear virtualenv
```sh
python3 -m venv env_cumplo
source env_cumplo/bin/activate
```
Instalacion de paquetes
```
cd cumplo
pip install -r requirements.txt
```

### Run 
Comando para migrar, correr y demas, como se corre el command

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