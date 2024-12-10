import re
import copy
FAILURE_MSG = "Query cannot be proven."
class HornClause:
    """A class for Horn Clauses e.g. P(x) <- L(x), M(x)"""
    # body : list[Rule]
    # head : Rule
    def __init__(self, head, body=None):
        self.head = Rule(head)
        if body:
            self.body = [Rule(item) for item in body]
        else:
            self.body = None

    def __str__(self):
        if self.body:
            return f"{str(self.head)} <- {', '.join([str(item) for item in self.body])}"
        return str(self.head)   
    def remove(self, rule):
        """Removes the rule from the body"""
        if self.body:
            for item in self.body:
                if item == rule:
                    self.body.remove(item)
                    return self
    def replace(self, new_hc):
        """Replaces the head and body of the Horn Clause with the new Horn Clause"""
        self.head = new_hc.head
        self.body = new_hc.body

class Rule:
    """A class for rules e.g. Loves(x,y)"""
    # predicate : str
    # args : List[str]
    def __init__(self, input_string):
        match = re.match(r'(\w+)\(([^)]*)\)', input_string)
        if match:
            predicate = match.group(1)  # The part before the parenthesis
            args = match.group(2).split(',') if match.group(2) else []  # Split arguments by commas
            self.predicate = predicate
            self.args = args
        else:
            raise ValueError("Input string does not match the expected format")       
        for arg in args:
            if arg[0].islower():
                return
    def __str__(self):
        return f"{self.predicate}({','.join(self.args)})"  
    def __eq__(self, other):
        return self.predicate == other.predicate and self.args == other.args
    def isfact(self):
        """Checks if the rule is a fact
        e.g. Loves("Feyza","Can") is a fact while Loves(x,y) is not"""
        for arg in self.args:
            if arg[0].islower():
                return False
        return True
    def replace(self, new_rule):
        """Replaces the predicate and arguments of the rule with the new rule"""
        self.predicate = new_rule.predicate
        self.args = new_rule.args  
def parse(kb):
    """For parsing the input knowledge base into Horn Clauses"""
    horn_clauses = []
    for clause in kb:
        if '<-' in clause:
            head, body = clause.split('<-')
            body = re.findall(r'\w+\([^\)]*\)', body)
            horn_clauses.append(HornClause(head, body))
        else:
            horn_clauses.append(HornClause(clause))
    return horn_clauses

def mgu(rule: Rule, hc):
    """Most General Unifier"""
    # rule1 = Rule("Loves(x,x)") clause
#     rule2 = Rule("Loves(Feyza,Can)") hc
    if isinstance(hc, Rule):
        predicate = rule.predicate
        args = rule.args
        if len(hc.args) != len(args) or hc.predicate != predicate:
            return None
        mgu_ = {}
        for i,arg in enumerate(args):
            if hc.args[i] == arg:
                continue
            if hc.args[i][0].islower():
                # if there is already a value assigned to the variable,
                # we should check if the values are the same
                if (hc.args[i] in mgu_ and mgu_[hc.args[i]] != arg) or (arg in mgu_ and mgu_[arg] != hc.args[i]):
                    return None
                mgu_[hc.args[i]] = arg
                continue
            if arg[0].islower():
                if (hc.args[i] in mgu_ and mgu_[hc.args[i]] != arg) or (arg in mgu_ and mgu_[arg] != hc.args[i]):
                    return None
                mgu_[arg] = hc.args[i]
                continue
            return None
        return mgu_ if mgu_ else None
    body = hc.body
    predicate = rule.predicate
    args = rule.args
    for item in body:
        if item.predicate != predicate or len(item.args) != len(args):
            continue
        mgu_ = {}
        for i,arg in enumerate(args):
            if item.args[i] == arg:
                continue
            if item.args[i][0].islower():
                if (item.args[i] in mgu_ and mgu_[item.args[i]] != arg) or (arg in mgu_ and mgu_[arg] != item.args[i]):
                    return None
                mgu_[item.args[i]] = arg
                continue
            if arg[0].islower():
                if (item.args[i] in mgu_ and mgu_[item.args[i]] != arg) or (arg in mgu_ and mgu_[arg] != item.args[i]):
                    return None
                mgu_[arg] = item.args[i]
                continue
            return None
        return mgu_ if mgu_ else None
    return mgu(rule, hc.head)

