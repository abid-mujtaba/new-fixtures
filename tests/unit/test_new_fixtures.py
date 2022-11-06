"""Test the new fixtures."""

import pytest

from .utils import fixture_a, TypeA
from .utils import fixture_b, TypeB1, TypeB2, TypeB3
from .utils import fixture_c, TypeC
from .utils import fixture_d, TypeD1, TypeD2
from .utils import fixture_e, TypeE
from .utils import fixture_f, TypeF1, TypeF2


@fixture_a()
def test_a(val_a: TypeA) -> None:
    """Test fixture_a in isolation."""
    assert val_a == "Value A"


@fixture_b(TypeB1(42), TypeB2(3.14))
def test_b(val_b: TypeB3) -> None:
    """Test parametrized fixture_b in isolation."""
    assert val_b == "Injected into fixture_b 42 and 3.14"


@fixture_c()  # pylint: disable=E1120
def test_c(val_c: TypeC) -> None:
    """Test fixture_c which receives values from fixture_b."""
    assert val_c == "Injected into fixture_c: Injected into fixture_b 13 and 1.44"


@fixture_d(TypeD1(True))  # pylint: disable=E1120
def test_d(val_d: TypeD2) -> None:
    """Test fixture_d which receives values from both fixture_b and the test site."""
    assert (
        val_d == "Injected into fixture_d from both b: "
        "Injected into fixture_b 123 and 1.23 and test site: True"
    )


@fixture_b(TypeB1(88), TypeB2(12.3))
@fixture_a()
def test_a_and_b(val_a: TypeA, val_b: TypeB3) -> None:
    """Test application of two fixtures to one test."""
    assert val_a == "Value A"
    assert val_b == "Injected into fixture_b 88 and 12.3"


@fixture_e()
def test_e(val_e: TypeE) -> None:
    """Test mutation of injected state by fixture_e."""
    assert val_e == 1


@pytest.mark.skip
@fixture_f(TypeF1(42))  # pylint: disable=E1120
@fixture_e()
def test_fixture_f(val_e: TypeE, val_f: TypeF2) -> None:
    """Test fixture_f and double injecion of fixture_e."""
    assert val_e == 1
    assert val_f == (
        "Injected into fixture_f values from fixture_e 1 and from test site 42"
    )


# @fixture_b(TypeB("Value B"), inject=False)
# def test_b_no_injection() -> None:
#     """The value yielded by fixture_b is NOT injected into the test."""
