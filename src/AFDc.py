class AFD:

		# lista de estados del AFD
		#estados
		#Funcion de transicion de estados -> (char,estado)
		#delta;
		#estados_finales;
		#alfabeto;
		#estado_inicial;

		



	def __init(self):
		self.estados = [];
		self.delta = {};
		self.estados_finales = [];
		self.alfabeto = [];
		self.estado_inicial = None;

	def agregar_estado(self,estado):
		if estado not in self.estados:
			self.estados.append(estado);
			self.delta[estado] = [];

	def acepta(self,cadena):
		acepta_desde(self,self.estado_inicial,cadena);

	def	acepta_desde(self,estado,cadena):
		aux = [ est | (char,est) in self.delta[estado], char == cadena[0]];
		if aux.len != 0:
			return acepta_desde(self,aux[0],cadena.pop([0]));
		else:
			return False;

	def	fromRegex(self, regex_file):
		return

	def	fromFile(self, file):
		return

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
