"""Ejecuta los métodos de búsqueda de raíces y guarda los resultados."""
import csv
import os

import numpy as np

import metodos as m
from analisis import ejecutar_metodos, metricas
from funciones import FUNCIONES, raiz_referencia
from graficos import graficar_convergencia, graficar_funcion, graficar_resumen
from verificacion import verificar
import sensibilidad

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DATA = os.path.join(BASE, "data")
DIR_ASSETS = os.path.join(BASE, "assets")


def escribir_csv(ruta, columnas, filas):
    with open(ruta, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)


def main():
    os.makedirs(DIR_DATA, exist_ok=True)
    os.makedirs(DIR_ASSETS, exist_ok=True)
    print(f"Tolerancia = {m.TOL:g} | Máx. iteraciones = {m.MAX_ITER}\n")

    filas_resumen, filas_verif, todos = [], [], {}

    for func in FUNCIONES:
        raiz = raiz_referencia(func)

        # Verificación de raíces
        v = verificar(func, raiz)
        filas_verif.append(v)
        print(f"[{func.clave}] {func.expresion}")
        print(f"   raíz de referencia = {raiz:.12f}")
        print(f"   {v['conclusion']}")

        # Datos de la función
        x = np.linspace(*func.rango_grafico, 400)
        with np.errstate(all="ignore"):
            y = func.f(x)
        escribir_csv(os.path.join(DIR_DATA, f"{func.clave}.csv"), ["x", "f(x)"],
                     [{"x": float(xi), "f(x)": float(yi)} for xi, yi in zip(x, y)])

        # Métodos numéricos
        resultados = ejecutar_metodos(func)
        extendidos = {r.metodo: r for r, _ in ejecutar_metodos(func, tol=1e-14)}  # Estimación del orden de convergencia
        todos[func] = resultados
        for res, params in resultados:
            mt = metricas(func, res, raiz, extendidos[res.metodo])
            filas_resumen.append({
                "funcion": func.clave,
                "categoria": func.categoria,
                "metodo": res.metodo,
                "parametros_iniciales": params,
                "aplica": res.aplica,
                "convergio": res.convergio,
                "iteraciones": res.iteraciones if res.aplica else "",
                "raiz_aproximada": res.raiz,
                "raiz_referencia": raiz,
                "error_absoluto": mt["error"],
                "ultimo_paso": mt["paso_final"],
                "f(raiz_aprox)": mt["f_raiz"],
                "criterio_parada": res.criterio,
                "orden_empirico": mt["orden_empirico"],
                "estado": res.estado,
            })
            it = res.iteraciones if res.aplica else "-"
            print(f"   {res.metodo:<16} it={str(it):<4} raíz={res.raiz:<20.12g} "
                  f"error={mt['error']:<10.3e} {res.estado}")

        # Gráficos por función
        graficar_funcion(func, raiz, os.path.join(DIR_ASSETS, f"{func.clave}_funcion.png"))
        graficar_convergencia(func, raiz, resultados,
                              os.path.join(DIR_ASSETS, f"{func.clave}_convergencia.png"))
        print()

    # Resúmenes CSV
    escribir_csv(os.path.join(DIR_DATA, "resumen_convergencia.csv"),
                 list(filas_resumen[0].keys()), filas_resumen)
    escribir_csv(os.path.join(DIR_DATA, "verificacion_raices.csv"),
                 list(filas_verif[0].keys()), filas_verif)

    # Resumen de iteraciones
    graficar_resumen(todos, os.path.join(DIR_ASSETS, "resumen_iteraciones.png"))

    # Análisis de sensibilidad
    sensibilidad.ejecutar(DIR_DATA, DIR_ASSETS)

    print(f"\nListo. CSV en {DIR_DATA}\nGráficos en {DIR_ASSETS}")


if __name__ == "__main__":
    main()
