# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from cgitb import text
from distutils.filelist import findall
from email import message
from typing import Any, Text, Dict, List
from time import sleep
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from swiplserver import PrologMQI, PrologThread

import random
import os.path
import json

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_materia"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia=next(tracker.get_latest_entity_values("materia"),None)
        if materia in ["Prog Exploratoria", "Sistemas Operativos", "Bases de Datos", "Investigacion Operativa", "Lenguajes de Programacion"]:
            message="sisi la estoy cursando este cuatri "
        else:
            message="nono, no la estoy cursando"
        dispatcher.utter_message(text=str(message))
        return []

class ActionReconocimiento(Action):

    def name(self) -> Text:
        return "action_cargo"
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cargo=next(tracker.get_latest_entity_values("cargo_facultad"),None)
        message="Ah sos " + cargo + "!"
        if str(cargo)==("estudiante") or str(cargo)==("alumno"):
            message=message + " cual es tu nombre?"
            dispatcher.utter_message(text=str(message))
            return[SlotSet("docente", False)]
        elif str(cargo)==("ayudante") or str(cargo)==("profesor") or str(cargo)==("docente"):
            message=message + " disculpa pense que eras un compañero, me recordas tu nombre?"
            dispatcher.utter_message(text=str(message))
            return[SlotSet("docente", True)]
        else:
            dispatcher.utter_message(template="utter_cargo_desconocido")
            return[SlotSet("docente", False)]

#------------------------------ACCIONES CON PROLOG------------------------------

class ActionWithProlog(Action):
    def name(self) -> Text:
        return "action_materias"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        anio=next(tracker.get_latest_entity_values("anio_materia"),None)
        intent=tracker.latest_message['intent'].get('name')
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\plan.pl')", find_all=False)
                    if (str(intent)=="materias_por_anio"):
                        if (int(anio) > 5 ):
                            dispatcher.utter_message(text="La carrera solo tiene 5 años!")
                        else:
                            prolog_thread.query_async(f"materias_de({anio},Materias)", find_all=False)
                            result = prolog_thread.query_async_result()[0]['Materias']
                            dispatcher.utter_message(f"Las materias de {anio} son: \n")
                            for materia in result:
                                dispatcher.utter_message(text = materia) 
                    elif (str(intent)=="todas_las_materias_del_plan"):
                        prolog_thread.query_async(f"plan_is_lista(Materias,Anio,Cuatri)", find_all=False)
                        materias = prolog_thread.query_async_result()[0]['Materias']
                        dispatcher.utter_message(f"Ahi te paso el plan completo, lo tengo guardado en otro chat: \n")
                        for materia in materias:
                            dispatcher.utter_message(text = materia) 
        return []

class ActionWithProlog(Action):
    def name(self) -> Text:
        return "action_amigos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre=tracker.get_slot("amigo")
        nombre_minusculas=nombre.lower()
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\botdavid.pl')", find_all=False)
                    prolog_thread.query_async(f"es_amigo(\"{nombre_minusculas}\")", find_all=False)
                    result = prolog_thread.query_async_result()
                    if result==True:
                        dispatcher.utter_message(f"Sii! {nombre} es mi amigo")
                    else:
                        dispatcher.utter_message(f"Nono, {nombre} no es amigo mio pero la mejor con el")
                    return []

class ActionWithProlog(Action):
    def name(self) -> Text:
        return "action_promocionada"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia=next(tracker.get_latest_entity_values("materia"),None)
        materia_minusculas=materia.lower()
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\botdavid.pl')", find_all=False)
                    prolog_thread.query_async(f"materia_promocionada(\"{materia_minusculas}\")", find_all=False)
                    result = prolog_thread.query_async_result()
                    if result==True:
                        dispatcher.utter_message(f"Sisi, pude promocionar {materia}! ")
                    else:
                        prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\botdavid.pl')", find_all=False)
                        prolog_thread.query_async(f"materia_cursada(\"{materia_minusculas}\")", find_all=False)
                        aprobada = prolog_thread.query_async_result()
                        if aprobada==True:
                            dispatcher.utter_message(f"Esa materia no la promocione, pero la aprobe rindiendo el final!")
                        else:
                            dispatcher.utter_message(f"Esa materia no la promocione, solo aprobe la cursada")
                    return []

#---------------------------------ACCIONES CON JSON ------------------------------

