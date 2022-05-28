import math


class HalDivision:
    @staticmethod
    def find_root(a, b, accuracy, func):
        steps = 0
        x = (a + b) / 2
        while math.fabs(b - a) > accuracy and math.fabs(func(x)) > accuracy:
            x = (a + b) / 2
            if func(a) * func(x) > 0:
                a = x
            else:
                b = x
            steps += 1

        x = (a + b) / 2

        return {'root': x, 'steps': steps, 'accuracy': accuracy}
