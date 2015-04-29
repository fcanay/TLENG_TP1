#!/bin/sh

RUTA="./"


#Regex
TEST_REGEX=""
for TEST in $TEST_REGEX
do
python AFD.py -len "Regex/$TEST".regex -aut "$Regex/TEST".aut
RES = ´python AFD.py -equival -aut1 "$Regex/TEST".res -aut2 "$Regex/TEST".aut´
if [ $RES = "FALSE"]; then
	cout "ERROR TEST REGEX: $TEST"
else 
	if  [ $RES != "TRUE"]; then
		cout "ERROR fallo en equivalente, no devuelve un valor esperado: $TEST"
	fi
fi
done

#Acepta
TEST_ACEPTA=""
for TEST in $TEST_ACEPTA
do
	while read PALABRA
	do
		RES = ´python AFD.py -aut "Acepta/$TEST".aut "$PALABRA"´
		if [ $RES = "FALSE"]; then
			cout "ERROR TEST ACEPTA: $TEST no acepta la palabra $PALABRA pero debería"
		else 
			if  [ $RES != "TRUE"]; then
				cout "ERROR fallo en ACEPTA, no devuelve un valor esperado: $TEST,$PALABRA"
			fi
		fi
	done < "Acepta/$TEST".acepta

	while read PALABRA
	do
		RES = ´python AFD.py -aut "Acepta/$TEST".aut "$PALABRA"´
		if [ $RES = "TRUE"]; then
			cout "ERROR TEST ACEPTA: $TEST acepta la palabra $PALABRA pero no debería"
		else 
			if  [ $RES != "FALSE"]; then
				cout "ERROR fallo en ACEPTA, no devuelve un valor esperado: $TEST,$PALABRA"
			fi
		fi
	done < "Acepta/$TEST".noacepta
done

#Interseccion
TEST_INTERSECCION=""
for TEST in $TEST_INTERSECCION
do
python AFD.py -intersec -aut1 "Interseccion/$TEST".1.autin -aut2 "Interseccion/$TEST".2.autin -aut "Interseccion/$TEST".aut
RES = ´python AFD.py -equival -aut1 "Interseccion/$TEST".res -aut2 "Interseccion/$TEST".aut´
if [ $RES = "FALSE"]; then
	cout "ERROR TEST INTERSECCION: $TEST"
else 
	if  [ $RES != "TRUE"]; then
		cout "ERROR fallo en equivalente, no devuelve un valor esperado: $TEST"
	fi
fi
done


#Complemento
TEST_COMPLEMENTO=""
for TEST in $TEST_COMPLEMENTO
do
python AFD.py -complemento -aut1 "Complemento/$TEST".autin -aut "Complemento/$TEST".aut
RES = ´python AFD.py -equival -aut1 "Complemento/$TEST".res -aut2 "Complemento/$TEST".aut´
if [ $RES = "FALSE"]; then
	cout "ERROR TEST COMPLEMENTO: $TEST"
else 
	if  [ $RES != "TRUE"]; then
		cout "ERROR fallo en equivalente, no devuelve un valor esperado: $TEST"
	fi
fi
done