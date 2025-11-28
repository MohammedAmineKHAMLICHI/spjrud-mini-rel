% ajout du 8 avril : @let peuvent etre utilises apres un @let

@let U = @relation [NU, NomU, Ville] {
  < 1,    A,    Paris >
  < 2,    B,    Paris >
  < 3,    C,    Paris >
  < 4,    D,    Londres >
  < 5,    E,    Londres >
}

@print U

@let R1 = U

@let R2 = @select {Ville="Londres"} U

@print R1

@let P = @relation [NP, NomP, Couleur, Poids] {
  <1,   iPhone,   rouge,  100>
  <2,   iPhone,   gris,   100>
  <3,   iMac,     blanc,  300>
  <4,   MacBook,  blanc,  200>
  <5,   MacBook,  noir,   200>
}

@let R3 = @rename {Ville:VilleU} @project {Ville} U

@print R3