from enum import Enum


class UserRoles(Enum):
    master = 'master'
    player = 'player'


class Origins(Enum):
    academico = 'academico'
    agente_de_saude = 'agente_de_saude'
    amnesico = 'amnesico'
    artista = 'artista'
    atleta = 'atleta'
    chef = 'chef'
    cientista_forense = 'cientista_forense'
    criminoso = 'criminoso'
    cultista_arrependido = 'cultista_arrependido'
    desgarrado = 'desgarrado'
    engenheiro = 'engenheiro'
    executivo = 'executivo'
    escritor = 'escritor'
    investigador = 'investigador'
    jornalista = 'jornalista'
    lutador = 'lutador'
    magnata = 'magnata'
    mercenario = 'mercenario'
    militar = 'militar'
    operario = 'operario'
    policial = 'policial'
    professor = 'professor'
    religioso = 'religioso'
    servidor_publico = 'servidor_publico'
    teorico_da_conspiracao = 'teorico_da_conspiracao'
    ti = 'ti'
    trabalhador_rural = 'trabalhador_rural'
    trambiqueiro = 'trambiqueiro'
    universitario = 'universitario'
    vitima = 'vitima'
    prodigio_paranormal = 'prodigio_paranormal'
    oficial_militar = 'oficial_militar'


class Classes(Enum):
    mundano = 'mundano'
    combatente = 'combatente'
    especialista = 'especialista'
    ocultista = 'ocultista'
    transformado = 'transformado'


class Trails(Enum):
    none = 'none'
    aniquilador = 'aniquilador'
    comandante_de_campo = 'comandante_de_campo'
    guerreiro = 'guerreiro'
    operacoes_especiais = 'operacoes_especiais'
    tropa_de_choque = 'tropa_de_choque'
    atirador_de_elite = 'atirador_de_elite'
    infiltrador = 'infiltrador'
    medico_de_campo = 'medico_de_campo'
    negociador = 'negociador'
    tecnico = 'tecnico'
    conduite = 'conduite'
    flagelador = 'flagelador'
    graduado = 'graduado'
    intuitivo = 'intuitivo'
    lamina_paranormal = 'lamina_paranormal'


class Ranks(Enum):
    none = 'none'
    recruta = 'recruta'
    operador = 'operador'
    agente_especial = 'agente_especial'
    oficial_de_operacoes = 'oficial_de_operacoes'
    agente_de_elite = 'agente_de_elite'
