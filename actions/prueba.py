from swiplserver import PrologMQI, PrologThread

with PrologMQI(port=8000) as mqi:
    with mqi.create_thread() as prolog_thread:
            prolog_thread.query_async(r"consult('C:\\Users\\54223\\RasaDavid\\data\\plan.pl')", find_all=False)
            prolog_thread.query_async(f"materias(6223,_,_,_)", find_all=False)
            result = prolog_thread.query_async_result()
            print(str(result))