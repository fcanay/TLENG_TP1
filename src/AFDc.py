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
		lines = regex_file.readlines()
		return  createFromRegex(lines)

	def createFromRegex(s):
		if s[0:7] == "{CONCAT}":
			parts = partition(s)
			afd = createFromRegex(parts[0])
			for x in xrange(1,s[8]-1):
				afd.concat(createFromRegex(parts[x]))
			return afd
		else if s[0:5] == "{STAR}":

		else if s[0:5] == "{PLUS}":

		else if s[0:4] == "{OPT}":

		else if s[0:3] == "{OR}":

		else:

def partition(s):
	lines = s.split("\n")
	res = []
	i = 1
	while i <  len(lines):
		res.append([lines[i][1:]])
		i+=1
		while (lines[i][2] == "\t") && (i <  len(lines)):
			res[len(res)-1].append(lines[i][1:])
			i+=1
	return res


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
