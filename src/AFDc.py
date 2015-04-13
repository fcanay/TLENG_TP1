nuestroLambda = " "

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
		if (estado1 in self.estados) && (estado2 in self.estados) && (char in self.alfabeto):
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
		return

	#casos base
	def letra(caracter):
		res = AFD()
		res.estados = ["q1", "q2"]
		res.agregar_transicion("q1", caracter, "q2")
		res.estados_finales = ["q2"];
		res.alfabeto = [caracter];
		res.estado_inicial = "q1";
		return res

	def lambdaAFD(slf):
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

	def nuevoEstado(estado, anteriores):
		valorFinal = int(estado[1:]) + anteriores
		return "q" + str(valorFinal)

	def star(self):
		#Reorganizo estados y delta
		estadoInicial = "q1"
		i = self.reorganizarEstados(2)
		estadoFinal = "q" + str(i)
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
		i = self.reorganizarEstados(2)
		i = otroAFD.reorganizarEstados(i)
		estadoFinal = "q" + str(i)
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

	def reorganizarEstados(self, i):
		for est in self.estados:
			self.agregar_estado("q" + str(i))
			for (simbolo,estado) in self.delta[est]:
				self.agregar_transicion("q" + str(i), simbolo, nuevoEstado(estado, i))
			i += 1
		return i

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

	def	interseccion(self, adf1):
		return

	def	complemento(self):
		return

	def	equivalente(self, adf1):
		return