def replace(clause: Rule, mgu_):
    """returns a new rule with the values replaced according to the mgu"""
    new_rule = copy.deepcopy(clause)
    new_args = new_rule.args
    args = clause.args
    for (key, value) in mgu_.items():
        for i in range(len(clause.args)):
            arg = args[i]
            if arg == key:
                new_args[i] = value
    return new_rule

def replace_hc(hc: HornClause, mgu_):
    """returns a new Horn Clause with the values replaced according to the mgu"""
    new_hc = copy.deepcopy(hc)
    changed = True
    while changed:
        changed = False
        for body_item in new_hc.body:
            rule = body_item
            new_rule = replace(rule, mgu_)
            if new_rule != rule:
                body_item.replace(new_rule)
                changed = True
        new_hc.head = replace(new_hc.head, mgu_)
    return new_hc

def contains(body: list[HornClause] | list[Rule], clause: HornClause | Rule) -> bool:
    """Checks if the body contains the clause"""
    if isinstance(clause, HornClause):
        for item in body:
            if item.head == clause.head and item.body == clause.body:
                return True
        return False
    if isinstance(clause, Rule):
        for item in body:
            if item == clause:
                return True
        return False
    raise TypeError("Second argument should be either HornClause or Rule")

def forward_chaining(kb, q):
    #initialization
    q_rule = Rule(q)
    horn_clauses = parse(kb)
    is_kb_changed = True
    agenda = []
    inferred = []
    count = {}
    for hc in horn_clauses:
        if hc.body:
            count[str(hc)] = len(hc.body)
        else:
            agenda.append(hc.head)
            count[str(hc)] = 0

    while(is_kb_changed): # if the knowledge base is not changed in the last iteration, we can stop
        is_kb_changed = False
        for agenda_item in agenda:
            for hc in horn_clauses:
                body = hc.body
                if count[str(hc)] == 0:
                    continue
                for rule in body:
                    if rule.predicate != agenda_item.predicate:
                        continue
                    if rule.args == agenda_item.args:
                        count[str(hc)] -= 1
                        if count[str(hc)] == 0:
                            if (hc.head.isfact() and not contains(inferred, hc.head)):
                                #append to inferred and agenda if the inferred item is a fact (like loves("Feyza,"Can") rather than loves("Feyza","x"))
                                agenda.append(hc.head)
                                inferred.append(hc.head)
                                if (hc.head == q_rule): #target is reached
                                    return [str(item) for item in inferred]
                        continue
                    # if we encounter a rule that has the same predicate but different arguments, we try to unify them,
                    # if unification is successful, we generate a new horn clause and add it to the knowledge base
                    #if not, we simply continue to the next rule
                    mgu_ = mgu(agenda_item, hc)
                    if mgu_:
                        new_hc = replace_hc(hc, mgu_).remove(agenda_item) # e.g. if hc is P(x) <- L(x), M(x) and agenda_item is L("Onat"), then new_hc will be P("Onat") <- M("Onat")
                        if (not contains(horn_clauses,new_hc)): # if the new horn clause is not already in the knowledge base
                            if (not new_hc.body and new_hc.head.isfact() and not contains(inferred, new_hc.head)):
                                agenda.append(new_hc.head)
                                inferred.append(new_hc.head)
                                if (new_hc.head == q_rule):
                                    return [str(item) for item in inferred]
                            horn_clauses.append(new_hc)
                            count[str(new_hc)] = len(new_hc.body)
                            is_kb_changed = True
    return FAILURE_MSG # the target is not reached


def stack_check(stack, hc):
    """Checks if the stack contains the predicate of the Horn Clause. Used for backward chaining"""
    for stack_item in stack:
        for item in hc.body:
            if stack_item.predicate == item.predicate:
                return False
    return True
