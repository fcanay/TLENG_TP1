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

	def agregar_estado(self,estado):
		if estado not in self.estados:
			self.estados.append(estado);
			self.delta[estado] = [];

	def agregar_transicion(self,estado1,char,estado2):
		if (estado1 in self.estados) and (estado2 in self.estados) and (char in self.alfabeto) and 
		(not (char,estado2) in self.delta[estado1]):
			self.delta[estado1] = self.delta[estado1].append((char,estado2)) 

	def acepta(self,cadena):
		self.acepta_desde(self.estado_inicial,cadena);

	def	acepta_desde(self,estado,cadena):
		aux = [ est | (char,est) in self.delta[estado], char == cadena[0]];
		if aux.len != 0:
			return self.acepta_desde(aux[0],cadena.pop([0]));
    else:
      return False;

	def	fromRegex(self, regex_file):
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

		else if s[0:5] == "{STAR}":
			afd.star()
		else if s[0:5] == "{PLUS}":
			afd.plus()
		else if s[0:4] == "{OPT}":
			afd.opt()
		else if s[0:3] == "{OR}":
			for x in xrange(1,s[4]-1):
				afd.orAFD(createFromRegex(parts[x]))
		return afd

	#casos base
	def letra(caracter):
		res = AFD()
		res.estados = ["q1", "q2"]
		res.agregar_transicion("q1", caracter, "q2")
		res.estados_finales = ["q2"];
		res.alfabeto = [caracter];
		res.estado_inicial = "q1";
		return res

	def lambdaAFD():
		res = AFD()
		res.estados = ["q1"]
		res.estados_finales = ["q1"]
		res.estado_inicial = "q1"
		return res

	#casos recursivos
	def concat(self, otroAFD):
		#Reorganizo estados y delta
		otroAFD.reorganizarEstados(len(self.estados) + 1)

		# lambda es ' '. Checkear que onda con "acepta"
		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, otroAFD.estado_inicial)

		self.estados_finales = otroAFD.estados_finales
		
		#Nuevo Alfabeto
		self.alfabeto = list(set(self.alfabeto ++ otroAFD.alfabeto))

	def star(self):
		#Reorganizo estados y delta
		estadoInicial = "q1"
		i = self.reorganizarEstados(1)
		estadoFinal = "q" + str(i+1)
		self.agregar_estado(estadoFinal)

		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
			self.agregar_transicion(final, nuestroLambda, self.estado_inicial)

		self.estados_finales = estadoFinal

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
		estadoInicial = "q1"
		i = self.reorganizarEstados(1)
		i = otroAFD.reorganizarEstados(i)
		estadoFinal = "q" + str(i+1)
		self.agregar_estado(estadoFinal)

		#Actualizo estados finales
		for final in self.estados_finales:
			self.agregar_transicion(final, nuestroLambda, estadoFinal)
		for final in otroAFD.estados_finales:
			otroAFD.agregar_transicion(final, nuestroLambda, estadoFinal)

		self.estados_finales = estadoFinal

		#Actualizo estados inciales
		self.agregar_transicion(estadoInicial, nuestroLambda, self.estado_inicial)
		otroAFD.agregar_transicion(estadoInicial, nuestroLambda, otroAFD.estado_inicial)

		self.estado_inicial = estadoInicial

		#Nuevo Alfabeto		
		self.alfabeto = list(set(self.alfabeto ++ otroAFD.alfabeto))
		return

  def nuevoEstado(estado, anteriores):
    valorFinal = int(estado[1:]) + anteriores
    return "q" + str(valorFinal)

	# def reorganizarEstados(self, i):
	# 	for est in self.estados:
	# 		self.agregar_estado("q" + str(i))
	# 		for (simbolo,estado) in self.delta[est]:
	# 			self.agregar_transicion("q" + str(i), simbolo, nuevoEstado(estado, i))
	# 		i += 1
	# 	return i

  def reorganizarEstados(self, i):
    i += len(self.estados)
    for est in self.estados.reverse():
      self.agregar_estado("q" + str(i))
      for (simbolo,estado) in self.delta[est]:
        self.agregar_transicion("q" + str(i), simbolo, nuevoEstado(estado, i))
        sels.delta[est].remove((simbolo,estado)) 
      i -= 1
      self.estados.remove(est)
      self.deta[est] = []
    return i+len(self.estados)
    #Habria que ver si es necesario devolverlo

	def	fromFile(self,file):
		afd = AFD();
		auxEstados = file.next().split();
		for est in auxEstados:
			afd.agregar_estado(est);
		afd.alfabeto = file.next().split();
		afd.estado_inicial = file.next();
		afd.estados_finales = file.next().split();

		for line in file:
			pieces = line.split()
			afd.agregar_transicion(pieces[0],pieces[1],pieces[2])
		return afd;

	def	determinizar(self):
		return

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
				res.agregar_estado(nodo1 + nodo2)

				if (nodo1 in self.estados_finales) and (nodo2 in afd1.estados_finales):
					res.estados_finales.append(nodo1 + nodo2)

				if (nodo1 == self.estado_inicial) and (nodo2 == afd1.estado_inicial):
					res.estado_inicial = nodo1 + nodo2

				for (char1, estado1) in self.delta[nodo1]:
					for (char2, estado2) in afd1.delta[nodo2]:
						if(char1 == char2):
							res.agregar_transicion(nodo1 + nodo2, char1, estado1 + estado2)

		self.alfabeto = list(set(self.alfabeto).interseccion(set(afd1.alfabeto)))

		self = res
		return

	def	complemento(self):
		self.completar()
		self.estados_finales = [estado | estado in self.estados, estado not in self.estados_finales]
		
	def completar(self):
		self.agregar_estado("qTrampa")
		for e in self.estados
			charsAux = [char | (char,e1) in self.delta[e]]
			for char in self.alfabeto
				if char not in charsAux:
					self.agregar_transicion(e,char,"qTrampa")

	def	equivalente(self, adf1):
		return
