@let CHANTEURS
   = @relation [ Prenom,     Nom,    Genre,  Age,  Salaire,  Vivant]   {
  < Frederic,   Francois,   H,    60,   25.000,   Oui > 
}

@let R1 = @rename {Prenom: C_Prenom} CHANTEURS
@let R2 = @rename {Nom: C_Nom} CHANTEURS
@let R3 = @rename {Prenom: C_Prenom, Nom: C_Nom} CHANTEURS
@let R4 = @rename {} CHANTEURS
@let R5 = @rename {Prenom:Nom, Nom:Prenom} CHANTEURS

@print CHANTEURS
@print R1, R2, R3, R4, R5