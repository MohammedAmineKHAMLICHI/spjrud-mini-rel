@allow <>

% base de donnees question 2
@let Cities = @relation [Name, Country, Population] {
  <Bergen,    Belgium,  20.3>
  <Bergen,    Norway,   30.5>
  <Brussels,  Belgium, 370.6>
}

@let Countries = @relation [Name, Capital, Population, Currency] {
  <Belgium,   Brussels,        10 255.6,   EUR>
  <Norway,    Oslo,             4 463.2,   NOK>
  <Japan,     Tokyo,          128 888.0,   YEN>
  <France,    Paris,           10 255.6,   EUR>
  <Salvador,  San Salvador,     6 328.1,   USD> 
  <USA,       Washington,     318 900.3,   USD> 
}

% Q11. Quelle est la population de la capitale de la Belgique ?
@let CC = @rename{Name:Country} @project{Name, Capital} Countries
@let R11 = @project{Population} (
              @rename{Name:Capital} Cities 
                @join 
              @select{Country="Belgium"} CC )
@print R11

% Q12 : Quelle monnaie est utilisee dans plusieurs pays ?
@let CURRENCIES = @project{Name, Currency} Countries
@let R12 = @project{Currency} @select{Country<>Name} (
                @rename{Name:Country} CURRENCIES @join CURRENCIES)
@print R12


@print Countries @join Cities, R11