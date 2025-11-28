@allow <>
% base de donnees question 4
@let WAREHOUSES = @relation [W#, Address, City]{
  < D1, "6, Rue de lEglise", Mons     >
  < D2, "18, Place du Parc",  Mons     >
  < D3, "18, Place du Parc",  Chimay   >
  < D4, "5, Avenue Louise",   Enghien  >
}

@let STOCK = @relation [W#, Product, Color, Qty]{
  < D1, hinge,   yellow,  200 >
  < D1, hinge,   blue,    150 >
  < D2, lock,    blue,    100 >
  < D2, hinge,   yellow,  200 >
  < D2, handle,  red,     100 >
  < D4, hinge,   red,     150 >
  < D4, lock,    red,     600 >
}

% Q16 Quels produits sont disponibles en plusieurs couleurs dans un meme depot ? ; hinge
% on se debarrasse de Qty
@let STOCK2 = @p{W#, Product, Color} STOCK
% join pour obtenir les combinaisons de couleurs d'un meme produit dans un meme depot
@let COMBI = @r{Color:Color1} STOCK2 * @r{Color:Color2} STOCK2
@let R16a = @p{Product} @s {Color1<>Color2} COMBI
@print R16a
% version sans utiliser <>
@let R16b = @p {Product} ( COMBI - @s {Color1=Color2} COMBI )
@print R16b


%Q17 Quel entrepot ne stocke aucun produit rouge ?
% entrepots qui stockent au moins un produit rouge
@let W_Rouge = @p {W#} @s {Color="red"} STOCK
@let R17 = @p {W#} WAREHOUSES - W_Rouge
@print R17

% Q18 Quel entrepot ne stocke aucun produit non-rouge ?
% entrepots qui stockent au moins un produit non-rouge
@let W_notRed1 = @p {W#} @s {Color<>"red"} STOCK
% idem mais sans <>
@let W_notRed2 = @p {W#} (STOCK - @s {Color="red"} STOCK)
@let R18 = @p {W#} WAREHOUSES - W_notRed1
@print R18
