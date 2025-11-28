@let CHANTEURS 
   = @relation [ Prenom,     Nom,    Genre,  Age,  Salaire,  Vivant] {
  < Frederic,   Francois,   H,    60,   25000,   Oui > 
  < Claude,     Francois,   H,    40,   30000,   Non > 
  < Claude,     Nougaro,    H,    60,   20000,   Non > 
  < Michel,     Sardou,     H,    65,   30000,   Oui > 
  < Barbara,    '',         F,    50,   50000,   Non > 
  < Mireille,   Mathieu,    F,    65,   30000,   Non > 
}

@let CHANTEURS_VIDE = @relation [Prenom, Nom, Genre, Age, Salaire, Vivant] {}


@let R1 = @project{Prenom}  CHANTEURS
@let R2 = @project{Nom}     CHANTEURS
@let R3 = @project{Age}     CHANTEURS
@let R4 = @project{Genre}   CHANTEURS
@let R5 = @project{Salaire} CHANTEURS
@let R6 = @project{Vivant}  CHANTEURS

@let R7 = @project{}    CHANTEURS
@let R8 = @project{}    CHANTEURS_VIDE

@let R9 = @project{Prenom, Nom}   CHANTEURS
@let R10 = @project{Nom, Prenom}  CHANTEURS

@let R11 = @project{Nom, Prenom, Genre} @select{Genre="H"} CHANTEURS

@let R12 = @select{Genre="H"} @project{Nom, Prenom, Genre} CHANTEURS

@let R13 = @project{Nom, Prenom} @select{Genre="F"} CHANTEURS

@let R14 = @project{Salaire, Age} CHANTEURS

@let R15 = @project{} @project{Nom} CHANTEURS

@print CHANTEURS, CHANTEURS_VIDE

@print R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15