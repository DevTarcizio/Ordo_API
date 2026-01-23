from enum import Enum


class TaskState(Enum):
    todo = 'todo'
    doing = 'doing'
    done = 'done'


class UserRoles(Enum):
    master = 'master'
    player = 'player'


class Origins(Enum):
    academico = 'Acadêmico'
    agente_de_saude = 'Agente de Saúde'
    amnesico = 'Amnésico'
    artista = 'Artista'
    atleta = 'Atleta'
    chef = 'Chef'
    cientista_forense = 'Cientista Forense'
    criminoso = 'Criminoso'
    cultista_arrependido = 'Cultista Arrependido'
    desgarrado = 'Desgarrado'
    engenheiro = 'Engenheiro'
    executivo = 'Executivo'
    escritor = 'Escritor'
    investigador = 'Investigador'
    jornalista = 'Jornalista'
    lutador = 'Lutador'
    magnata = 'Magnata'
    mercenario = 'Mercenário'
    militar = 'Militar'
    operario = 'Operário'
    policial = 'Policial'
    professor = 'Professor'
    religioso = 'Religioso'
    servidor_publico = 'Servidor Público'
    teorico_da_conspiracao = 'Teórico da Conspiração'
    ti = 'TI'
    trabalhador_rural = 'Trabalhador Rural'
    trambiqueiro = 'Trambiqueiro'
    universitario = 'Universitário'
    vitima = 'Vítima'
    prodigio_paranormal = 'Prodígio Paranormal'
    oficial_militar = 'Oficial Militar'


class Classes(Enum):
    mundano = 'Mundano'
    combatente = 'Combatente'
    especialista = 'Especialista'
    ocultista = 'Ocultista'
    transformado = 'Transformado'


class Trails(Enum):
    none = 'none'
    aniquilador = 'Aniquilador'
    comandante_de_campo = 'Comandante de Campo'
    guerreiro = 'Guerreiro'
    operacoes_especiais = 'Operações Especiais'
    tropa_de_choque = 'Tropa de Choque'
    atirador_de_elite = 'Atirador de Elite'
    infiltrador = 'Infiltrador'
    medico_de_campo = 'Médico de Campo'
    negociador = 'Negociador'
    tecnico = 'Técnico'
    conduite = 'Conduíte'
    flagelador = 'Flagelador'
    graduado = 'Graduado'
    intuitivo = 'Intuitivo'
    lamina_paranormal = 'Lâmina Paranormal'


class Ranks(Enum):
    none = 'none'
    recruta = 'Recruta'
    operador = 'Operador'
    agente_especial = 'Agente Especial'
    oficial_de_operacoes = 'Oficial de Operacoes'
    agente_de_elite = 'Agente de Elite'
