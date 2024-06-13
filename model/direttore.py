from dataclasses import dataclass

@dataclass
class Direttore:
    id:int
    first_name:str
    last_name:str


    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"