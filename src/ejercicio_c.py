# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def grafo(archivo_automata, archivo_dot):
    afd = AFDc.fromFile(archivo_automata)
    # print afd.estados
    # print afd.delta
    # print afd.estado_inicial
    # print afd.estados_finales
    # print afd.alfabeto
    afd.toDOT(archivo_dot)