# -*- coding: utf-8 -*- 
#!/usr/bin/python
from AFDc import *

def afd_minimo(archivo_regex, archivo_automata):
    afd = fromRegex(archivo_regex);
    print afd.estados
    print afd.delta
    afd.determinizar();
    afd.minimizar();
    afd.toFile(archivo_automata);
