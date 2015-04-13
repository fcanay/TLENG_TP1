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

<<<<<<< HEAD
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
=======
	def	fromFile(self, file):
		return
>>>>>>> e387dbe0d51be34e680a4e4e2e4b41eda2fea762

	def	determinizar(self):
		return

	def	minimizar(self):
		return

<<<<<<< HEAD
	def	toFile(file):
=======
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
>>>>>>> e387dbe0d51be34e680a4e4e2e4b41eda2fea762
		return

	def	toDOT(self, file):
		return

	def	interseccion(self, adf1):
		return

	def	complemento(self):
		return

	def	equivalente(self, adf1):
		return
