from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term
"""
copa_mundo_desaparecida.py — La Desaparición de la Copa del Mundo

La Copa del Mundo desapareció de la sala de trofeos durante una ceremonia privada.
El Curador Medina tenía acceso autorizado a la sala de trofeos esa noche.
La Empresaria Valeria había intentado comprar la copa de forma ilegal días antes.
El Exjugador Rivas fue visto cerca de la vitrina principal durante el apagón.
La Periodista Salazar estaba transmitiendo en vivo desde otra zona del estadio y tiene registro público de su ubicación.
Las huellas del Curador Medina aparecen en la vitrina forzada.
La vitrina forzada es el objeto principal de la escena del crimen.
El Curador Medina no tiene coartada verificada.
La Empresaria Valeria no tiene coartada verificada.
El Exjugador Rivas tiene coartada parcial, pero no verificada por medios oficiales.
El Curador Medina acusa al Exjugador Rivas.
La Empresaria Valeria declara que el Curador Medina estuvo con ella durante el apagón.
El Exjugador Rivas acusa a la Empresaria Valeria.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro público verificable lejos de la sala de trofeos queda descartado.
Quien tenía acceso autorizado a la sala de trofeos tenía oportunidad de cometer el robo.
Quien intentó comprar la copa ilegalmente tiene motivo económico.
Quien fue visto cerca de la vitrina durante el apagón tiene presencia sospechosa.
Quien tiene huellas en el objeto principal de la escena tiene evidencia física en su contra.
Quien tiene oportunidad, evidencia física y no tiene coartada verificada es culpable.
Quien tiene motivo económico y no tiene coartada verificada es sospechoso fuerte.
Quien da coartada a un culpable está encubriendo el crimen.
Cuando un culpable acusa a otra persona, esa acusación es un desvío sospechoso.
Si todos los culpables tenían oportunidad, entonces el robo fue cometido desde dentro de la organización.
"""

def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    # Constantes del caso
    curador_medina = Term("curador_medina")
    empresaria_valeria = Term("empresaria_valeria")
    exjugador_rivas = Term("exjugador_rivas")
    periodista_salazar = Term("periodista_salazar")
    vitrina_forzada = Term("vitrina_forzada")

    # Variables
    x = Term("$X")
    y = Term("$Y")
    obj = Term("$OBJ")

    # Hechos
    kb.add_fact(Predicate("acceso_autorizado", (curador_medina,)))
    kb.add_fact(Predicate("intento_compra_ilegal", (empresaria_valeria,)))
    kb.add_fact(Predicate("visto_cerca_vitrina", (exjugador_rivas,)))
    kb.add_fact(Predicate("registro_publico_lejos", (periodista_salazar,)))
    kb.add_fact(Predicate("huellas", (curador_medina, vitrina_forzada)))
    kb.add_fact(Predicate("objeto_escena", (vitrina_forzada,)))

    kb.add_fact(Predicate("no_coartada_verificada", (curador_medina,)))
    kb.add_fact(Predicate("no_coartada_verificada", (empresaria_valeria,)))
    kb.add_fact(Predicate("no_coartada_verificada", (exjugador_rivas,)))

    kb.add_fact(Predicate("acusa", (curador_medina, exjugador_rivas)))
    kb.add_fact(Predicate("acusa", (exjugador_rivas, empresaria_valeria)))
    kb.add_fact(Predicate("da_coartada", (empresaria_valeria, curador_medina)))

    # Reglas
    kb.add_rule(Rule(
        head=Predicate("descartado", (x,)),
        body=(
            Predicate("registro_publico_lejos", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("oportunidad", (x,)),
        body=(
            Predicate("acceso_autorizado", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("motivo_economico", (x,)),
        body=(
            Predicate("intento_compra_ilegal", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("presencia_sospechosa", (x,)),
        body=(
            Predicate("visto_cerca_vitrina", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (x,)),
        body=(
            Predicate("huellas", (x, obj)),
            Predicate("objeto_escena", (obj,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("culpable", (x,)),
        body=(
            Predicate("oportunidad", (x,)),
            Predicate("evidencia_fisica", (x,)),
            Predicate("no_coartada_verificada", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("sospechoso_fuerte", (x,)),
        body=(
            Predicate("motivo_economico", (x,)),
            Predicate("no_coartada_verificada", (x,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("encubridor", (x,)),
        body=(
            Predicate("da_coartada", (x, y)),
            Predicate("culpable", (y,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("desvio_sospechoso", (x, y)),
        body=(
            Predicate("culpable", (x,)),
            Predicate("acusa", (x, y)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="copa_mundo_desaparecida",
    title="La Desaparición de la Copa del Mundo",
    suspects=(
        "curador_medina",
        "empresaria_valeria",
        "exjugador_rivas",
        "periodista_salazar",
    ),
    narrative=__doc__,
    description=(
        "La Copa del Mundo desapareció durante una ceremonia privada. "
        "El Curador Medina tenía acceso, huellas en la vitrina forzada y no tenía coartada. "
        "La Empresaria Valeria tenía motivo económico y pudo estar encubriéndolo."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La Periodista Salazar está descartada?",
            goal=Predicate("descartado", (Term("periodista_salazar"),)),
        ),
        QuerySpec(
            description="¿El Curador Medina tiene evidencia física en su contra?",
            goal=Predicate("evidencia_fisica", (Term("curador_medina"),)),
        ),
        QuerySpec(
            description="¿El Curador Medina es culpable?",
            goal=Predicate("culpable", (Term("curador_medina"),)),
        ),
        QuerySpec(
            description="¿La Empresaria Valeria es sospechosa fuerte?",
            goal=Predicate("sospechoso_fuerte", (Term("empresaria_valeria"),)),
        ),
        QuerySpec(
            description="¿La Empresaria Valeria encubre al culpable?",
            goal=Predicate("encubridor", (Term("empresaria_valeria"),)),
        ),
        QuerySpec(
            description="¿Existe algún culpable en el caso?",
            goal=ExistsGoal("$X", Predicate("culpable", (Term("$X"),))),
        ),
        QuerySpec(
            description="¿Todo culpable tenía oportunidad de cometer el robo?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("oportunidad", (Term("$X"),)),
            ),
        ),
    ),
)