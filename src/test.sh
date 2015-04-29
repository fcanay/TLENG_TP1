#!/bin/sh

RUTA="./"


#Regex
TEST_REGEX=""
for TEST in $TEST_REGEX
do
python AFD.py -len "$TEST".regex -aut "$TEST".aut
RES = ´python AFD.py -equival -aut1 "$TEST".res -aut2 "$TEST".aut´
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
		RES = ´python AFD.py -aut "$TEST".aut "$PALABRA"´
		if [ $RES = "FALSE"]; then
			cout "ERROR TEST ACEPTA: $TEST no acepta la palabra $PALABRA pero debería"
		else 
			if  [ $RES != "TRUE"]; then
				cout "ERROR fallo en ACEPTA, no devuelve un valor esperado: $TEST,$PALABRA"
			fi
		fi
	done < "$TEST".acepta

	while read PALABRA
	do
		RES = ´python AFD.py -aut "$TEST".aut "$PALABRA"´
		if [ $RES = "TRUE"]; then
			cout "ERROR TEST ACEPTA: $TEST acepta la palabra $PALABRA pero no debería"
		else 
			if  [ $RES != "FALSE"]; then
				cout "ERROR fallo en ACEPTA, no devuelve un valor esperado: $TEST,$PALABRA"
			fi
		fi
	done < "$TEST".noacepta
done

#Interseccion
TEST_INTERSECCION=""
for TEST in $TEST_INTERSECCION
do
python AFD.py -intersec -aut1 "$TEST".1.autin -aut2 "$TEST".2.autin -aut "$TEST".aut
RES = ´python AFD.py -equival -aut1 "$TEST".res -aut2 "$TEST".aut´
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
python AFD.py -complemento -aut1 "$TEST".autin -aut "$TEST".aut
RES = ´python AFD.py -equival -aut1 "$TEST".res -aut2 "$TEST".aut´
if [ $RES = "FALSE"]; then
	cout "ERROR TEST COMPLEMENTO: $TEST"
else 
	if  [ $RES != "TRUE"]; then
		cout "ERROR fallo en equivalente, no devuelve un valor esperado: $TEST"
	fi
fi
done