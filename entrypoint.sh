#!/bin/bash

# Inicia o webserver em background
python src/webserver.py &

# Aguarda um pouco para o webserver iniciar
sleep 2

# Inicia o bot
python main.py
