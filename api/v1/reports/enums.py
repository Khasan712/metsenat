from enum import Enum


class StatusSponsor(Enum):
    new = 'new'
    inMediration = 'inMediration'
    confirmed = 'confirmed'
    rejected = 'rejected'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class PriceType(Enum):
    USD = 'USD'
    UZS = 'UZS'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)