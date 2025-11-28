% usines
@let A1 = @relation [a1, a2, a3] {}
@let A2 = @relation [a1, a2, a3] {}
@let A3 = @relation [a1, a2, a3] {}

@let r1 = A1 @join A2 @join A3
@let r2_1 = A1 @union A2 @union A3
@let r2_2 = A1 @minus A2 @minus A3
@let r3 = A1 @minus A2 @union A3
@let r4 = A1 @union A2 @minus A3

@let r5 = @select{a1=a2} A1 @union @select{a1=a2} A2

@print r1, r2_1, r2_2, r3, r4, r5