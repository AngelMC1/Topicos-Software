#!/bin/sh
set -e

echo ">>> Compilando traducciones..."
python manage.py compilemessages

echo ">>> Aplicando migraciones..."
python manage.py migrate --noinput

echo ">>> Cargando productos de prueba..."
python manage.py loaddata orders/fixtures/sample_products.json 2>/dev/null || echo "   (ya existían, omitiendo)"

echo ">>> Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
