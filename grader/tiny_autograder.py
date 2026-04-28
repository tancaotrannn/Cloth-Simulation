from cloth import Cloth
try:
    c = Cloth(6,4)
    c.step(0.01)
    print("P4 tiny autograder: PASS (integration exists)")
except NotImplementedError as e:
    print("P4 tiny autograder: NOT READY —", e)