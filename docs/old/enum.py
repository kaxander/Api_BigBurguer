from enum import Enum


class StatusPedidoEnum(Enum):
    PENDENTE = "PENDENTE"
    EM_ESPERA = "EM_ESPERA"
    EM_PRODUCAO = "EM_PRODUCAO"
    FINALIZADO = "FINALIZADO"
