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
		alfabeto = [];
		estado_inicial = None;

	def agregar_estado(self,estado):
		if estado not in self.estados:
			self.estados.append(estado);
			self.delta[estado] = [];

	def acepta(self,cadena):
		acepta_desde(self,self.estado_inicial,cadena);

	def	acepta_desde(self,estado,cadena):
		aux = [ est| (char,est) in self.delta[estado],char==cadena[0]];
		if aux.len != 0:
			return acepta_desde(self,aux[0],cadena.pop([0]));
		else:
			return False;

	def	fromRegex(regex_file):
		return

	def	fromFile(file):
		return

	def	determinizar():
		return

	def	minimizar():
		return

	def	toFile(file):
		afd = AFD();
		
		return afd;

	def	toDOT(file):
		return;

	def	interseccion(adf1):
		return;

	def	complemento():
		return;

	def	equivalente(adf1):
		return;