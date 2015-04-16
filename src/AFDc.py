nuestroLambda = " "

#auxiliares
def partition(s):
	lines = s.split("\n")
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
	return  createFromRegex(lines)

def createFromRegex(s):
	if s[0] != '{':
		if s[0] == '\\' and len(s) > 1 and s[1] == 't':
			return letra('\t')
		return letra(s[0])
	parts = partition(s)
	afd = createFromRegex(parts[0])
	if s[0:7] == "{CONCAT}":
		for x in xrange(1,s[8]-1):
			afd.concat(createFromRegex(parts[x]))

	elif s[0:5] == "{STAR}":
		afd.star()
	elif s[0:5] == "{PLUS}":
		afd.plus()
	elif s[0:4] == "{OPT}":
		afd.opt()
	elif s[0:3] == "{OR}":
		for x in xrange(1,s[4]-1):
			afd.orAFD(createFromRegex(parts[x]))
	return afd

#casos base
def letra(caracter):
	res = AFD()
	res.estados = [1, 2]
	res.agregar_transicion(1, caracter, 2)
	res.estados_finales = [2];
	res.alfabeto = [caracter];
	res.estado_inicial = 1;
	return res

def lambdaAFD():
	res = AFD()
	res.estados = [1]
	res.estados_finales = [1]
	res.estado_inicial = 1
	return res

#TODO Funciona si el archivo tiene numeros en los nombres, sino cambiarlos antes de devolver el AFD
def fromFile(file):
	afd = AFD();
	auxEstados = file.next().split();
	for est in auxEstados:
		afd.agregar_estado();
	afd.alfabeto = file.next().split();
	afd.estado_inicial = file.next();
	afd.estados_finales = file.next().split();

	for line in file:
		pieces = line.split()
		afd.agregar_transicion(pieces[0],pieces[1],pieces[2])
	return afd;
		
def partes(lista):
	return
		
