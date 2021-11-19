class Coordinador:
    def __init__(self, agentes):
        self.agentes = agentes
        self.roles = [agente.rol for agente in agentes]


    def distribuir_turno_equitativamente(self):
        self.turnos = [True for _ in self.agentes]

    def distribuir_turno_a_roles(self, roles):
        self.turnos = [True if rol in roles else None for rol in self.roles ]

    def comenzar(self):
        for agente in self.agentes:
            if agente.turno:
                agente.accionar()




