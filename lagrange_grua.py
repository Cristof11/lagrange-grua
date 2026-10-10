# -*- coding: utf-8 -*-
"""
Taller en clase - Análisis Numérico
Ejercicio 1: Interpolación de Lagrange

Una grúa presenta los siguientes valores de "extensión adicional" del cable
de carga según la tabla. Estimar la lectura que debe corresponder en la
escala para una carga de 4.85 ton, hallar el polinomio de Lagrange y graficar.

    Carga (ton) | Lectura (mm)
    ------------+-------------
         4      |    76.5
         6      |    78.0
         8      |    79.3

Autor: Jeison Crishtofer Rojas
Requisitos: Python 3.8+, matplotlib, numpy  (tkinter viene con Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# ----------------------------------------------------------------------------
#  Datos del ejercicio
# ----------------------------------------------------------------------------
DATOS_X = [4.0, 6.0, 8.0]          # Carga (ton)
DATOS_Y = [76.5, 78.0, 79.3]       # Lectura (mm)
X_ESTIMAR = 4.85                   # Carga a estimar (ton)


# ----------------------------------------------------------------------------
#  Utilidades de formato
# ----------------------------------------------------------------------------
def num(v, dec=6):
    """Formatea un número quitando ceros innecesarios."""
    if abs(v) < 1e-12:
        v = 0.0
    s = f"{v:.{dec}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def factor(xj):
    """Texto del factor (x - xj)."""
    if xj < 0:
        return f"(x + {num(-xj)})"
    return f"(x - {num(xj)})"


def poly_mul(a, b):
    """Multiplica dos polinomios (coeficientes de menor a mayor grado)."""
    r = [0.0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] += ai * bj
    return r


def poly_texto(c, var="x"):
    """Polinomio en texto, de mayor a menor grado."""
    partes = []
    for k in range(len(c) - 1, -1, -1):
        a = c[k]
        if abs(a) < 1e-12:
            continue
        signo = "-" if a < 0 else "+"
        mag = abs(a)
        if k == 0:
            t = num(mag)
        else:
            coef = "" if abs(mag - 1) < 1e-12 else num(mag)
            t = f"{coef}{var}" + (f"²" if k == 2 else (f"³" if k == 3 else (f"^{k}" if k > 1 else "")))
        partes.append((signo, t))
    if not partes:
        return "0"
    s = ("-" if partes[0][0] == "-" else "") + partes[0][1]
    for sg, t in partes[1:]:
        s += f" {sg} {t}"
    return s


def poly_eval(c, x):
    return sum(a * x ** k for k, a in enumerate(c))


# ----------------------------------------------------------------------------
#  Núcleo: interpolación de Lagrange
# ----------------------------------------------------------------------------
def lagrange(xs, ys, x):
    """
    Devuelve un diccionario con todo el desarrollo:
      - bases:   coeficientes de cada L_i(x)
      - den:     denominador de cada L_i
      - Li_val:  valor de L_i en x
      - poli:    coeficientes del polinomio P(x)
      - valor:   P(x)
    """
    n = len(xs)
    bases, dens, Li_val = [], [], []
    poli = [0.0] * n
    for i in range(n):
        num_poly = [1.0]
        den = 1.0
        val = 1.0
        for j in range(n):
            if j == i:
                continue
            num_poly = poly_mul(num_poly, [-xs[j], 1.0])
            den *= (xs[i] - xs[j])
            val *= (x - xs[j]) / (xs[i] - xs[j])
        coef = [c / den for c in num_poly]
        bases.append(coef)
        dens.append(den)
        Li_val.append(val)
        for k, c in enumerate(coef):
            poli[k] += ys[i] * c
    valor = sum(ys[i] * Li_val[i] for i in range(n))
    return {"bases": bases, "den": dens, "Li_val": Li_val,
            "poli": poli, "valor": valor}


def desarrollo_texto(xs, ys, x, r):
    """Construye el desarrollo paso a paso como texto."""
    n = len(xs)
    L = []
    sep = "─" * 66
    L.append("EJERCICIO 1 — INTERPOLACIÓN DE LAGRANGE")
    L.append(sep)
    L.append("Una grúa presenta los siguientes valores de 'extensión adicional'")
    L.append("del cable de carga. Estimar la lectura en la escala para una")
    L.append(f"carga de {num(x)} ton.\n")

    L.append("PASO 1. Datos")
    L.append(sep)
    L.append("   i  |  Carga x_i (ton)  |  Lectura y_i (mm)")
    L.append("  ----+-------------------+------------------")
    for i in range(n):
        L.append(f"   {i}  |  {num(xs[i]):>15}  |  {num(ys[i]):>15}")
    L.append(f"\n   Valor a estimar: x = {num(x)} ton")
    L.append(f"   Con {n} puntos se obtiene un polinomio de grado {n - 1}.\n")

    L.append("PASO 2. Fórmula de Lagrange")
    L.append(sep)
    L.append("   P(x) = Σ y_i · L_i(x)")
    L.append("   L_i(x) = Π (x - x_j) / (x_i - x_j)   para j ≠ i\n")

    L.append("PASO 3. Polinomios base L_i(x)")
    L.append(sep)
    for i in range(n):
        numer = "".join(factor(xs[j]) for j in range(n) if j != i)
        denom = "".join(f"({num(xs[i])} - {num(xs[j])})" for j in range(n) if j != i)
        L.append(f"   L{i}(x) = {numer} / [{denom}]")
        L.append(f"         = {numer} / ({num(r['den'][i])})")
        L.append(f"         = {poly_texto(r['bases'][i])}\n")

    L.append(f"PASO 4. Evaluar cada L_i en x = {num(x)}")
    L.append(sep)
    for i in range(n):
        numer = "".join(f"({num(x)} - {num(xs[j])})" for j in range(n) if j != i)
        prod = 1.0
        for j in range(n):
            if j != i:
                prod *= (x - xs[j])
        L.append(f"   L{i}({num(x)}) = {numer} / ({num(r['den'][i])})")
        L.append(f"            = {num(prod)} / ({num(r['den'][i])}) = {num(r['Li_val'][i], 7)}")
    suma_L = sum(r["Li_val"])
    L.append(f"\n   Comprobación: L0 + L1 + ... = {num(suma_L, 7)}  (debe dar 1)\n")

    L.append(f"PASO 5. Calcular P({num(x)})")
    L.append(sep)
    terminos = " + ".join(f"({num(ys[i])})({num(r['Li_val'][i], 7)})" for i in range(n))
    L.append(f"   P({num(x)}) = {terminos}")
    prods = [ys[i] * r["Li_val"][i] for i in range(n)]
    L.append("          = " + " + ".join(f"({num(p, 7)})" for p in prods))
    L.append(f"          = {num(r['valor'], 7)} mm\n")

    L.append("PASO 6. Polinomio interpolante P(x)")
    L.append(sep)
    for i in range(n):
        L.append(f"   y{i}·L{i}(x) = {num(ys[i])}·[{poly_texto(r['bases'][i])}]")
        L.append(f"            = {poly_texto([ys[i] * c for c in r['bases'][i]])}")
    L.append("\n   Sumando términos semejantes:")
    L.append(f"\n   ►  P(x) = {poly_texto(r['poli'])}\n")

    L.append("PASO 7. Verificación en los nodos")
    L.append(sep)
    for i in range(n):
        L.append(f"   P({num(xs[i])}) = {num(poly_eval(r['poli'], xs[i]), 6)}   "
                 f"(tabla: {num(ys[i])})  ✓")
    L.append(f"   P({num(x)}) con el polinomio = {num(poly_eval(r['poli'], x), 7)}\n")

    L.append("RESPUESTA")
    L.append(sep)
    L.append(f"   Para una carga de {num(x)} ton, la lectura estimada en la escala es:")
    L.append(f"\n        Lectura ≈ {num(r['valor'], 4)} mm   (≈ {r['valor']:.2f} mm)")
    return "\n".join(L)


# ----------------------------------------------------------------------------
#  Interfaz gráfica
# ----------------------------------------------------------------------------
class App(tk.Tk):
    AZUL = "#1f4e79"
    NARANJA = "#d9480f"

    def __init__(self):
        super().__init__()
        self.title("Interpolación de Lagrange — Grúa (Análisis Numérico)")
        self.geometry("1250x760")
        self.minsize(1000, 640)
        self.filas = []          # [(entry_x, entry_y, frame)]
        self.mostrar_bases = tk.BooleanVar(value=False)
        self._bloquear = True    # evita que el deslizador recalcule durante la construcción
        self._estilos()
        self._construir()
        self._bloquear = False
        self.calcular()

    # ---------- estilos ----------
    def _estilos(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass
        st.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"), foreground=self.AZUL)
        st.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#444")
        st.configure("Res.TLabel", font=("Segoe UI", 22, "bold"), foreground=self.NARANJA)
        st.configure("Pol.TLabel", font=("Consolas", 12, "bold"), foreground=self.AZUL)
        st.configure("Acc.TButton", font=("Segoe UI", 10, "bold"))

    # ---------- layout ----------
    def _construir(self):
        cab = ttk.Frame(self, padding=(14, 10, 14, 4))
        cab.pack(fill="x")
        ttk.Label(cab, text="Ejercicio 1 · Interpolación de Lagrange",
                  style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(cab, text="Extensión adicional del cable de carga de una grúa — "
                            "estimar la lectura (mm) para una carga dada (ton).",
                  style="Sub.TLabel").pack(anchor="w")

        cuerpo = ttk.Frame(self, padding=(14, 6, 14, 12))
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # ---- panel izquierdo ----
        izq = ttk.Frame(cuerpo, width=320)
        izq.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        lf = ttk.LabelFrame(izq, text=" Tabla de datos ", padding=10)
        lf.pack(fill="x")
        enc = ttk.Frame(lf)
        enc.pack(fill="x")
        ttk.Label(enc, text="Carga (ton)", width=13, anchor="center",
                  font=("Segoe UI", 9, "bold")).grid(row=0, column=0)
        ttk.Label(enc, text="Lectura (mm)", width=13, anchor="center",
                  font=("Segoe UI", 9, "bold")).grid(row=0, column=1)
        self.cont_filas = ttk.Frame(lf)
        self.cont_filas.pack(fill="x")
        for xv, yv in zip(DATOS_X, DATOS_Y):
            self._agregar_fila(xv, yv)
        bts = ttk.Frame(lf)
        bts.pack(fill="x", pady=(8, 0))
        ttk.Button(bts, text="+ Punto", command=lambda: self._agregar_fila()).pack(side="left")
        ttk.Button(bts, text="− Punto", command=self._quitar_fila).pack(side="left", padx=4)
        ttk.Button(bts, text="Restaurar", command=self._restaurar).pack(side="right")

        lx = ttk.LabelFrame(izq, text=" Carga a estimar (ton) ", padding=10)
        lx.pack(fill="x", pady=10)
        self.var_x = tk.StringVar(value=num(X_ESTIMAR))
        ex = ttk.Entry(lx, textvariable=self.var_x, font=("Segoe UI", 12), width=10,
                       justify="center")
        ex.pack(fill="x")
        ex.bind("<Return>", lambda e: self.calcular())
        self.escala = ttk.Scale(lx, from_=min(DATOS_X), to=max(DATOS_X),
                                command=self._mover_escala)
        self.escala.set(X_ESTIMAR)
        self.escala.pack(fill="x", pady=(8, 0))
        ttk.Label(lx, text="Desliza para ver la estimación en vivo",
                  style="Sub.TLabel").pack(anchor="w")
        ttk.Button(lx, text="Calcular", style="Acc.TButton",
                   command=self.calcular).pack(fill="x", pady=(8, 0))

        lr = ttk.LabelFrame(izq, text=" Resultado ", padding=10)
        lr.pack(fill="x")
        self.lbl_res_x = ttk.Label(lr, text="", style="Sub.TLabel")
        self.lbl_res_x.pack(anchor="w")
        self.lbl_res = ttk.Label(lr, text="", style="Res.TLabel")
        self.lbl_res.pack(anchor="w")
        ttk.Label(lr, text="Polinomio de Lagrange:", style="Sub.TLabel").pack(anchor="w", pady=(8, 0))
        self.lbl_pol = ttk.Label(lr, text="", style="Pol.TLabel", wraplength=290)
        self.lbl_pol.pack(anchor="w")

        ttk.Checkbutton(izq, text="Mostrar términos yᵢ·Lᵢ(x) en la gráfica",
                        variable=self.mostrar_bases,
                        command=self.calcular).pack(anchor="w", pady=(10, 0))

        # ---- panel derecho: pestañas ----
        nb = ttk.Notebook(cuerpo)
        nb.grid(row=0, column=1, sticky="nsew")

        tab_g = ttk.Frame(nb)
        nb.add(tab_g, text="  Gráfica  ")
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab_g)
        NavigationToolbar2Tk(self.canvas, tab_g).update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        tab_d = ttk.Frame(nb)
        nb.add(tab_d, text="  Desarrollo paso a paso  ")
        self.txt = tk.Text(tab_d, wrap="none", font=("Consolas", 11),
                           bg="#fbfbfd", fg="#1d1d1f", padx=14, pady=10, relief="flat")
        sy = ttk.Scrollbar(tab_d, orient="vertical", command=self.txt.yview)
        sx = ttk.Scrollbar(tab_d, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.txt.pack(fill="both", expand=True)
        self.txt.tag_configure("tit", font=("Consolas", 11, "bold"), foreground=self.AZUL)
        self.txt.tag_configure("res", font=("Consolas", 13, "bold"), foreground=self.NARANJA)

    # ---------- filas de la tabla ----------
    def _agregar_fila(self, xv=None, yv=None):
        f = ttk.Frame(self.cont_filas)
        f.pack(fill="x", pady=2)
        ex = ttk.Entry(f, width=13, justify="center")
        ey = ttk.Entry(f, width=13, justify="center")
        ex.grid(row=0, column=0, padx=(0, 4))
        ey.grid(row=0, column=1)
        if xv is not None:
            ex.insert(0, num(xv))
        if yv is not None:
            ey.insert(0, num(yv))
        for e in (ex, ey):
            e.bind("<Return>", lambda ev: self.calcular())
        self.filas.append((ex, ey, f))

    def _quitar_fila(self):
        if len(self.filas) <= 2:
            messagebox.showinfo("Aviso", "Se necesitan al menos 2 puntos.")
            return
        ex, ey, f = self.filas.pop()
        f.destroy()
        self.calcular()

    def _restaurar(self):
        for _, _, f in self.filas:
            f.destroy()
        self.filas.clear()
        for xv, yv in zip(DATOS_X, DATOS_Y):
            self._agregar_fila(xv, yv)
        self.var_x.set(num(X_ESTIMAR))
        self.calcular()

    def _leer_datos(self):
        xs, ys = [], []
        for ex, ey, _ in self.filas:
            sx, sy = ex.get().strip(), ey.get().strip()
            if not sx and not sy:
                continue
            xs.append(float(sx.replace(",", ".")))
            ys.append(float(sy.replace(",", ".")))
        if len(xs) < 2:
            raise ValueError("Ingresa al menos 2 puntos.")
        if len(set(xs)) != len(xs):
            raise ValueError("Los valores de carga (x) no pueden repetirse.")
        x = float(self.var_x.get().strip().replace(",", "."))
        return xs, ys, x

    def _mover_escala(self, v):
        if getattr(self, "_bloquear", False):
            return
        self.var_x.set(num(float(v), 3))
        self.calcular(desde_escala=True)

    # ---------- cálculo y dibujo ----------
    def calcular(self, desde_escala=False):
        try:
            xs, ys, x = self._leer_datos()
        except ValueError as e:
            if not desde_escala:
                messagebox.showerror("Datos inválidos", str(e) if str(e) else
                                     "Revisa que todos los valores sean numéricos.")
            return

        r = lagrange(xs, ys, x)

        # rango de la escala según datos
        lo, hi = min(xs), max(xs)
        if not desde_escala:
            self._bloquear = True
            self.escala.configure(from_=lo - (hi - lo) * 0.25, to=hi + (hi - lo) * 0.25)
            self.escala.set(x)
            self.update_idletasks()
            self._bloquear = False

        self.lbl_res_x.configure(text=f"Lectura estimada para {num(x)} ton:")
        self.lbl_res.configure(text=f"{r['valor']:.4f} mm")
        self.lbl_pol.configure(text=f"P(x) = {poly_texto(r['poli'])}")
        if x < lo or x > hi:
            self.lbl_res_x.configure(text=f"⚠ Extrapolación ({num(x)} ton fuera de la tabla):")

        self._escribir_desarrollo(desarrollo_texto(xs, ys, x, r))
        self._graficar(xs, ys, x, r)

    def _escribir_desarrollo(self, texto):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        for linea in texto.split("\n"):
            if linea.startswith("PASO") or linea.startswith("EJERCICIO") or linea == "RESPUESTA":
                self.txt.insert("end", linea + "\n", "tit")
            elif "Lectura ≈" in linea or "►" in linea:
                self.txt.insert("end", linea + "\n", "res")
            else:
                self.txt.insert("end", linea + "\n")
        self.txt.configure(state="disabled")

    def _graficar(self, xs, ys, x, r):
        ax = self.ax
        ax.clear()
        if getattr(self, "ax2", None) is not None:
            self.ax2.remove()
            self.ax2 = None
        lo, hi = min(xs + [x]), max(xs + [x])
        m = (hi - lo) * 0.15 or 1
        xx = np.linspace(lo - m, hi + m, 400)
        yy = np.array([poly_eval(r["poli"], t) for t in xx])

        if self.mostrar_bases.get():
            colores = ["#7aa6c2", "#9bc59d", "#d6a2c8", "#e0b36b", "#a0a0d8"]
            ax2 = self.ax2 = ax.twinx()
            for i, c in enumerate(r["bases"]):
                yb = [ys[i] * poly_eval(c, t) for t in xx]
                ax2.plot(xx, yb, "--", lw=1, color=colores[i % len(colores)],
                         label=f"y{i}·L{i}(x)")
            ax2.set_ylabel("Términos yᵢ·Lᵢ(x)", color="#666")
            ax2.legend(loc="lower right", fontsize=8)

        ax.plot(xx, yy, color=self.AZUL, lw=2.2,
                label=f"P(x) = {poly_texto(r['poli'])}")
        ax.scatter(xs, ys, s=70, color="#2b8a3e", zorder=5, edgecolor="white",
                   linewidth=1.5, label="Datos de la tabla")
        for xi, yi in zip(xs, ys):
            ax.annotate(f"({num(xi)}, {num(yi)})", (xi, yi), textcoords="offset points",
                        xytext=(8, -14), fontsize=9, color="#2b8a3e")

        yv = r["valor"]
        ymin = min(yy.min(), min(ys))
        xmin = xx[0]
        ax.plot([x, x], [ymin - 0.3, yv], ":", color=self.NARANJA, lw=1.4)
        ax.plot([xmin, x], [yv, yv], ":", color=self.NARANJA, lw=1.4)
        ax.scatter([x], [yv], s=110, marker="*", color=self.NARANJA, zorder=6,
                   label=f"Estimación: P({num(x)}) = {yv:.4f} mm")
        ax.annotate(f"P({num(x)}) ≈ {yv:.4f} mm", (x, yv), textcoords="offset points",
                    xytext=(-20, 16), fontsize=10, fontweight="bold", color=self.NARANJA)

        ax.set_xlim(xx[0], xx[-1])
        ax.set_ylim(ymin - 0.3, max(yy.max(), max(ys)) + 0.4)
        ax.set_title("Interpolación de Lagrange — Extensión del cable de la grúa",
                     fontsize=12, fontweight="bold", color=self.AZUL)
        ax.set_xlabel("Carga (ton)")
        ax.set_ylabel("Lectura (mm)")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper left", fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()


if __name__ == "__main__":
    App().mainloop()
