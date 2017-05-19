import pytest

from modules.executable import MethodCall, MethodConfig, Replacement, Pipeline
import numpy as np


# static function call
def test_execute():
    ex = MethodCall('math', 'ceil', [2.3])
    assert ex.execute() == 3


# member function call
def test_execute2():
    a = np.array([1, 2, 3, 4])
    ex = MethodCall(a, 'reshape', [2, 2], False)
    b = ex.execute()
    assert np.array_equal(b, a.reshape(2, 2))


# modify the value
def test_execute3():
    a = np.array([1, 3, 2, 4])
    ex = MethodCall(a, 'sort', [], False)
    ex.execute()
    assert np.array_equal(a, [1, 2, 3, 4])


def test_method_config():
    ins = MethodConfig('math', 'ceil', True, [None], [True])
    assert ins.target == 'math'
    assert ins.method == 'ceil'
    assert ins.need_import


def test_replacement():
    with pytest.raises(ValueError) as error:
        Replacement('ab', 3, 3)
        assert error == 'Category ab not recognized.'


def test_replacement2():
    ins = Replacement('output', 3, 3)
    assert ins.category == 'output'


def test_pipeline():
    a = np.array([1, 2])
    b = np.array([3, 4])
    c = np.array([5, 6])
    d = np.array([3, 4])
    config1 = MethodConfig('numpy', 'multiply', True, [a, 2])
    config2 = MethodConfig('numpy', 'multiply', True, [b, 3])
    replacement1 = Replacement('output', 0)
    config3 = MethodConfig('numpy', 'multiply', True, [replacement1, 2], [True, None])
    config4 = MethodConfig('numpy', 'add', True, [c, d])
    replacement2 = Replacement('output', 2)
    replacement3 = Replacement('output', 3)
    config5 = MethodConfig('numpy', 'add', True, [replacement2, replacement3], [True, True])

    assert np.array_equal(Pipeline([config1, config2, config3, config4, config5]).run(), np.array([12, 18]))
