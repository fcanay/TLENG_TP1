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

def	fromRegex(regex_file):
	lines = regex_file.readlines()
	return  createFromRegex(lines)

def createFromRegex(s):
	if s[0] != '{':
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

def nuevoEstado(estado, anteriores):
    valorFinal = int(estado[1:]) + anteriores
    return "q" + str(valorFinal)

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
		self.delta[i] = {};
		return i

	def agregar_transicion(self,estado1,char,estado2):
		if (estado1 in self.estados) and (estado2 in self.estados) and (char in self.alfabeto) and (not (char,estado2) in self.delta[estado1]):
			self.delta[estado1] = self.delta[estado1].append((char,estado2)) 

	def acepta(self,cadena):
		self.acepta_desde(self.estado_inicial,cadena);

	def	acepta_desde(self,estado,cadena):
		if len(cadena) == 0:
			return estado in self.estados_finales
		aux = [ est | (char,est) in self.delta[estado], char == cadena[0]];
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
	def	determinizar(self):
		self.AFNDLambdaToAFND()
		self.AFNDToAFD()
		return

	def Mover(self,est,char):
		res = MoverSinLamdaInicio(self,est,char)
		aux = ClausuraLamda(est)
		for e in aux:
			res.union(MoverSinLamdaInicio(e))

	def MoverSinLamdaInicio(self,est,char):
		res = set()
		aux = [e | (c,e) in self.delta[est], c==char]
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
		return set([ x | (char,x) in self.delta[e], x!=e and char = nuestroLambda])


	def AFNDLambdaToAFND(self):
		return

	#TODO: TESTEAR
	def AFNDToAFD(self):
		res = AFD()
		res.estados = partes(self.estados)
		res.estado_inicial = set(self.estado_inicial)
		res.estados_finales = set([ x | x in res.estados, len(x.intersection(set(self.estados_finales))) > 0])
		res.alfabeto = self.alfabeto

		#deltaAux tiene "a donde llego", "desde donde"
		deltaAux = {}
		for letra in self.alfabeto:
			for est in self.estados:
				estadosAux = set([ x | (a,x) in self.delta[est], a == letra ])
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
	

	def	minimizar(self):
		return

	def	toFile(self, file):
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

	def	toDOT(self, file):
		return

	#Suponemos que al concatenar los nombres de los nodos, no estamos repitiendo
	#Ejemplo, NO PASA: nodo1 = a, nodo2 = ba por un lado y nodo1 = ab, nodo2 = a por otro.
	def	interseccion(self, adf1):
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

		res.reorganizarParesEstados(len(self.estados),len(adf1.estados))
		self.alfabeto = list(set(self.alfabeto).interseccion(set(afd1.alfabeto)))

		self = res
		return

	def reorganizarParesEstados(self,i,j):
		deltaAux = {}
		for (a,b) in self.estados:
			deltaAux[a*i+(b-1)*j] = [ c*i+(d-1)*j | (c,d) in self.delta[a*i+(b-1)*j]]
		self.delta = deltaAux
		self.estados = [ a*i+(b-1)*j | (a,b) in self.estados]
		self.estado_inicial = self.estado_inicial[0]*i+(self.estado_inicial[1]-1)*j
		self.estados_finales = [ a*i+(b-1)*j | (a,b) in self.estados_finales]

	def	complemento(self):
		self.completar()
		self.estados_finales = [estado | estado in self.estados, estado not in self.estados_finales]
		
	def completar(self):
		i = self.agregar_estado()
		for e in self.estados
			charsAux = [char | (char,e1) in self.delta[e]]
			for char in self.alfabeto
				if char not in charsAux:
					self.agregar_transicion(e,char,i)

	def	equivalente(self, adf1):
		return
