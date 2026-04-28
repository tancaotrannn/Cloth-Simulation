import pytest
from cloth import Cloth

def test_shapes():
    c = Cloth(8,6)
    assert c.pos.shape == (6,8,3)
    with pytest.raises(NotImplementedError):
        c.step(0.01)