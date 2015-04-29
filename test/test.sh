#!/bin/sh

RUTA="./"
FALLOS="0"
ACIERTOS="0"
ERROR=""

#Regex
TEST_REGEX="regex_ej1 regex_ej2 regex_ej3 regex3"
for TEST in $TEST_REGEX
do
python ../src/AFD.py -leng "Regex/$TEST".regex -aut "Regex/$TEST".aut
RES=`python ../src/AFD.py -equival -aut1 "Regex/$TEST".res -aut2 "Regex/$TEST".aut`
rm "Regex/$TEST".aut
if [ $RES = "FALSE" ] ; then
	FALLOS=$((FALLOS+1))
	ERROR="$ERROR TEST REGEX: $TEST\n"
else 
	if  [ $RES = "TRUE" ]
	then
		ACIERTOS=$((ACIERTOS+1))	
	else
		FALLOS=$((FALLOS+1))
		ERROR="$ERROR fallo en equivalente REGEX, no devuelve un valor esperado en $TEST : $RES\n"
	fi
fi
done

#Acepta
TEST_ACEPTA="triplas0 minimizado noMinimizado noComienzaConUno"
for TEST in $TEST_ACEPTA
do
	while read PALABRA
	do
		RES=`python ../src/AFD.py -aut "Acepta/$TEST".aut "$PALABRA"`
		if [ $RES = "FALSE" ] ; then
			FALLOS=$((FALLOS+1))
			ERROR="$ERROR TEST ACEPTA: $TEST no acepta la palabra $PALABRA pero debería\n"
		else 
			if  [ $RES = "TRUE" ]
			then
				ACIERTOS=$((ACIERTOS+1))	
			else
				FALLOS=$((FALLOS+1))
				ERROR="$ERROR fallo en ACEPTA, no devuelve un valor esperado en $TEST : $RES,$PALABRA\n"
			fi
		fi
	done < "Acepta/$TEST".acepta

	while read PALABRA
	do
		RES=`python ../src/AFD.py -aut "Acepta/$TEST".aut "$PALABRA"`
		if [ $RES = "TRUE" ] ; then
			FALLOS=$((FALLOS+1))
			ERROR="$ERROR TEST ACEPTA: $TEST acepta la palabra $PALABRA pero no debería\n"
		else 
			if  [ $RES = "FALSE" ]
			then
				ACIERTOS=$((ACIERTOS+1))	
			else
				FALLOS=$((FALLOS+1))
				ERROR="$ERROR fallo en ACEPTA, no devuelve un valor esperado en $TEST : $RES,$PALABRA\n"
			fi
		fi
	done < "Acepta/$TEST".noacepta
done

#Interseccion
TEST_INTERSECCION="triplas0 elMismo elComplemento caracteres" 
for TEST in $TEST_INTERSECCION
do
python ../src/AFD.py -intersec -aut1 "Interseccion/$TEST".1.autin -aut2 "Interseccion/$TEST".2.autin -aut "Interseccion/$TEST".aut
RES=`python ../src/AFD.py -equival -aut1 "Interseccion/$TEST".res -aut2 "Interseccion/$TEST".aut`
rm "Interseccion/$TEST".aut
if [ $RES = "FALSE" ] ; then
	FALLOS=$((FALLOS+1))
	ERROR="$ERROR TEST INTERSECCION: $TEST\n"
else 
	if  [ $RES = "TRUE" ]
	then
		ACIERTOS=$((ACIERTOS+1))	
	else
		FALLOS=$((FALLOS+1))
		ERROR="$ERROR fallo en equivalente INTERSECCION, no devuelve un valor esperado en $TEST : $RES\n"
	fi
fi
done


#Complemento
TEST_COMPLEMENTO="triplas0 comienzaConUno hp"
for TEST in $TEST_COMPLEMENTO
do
python ../src/AFD.py -complemento -aut1 "Complemento/$TEST".autin -aut "Complemento/$TEST".aut
RES=`python ../src/AFD.py -equival -aut1 "Complemento/$TEST".res -aut2 "Complemento/$TEST".aut`
rm  "Complemento/$TEST".aut
if [ $RES = "FALSE" ] 
then
	FALLOS=$((FALLOS+1))
	ERROR="$ERROR TEST COMPLEMENTO: $TEST\n"
else 
	if  [ $RES = "TRUE" ] 
	then
		ACIERTOS=$((ACIERTOS+1))	
	else
		FALLOS=$((FALLOS+1))
		ERROR="$ERROR fallo en equivalente COMPLEMENTO, no devuelve un valor esperado en $TEST : $RES\n"
	fi
fi
done

echo "Resumen TEST"
echo "Aciertos: $ACIERTOS"
echo "Fallos: $FALLOS"
if [ "$FALLOS" != "0" ]
then
	echo "Errores:\n $ERROR"
fi