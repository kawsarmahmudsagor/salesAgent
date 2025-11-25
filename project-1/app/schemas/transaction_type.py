from enum import Enum

class TrnTypeEnum(str, Enum):
    payment = "payment"
    refund = "refund"
    adjustment = "adjustment"
