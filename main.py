import math

import numpy as np
import matplotlib.pyplot as plt
from half_division_method import HalDivision
from simple_iteration_method import SimpleIteration
from SystemSolver import SystemSolver
import sympy as sp


class WrongData(Exception):
    pass


functions = {
    '1': lambda x: 2.74 * (x ** 3) - 1.93 * (x ** 2) - 15.28 * x - 3.72,
    '2': lambda x: x + 2,
    '3': lambda x: math.sin(x),
    '4': lambda x: math.sqrt(x)
}


def draw_orig_graphic(function_to_draw, left, right):
    xarr = np.linspace(left, right, 1000)
    try:
        for x in xarr:
            function_to_draw(x)
    except ValueError:
        xarr = np.linspace(0, 10, 1000)

    yarr = []
    for x in xarr:
        yarr.append(function_to_draw(x))

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')

    plt.plot(xarr, yarr, 'r')


def draw_and_print_root(root, root_name, func):
    print(root_name + ' =', round(root['root'], 3), root)
    plt.plot([root['root']], [func(root['root'])], color='b', marker='.', markersize=3)


def lab2_interactive():
    print("Select equation:")
    print("1: 2.74x^3 - 1.93x^2 - 15.28x - 3.72")
    print('2: x + 2')
    print('3: sin(x)')
    print('4: sqrt(x)')
    selected_function = input(">>> ")
    try:
        function = functions[selected_function]
    except KeyError:
        print("No such answer.")
        return

    root_number = 1
    min_a = -1
    max_b = 1
    while True:
        try:
            # get interval
            a = float(input("\nEnter the left boundary of the interval of the initial approximation:\n>>> "))
            b = float(input("Enter the right boundary of the interval of the initial approximation:\n>>> "))

            # for correct graphic drawing
            if min_a > a:
                min_a = a
            if max_b < b:
                max_b = b

            # pre-check if we have root on this interval
            try:
                if function(a) * function(b) > 0:
                    print("There is no root on this interval.")
                    continue
            except ValueError:
                raise ValueError("this function cannot be differentiated on this interval. Try other intervals.")

            accuracy = float(input("Enter accuracy:\n>>> "))
            method = int(input("Enter solving method (1 - HalfDivision/2 - SimpleIterations):\n>>> "))

            root = None
            if method == 1:
                root = HalDivision.find_root(a, b, accuracy, function)
            elif method == 2:
                root = SimpleIteration.find_root(a, b, accuracy, function)

            # so yeah, draw and print root
            draw_and_print_root(root, 'Root', function)
            root_number += 1

            need_to_continue = input(
                "Do you want to continue? (y - continue/anything else - show result and end)\n>>> ")
            if need_to_continue != "y":
                draw_orig_graphic(function, min_a, max_b)
                break
        except (WrongData, ValueError) as some_exception:
            print('Error:', some_exception.args[0])
            continue

    plt.savefig("graphicHD.jpg", dpi=600)
    plt.show()


def lab2_noninteractive():
    print("Roots of f(x)=(2.74x^3 - 1.93x^2 - 15.28x - 3.72):")
    draw_orig_graphic(functions['1'], -5, 5)

    root_right = HalDivision.find_root(2, 4, 0.01, functions['1'])
    draw_and_print_root(root_right, 'Right root', functions['1'])

    left_root = SimpleIteration.find_root(-3, -1, 0.01, functions['1'])
    draw_and_print_root(left_root, 'Left root', functions['1'])

    central_root = SimpleIteration.find_root(-1, 1, 0.01, functions['1'])
    draw_and_print_root(central_root, 'Central root', functions['1'])

    plt.savefig("graphicHD.jpg", dpi=600)
    plt.show()

    f1 = "x ** 2 + y ** 2 - 4"
    f2 = "-3 * x ** 2 + y"
    print("\nSystem of")
    print(" /")
    print(" |", f1, "= 0")
    print("<")
    print(" |", f2, "= 0")
    print(" \\")

    functions_to_draw = SystemSolver.parse_functions(f1, f2)
    SystemSolver.draw_graphic(sp.Eq(functions_to_draw['func1'], 0),
                              sp.Eq(functions_to_draw['func2'], 0))

    print("\nAt closing x = 1, y = 1")
    system_solution = SystemSolver.solve(f1, f2, 1, 1, 0.01)
    print('x1 =', round(system_solution['x'].evalf(), 3))
    print('y1 =', round(system_solution['y'].evalf(), 3))
    print(system_solution)

    print("\nAt closing x = -1, y = 1")
    system_solution = SystemSolver.solve(f1, f2, -1, 1, 0.01)
    print('x2 =', round(system_solution['x'].evalf(), 3))
    print('y2 =', round(system_solution['y'].evalf(), 3))
    print(system_solution)


def lab2_systems_interactive():
    try:
        f1 = input("Enter first func:\n>>> ")
        f2 = input("Enter second func:\n>>> ")

        functions_to_draw = SystemSolver.parse_functions(f1, f2)
        SystemSolver.draw_graphic(sp.Eq(functions_to_draw['func1'], 0),
                                  sp.Eq(functions_to_draw['func2'], 0))

        print("Check graphic and choose the nearest (on your opinion) point to the desired root:")
        closing_x = float(input("Enter closing x:\n>>> "))
        closing_y = float(input("Enter closing y:\n>>> "))
        accuracy = float(input("Enter accuracy:\n>>> "))
        system_solution = SystemSolver.solve(f1, f2, closing_x, closing_y, accuracy)
        print('x =', round(system_solution['x'].evalf(), 3))
        print('y =', round(system_solution['y'].evalf(), 3))
        print(system_solution)
    except (SyntaxError, TypeError, ValueError) as syntax_error:
        print("Error:", syntax_error.args[0])


if __name__ == '__main__':
    try:
        answer = int(input("How do you want to run program?"
                           "\n1 - standard root finder and system solver example"
                           "\n2 - interactive root finder"
                           "\n3 - interactive system solver"
                           "\n>>> "))
        if answer == 1:
            lab2_noninteractive()
        elif answer == 2:
            lab2_interactive()
        elif answer == 3:
            lab2_systems_interactive()
        else:
            raise (TypeError, ValueError)
    except ValueError:
        print("No such answer.")
