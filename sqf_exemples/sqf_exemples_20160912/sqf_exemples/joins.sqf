% exemples tires du syllabus de Monsieur Wijsen (Base de donnees I)

@let EO = @relation [Espece, Ordre] {
  < Lion,         Carnivores >
  < Loup,         Carnivores >
  < Tigre,        Carnivores >
  < Hyene,        Carnivores >
  < Girafe,       Artiodactyles >
  < Hippopotame,  Artiodactyles >
  < Cobra,        Serpents >
}

@let OC = @relation [Ordre, Classe] {
  < Carnivores,   Mammiferes >
  < Artiodactyles, Mammiferes >
  < Serpents,     Reptiles >
}

@let VIT = @relation [Espece, Continent] {
  < Lion,         Afrique >
  < Lion,         Asie >
  < Loup,         Europe >
  < Loup,         Asie >
  < Tigre,        Asie >
  < Hyene,        Afrique >
  < Girafe,       Afrique >
  < Hippopotame,  Afrique >
  < Cobra,        Asie >
}

@let R1 = EO @join OC
@let R2 = OC @join EO
@let R3 = EO @join VIT
@let R4 = OC @join VIT
@let R5 = EO @join OC @join VIT

@print EO, OC, VIT, R1, R2, R3, R4, R5






