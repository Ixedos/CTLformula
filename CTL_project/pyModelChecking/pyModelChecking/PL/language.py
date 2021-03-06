
import sys

from .. import language as BooleanLogics

from ..language import LNot
from ..language import get_alphabet


class Formula(BooleanLogics.Formula):
 

    __desc__ = 'propositional formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, sys.modules[self.__module__].Formula)

    def wrap_subformulas(self, subformulas, FormulaClass):


        def err_msg(phi):
            return ('expected a {}, '.format(FormulaClass.__desc__) +
                    'got the {} {}'.format(phi.__desc__, phi))

        Lang = sys.modules[self.__module__]

        self._subformula = []
        self.height = 0

        for phi in subformulas:
            if isinstance(phi, bool):
                self._subformula.append(Lang.Bool(phi))
            else:
                if isinstance(phi, str):
                    self._subformula.append(Lang.AtomicProposition(phi))
                else:
                    if not isinstance(phi, FormulaClass):
                        if (isinstance(phi, Lang.Formula) or
                                not isinstance(phi, Formula)):

                            raise TypeError(err_msg(phi))

                        phi = phi.cast_to(Lang)

                        if not isinstance(phi, FormulaClass):
                            raise TypeError(err_msg(phi))

                    self._subformula.append(phi)
                    self.height = max(self.height, phi.height+1)

    def cast_to(self, Lang):

        if isinstance(self, Bool):
            return Lang.Bool(bool(self._value))
        if isinstance(self, AtomicProposition):
            return Lang.AtomicProposition(str(self.name))

        symbol_name = self.__class__.__name__
        if symbol_name not in Lang.alphabet:
            raise TypeError('{} is not in the alphabet '.format(symbol_name) +
                            'of {}, thus {} is '.format(Lang.__name__, self) +
                            'not a {} formula'.format(Lang.__name__))

        subformulas = []
        for subformula in self.subformulas():
            subformulas.append(Formula.cast_to(subformula, Lang))

        return Lang.alphabet[symbol_name](*subformulas)


class AtomicProposition(Formula, BooleanLogics.AlphabeticSymbol):
    '''
    The class representing atomic propositionic propositions.

    '''
    def __init__(self, name):
        ''' Initialize a atomic proposition.

        This method builds a atomic propositionic proposition.

        :param name: the name of the atomic proposition.
        :type name: str
        '''
        if not isinstance(name, str):
            raise TypeError('name = \'{}\' must be '.format(name) +
                            'a {} object, but it is '.format(str) +
                            '{} object'.format(name.__class__))
        self.name = str(name)
        self.height = 0

    def clone(self):
        ''' Clones an atomic proposition

        :returns: a clone of the current atomic proposition
        :rtype: PL.AtomicProposition
        '''
        return self.__class__(str(self.name))

    def subformula(self, i):
        ''' Returns the :math:`i`-th subformula.

        :param i: the index of the subformula to be returned
        :type i: Integer
        :raise TypeError: atomic propositions have not subformulas
        '''
        raise TypeError('AtomicPropositions have not subformulas.')

    def subformulas(self):
        ''' Returns the list of all the subformulas.

        :returns: returns the empty list of the subformulas of the current
            formula
        :rtype: list
        '''
        return []

    def __str__(self):
        return '{}'.format(self.name)


class Bool(BooleanLogics.Bool, AtomicProposition):
    '''
    The class of Boolean atomic propositions.

    '''
    pass


class LogicOperator(Formula, BooleanLogics.LogicOperator):
    '''
    A class to represent logic operator such as :math:`\land` or :math:`\lor`.

    '''
    pass


class Not(LogicOperator, BooleanLogics.Not):
    '''
    Represents logic negation.

    '''
    pass


class Or(LogicOperator,  BooleanLogics.Or):
    '''
    Represents logic non-exclusive disjunction.

    '''
    pass


class And(LogicOperator, BooleanLogics.And):
    '''
    Represents logic conjunction.

    '''
    pass


class Imply(LogicOperator, BooleanLogics.Imply):
    '''
    Represents logic implication.

    '''
    pass


def get_symbols(alphabet):
    symbols = list()

    for name, c in alphabet.items():
        if name == 'Bool':
            symbols.extend(Bool.symbols.values())
        else:
            if name != 'AtomicProposition':
                symbols.extend(c.symbols)

    return symbols


alphabet = get_alphabet(__name__)
symbols = get_symbols(alphabet)
