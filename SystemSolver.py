import math

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from numpy import linspace


class SystemSolver:
    def __init__(self):
        self.x, self.y = sp.Symbol('x y', real=True)
        self.func1 = None
        self.func2 = None

    @staticmethod
    def draw_graphic(eq1, eq2):
        plot_equation1 = sp.plot_implicit(eq1, line_color='r', show=False)
        plot_equation2 = sp.plot_implicit(eq2, line_color='g', show=False)
        plot_equation1.extend(plot_equation2)
        plot_equation1.show()

    @staticmethod
    def parse_functions(func1_str, func2_str):
        try:
            transformations = sp.parsing.sympy_parser.standard_transformations
            func1 = sp.parse_expr(func1_str, evaluate=False, transformations=transformations)
            func2 = sp.parse_expr(func2_str, evaluate=False, transformations=transformations)
            return {'func1': func1, 'func2': func2}
        except (ValueError, SyntaxError):
            raise SyntaxError("Functions parsing error!")

    @staticmethod
    def solve(func1_str, func2_str, closing_x, closing_y, accuracy):
        # define values
        functions = SystemSolver.parse_functions(func1_str, func2_str)
        func1 = functions['func1']
        func2 = functions['func2']

        x, y, dx, dy = sp.symbols('x y dx dy')

        # create jacobian matrix and vector-matrix of input functions
        F = sp.Matrix([func1, func2])

        J = F.jacobian([x, y])
        V = sp.Matrix([dx, dy])
        JV = J * V

        first_equation = sp.Eq(JV[0], -F[0])
        second_equation = sp.Eq(JV[1], -F[1])

        x0, x1 = 0, closing_x
        y0, y1 = 0, closing_y

        steps = 0
        while math.fabs(x1 - x0) > accuracy and math.fabs(y1 - y0) > accuracy:
            steps += 1

            x0 = x1
            y0 = y1

            eq1 = first_equation.subs({x: x0, y: y0})
            eq2 = second_equation.subs({x: x0, y: y0})

            deltas = sp.solve([eq1, eq2], [dx, dy])

            x1 = x0 + deltas[dx]
            y1 = y0 + deltas[dy]

        return {'x': x1, 'y': y1, 'steps': steps, 'accuracy': accuracy}
