# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
    afd1 = AFDc.fromFile(archivo_automata1)
    afd2 = AFDc.fromFile(archivo_automata2)
    afd1.interseccion(afd2)
    afd1.minimizar()
    afd1.toFile(archivo_automata)