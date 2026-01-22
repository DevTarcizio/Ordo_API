from enum import Enum

class TaskState(Enum):
    todo = 'todo'
    doing = 'doing'
    done = 'done'


class UserRoles(Enum):
    master = 'master'
    player = 'player'


class Origins(Enum):
    academico = 'academico'
    agente_de_saude = 'agente_de_saude'
    amnesico = 'amnesico'

class Classes(Enum):
    mundano = 'mundano'
    combatente = 'combatente'
    especialista = 'especialista'
    ocultista = 'ocultista'

class Trails(Enum):
    none = 'none'
    aniquilador = 'aniquilador'
    comandante_de_campo = 'comandante_de_campo'
    guerreiro = 'guerreiro'
    operacoes_especiais = 'operacoes_especiais'
    tropa_de_choque = 'tropa_de_choque'
    atirador_de_elite = 'atirador_de_elite'
    infiltrador = 'infiltrador'

class Ranks(Enum):
    none = 'none'
    recruta = 'recruta'
    operador = 'operador'
    agente_especial = 'agente_especial'
    oficial_de_operacoes = 'oficial_de_operacoes'
    agente_de_elite = 'agente_de_elite'