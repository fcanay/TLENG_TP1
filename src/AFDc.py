import sys
import os

nuestroLambda = ""

#auxiliares
def partition(s):
	lines = s
	res = []
	i = 1
	while i < len(lines):
		res.append([lines[i][1:]])
		i+=1
		while (i < len(lines)) and (lines[i][1] == "\t"):
			res[len(res)-1].append(lines[i][1:])
			i+=1
	return res

def fromRegex(regex_file):
	lines = regex_file.readlines()
	return createFromRegex(lines)

#Define un automata recursivamente a partir de una expresion regular
def createFromRegex(s):
	if s[0][0] != '{':		
		if s[0][0] == '\\' and len(s[0]) > 1 and s[0][1] == 't':
			return letra('\t')
		return letra(s[0][0])
	parts = partition(s)
	afd = createFromRegex(parts[0])
	if s[0][0:8] == "{CONCAT}":
		for x in xrange(1,int(s[0][8])):
			afd.concat(createFromRegex(parts[x]))

	elif s[0][0:6] == "{STAR}":
		afd.star()
	elif s[0][0:6] == "{PLUS}":
		afd.plus()
	elif s[0][0:5] == "{OPT}":
		afd.opt()
	elif s[0][0:4] == "{OR}":
		for x in xrange(1,int(s[0][4])):
			afd.orAFD(createFromRegex(parts[x]))
	return afd

#casos base de creacion de automata
def letra(caracter):
	res = AFD()
	res.agregar_estado()
	res.agregar_estado()
	res.alfabeto = [caracter]
	res.agregar_transicion(1, caracter, 2)
	res.estados_finales = [2]
	res.estado_inicial = 1
	return res

def lambdaAFD():
	res = AFD()
	res.agregar_estado
	res.estados_finales = [1]
	res.estado_inicial = 1
	return res

def fromFile(file):
	afd = AFD()

	auxEstados = file.next().replace('\n','').split('\t')
	for est in auxEstados:
		afd.estados.append(est)
		afd.delta[est] = []

	afd.alfabeto = file.next().replace('\n','').split('\t')

	afd.estado_inicial = file.next().split()[0]

	auxEstados = file.next().replace('\n','').split('\t')
	for est in auxEstados:
		if est != "":
			afd.estados_finales.append(est)

	for line in file:
		pieces = line.replace('\n','').split('\t')
		if len(pieces) == 3:
			afd.agregar_transicion(pieces[0], pieces[1], pieces[2])

	afd.nodosToInt()

	return afd
		
