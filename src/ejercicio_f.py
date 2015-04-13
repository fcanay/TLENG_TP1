# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc


def equivalentes(archivo_automata1, archivo_automata2):
    afd1 = fromFile(archivo_automata1);
    afd2 = fromFile(archivo_automata2);
    if afd1.equivalente(afd2):
    	print "TRUE";
    else:
    	print "FALSE";
