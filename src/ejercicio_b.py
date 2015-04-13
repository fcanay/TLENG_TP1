# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc


def pertenece_al_lenguaje(archivo_automata, cadena):
    afd = fromFile(archivo_automata);
    if afd.acepta(cadena):
    	print "TRUE";
    else:
    	print "FALSE";
