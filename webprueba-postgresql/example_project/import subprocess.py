#!usr/bin/env Python

import os, sys


# Ejecutar un comando con "os.system(comando)" y mostrar en
# pantalla la salida del comando y el resultado de la 
# ejecución.
# Si su valor es 0 la ejecución finalizó con éxito.


valor1 = os.system("cd /home/aaron/Desktop/django/1.django-dynamic-scraper/example_project")
valor2 = os.system("scrapy crawl article_spider -a id=1 -a do_action=yes")
valor3 = os.system("scrapy crawl article_spider -a id=2 -a do_action=yes")
