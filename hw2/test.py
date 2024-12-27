from e2448835_hw2 import HornClause, Rule, mgu, replace_hc, forward_chaining, backward_chaining


kb0 = ["Partner(x,y) <- Loves(x,y), Loves(y,x)", "Happy(y) <- Gift(x,z), Partner(x,y)",
"Loves(Feyza,Can)",
"Loves(Can,Feyza)",
"Gift(Eren,z)"]
q0 = "Happy(Feyza)"


kb1 = ["Q(x) <- P(x)", "P(x) <- L(x), M(x)", "M(x) <- B(x), L(x)",
"L(x) <- A(x), P(x)", "L(x) <- A(x), B(x)", "A(John)", "B(John)"]
q1 = "Q(John)"

kb2 = ["Q(x) <- P(x)", "P(x) <- L(x), M(x)", "M(x) <- B(x), L(x)",
"L(x) <- A(x), P(x)", "L(x) <- A(x), B(x)", "A(John)", "B(John)"]
q2 = "Q(John)"

# parse(kb)


# mgu = mgu(rule, hc)
# print(mgu)
# print(replace_hc(hc, mgu))

# print(forward_chaining(kb, q))
# print(forward_chaining(kb1, q1))
# print(forward_chaining(kb2, q2))

kb3 = ["Q(x) <- P(x)", "P(x) <- L(x), M(x)", "M(x) <- B(x), L(x)",
"L(x) <- A(x), P(x)", "L(x) <- A(x), B(x)", "A(John)"]
q3 = "Q(John)"


kb4 = ["Q(x) <- P(x)", "P(x) <- L(x), M(x)", "M(x) <- B(x), L(x)",
"L(x) <- A(x), P(x)", "L(x) <- A(x), B(x)", "A(John)"]
q4 = "Q(John)"

kb5 = ["Criminal(x) <- American(x), Weapon(y), Sells(x,y,z), Hostile(z)",
"Weapon(x) <- Missile(x)",
"Missile(M)",
"Owns(Nono,M)",
"Sells(West,x,Nono) <- Owns(Nono,x), Missile(x)",
"Hostile(x) <- Enemy(x,America)",
"American(West)",
"Enemy(Nono,America)"]
q5 = "Criminal(West)"



kb6 = [ "B(x) <- A(x)",
       "C(x) <- A(x)",
       "D(x) <- A(x)",
       "E(x) <- B(x), C(x), D(x)",
       "F(x) <- E(x), D(x)",
       "G(x) <- F(x), E(x)",
         "A(John)"]
q6 = "G(John)"
# print(forward_chaining(kb0, q0))
# print(forward_chaining(kb1, q1))
# print(backward_chaining(kb2, q2))
# print(forward_chaining(kb3, q3))
# print(backward_chaining(kb4, q4))
# print(backward_chaining(kb5, q5))
print(backward_chaining(kb6, q6))
# print(mgu(Rule("Missile(y)"), Rule("Missile(M)")))


rule1 = Rule("Loves(x,y)")
rule2 = Rule("Loves(y,z)")
#print(mgu(rule2, rule1))