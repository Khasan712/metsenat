from enum import Enum


class UserRoles(Enum):
    student = 'student'
    sponsor = 'sponsor'
    admin = 'admin'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
    
class Regions(Enum):
    tashkent = 'Toshkent'
    samarkand = 'Samarqand'
    andijan = 'Andijon'
    fargona = 'Fargona'
    namangan = 'Namangan'
    qashqadaryo = 'Qashqadaryo'
    surxondaryo = 'Surxondaryo'
    buxoro = 'Buxoro'
    navoiy = 'Navoiy'
    xorazm = 'Xorazm'
    sirdaryo = 'Sirdaryo'
    jizzax = 'Jizzax'
    qoraqalpoq = 'Qoraqalpog\'iston Respublikasi'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



class Gender(Enum):
    man = 'man'
    woman = 'woman'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
class StudentType(Enum):
    bachelor = 'bachelor'
    master = 'master'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    
class IOHE(Enum):
    TATU = 'TATU'
    YOJU = 'YOJU'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)