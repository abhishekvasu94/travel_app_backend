curl -X 'GET' \
        'http://127.0.0.1:8000/get_route' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "selected_cities": [
        "Oaxaca", "Mexico City", "Puebla", "Merida"
        ]
    }'
