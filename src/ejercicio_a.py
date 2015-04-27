# -*- coding: utf-8 -*- 
#!/usr/bin/python
from AFDc import *

def afd_minimo(archivo_regex, archivo_automata):
    afd = fromRegex(archivo_regex)
    print afd.estados
    print afd.delta
    print afd.estado_inicial
    print afd.estados_finales
    print afd.alfabeto
    afd.determinizar();
    #afd.minimizar();
    afd.toDOT(archivo_automata)
    #afd.toFile(archivo_automata);
