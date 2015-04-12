# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc


def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
    afd1 = fromFile(archivo_automata1);
    afd2 = fromFile(archivo_automata2);
    afd3 = afd1.interseccion(afd2);
    afd3.minimizar();
    afd3.toFile(archivo_automata);