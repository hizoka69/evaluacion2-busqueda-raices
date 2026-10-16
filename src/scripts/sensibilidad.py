import csv
import os
import numpy as np
import metodos as m
from funciones import FUNCIONES, raiz_referencia
from graficos import graficar_sensibilidad

#.py creado para pregunta 5 y no mezclar demas

INTERVALOS = {
    "f1_polinomica_simple": [(1, 2), (0, 3), (-5, 10), (-100, 100)],
    "f2_polinomica_doble":  [(1, 3), (0, 4)],
    "f3_logaritmica":       [(2, 3), (1, 5), (0.5, 10), (0.01, 1000)],
    "f4_exponencial":       [(0, 1), (-1, 2), (-10, 20), (-30, 100)],
    "f5_trigonometrica":    [(0, 1), (-1, 2), (-10, 10), (-100, 100)],
    "f6_mixta":             [(0.1, 1), (0.01, 2), (0.0001, 50), (1e-6, 1e4)],
}

ESTIMACIONES = {
    "f1_polinomica_simple": [1.5, 5.0, 0.5, 0.0],
    "f2_polinomica_doble":  [1.2, 0.0, 5.0, 1.9],
    "f3_logaritmica":       [2.5, 0.1, 10.0, 600.0],
    "f4_exponencial":       [0.5, -5.0, 10.0, 50.0],
    "f5_trigonometrica":    [0.5, 3.0, 10.0, -1.5],
    "f6_mixta":             [0.55, 0.01, 5.0, 50.0],
}

PASO_SECANTE = 0.1


UMBRAL_ESPURIA = 1e-2   # "convergio" con error real mayor a esto = convergencia espuria


def _fila(func, analisis, escenario, res):
    ref = raiz_referencia(func)
    error = abs(res.raiz - ref) if np.isfinite(res.raiz) else float("nan")
    espuria = bool(res.convergio and error > UMBRAL_ESPURIA)
    return {
        "funcion": func.clave, "nombre_funcion": func.nombre,
        "analisis": analisis, "escenario": escenario, "metodo": res.metodo,
        "aplica": res.aplica, "convergio": res.convergio,
        "iteraciones": res.iteraciones if res.aplica else "",
        "raiz": res.raiz, "error_absoluto": error,
        "convergencia_espuria": espuria,
        "estado": ("Convergencia ESPURIA (el criterio de parada se cumplio lejos de la raiz)"
                   if espuria else res.estado),
    }


def ejecutar(dir_data: str, dir_assets: str) -> None:
    filas_int, filas_est = [], []
    for func in FUNCIONES:
        for a, b in INTERVALOS[func.clave]:
            esc = f"[{a:g}, {b:g}]"
            filas_int.append(_fila(func, "intervalo", esc, m.biseccion(func.f, a, b)))
            filas_int.append(_fila(func, "intervalo", esc, m.falsa_posicion(func.f, a, b)))
        for x0 in ESTIMACIONES[func.clave]:
            esc = f"x0={x0:g}"
            filas_est.append(_fila(func, "estimacion_inicial", esc, m.punto_fijo(func.f, func.g, x0)))
            filas_est.append(_fila(func, "estimacion_inicial", esc,
                                   m.secante(func.f, x0, x0 + PASO_SECANTE)))
            filas_est.append(_fila(func, "estimacion_inicial", esc, m.newton_raphson(func.f, func.df, x0)))
            filas_est.append(_fila(func, "estimacion_inicial", esc,
                                   m.newton_mejorado(func.f, func.df, func.d2f, x0)))

    todas = filas_int + filas_est
    ruta_csv = os.path.join(dir_data, "sensibilidad.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(todas[0].keys()))
        w.writeheader()
        w.writerows(todas)

    graficar_sensibilidad(filas_int, ["Bisección", "Falsa posición"],
                          "Sensibilidad al intervalo inicial [a, b] (métodos cerrados)",
                          os.path.join(dir_assets, "sensibilidad_intervalo.png"))
    graficar_sensibilidad(filas_est, ["Punto fijo", "Secante", "Newton-Raphson", "Newton mejorado"],
                          "Sensibilidad a la estimación inicial x0 (métodos abiertos)",
                          os.path.join(dir_assets, "sensibilidad_estimacion.png"))

    # Resumen por consola
    print("\n=== SENSIBILIDAD ===")
    for f in todas:
        it = f["iteraciones"] if f["aplica"] else "-"
        print(f"{f['funcion']:<22} {f['analisis']:<19} {f['escenario']:<16} "
              f"{f['metodo']:<16} it={str(it):<4} {f['estado']}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ejecutar(os.path.join(base, "data"), os.path.join(base, "assets"))
