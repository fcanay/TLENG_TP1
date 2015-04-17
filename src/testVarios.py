#python testVarios.py; dot -Tps blabla.dot -o blabla.ps

def main():
	x = AFD()
	x.estados = [1,2,3,4,5,6, 7]
	x.delta = {1: [('o',2), ('a',3)], 2: [('s',4)], 3: [('s',5)], 4: [('a',6)], 5: [('a',7)], 6: [], 7: []}
	x.estados_finales = [6,7]
	x.alfabeto = ['a', 's', 'o']
	x.estado_inicial = 1
	x.completar()
	x = x.minimizar()
	x.toDOT('blabla.dot')

	# x = AFD()
	# x.estados = [1,2,3,4,5,6, 7]
	# x.delta = {1: [('o',2), ('a',3)], 2: [('s',4)], 3: [('s',5)], 4: [('a',6)], 5: [('a',7)], 6: [], 7: []}
	# x.estados_finales = [6,7]
	# x.alfabeto = ['a', 's', 'o']
	# x.estado_inicial = 1
	# x.completar()
	# x.completar()
	# x.toDOT('blabla.dot')

	# x = AFD()
	# x.estados = [1, 2, 3]
	# x.delta = {1: [('a',2), ('b',3)], 2: [('a',2)], 3: [('a',1)]}
	# x.estados_finales = [2]
	# x.alfabeto = ['a','b']
	# x.estado_inicial = 1
	# x.completar()
	# x.toDOT('blabla.dot')

	# x = AFD()
	# x.estados = [1, 2, 3, 4]
	# x.delta = {1: [('a',2), ('b',3)], 2: [('a',2), ('b',4)], 3: [('a',1), ('b',4)],  4: [('a',4), ('b',4)]}
	# x.estados_finales = [2]
	# x.alfabeto = ['a','b']
	# x.estado_inicial = 1
	# x.toDOT('blabla.dot')

	# x = AFD()
	# x.estados = [1,2]
	# x.delta = {1: [('a',2), ('b',2)], 2: [('a',2), ('b',2)]}
	# x.estados_finales = [2]
	# x.alfabeto = ['a','b']
	# x.estado_inicial = 1
	# x.toDOT('blabla.dot')
