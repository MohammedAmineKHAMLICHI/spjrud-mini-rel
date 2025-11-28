@allow < <= <>

@let PROFS1 = @relation [Nom, Prenom] {
  <Bruyere, Veronique>
  <Wijsen, Jozef>
  <Mens, Tom>
  <Francois, Francois>
  <Francois, Claude>
  <Francois, Frederic>
  <Valery, Francois>
  
}

@let AUTRE = @relation [] {}

@let R1 = @select{Nom="Mens"} PROFS1

@let R2 = @select{Nom='Bruyere'} PROFS1

@let R3 = @select{Nom=Prenom} PROFS1

@let R4 = @select{Nom='Francois'} PROFS1

@let R5 = @select{Prenom="Francois"} PROFS1

@let R6 = @select{Prenom="Francois"} (PROFS1)

@let R7 = @select{Prenom="Francois"} @select{Nom="Valery"} PROFS1 

@let R8 = @select{Prenom="Francois"} (@select{Nom="Valery"} PROFS1) 

@let R9 = ( @select{Prenom="Francois"} ( @select{Nom="Valery"} PROFS1 ) )

@let R10 = PROFS1

@let R11 = (((((PROFS1)))))
 
@let R12 = @select{Nom="inconnu"} PROFS1

@let R13 = @select {Nom<='Francois'} PROFS1

@let R14 = @select {Nom<'Francois'} PROFS1

@let R15 = @select {Nom<>'Francois'} PROFS1

@print PROFS1, AUTRE, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15