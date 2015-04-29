# -*- coding: utf-8 -*- 
#!/usr/bin/python
import AFDc

def equivalentes(archivo_automata1, archivo_automata2):
	afd1 = AFDc.fromFile(archivo_automata1)
	afd2 = AFDc.fromFile(archivo_automata2)
	if afd2.equivalente(afd1):
		print "TRUE"
	else:
		print "FALSE"
