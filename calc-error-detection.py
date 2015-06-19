#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
計算誤差の検出

使い方:
python calc-error-detection.py int
python calc-error-detection.py float
"""

# 以下の行を有効にすると標準ライブラリの分数クラスを使用する(高機能な分遅い)
# from fractions import Fraction
import sys

__author__ = "peta_okechan"
__status__ = "development"
__version__ = "0.0.1"
__date__ = "2015.06.19"


# 演算子
operators = [
    ('+', lambda a, b: a + b),
    ('-', lambda a, b: a - b),
    ('*', lambda a, b: a * b),
    ('/', lambda a, b: a / b),
]

# 利用する数字のリスト
digits = range(0, 10)

# 目指す真の答え
answer = 10

# 式の項数
terms = 4


if 'Fraction' not in locals():
    class Fraction():
        '''
        分数クラス（約分非対応）
        実はPython 2.6から分数モジュール（fractions）が追加されているので
        必ずしも実装する必要はないのだが、
        四則演算用の特殊メソッドの例を示すため敢えて実装している。
        '''
        def __init__(self, num=0, denom=1):
            self.num = num
            self.denom = denom

        def __add__(self, other):
            if self.denom != other.denom:
                return self * Fraction(other.denom, other.denom)\
                    + other * Fraction(self.denom, self.denom)
            return Fraction(self.num + other.num, self.denom)

        def __sub__(self, other):
            return self + -other

        def __mul__(self, other):
            return Fraction(self.num * other.num, self.denom * other.denom)

        def __div__(self, other):
            return self * Fraction(other.denom, other.num)

        def __eq__(self, other):
            if other is None:
                return False
            return self.num * other.denom == other.num * self.denom

        def __neg__(self):
            return Fraction(-self.num, self.denom)


class Constant():
    '''
    定数式
    '''
    def __init__(self, num):
        self.num = num

    def eval(self, evaltype):
        '''
        定数を評価する
        evaltype: 評価時の型
        '''
        return evaltype(self.num)

    def __repr__(self):
        return self.num.__repr__()


class Binomial():
    '''
    二項式
    ツリーで式を表現する。
    計算結果がNaNになる場合はNoneを返す。
    '''
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def eval(self, evaltype):
        '''
        式を評価する
        evaltype: 評価時の型
        '''
        lv = self.lhs.eval(evaltype)
        rv = self.rhs.eval(evaltype)
        if self.op[0] == '/' and rv == evaltype(0):
            return None
        if lv is None or rv is None:
            return None
        return self.op[1](lv, rv)

    def __repr__(self):
        return '({} {} {})'.format(
            self.lhs.__repr__(),
            self.op[0],
            self.rhs.__repr__()
        )


class NumbersGenerator():
    '''
    総当たりで数字のリストを生成するクラス
    数字を生成するのではなく、数字のリストを生成する点に注意。
    '''
    def __init__(self, length):
        self.numbers = [None for i in range(length)]
        self.length = length

    def __iter__(self, depth=0):
        if self.length > depth:
            for i in digits:
                self.numbers[depth] = i
                for n in self.__iter__(depth + 1):
                    yield self.numbers
        else:
            yield self.numbers


class ExpressionGenerator():
    '''
    総当たりで式を生成するクラス
    '''
    def __init__(self, numbers):
        self.numbers = numbers

    def __iter__(self, left=0, right=None):
        if right is None:
            right = len(self.numbers) - 1

        if left == right:
            yield Constant(self.numbers[left])
        else:
            for i in range(left, right):
                for e1 in self.__iter__(left, i):
                    for e2 in self.__iter__(i + 1, right):
                        for op in operators:
                            yield Binomial(e1, op, e2)


def check(length, evaltype):
    '''
    分数で評価するとanswerになるが、evaltypeで評価すると
    誤差でanswerにならない式を表示する。
    '''
    numgen = NumbersGenerator(length)
    for numbers in numgen:
        expgen = ExpressionGenerator(numbers)
        for exp in expgen:
            val = exp.eval(evaltype)
            fracval = exp.eval(Fraction)
            if evaltype(answer) != val and Fraction(answer) == fracval:
                print('{} = {} ({})'.format(exp, answer, repr(val)))

if __name__ == '__main__':
    types = {
        'int': int,
        'float': float,
    }
    if len(sys.argv) == 2 and sys.argv[1] in types:
        check(terms, types[sys.argv[1]])
