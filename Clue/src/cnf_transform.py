"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from src.logic_core import And, Atom, Formula, Not, Or, Iff, Implies


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    """
    Elimina bicondicionales recursivamente.

    Transformacion:
        Iff(a, b) -> And(Implies(a, b), Implies(b, a))

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_iff(Iff(Atom('p'), Atom('q')))
        And(Implies(Atom('p'), Atom('q')), Implies(Atom('q'), Atom('p')))

    Hint: Usa pattern matching sobre el tipo de la formula.
          Para cada tipo, aplica eliminate_iff recursivamente a los operandos,
          y solo transforma cuando encuentras un Iff.
    """
    # === YOUR CODE HERE ===
    # Átomo
    if isinstance(formula, Atom):
        return formula
    # NOT
    if isinstance(formula, Not):
        return Not(eliminate_iff(formula.operand))
    # COR
    if isinstance(formula, And):
        nuevos = [eliminate_iff(c) for c in formula.conjuncts]
        return And(*nuevos)
    # AND
    if isinstance(formula, Or):
        nuevos = [eliminate_iff(d) for d in formula.disjuncts]
        return Or(*nuevos)
    # Implicación ----->
    if isinstance(formula, Implies):
        return Implies(eliminate_iff(formula.antecedent),
                       eliminate_iff(formula.consequent))
    # <--->
    if isinstance(formula, Iff):
        a = eliminate_iff(formula.left)
        b = eliminate_iff(formula.right)
        return And(Implies(a, b), Implies(b, a))
    # Cualquier otro (no debería ocurrir)
    return formula
    # === END YOUR CODE ===


def eliminate_implication(formula: Formula) -> Formula:
    """
    Elimina implicaciones recursivamente.

    Transformacion:
        Implies(a, b) -> Or(Not(a), b)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_implication(Implies(Atom('p'), Atom('q')))
        Or(Not(Atom('p')), Atom('q'))

    Hint: Similar a eliminate_iff. Recorre recursivamente y transforma
          solo los nodos Implies.
    """
    # === YOUR CODE HERE ===

    # Caso ATOOMP

    if isinstance(formula, Atom):
        return formula
    
    if isinstance(formula, Not):
        return Not(eliminate_implication(formula.operand))
    
    if isinstance(formula, And):
        n = [eliminate_implication(c) for c in formula.conjuncts]
        return And(*n)
    
    if isinstance(formula, Or):
        n = [eliminate_implication(d) for d in formula.disjuncts]
        return Or(*n)
    
    if isinstance(formula, Implies):
        a = eliminate_implication(formula.antecedent)
        b = eliminate_implication(formula.consequent)
        return Or(Not(a), b)
    
    if isinstance(formula, Iff):
 
        return Iff(eliminate_implication(formula.left), eliminate_implication(formula.right))
    
    return formula
    # === END YOUR CODE ===


def push_negation_inward(formula: Formula) -> Formula:
    """
    Aplica las leyes de De Morgan y mueve negaciones hacia los atomos.

    Transformaciones:
        Not(And(a, b, ...)) -> Or(Not(a), Not(b), ...)   (De Morgan)
        Not(Or(a, b, ...))  -> And(Not(a), Not(b), ...)   (De Morgan)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> push_negation_inward(Not(And(Atom('p'), Atom('q'))))
        Or(Not(Atom('p')), Not(Atom('q')))
        >>> push_negation_inward(Not(Or(Atom('p'), Atom('q'))))
        And(Not(Atom('p')), Not(Atom('q')))

    Hint: Cuando encuentres un Not, revisa que hay adentro:
          - Si es Not(And(...)): aplica De Morgan para convertir en Or de negaciones.
          - Si es Not(Or(...)): aplica De Morgan para convertir en And de negaciones.
          - Si es Not(Atom): dejar como esta.
          Para And y Or sin negacion encima, simplemente recursa sobre los hijos.

    Nota: Esta funcion se llama DESPUES de eliminar Iff e Implies,
          asi que no necesitas manejar esos tipos.
    """
    # === YOUR CODE HERE ===

    # Átomo
    if isinstance(formula, Atom):
        return formula

    # ELIMINAR NEGACIONES
    if isinstance(formula, Not):
        inner = formula.operand

        # CASO DONDE HAY NEGACION AFUERA DE UNA OPERACION CON UN AND - DISTRIBUIR 
        if isinstance(inner, And):
            negados = [push_negation_inward(Not(c)) for c in inner.conjuncts]
            return Or(*negados)

        # CASO DONDE HAY NEGACION AFUERA DE UNA OPERACION CON UN AND - DISTRIBUIR 
        if isinstance(inner, Or):
            neg = [push_negation_inward(Not(d)) for d in inner.disjuncts]
            return And(*neg)
        if isinstance(inner, Or):
            nots = [push_negation_inward(Not(d)) for d in inner.disjuncts]
            return And(*nots)

        # ELIMINAR DOBLE NEGACION
        if isinstance(inner, Not):
            return push_negation_inward(inner.operand)

        if isinstance(inner, Atom):
            return formula

        # VERIFICACION DE 
        return Not(push_negation_inward(inner))

    # AND SIN NOT
    if isinstance(formula, And):
        nuevos = [push_negation_inward(c) for c in formula.conjuncts]
        return And(*nuevos)

    # OR SIN NOT
    if isinstance(formula, Or):
        nuevos = [push_negation_inward(d) for d in formula.disjuncts]
        return Or(*nuevos)

    # --->
    if isinstance(formula, Implies):
        return Implies(push_negation_inward(formula.antecedent),
                       push_negation_inward(formula.consequent))

    # <-->
    if isinstance(formula, Iff):
        return Iff(push_negation_inward(formula.left),
                   push_negation_inward(formula.right))

    return formula
    # === END YOUR CODE ===


