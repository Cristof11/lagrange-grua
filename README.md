# Interpolación de Lagrange — Grúa

**Análisis Numérico · Taller en clase · Ejercicio 1**
Jeison Crishtofer Rojas — Ingeniería de Sistemas, Universidad de Cundinamarca

## Enunciado

Una grúa presenta los siguientes valores de “extensión adicional” del cable de carga:

| Carga (ton) | Lectura (mm) |
|:-----------:|:------------:|
| 4           | 76.5         |
| 6           | 78.0         |
| 8           | 79.3         |

Estimar, por **interpolación de Lagrange**, la lectura que debe corresponder en la escala para una carga de **4.85 ton**, hallar el polinomio y graficarlo.

## Resultado

- Polinomio de Lagrange: **P(x) = −0.025x² + x + 72.9**
- Lectura estimada: **P(4.85) = 77.1619 mm**

## Contenido

| Archivo | Descripción |
|---|---|
| `index.html` | Aplicación web interactiva (se publica con GitHub Pages). Muestra la gráfica, el desarrollo paso a paso y permite cambiar los datos. |
| `lagrange_grua.py` | Versión de escritorio en Python (tkinter + matplotlib). |

## Cómo usar la página

- Escribe una carga o mueve el deslizador para ver la estimación en vivo.
- Haz clic sobre la gráfica para estimar en ese punto.
- La pestaña **Polinomios base Lᵢ(x)** muestra cada base y su valor en x.
- Puedes editar la tabla, agregar o quitar puntos; **Restaurar** vuelve al ejercicio original.
- **Imprimir / Guardar PDF** genera la solución en PDF desde el navegador.

## Versión de escritorio

```bash
pip install matplotlib numpy
python lagrange_grua.py
```