class AFD:

		# lista de estados del AFD
		#estados
		#Funcion de transicion de estados -> (char,estado)
		#delta;
		#estados_finales;
		#alfabeto;
		#estado_inicial;

	def __init__(self):
		self.estados = [];
		self.delta = {};
		self.estados_finales = [];
		self.alfabeto = [];
		self.estado_inicial = None;

	def agregar_estado(self):
		i = len(self.estados) +1
		self.estados.append(i);
		self.delta[i] = [];
		return i

	def agregar_transicion(self,estado1,char,estado2):
		if (estado1 in self.estados) and (estado2 in self.estados) and (char in self.alfabeto) and (not (char,estado2) in self.delta[estado1]):
			self.delta[estado1] = self.delta[estado1].append((char,estado2)) 

	def acepta(self,cadena):
		self.acepta_desde(self.estado_inicial,cadena);

	def acepta_desde(self,estado,cadena):
		if len(cadena) == 0:
			return estado in self.estados_finales
		aux = [ est for (char,est) in self.delta[estado], char == cadena[0]];
		if aux.len != 0:
			return self.acepta_desde(aux[0],cadena.pop([0]));
		else:
			return False;


	#casos recursivos
	def concat(self, otroAFD):
		#Reorganizo estados y delta
		otroAFD.reorganizarEstados(len(self.estados))

		# lambda es ' '. Checkear que onda con "acepta"
		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, otroAFD.estado_inicial)

		self.estados_finales = otroAFD.estados_finales
		
		#Nuevo Alfabeto
		self.alfabeto = list(set(self.alfabeto ++ otroAFD.alfabeto))

	def reorganizarEstados(self, i):
		deltaAux = {}
		for est in self.estados:
			deltaAux[est] = [e + i for e in self.delta[e]]
		self.delta = deltaAux
		self.estados = [est + i for est in self.estados]
		self.estado_inicial += i
		self.estados_finales = [est + i for est in self.estados_finales]

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
		self.agregar_transicion(estadoInicial, nuestroLambda, self.estadoFinal)

		self.estado_inicial = estadoInicial

		return

	def plus(self):
		return self.concat(self.star())

	def opt(self):
		return self.orAFD(lambdaAFD())

	def orAFD(self, otroAFD):
		#Reorganizo estados y delta
		estadoInicial = self.agregar_estado()
		estadoFinal = self.agregar_estado()
		otroAFD.reorganizarEstados(len(self.estados))
		for x in xrange(1,len(otroAFD.estados)):
			self.agregar_estado()
		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
		for final in otroAFD.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)

		self.estados_finales = estadoFinal

		#Actualizo estados inciales
		self.agregar_transicion(estadoInicial, nuestroLambda, self.estado_inicial)
		self.agregar_transicion(estadoInicial, nuestroLambda, otroAFD.estado_inicial)

		self.estado_inicial = estadoInicial

		#Nuevo Alfabeto     
		self.alfabeto = list(set(self.alfabeto ++ otroAFD.alfabeto))
		return

	#Asumimos AFND y no AFND-lambda
	def determinizar(self):
		res = AFD()
		res.alfabeto = self.alfabeto
		res.estado_inicial = set(ClausuraLamda(self.estado_inicial))
		porRecorrer = set(res.estado_inicial)

		while len( porRecorrer ) > 0:
			#El nodo es un conjunto de estados de self
			nodo = porRecorrer.pop()
			res.estados.append(nodo)
			res.delta[nodo] = []

			for a in self.alfabeto:
				aux = self.Mover(nodo, a)
				res.delta[nodo].append((a, aux))
				if aux not in res.estados:
					porRecorrer.add(aux)
					
		for e in res.estados:
			for f in self.estados_finales:
				if f in e:
					res.estados_finales.append(e)
					break

		res.nodosToInt()
		self = res

	def Mover(self,ests,char):
		aux = set()
		for est in ests:
			aux.union([e for (c,e) in self.delta[est], c == char])
		res = set()
		for e in aux:
			res.union(ClausuraLamda(e))

	def ClausuraLamda(self,e):
		res = set(e)
		porRecorrer = set(e)  
		while len(porRecorrer) > 0:
			aux = res.intersection(aUnPasoLamda(porRecorrer.pop()))
			res.union(aux)
			porRecorrer.union(aux)
		return res


	def aUnPasoLamda(self,e):
		return set([ x for (char,x) in self.delta[e], x!=e and char == nuestroLambda])


	def AFNDLambdaToAFND(self):
		return

	#TODO: TESTEAR
	def AFNDToAFD(self):
		res = AFD()
		res.estados = partes(self.estados)
		res.estado_inicial = set(self.estado_inicial)
		res.estados_finales = set([ x for x in res.estados, len(x.intersection(set(self.estados_finales))) > 0])
		res.alfabeto = self.alfabeto

		#deltaAux tiene "a donde llego", "desde donde"
		deltaAux = {}
		for letra in self.alfabeto:
			for est in self.estados:
				estadosAux = set([ x for (a,x) in self.delta[est], a == letra ])
				if(estadosAux in deltaAux[letra]):
					deltaAux[letra][estadosAux].add(est)
				else:
					deltaAux[letra][estadosAux] = set(est)

		#Ahora tenemos que armar el delta (que es al reves que deltaAux)
		for (key,value) in deltaAux:
			for v2 in partes(value):
				res.delta[v2] = partes(key)
		self = res

	#devuelve sets
	

	#Minimizar se llama siempre que el AF sea deterministico
	def minimizar(self):
		self.completar()
		clasesEquiv, matrizDeResultados = self.dameClasesEquiv()

		#Crear el nuevo AFD
		res = AFD()
		res.estados = clasesDeEquiv.keys()
		res.alfabeto = self.alfabeto
		res.estado_inicial = clasesEquiv[self.estado_inicial]
		for f in estados_finales:
			if clasesEquiv[f] not in res.estados_finales:
				res.estados_finales.append(clasesEquiv[f])

		for est in res.estados:
			for (char, est2) in matrizDeResultados[est]:
				res.delta[est].append((char, est2))

		self = res
		return

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


	#Solo usar si sabes que esta
	def dameTransicion(self, est, letra):
		for (char,estado) in self.delta[est]:
			if char == letra:
				return estado

	def toFile(self, file):
		lineas = []
		lineas.append( join('\t', self.estados) )
		lineas.append( join('\t', self.alfabeto) )
		lineas.append( self.estado_inicial )
		lineas.append( join('\t', self.estados_finales) )

		for transicion in self.delta:
			for (simbolo,estado) in self.delta[transicion]:
				lineas.append(join('\t', [transicion, simbolo, estado]))

		file.write(join('\n', lineas))
		return

	def toDOT(self, file):
		file.write("strict digraph {\n")
		file.write("\trankdir=LR\n")
		file.write("\tnode [shape = none, label \"\", width = 0, height = 0]; qd \n")
		file.write("\tnode [label=\"\\N\", width = 0.5, width = 0.5];\n")
		file.write("\tnode [shape = doublecircle];")
		
		for est in self.estados_finales:
			file.write(" " + str(est))
		file.write(";")

		file.write("qd -> " + str(self.estado_inicial) + "\n")

		for est in self.estados:
			letrasAImprimir = {}
			for (letra, est2) in self.delta[est]:
				if est2 in letrasAImprimir:
					letrasAImprimir[est2].append(letra)
				else:
					letrasAImprimir[est2] = letra;

			for est in letrasAImprimir:
				file.write(str(est) + " -> " + str (est2) + "[label=\""
				for letra in letrasAImprimir[est]:
					if letra == letrasAImprimir[0]:
						file.write(letra)
					else:
						file.write(", " + letra)
				file.write("\"]\n")

		file.write("}")
		return

	#Suponemos que al concatenar los nombres de los nodos, no estamos repitiendo
	#Ejemplo, NO PASA: nodo1 = a, nodo2 = ba por un lado y nodo1 = ab, nodo2 = a por otro.
	def interseccion(self, adf1):
		res = AFD()
		#Estados y delta
		for nodo1 in self.estados:
			for nodo2 in afd1.estados:
				res.agregar_estado((nodo1,nodo2))

				if (nodo1 in self.estados_finales) and (nodo2 in afd1.estados_finales):
					res.estados_finales.append((nodo1,nodo2))

				if (nodo1 == self.estado_inicial) and (nodo2 == afd1.estado_inicial):
					res.estado_inicial = (nodo1,nodo2)

				for (char1, estado1) in self.delta[nodo1]:
					for (char2, estado2) in afd1.delta[nodo2]:
						if(char1 == char2):
							res.agregar_transicion((nodo1,nodo2), char1, (estado1,estado2))

		res.nodosToInt()
		self.alfabeto = list(set(self.alfabeto).interseccion(set(afd1.alfabeto)))

		self = res
		return

	def complemento(self):
		self.completar()
		self.estados_finales = [estado for estado in self.estados, estado not in self.estados_finales]
		
	def completar(self):
		i = self.agregar_estado()
		for e in self.estados:
			charsAux = [char for (char,e1) in self.delta[e]]
			for char in self.alfabeto:
				if char not in charsAux:
					self.agregar_transicion(e,char,i)

	def nodosToInt(self):
		dicc = {}
		estados = [1..len(self.estados)]
		deltaAux = {}
		for i in estados:
			dicc[self.estados[i]] = i
		for i in estados:
			deltaAux[i] = [ (c,dicc[e]) for (c,e) in delta[self.estados[i]]]

		self.estados = estados
		self.delta = deltaAux

	def	equivalente(self, adf1):
		return
