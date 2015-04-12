class AFD {
	#Grafo g;
	nodos_finales;
	alfabeto;
	nodo_inicial;

	__init__(archivo_regex);
	determinizar();
	minimizar();
	toFile(file);
	acepta(cadena);
	interceccion(adf1);
	complemento();
	equivalente(adf1);

}