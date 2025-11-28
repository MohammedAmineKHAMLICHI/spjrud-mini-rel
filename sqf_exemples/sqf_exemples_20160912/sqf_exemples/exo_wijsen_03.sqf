% base de donnees question 3
@let TRIPS = @relation [Date, Number_Plate, Driver, Destination, Departure_Time] {
  < 15/10/2001,   DDT 123,    John,   Antwerp Zoo,        09.00 >
  < 15/10/2001,   LPG 234,    Tim,    Ostende Beach,      08.00 >
  < 16/10/2001,   DDT 123,    Tim,    Dinant Citadel,     10.00 >
  < 17/10/2001,   LPG 234,    John,   Antwerp Zoo,        08.15 >
  < 17/10/2001,   DDT 123,    Tim,    Antwerp Zoo,        08.15 >
  < 18/10/2001,   DDT 123,    Tim,    Brussels Atomium,   09.20 >
}

@let BUSES = @relation [Number_Plate, Chassis, Make, Mileage]{
  < DDT 123,    XGUR6775,   Renault,    212 342 >
  < LPG 234,    ZXRY9823,   Mercedes,   321 734 >
  < RAM 221,    XXZZ7345,   Renault,     10 000 >
}

@let DESTINATIONS = @relation [Name]{
  < Antwerp Zoo       >
  < Ostende Beach     >
  < Dinant Citadel    >
  < Brussels Atomium  > 
}

@print TRIPS
@print BUSES
@print DESTINATIONS

% Q13 Quel chauffeur a ete a toutes les destinations ?
@let R = ( @p{Driver} TRIPS * DESTINATIONS ) 
            -  @r{Destination:Name} @p{Driver, Destination} TRIPS
@let R13 = @project{Driver} TRIPS - @project{Driver} R
@print R13

% Q14 Quelles destinations nont jamais ete visitees par John ?
@let R14 = DESTINATIONS - @r{Destination:Name} @p{Destination}
                  @s{Driver="John"} TRIPS
                  
@print R14

% Q15 Qui a conduit un autobus de la marque Renault pour aller a Antwerp Zoo ?
@let RENAULT_ANTWERP = @select{Make="Renault"} BUSES
                          *
                       @select{Destination="Antwerp Zoo"} TRIPS
@let R15 = @project{Driver} RENAULT_ANTWERP
@print R15