class AFD:

		# estados
			# lista de estados del AFD
		# delta
			# Funcion de transicion de estados -> (char,estado)
		# estados_finales
		# alfabeto
		# estado_inicial

	def __init__(self):
		self.estados = []
		self.delta = {}
		self.estados_finales = []
		self.alfabeto = []
		self.estado_inicial = None

	def copy(self):
		res = AFD()
		res.estados = self.estados
		res.delta = self.delta
		res.estados_finales = self.estados_finales
		res.alfabeto = self.alfabeto
		res.estado_inicial = self.estado_inicial
		return res

	def agregar_estado(self):
		i = len(self.estados) + 1
		self.estados.append(i)
		self.delta[i] = []
		return i

	def agregar_transicion(self,estado1,char,estado2):
		enEstados1 = estado1 in self.estados
		enEstados2 = estado2 in self.estados
		enAlfabetoOLambda = (char in self.alfabeto) or (char == nuestroLambda)
		queNoEste = (char,estado2) not in self.delta[estado1]
		if enEstados1 and enEstados2 and enAlfabetoOLambda and queNoEste:
			self.delta[estado1].append((char,estado2)) 


	def acepta(self,cadena):
		return self.acepta_desde(self.estado_inicial,cadena)

	def acepta_desde(self, estado, cadena):
		estado = int(estado)
		if len(cadena) == 0:
			return estado in self.estados_finales

		aux = [ est for (letra, est) in self.delta[estado] if letra == cadena[0]]

		valeCadena = False
		cadenaSiguiente = cadena[1:len(cadena)]
		for est in aux:
			valeCadena = valeCadena or self.acepta_desde(est, cadenaSiguiente)

		return valeCadena

	def reorganizarEstados(self, i):
		deltaAux = {}
		for est in self.estados:
			deltaAux[est+i] = [(char,e + i) for (char,e) in self.delta[est]]
		self.delta = deltaAux
		self.estados = [est + i for est in self.estados]
		self.estado_inicial += i
		self.estados_finales = [est + i for est in self.estados_finales]

	#casos recursivos de creacion de automata
	def concat(self, otroAFD):
		#Reorganizo estados y delta
		otroAFD.reorganizarEstados(len(self.estados))


		for x in xrange(0,len(otroAFD.estados)):
			self.agregar_estado()

		for e in otroAFD.estados:
			self.delta[e] = otroAFD.delta[e]
		# lambda es ' '. Checkear que onda con "acepta"
		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, otroAFD.estado_inicial)

		self.estados_finales = otroAFD.estados_finales
		
		#Nuevo Alfabeto
		self.alfabeto = list(set(self.alfabeto + otroAFD.alfabeto))

	def star(self):
		#Reorganizo estados y delta
		estadoInicial = self.agregar_estado() 
		estadoFinal = self.agregar_estado()

		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
			self.agregar_transicion(final, nuestroLambda, self.estado_inicial)

		self.estados_finales = [estadoFinal]

		#Actualizo estados inciales
		self.agregar_transicion(estadoInicial, nuestroLambda, self.estado_inicial)
		self.agregar_transicion(estadoInicial, nuestroLambda, estadoFinal)

		self.estado_inicial = estadoInicial

	def plus(self):
		aux = self.copy()
		aux.star()
		return self.concat(aux)

	def opt(self):
		return self.orAFD(lambdaAFD())

	def orAFD(self, otroAFD):
		#Reorganizo estados y delta
		otroAFD.reorganizarEstados(len(self.estados))
		for x in xrange(0,len(otroAFD.estados)):
			self.agregar_estado()
		estadoInicial = self.agregar_estado()
		estadoFinal = self.agregar_estado()
		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
		for final in otroAFD.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
		for est in otroAFD.estados:
			self.delta[est] = self.delta[est] + otroAFD.delta[est]

		self.estados_finales = [estadoFinal]

		#Actualizo estados inciales
		self.agregar_transicion(estadoInicial, nuestroLambda, self.estado_inicial)
		self.agregar_transicion(estadoInicial, nuestroLambda, otroAFD.estado_inicial)

		self.estado_inicial = estadoInicial

		#Nuevo Alfabeto     
		self.alfabeto = list(set(self.alfabeto + otroAFD.alfabeto))

	def determinizar(self):

		res = AFD()
		res.alfabeto = self.alfabeto
		res.estado_inicial = self.ClausuraLambda(self.estado_inicial)
		porRecorrer = [list(res.estado_inicial)] 
		res.estado_inicial = ",".join(str(x) for x in res.estado_inicial)
		while len( porRecorrer ) > 0:
			#El nodo es un conjunto de estados de self
			nodo = porRecorrer.pop()
			res.estados.append(",".join(str(x) for x in nodo))
			res.delta[(",".join(str(x) for x in nodo))] = []

			for a in self.alfabeto:
				aux = self.Mover(nodo, a)
				if aux != []:
					res.delta[(",".join(str(x) for x in nodo))].append((a, ",".join(str(x) for x in aux)))
					if (",".join(str(x) for x in list(aux))) not in res.estados:
						porRecorrer.append(aux)
					
		for e in res.estados:
			for f in self.estados_finales:
				if str(f) in e:
					res.estados_finales.append(e)
					break

		res.nodosToInt()

		self.estados = res.estados
		self.estados_finales = res.estados_finales
		self.estado_inicial= res.estado_inicial
		self.alfabeto = res.alfabeto
		self.delta = res.delta

	#Auxiliares de determinizar
	def Mover(self,ests,char):
		aux = set()
		for est in ests:
			aux = aux.union(set([e for (c,e) in self.delta[est] if c == char]))
		res = set()
		for e in aux:
			res = res.union(self.ClausuraLambda(e))
		return list(res)

	def ClausuraLambda(self,e):
		res = set([e])
		porRecorrer = set([e])  
		while len(porRecorrer) > 0:
			aux = self.aUnPasoLamda(porRecorrer.pop()).difference(res)
			res = res.union(aux)
			porRecorrer = porRecorrer.union(aux)
		return res

	def aUnPasoLamda(self,e):
		return set([ x for (char,x) in self.delta[e] if x!=e and char == nuestroLambda])
	
	#Minimizar se llama siempre que el AF sea deterministico
	def minimizar(self):
		self.completar()
		clasesEquiv, matrizDeResultados = self.dameClasesEquiv()

		#Crear el nuevo AFD
		res = AFD()
		for est in clasesEquiv:
			res.estados.append(clasesEquiv[est])
		res.estados = list(set(res.estados)) #saco repe

		res.alfabeto = self.alfabeto
		res.estado_inicial = clasesEquiv[self.estado_inicial]
		for f in self.estados_finales:
			if clasesEquiv[f] not in res.estados_finales:
				res.estados_finales.append(clasesEquiv[f])

		for est in self.estados:
			res.delta[clasesEquiv[est]] = []
			for (char, est2) in matrizDeResultados[est]:
				res.delta[clasesEquiv[est]].append((char, est2))

		self.estados = res.estados
		self.estados_finales = res.estados_finales
		self.estado_inicial = res.estado_inicial
		self.alfabeto = res.alfabeto
		self.delta = res.delta

	def dameClasesEquiv(self):
		congruenciaVieja = {}
		congruenciaNueva = {}
		matrizDeResultados = {} #dado un estado, me da una lista de pares (caracter, clase de equivalencia)

		#Congruencia 0. Los finales van al 2, los otros al 1
		for est in self.estados:
			if est in self.estados_finales:
				congruenciaNueva[est] = 2
			else:
				congruenciaNueva[est] = 1

		while congruenciaVieja != congruenciaNueva:
			#Preparo para un nuevo loop
			matrizDeResultados = {}
			congruenciaVieja = congruenciaNueva
			congruenciaNueva = {}

			#Completamos la matriz de resultados
			for est in self.estados:
				matrizDeResultados[est] = []
				for letra in self.alfabeto:
					matrizDeResultados[est].append( (letra, congruenciaVieja[self.dameTransicion(est, letra)]) )

			#Creamos la nueva congruencia
			clasesDeEquiv = [] #Lista de pares(clase equiv de congruencia anterior, [clase equiv que vienen de matrizDeResultados])
			for est in self.estados:
				#claseActual es local al for
				claseActual = (congruenciaVieja[est], matrizDeResultados[est])  
				
				if not(claseActual in clasesDeEquiv):
					clasesDeEquiv.append(claseActual)
				
				congruenciaNueva[est] = clasesDeEquiv.index(claseActual) + 1
			
		return congruenciaNueva, matrizDeResultados

	#Solo usar si sabes que esta la transicion
	def dameTransicion(self, est, letra):
		for (char,estado) in self.delta[est]:
			if char == letra:
				return estado

	def toFile(self, file):
		lineas = []
		tab = "\t"

		lineasAux = []
		for est in self.estados:
			lineasAux.append(str(est))
		lineas.append( tab.join(lineasAux) )

		lineasAux = []
		for simbolo in self.alfabeto:
			if simbolo == "\t":
					simbolo = "\\t"
			lineasAux.append(str(simbolo))
		lineas.append( tab.join(lineasAux) )

		lineas.append( str(self.estado_inicial) )

		lineasAux = []
		for est in self.estados_finales:
			lineasAux.append(str(est))
		lineas.append( tab.join(lineasAux) )

		for transicion in self.delta:
			for (simbolo,estado) in self.delta[transicion]:
				if simbolo == "\t":
					simbolo = "\\t"
				lineas.append(tab.join([str(transicion), str(simbolo), str(estado)]))

		for linea in lineas:
			file.write(linea)
			file.write("\n")

	def toDOT(self, file):
		file.write("strict digraph {\n")
		file.write("\trankdir=LR;\n")
		file.write("\tnode [shape = none, label = \"\", width = 0, height = 0]; qd;\n")
		file.write("\tnode [label=\"\\N\", width = 0.5, width = 0.5];\n")
		file.write("\tnode [shape = doublecircle];")
		
		for est in self.estados_finales:
			file.write(" " + str(est))
		file.write(";\n")

		file.write("\tnode [shape = circle];\n")

		file.write("\tqd -> " + str(self.estado_inicial) + "\n")

		for est in self.estados:
			letrasAImprimir = {}
			for (letra, est2) in self.delta[est]:
				if est2 in letrasAImprimir:
					letrasAImprimir[est2].append(letra)
				else:
					letrasAImprimir[est2] = [letra]

			for est2 in letrasAImprimir:
				file.write("\t" + str(est) + " -> " + str (est2) + "[label=\"")
				for letra in letrasAImprimir[est2]:
					if letra == letrasAImprimir[est2][0]:
						# Casos letras especiales
						if letra == "\\t":
							letra = "\\\\t"
						if letra == nuestroLambda:
							letra = "lambda"
						if letra == " ":
							letra = "espacio"
						if letra == '\\':
							letra = '\\\\ '
							
						file.write(letra)
					else:
						# Casos letras especiales
						if letra == "\\t":
							letra = "\\\\t"
						if letra == nuestroLambda:
							letra = "lambda"
						if letra == " ":
							letra = "espacio"
						if letra == '\\':
							letra = '\\\\ '

						file.write(", " + letra)
				file.write("\"]\n")

		file.write("}")
		
	def interseccion(self, afd1):
		#El alfabeto final es la interseccion de ambos
		alfabetoFinal = [caracter for caracter in self.alfabeto if caracter in afd1.alfabeto]
		# Amplio alfabetos para que ambos tengan el mismo
		alfabetoGrande = list(set(self.alfabeto + afd1.alfabeto))
		self.alfabeto = alfabetoGrande
		#TODO: Habria que hacer una copia para no cambiar afd1?
		afd1Aux = afd1.copy()
		afd1Aux.alfabeto = alfabetoGrande 

		self.complemento()
		afd1Aux.complemento()
		self.orAFD(afd1Aux)

		# Arreglamos AFD antes de complementarlo porque orAFD no te asegura que sea deterministico, o completo
		self.determinizar()
		self.minimizar()
		self.complemento()
		self.alfabeto = alfabetoFinal


	def complemento(self):
		self.completar()
		self.estados_finales = [estado for estado in self.estados if estado not in self.estados_finales]
		
	def completar(self):
		estaCompleto = True
		for e in self.estados:
			charsAux = [char for (char,e1) in self.delta[e]]
			for char in self.alfabeto:
				if char not in charsAux:
					if estaCompleto:
						i = self.agregar_estado()
						estaCompleto = False
					self.agregar_transicion(e,char,i)

	# Toma un automata cuyos estados son de cualquier tipo y devuelve uno equivalente con estados enteros de 1 a len(estados)
	def nodosToInt(self):
		dicc = {}
		estados = range(1, len(self.estados) + 1)
		deltaAux = {}
		for i in estados:
			dicc[self.estados[i-1]] = i
		for i in estados:
			deltaAux[i] = [ (c,dicc[e]) for (c,e) in self.delta[self.estados[i-1]]]

		self.estados = estados
		self.delta = deltaAux
		self.estado_inicial = dicc[self.estado_inicial]
		self.estados_finales = [dicc[e] for e in self.estados_finales]

	def	equivalente(self, afd1):
		#Ampliamos alfabetos para luego preguntar equivalencia
		alfabetoGrande = list(set(self.alfabeto + afd1.alfabeto))
		selfAux = self.copy()
		afd1Aux = afd1.copy()
		selfAux.alfabeto = alfabetoGrande
		afd1Aux.alfabeto = alfabetoGrande
		return selfAux.incluidoEn(afd1Aux) and afd1Aux.incluidoEn(selfAux)

	def incluidoEn(self, afd1):
		selfAux = self.copy()
		afd1Aux = afd1.copy()
		afd1Aux.complemento()
		selfAux.interseccion(afd1Aux)
		selfAux.minimizar()
		return selfAux.esVacio()

	# Para ver si un automata ya minimizado es vacio, checkeamos si el inicial no esta en los finales (es decir, no acepta lambda)
	# y, por otro lado, que el inicial no pueda llegar con ninguna cadena a un estado final.
	def esVacio(self):
		yaRecorri = set()
		porRecorrer = set([self.estado_inicial])

		while len(porRecorrer) > 0:
			actual = porRecorrer.pop()
			if actual in self.estados_finales:
				return False
			yaRecorri.add(actual)
			for (char,e) in self.delta[actual]:
				if e not in yaRecorri:
					porRecorrer.add(e)

		return True
