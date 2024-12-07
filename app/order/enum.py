from enum import Enum


class StatusEnum(Enum):
    PENDING = "PENDING"
    WAITING = "WAITING"
    IN_PRODUCTION = "IN_PRODUCTION"
    FINALIZED = "FINALIZED"
