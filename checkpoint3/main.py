from mandelbrot import Mandelbrot
from julia import Julia

mandelbrot1 = Mandelbrot(color_bar=True)
julia1 = Julia(-0.1+0.8j, color_bar=True, interpolation="none")

# mandelbrot1.compute()
julia1.compute()