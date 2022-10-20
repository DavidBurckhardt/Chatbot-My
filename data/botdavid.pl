amigo("tincho").
amigo("martino").
amigo("juan").
amigo("sol").
amigo("juani").
amigo("martin").
amigo("herre").
amigo("nacho").
amigo("agustin").
amigo("juan francisco")

materia_cursada("introduccion a la programacion i").
materia_cursada("analisis matematico i").
materia_cursada("algebra i").
materia_cursada("quimica").
materia_cursada("ciencias de la computacion i").
materia_cursada("introduccion a la programacion II").
materia_cursada("algebra lineal").
materia_cursada("fisica general").
materia_cursada("matematica discreta").
materia_cursada("ciencias de la computacion ii").
materia_cursada("analisis y dise�o de algoritmos i").
materia_cursada("introduccion a la arquitectura de sistemas").
materia_cursada("analisis matematico ii").
materia_cursada("electricidad y Magnetismo").
materia_cursada("analisis y Dise�o de Algoritmos ii").
materia_cursada("comunicacion de Datos i").
materia_cursada("probabilidades y estadistica").
materia_cursada("electronica digital").
materia_cursada("programacion orientada a objetos").
materia_cursada("estructuras de almacenamiento de datos").
materia_cursada("metodologias de desarrollo de software").
materia_cursada("arquitectura de computadoras i").

materia_promocionada("introduccion a la programacion i").
materia_promocionada("analisis matematico i").
materia_promocionada("algebra i").
materia_promocionada("ciencias de la computacion i").
materia_promocionada("introduccion a la programacion ii").
materia_promocionada("algebra lineal").
materia_promocionada("fisica general").
materia_promocionada("matematica discreta").
materia_promocionada("ciencias de la computacion ii").
materia_promocionada("introduccion a la arquitectura de sistemas").
materia_promocionada("electricidad y magnetismo").
materia_promocionada("analisis y dise�o de algoritmos ii").
materia_promocionada("probabilidades y estadistica").
materia_promocionada("metodologias de desarrollo de software").
materia_promocionada("arquitectura de computadoras i").

dia_cursada("lunes").
dia_cursada("martes").
dia_cursada("miercoles").
dia_cursada("jueves").


cursas(X) :- dia_cursada(X).
es_amigo(X):- amigo(X).
cursaste(X) :- materia_cursada(X).
promocionaste(X) :- materia_promocionada(X).
todas_las_promocionadas(L) :- findall(X,(materia_promocionada(X)),L).
todas_las_cursadas(L) :- findall(X,(materia_cursada(X)),L).
tu_grupo_de_amigos(L) :- findall(X,(amigo(X)),L).
