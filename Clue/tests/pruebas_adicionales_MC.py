from src.logic_core import Atom, And, Or, Not, Implies
from src.model_checking import check_satisfiable, truth_table, check_entailment, check_valid

print(check_satisfiable(And(Atom("p"), Not(Atom("p")))))

print(check_satisfiable(Or(Atom("p"), Atom("q"))))

print(check_valid(Or(Atom("p"), Not(Atom("p")))))

print(check_valid(Atom("p")))

kb = [Implies(Atom("p"), Atom("q")), Atom("p")]
print(check_entailment(kb, Atom("q")))

kb = [Or(Atom("a_culpable"), Atom("b_culpable"))]
print(check_entailment(kb, Atom("a_culpable")))

table = truth_table(Implies(Atom("p"), Atom("q")))
for model, result in table:
    print(model, "=>", result)