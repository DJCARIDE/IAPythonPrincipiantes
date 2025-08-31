class PartyAnimal:
    x = 0 # atributo de clase

    def party(self) : # método de instancia
        self.x = self.x + 1
        print("Hasta ahora", self.x)

# instancia de la clase PartyAnimal
an = PartyAnimal()

# Llamadas al método party
an.party()
an.party()
an.party()
#print(type(an))
#print(dir(an))

