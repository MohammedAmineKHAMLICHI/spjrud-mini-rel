@let PROFS1 = @relation [Nom, Prenom] {
  <Bruyere, Veronique>
  <Wijsen, Jozef>
  <Servais, Frederic>
  <Fortz, Bernard>
  <Quoitin, Bruno>
}

@let PROFS2 = @relation [Nom, Prenom] {
  <Servais, Frederic>
  <Melot, Hadrien>
  <Quoitin, Bruno>
  <Mens, Tom>
  <Buys, Alain>
  <Glineur, Pol>
}

% same as PROFS2, with another attribute order
@let PROFS3 = @relation [Prenom, Nom] {
  <Frederic, Servais>
  <Hadrien, Melot>
  <Bruno, Quoitin>
  <Tom, Mens>
  <Alain, Buys>
  <Pol, Glineur>
}

@let EMPTY = @relation [Nom, Prenom] {}

@let P1_P2 = PROFS1 @union PROFS2
@let P1_P1 = PROFS1 @union PROFS1
@let P1_E  = PROFS1 @union EMPTY
@let P1_P3 = PROFS1 @union PROFS3
@let P3_P1 = PROFS3 @union PROFS1
@let P2_P3 = PROFS2 @union PROFS3
@let P3_P2 = PROFS3 @union PROFS2



@print PROFS1, PROFS2, PROFS3, EMPTY, P1_P2, P1_P1, P1_E, P1_P3, P3_P1, P2_P3, P3_P2

