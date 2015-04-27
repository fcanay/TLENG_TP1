# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def complemento(archivo_automata1, archivo_automata):
    afd = AFDc.fromFile(archivo_automata1)
    afd.complemento()
    afd.minimizar()
    afd.toFile(archivo_automata)
