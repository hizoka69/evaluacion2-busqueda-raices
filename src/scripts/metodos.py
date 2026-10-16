"""Métodos numéricos para buscar raíces y registrar iteraciones."""
from dataclasses import dataclass, field
from typing import Callable, List

import numpy as np

TOL = 1e-6
MAX_ITER = 100
LIMITE_DIVERGENCIA = 1e12  # Límite para detectar divergencia

NOMBRES = ["Bisección", "Falsa posición", "Punto fijo",
           "Secante", "Newton-Raphson", "Newton mejorado"]


@dataclass
class Resultado:
    metodo: str
    aplica: bool = True
    convergio: bool = False
    iteraciones: int = 0
    raiz: float = float("nan")
    historial: List[float] = field(default_factory=list)
    criterio: str = ""
    estado: str = ""


# Funciones auxiliares
def _ev(fun: Callable, x: float) -> float:
    """Evalúa la función evitando advertencias numéricas."""
    with np.errstate(all="ignore"):
        return float(fun(np.float64(x)))


def _criterio(fx: float, x_nuevo: float, x_ant: float, tol: float) -> str:
    if abs(fx) < tol:
        return "|f(x_n)| < tol"
    if abs(x_nuevo - x_ant) < tol:
        return "|x_n - x_(n-1)| < tol"
    return ""


def _registrar(r: Resultado, k: int, xn: float) -> bool:
    """Registra una aproximación válida."""
    r.iteraciones = k
    if not np.isfinite(xn):
        r.estado = "Falla: valor no finito (fuera del dominio de la función)"
        return False
    if abs(xn) > LIMITE_DIVERGENCIA:
        r.estado = "Diverge: |x_n| > 1e12"
        return False
    r.historial.append(float(xn))
    r.raiz = float(xn)
    return True


def _exito(r: Resultado, crit: str) -> Resultado:
    r.convergio = True
    r.criterio = crit
    r.estado = "Convergió"
    return r


def _sin_convergencia(r: Resultado, max_iter: int) -> Resultado:
    r.estado = f"No convergió en {max_iter} iteraciones"
    return r


# Métodos cerrados
def biseccion(f, a, b, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    r = Resultado("Bisección")
    fa, fb = _ev(f, a), _ev(f, b)
    if fa * fb > 0:
        r.aplica = False
        r.estado = "No aplica: f(a)·f(b) > 0 (sin cambio de signo)"
        return r
    if fa == 0 or fb == 0:
        r.raiz = a if fa == 0 else b
        return _exito(r, "f(extremo) = 0")

    previo = np.nan
    for k in range(1, max_iter + 1):
        c = 0.5 * (a + b)
        fc = _ev(f, c)
        _registrar(r, k, c)
        crit = _criterio(fc, c, previo, tol)
        if crit:
            return _exito(r, crit)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        previo = c
    return _sin_convergencia(r, max_iter)


def falsa_posicion(f, a, b, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    r = Resultado("Falsa posición")
    fa, fb = _ev(f, a), _ev(f, b)
    if fa * fb > 0:
        r.aplica = False
        r.estado = "No aplica: f(a)·f(b) > 0 (sin cambio de signo)"
        return r
    if fa == 0 or fb == 0:
        r.raiz = a if fa == 0 else b
        return _exito(r, "f(extremo) = 0")

    previo = np.nan
    for k in range(1, max_iter + 1):
        if fb - fa == 0:
            r.estado = "Falla: denominador nulo (f(a) = f(b))"
            return r
        c = (a * fb - b * fa) / (fb - fa)
        fc = _ev(f, c)
        _registrar(r, k, c)
        crit = _criterio(fc, c, previo, tol)
        if crit:
            return _exito(r, crit)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        previo = c
    return _sin_convergencia(r, max_iter)


# Métodos abiertos
def punto_fijo(f, g, x0, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    r = Resultado("Punto fijo")
    x = x0
    for k in range(1, max_iter + 1):
        xn = _ev(g, x)
        if not _registrar(r, k, xn):
            return r
        crit = _criterio(_ev(f, xn), xn, x, tol)
        if crit:
            return _exito(r, crit)
        x = xn
    return _sin_convergencia(r, max_iter)


def secante(f, x0, x1, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    r = Resultado("Secante")
    xa, xb = x0, x1
    fa, fb = _ev(f, xa), _ev(f, xb)
    for k in range(1, max_iter + 1):
        if not np.isfinite(fb - fa):
            r.iteraciones = k - 1
            r.estado = "Falla: x_n fuera del dominio de f (valor no finito)"
            return r
        if fb - fa == 0:
            r.iteraciones = k - 1
            r.estado = "Falla: denominador nulo (f(x_n) = f(x_(n-1)))"
            return r
        xn = xb - fb * (xb - xa) / (fb - fa)
        if not _registrar(r, k, xn):
            return r
        fn = _ev(f, xn)
        crit = _criterio(fn, xn, xb, tol)
        if crit:
            return _exito(r, crit)
        xa, fa, xb, fb = xb, fb, xn, fn
    return _sin_convergencia(r, max_iter)


def newton_raphson(f, df, x0, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    r = Resultado("Newton-Raphson")
    x = x0
    for k in range(1, max_iter + 1):
        fx, dfx = _ev(f, x), _ev(df, x)
        if not np.isfinite(dfx) or not np.isfinite(fx):
            r.iteraciones = k - 1
            r.estado = "Falla: x_n fuera del dominio de f o f' (valor no finito)"
            return r
        if dfx == 0:
            r.iteraciones = k - 1
            r.estado = "Falla: f'(x_n) = 0 (tangente horizontal)"
            return r
        xn = x - fx / dfx
        if not _registrar(r, k, xn):
            return r
        crit = _criterio(_ev(f, xn), xn, x, tol)
        if crit:
            return _exito(r, crit)
        x = xn
    return _sin_convergencia(r, max_iter)


def newton_mejorado(f, df, d2f, x0, tol=TOL, max_iter=MAX_ITER) -> Resultado:
    """Newton modificado para raíces múltiples."""
    r = Resultado("Newton mejorado")
    x = x0
    for k in range(1, max_iter + 1):
        fx, dfx, d2fx = _ev(f, x), _ev(df, x), _ev(d2f, x)
        den = dfx**2 - fx * d2fx
        if not np.isfinite(den) or not np.isfinite(fx):
            r.iteraciones = k - 1
            r.estado = "Falla: x_n fuera del dominio o desbordamiento (valor no finito)"
            return r
        if den == 0:
            r.iteraciones = k - 1
            r.estado = "Falla: f'^2 - f·f'' = 0 (cancelación numérica)"
            return r
        xn = x - fx * dfx / den
        if not _registrar(r, k, xn):
            return r
        crit = _criterio(_ev(f, xn), xn, x, tol)
        if crit:
            return _exito(r, crit)
        x = xn
    return _sin_convergencia(r, max_iter)
