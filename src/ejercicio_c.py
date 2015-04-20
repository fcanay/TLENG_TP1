# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def grafo(archivo_automata, archivo_dot):
    afd = AFDc.fromFile(archivo_automata)
    afd.toDOT(archivo_dot)