class OperarArchivo():

    @staticmethod
    def guardar(AGuardar):
        with open(".\\actions\\datos","w") as archivo_descarga:
            json.dump(AGuardar, archivo_descarga, indent=4)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivo(): 
        if os.path.isfile(".\\actions\\datos"):
            with open(".\\actions\\datos","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

class ActionExtraerDatos(Action):
    def name(self) -> Text:
       return "action_extraer_datos"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre=tracker.get_slot("nombre_conocido")
        nombre_minusculas=nombre.lower()
        alumnos= OperarArchivo.cargarArchivo()
        if nombre_minusculas in alumnos:
            mensaje="Ah sisi vos sos " + alumnos[nombre_minusculas]['nombre'] + " " + alumnos[nombre_minusculas]['apellido']
            materias=alumnos[nombre_minusculas]['materias_cursa_conmigo'] 
            if len(materias) >= 1 :
                mensaje=mensaje+" y cursas conmigo " 
                materias=alumnos[nombre_minusculas]['materias_cursa_conmigo']
                for materia in materias:
                    mensaje=mensaje+ materia + ","
            mensaje= mensaje+" que paso?"
            dispatcher.utter_message(text=str(mensaje))
            return[SlotSet("desconocido",False)]
        else:
            mensaje="Mmm no te conozco, me decis tu apellido?"
            dispatcher.utter_message(text=str(mensaje))
            return[SlotSet("desconocido",True)]

class ActionExtraerDatos(Action):
    def name(self) -> Text:
       return "action_guardar_datos"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        alumnos= OperarArchivo.cargarArchivo()
        nombre=tracker.get_slot("nombre_conocido")
        nombre_minusculas=nombre.lower()
        apellido=tracker.get_slot("slot_apellido")
        alumnos[nombre_minusculas]={}
        alumnos[nombre_minusculas]['nombre']=nombre
        alumnos[nombre_minusculas]['apellido']=apellido
        ultimo_intent=tracker.latest_message['intent'].get('name')
        alumnos[nombre_minusculas]['materias_cursa_conmigo']=[]
        if str(ultimo_intent)=="deny":
            mensaje="Un gusto " + nombre + ", que paso?" 
        else:
            materia= next(tracker.get_latest_entity_values("materia"), None)
            materias=alumnos[nombre_minusculas]['materias_cursa_conmigo']
            materias.append(materia)
            alumnos[nombre_minusculas]['materias_cursa_conmigo']=materias
            mensaje="Un gusto " + nombre_minusculas + ", no sabia que cursabas " + materia + " conmigo, que paso?" 
        OperarArchivo.guardar(alumnos)
        dispatcher.utter_message(text=str(mensaje))
        return []

#--------------------------------- ACCIONES CON JSON Y PROLOG ------------------------------

class OperarArchivoCursadas():

    @staticmethod
    def cargarArchivo(): 
        if os.path.isfile(".\\actions\\cursadas"):
            with open(".\\actions\\cursadas","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

class ActionWithProlog(Action):
    def name(self) -> Text:
        return "action_cursada"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dia=tracker.get_slot("slot_dia")
        dia=dia.lower()
        print(dia)
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                    prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\botdavid.pl')", find_all=False)
                    prolog_thread.query_async(f"cursas(\"{dia}\")", find_all=False)
                    result = prolog_thread.query_async_result()
                    print(result)
                    if result==True:
                        cursadas=OperarArchivoCursadas.cargarArchivo()
                        materias=cursadas[dia]['materias']
                        mensaje=f"Sii, ese dia curso "
                        for materia in materias:
                            mensaje=mensaje + materia + ", "
                        mensaje= mensaje + f"dia complicado los {dia} jajaj"
                        dispatcher.utter_message(text=mensaje)
                    else:
                        dispatcher.utter_message(f"Nono, el {dia} no curso nada")
                    return []

#--------------------------------- ACCIONES GRUPALES -------------------------------------

class OperarArchivoGrupal():

    @staticmethod
    def guardar(AGuardar):
        with open(".\\actions\\grupal","w") as archivo_descarga:
            json.dump(AGuardar, archivo_descarga, indent=4)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivo(): 
        if os.path.isfile(".\\actions\\grupal"):
            with open(".\\actions\\grupal","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

class Action_consultar_por_ejercicio(Action): 
    def name(self) -> Text:
        return "action_consultar_por_ejercicio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("la materia por entidad es: " + str(next(tracker.get_latest_entity_values("materia"), None)))
        # print("el tp de la materia es:" + str(next(tracker.get_latest_entity_values("tp"), None)))
        # print("el inciso de la materia es:" + str(next(tracker.get_latest_entity_values("inciso"), None)))
        tp = next(tracker.get_latest_entity_values("tp"), None)
        inciso = next(tracker.get_latest_entity_values("inciso"), None)

        if (next(tracker.get_latest_entity_values("materia"), None) != None):
            materia = next(tracker.get_latest_entity_values("materia"), None)
        else:
            materia = None
        print(materia)
        print(tp)
        print(inciso)
        if (materia):
            try:
                datos = OperarArchivoGrupal.cargarArchivo()
                materiaLower = datos["tranformacionesDeNombresMaterias"][materia.lower()]
                print(materiaLower)
                ejercicio = datos["ejercicios"][materiaLower][tp][inciso]["resolucion"]
                dispatcher.utter_message(text="si, ahí te lo paso", image=ejercicio)
            except:
                dispatcher.utter_message(response="utter_no_tengo_ejercicio")#, tp=tp,inciso=inciso, materia=materia)
        else:
            dispatcher.utter_message(response = "utter_no_conozco_materia")
        return []