def backward_chaining_helper(horn_clauses, q, inferred, stack, prev_hc=None) -> tuple[list[HornClause] |str , dict[str, str]]:
    """Helper function for backward chaining. Returns triggered Horn Clauses and the most general unifier"""
    result = []
    for inferred_item in inferred: # check if the query is already inferred
        if inferred_item == q:
            return [], None
        if inferred_item.predicate == q.predicate:
            mgu_ = mgu(q, inferred_item)
            if mgu_:
                new_hc = replace_hc(prev_hc, mgu_)
                prev_hc.replace(new_hc)
                if new_hc.head.isfact():
                    return [str(new_hc)], mgu_
                return [], mgu_           
    for stack_item in stack:
        if stack_item.predicate == q.predicate:
            return FAILURE_MSG, None
    stack.append(q)
    for hc in horn_clauses:
        flag = False # flag for breaking the loop
        if hc.head == q: # if the head of the Horn Clause is the query
            for hc_item in hc.body: #iterate over the body of the Horn Clause that contains the query
                tmp_result_tuple = backward_chaining_helper(horn_clauses, hc_item, inferred, stack, hc)
                tmp_result, mgu_ = tmp_result_tuple[0] , tmp_result_tuple[1]
                if tmp_result == FAILURE_MSG: # it means one of the body items cannot be proven, so we should continue to the next Horn Clause
                    flag = True
                    break
                result += [str(item) for item in tmp_result if item not in result]
                if mgu_: # if there is a most general unifier, we should replace the values in the Horn Clause
                    new_hc = replace_hc(hc, mgu_)
                    hc.replace(new_hc)
            if flag:
                continue
            if q.isfact(): # if the query is a fact, we should add it to the inferred list since it is proven
                inferred.append(q)
            stack.remove(q)
            return result, None
        if hc.head.predicate == q.predicate: # if the head of the Horn Clause has the same predicate with the query but different arguments
            mgu_ = mgu(q, hc)
            if mgu_: # An mgu is found. We should replace the values in the Horn Clause and add it to the inferred list
                new_hc = replace_hc(hc, mgu_)
                new_q = replace(q, mgu_)
                q.replace(new_q)
                horn_clauses.append(new_hc)
                if new_hc.head.isfact() and not contains(inferred, new_hc.head) and stack_check(stack, new_hc):
                    # if the head of the Horn Clause is a fact and not already inferred and not in the stack
                    result.append(str(new_hc))
    return FAILURE_MSG, None

    

def backward_chaining(kb, q):
    horn_clauses = parse(kb)
    tmp = []
    q = Rule(q)
    stack = [] # stack is for checking if the clause that we are trying to prove is already being processed. e.g.  P , L -> M,  M -> P. Otherwise, we could end up in an infinite loop
    inferred = []
    for hc in horn_clauses: # remove the Horn Clauses that have no body and add them to the inferred list
        if not hc.body:
            inferred.append(hc.head)
        else:
            tmp.append(hc)
    horn_clauses = tmp

    result = backward_chaining_helper(horn_clauses, q, inferred, stack)
    if result[0] == FAILURE_MSG:
        return FAILURE_MSG
    return [hc for hc in result[0]]



kb0 = ["Partner(x,y) <- Loves(x,y), Loves(y,x)", "Happy(y) <- Gift(x,z), Partner(x,y)",
"Loves(Feyza,Can)",
"Loves(Can,Feyza)",
"Gift(Can,z)"]
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

print(forward_chaining(kb0, q0))
print(forward_chaining(kb1, q1))
print(backward_chaining(kb2, q2))
print(forward_chaining(kb3, q3))
print(backward_chaining(kb4, q4))
print(backward_chaining(kb5, q5))
# print(mgu(Rule("Missile(y)"), Rule("Missile(M)")))


rule1 = Rule("Loves(x,y)")
rule2 = Rule("Loves(y,x)")
print(mgu(rule1, rule2))