# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def afd_minimo(archivo_regex, archivo_automata):
    afd = fromRegex(archivo_regex);
    afd.determinizar();
    afd.minimizar();
    afd.toFile(archivo_automata);