def distribute_or_over_and(formula: Formula) -> Formula:
    """
    Distribuye Or sobre And para obtener CNF.

    Transformacion:
        Or(A, And(B, C)) -> And(Or(A, B), Or(A, C))

    Debe aplicarse recursivamente hasta que no queden Or que contengan And.

    Ejemplo:
        >>> distribute_or_over_and(Or(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Atom('p'), Atom('q')), Or(Atom('p'), Atom('r')))

    Hint: Para un nodo Or, primero distribuye recursivamente en los hijos.
          Luego busca si algun hijo es un And. Si lo encuentras, aplica la
          distribucion y recursa sobre el resultado (podria haber mas).
          Para And, simplemente recursa sobre cada conjuncion.
          Atomos y Not se retornan sin cambio.

    Nota: Esta funcion se llama DESPUES de mover negaciones hacia adentro,
          asi que solo veras Atom, Not(Atom), And y Or.
    """
    # === YOUR CODE HERE ===
    # ÁtomoIgual
    if isinstance(formula, Atom):
        return formula

    
    if isinstance(formula, Not):
        return Not(distribute_or_over_and(formula.operand))

    # AND se distribuye en cada parte
    if isinstance(formula, And):
        n_partes = []
        for c in formula.conjuncts:
            n_partes.append(distribute_or_over_and(c))
        return And(*n_partes)

    # Disyunción (Or) → caso principal
    if isinstance(formula, Or):
        # Primero distribuir en cada OR y por eso se va creando un alista de ORS
        l_or = []
        for d in formula.disjuncts:
            l_or.append(distribute_or_over_and(d))

        # Buscar si algún disyunto es un And
        for i in range(len(l_or)):
            disyunto_actual = l_or[i]
            if isinstance(disyunto_actual, And):
                otros = l_or[:i] + l_or[i+1:]

                # Lista para guardar los nuevos Or que se crearán
                n_Ors = []

                # Recorrer cada elemento dentro del And
                for a_and in disyunto_actual.conjuncts:
                    # Crear un nuevo Or EL CUAL ES EL ELEMNTO DE AND ACTUAL + LOS OTROS DISYUNTOS
                    argumentos = [a_and] + otros
                    nuevo_or = Or(*argumentos)
                    # Distribuir recursivamente sobre ese nuevo Or (por si aparecen más And)
                    n_Ors.append(distribute_or_over_and(nuevo_or))

                # El resultado es un And que contiene todos los nuevos Ors
                resultado = And(*n_Ors)
                
                # Volver a distribuir sobre el resultado por si faltan más distribuciones
                return distribute_or_over_and(resultado)

        # Si no se encontró ningún And sedevuelve el Or ya distribuido
        return Or(*l_or)
    
    if isinstance(formula, Implies):
        return Implies(distribute_or_over_and(formula.antecedent), distribute_or_over_and(formula.consequent))
    
    if isinstance(formula, Iff):
        return Iff(distribute_or_over_and(formula.left), distribute_or_over_and(formula.right))

    return formula
    # === END YOUR CODE ===


def flatten(formula: Formula) -> Formula:
    """
    Aplana conjunciones y disyunciones anidadas.

    Transformaciones:
        And(And(a, b), c) -> And(a, b, c)
        Or(Or(a, b), c)   -> Or(a, b, c)

    Debe aplicarse recursivamente.

    Ejemplo:
        >>> flatten(And(And(Atom('a'), Atom('b')), Atom('c')))
        And(Atom('a'), Atom('b'), Atom('c'))
        >>> flatten(Or(Or(Atom('a'), Atom('b')), Atom('c')))
        Or(Atom('a'), Atom('b'), Atom('c'))

    Hint: Para un And, recorre cada hijo. Si un hijo tambien es And,
          agrega sus conjuncts directamente en vez de agregar el And.
          Igual para Or con sus disjuncts.
          Si al final solo queda 1 elemento, retornalo directamente.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula
    
    if isinstance(formula, Not):
        #mirar que si dentro de la negacion no haya otra formula que se pueda aplanar
        return Not(flatten(formula.operand))
    
    if isinstance(formula, And):
        nuevos = [] #Lista para poner los nuevo aplanados
        
            #Si esa parte ya es un And entoncesse añaden a la lista las subconjunciones.
        for parte in formula.conjuncts:
            aplan = flatten(parte)
            
            if isinstance(aplan, And):
                nuevos.extend(aplan.conjuncts)
            else:
                nuevos.append(aplan)
        
        
        #Se verifca que si la longitud es 1 se devuele solamente ese elemnt para no poner AND      
        if len(nuevos) == 1:
            return nuevos[0]
        
        return And(*nuevos)
    
    if isinstance(formula, Or): #repeticion pero con OR
        
        nuevos = []
        
        for d in formula.disjuncts:
            aplanar  = flatten(d)
            
            if isinstance(aplanar, Or):
                nuevos.extend(aplanar.disjuncts)
            else:
                nuevos.append(aplanar)
                
        if len(nuevos) == 1:
            return nuevos[0]
        
        return Or(*nuevos)
    
    #POR SI ACASO VOLVEMOS Y VERIFICAMOS IMPLIES Y BICONDICIONALES
    if isinstance(formula, Implies):
        return Implies(flatten(formula.antecedent), flatten(formula.consequent))
    
    if isinstance(formula, Iff):
        return Iff(flatten(formula.left), flatten(formula.right))
    return formula
    # === END YOUR CODE === 


# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula
