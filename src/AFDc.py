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
		alfabeto = [];
		estado_inicial = None;

	def agregar_estado(self,estado):
		if estado not in self.estados:
			self.estados.append(estado);
			self.delta[estado] = [];

	def agregar_transicion(self,estado1,char,estado2):
		if (estado1 in self.estados) && (char in self.alfabeto):
			self.delta[estado1] = self.delta[estado1] 

	def acepta(self,cadena):
		self.acepta_desde(self.estado_inicial,cadena);

	def	acepta_desde(self,estado,cadena):
		aux = [ est| (char,est) in self.delta[estado],char==cadena[0]];
		if aux.len != 0:
			return self.acepta_desde(aux[0],cadena.pop([0]));
		else:
			return False;

	def	fromRegex(regex_file):
		return

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

	def	determinizar():
		return

	def	minimizar():
		return

	def	toFile(file):
		return

	def	toDOT(file):
		return;

	def	interseccion(adf1):
		return;

	def	complemento():
		return;

	def	equivalente(adf1):
		return;