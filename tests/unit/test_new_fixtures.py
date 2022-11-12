"""Test the new fixtures."""

from .utils import fixture_a, Ao
from .utils import fixture_b, Bi1, Bi2, Bo
from .utils import fixture_c, Co
from .utils import fixture_d, Di, Do
from .utils import fixture_e, Eo
from .utils import fixture_f, Fi, Fo
from .utils import fixture_g, Gi, Go


@fixture_a
def test_a(a: Ao) -> None:
    """Test fixture_a in isolation."""
    assert a == "a"


def test_a_as_contextmanager() -> None:
    """Test fixture_a as a context_manager rather than as a decorator."""
    with fixture_a as a:  # pylint: disable=E1129
        assert a == "a"


@fixture_b.set(Bi1(42), Bi2(3.14))
def test_b(b: Bo) -> None:
    """Test parametrized fixture_b in isolation."""
    assert b == {"b1": 42, "b2": 3.14}


@fixture_b.set(Bi1(88), Bi2(12.3))
@fixture_a
def test_a_and_b(a: Ao, b: Bo) -> None:
    """Test application of two fixtures to one test."""
    print("Entering test a_and_b")

    assert a == "a"
    assert b == {"b1": 88, "b2": 12.3}

    print("Leaving test a_and_b")


@fixture_c
def test_c(c: Co) -> None:
    """Test fixture_c which receives values from fixture_b."""
    assert c == {"c": {"b1": 13, "b2": 1.44}}


@fixture_d.set(Di(True))
def test_d(d: Do) -> None:
    """Test fixture_d which receives values from both fixture_b and the test site."""
    assert d == {"b": {"b1": 123, "b2": 1.23}, "d": True}


@fixture_e
def test_e(e: Eo) -> None:
    """Test mutation of injected state by fixture_e."""
    assert e == 1


@fixture_f.set(Fi(42))
@fixture_e
def test_f(e: Eo, f: Fo) -> None:
    """Test fixture_f and double injecion of fixture_e."""
    print("Entering test f")

    assert e == 1
    assert f == {"e": 1, "f": 42}

    print("Leaving test f")


# NOTE: Since fixture_g requires injection from fixture_b AND we are setting the
#       state for fixture_b at the test site the fixture_b decorator here MUST
#       wrap the fixture_b decorator here.
#       Reversing the order will result in an error.
@fixture_b.set(Bi1(56), Bi2(9.7))
@fixture_g.set(Gi(41))
def test_g(g: Go, b: Bo) -> None:
    """Inject args into fixture from test site and trickle down to pulled in fixture."""
    assert b == {"b1": 56, "b2": 9.7}
    assert g == {"b": b, "g": 41}


# # @fixture_b(TypeB("Value B"), inject=False)
# # def test_b_no_injection() -> None:
# #     """The value yielded by fixture_b is NOT injected into the test."""
