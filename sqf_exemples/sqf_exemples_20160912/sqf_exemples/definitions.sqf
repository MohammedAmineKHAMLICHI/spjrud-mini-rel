% commentaires de ligne avec '%'. Tout ce qui suit sur la ligne est ignore par le parseur

% definir une relation
% '@let' ID ' = @relation [' ATTRIBUTE_LIST ']' '{' TUPLE_LIST '}'
@let PROFS1 = @relation [Nom, Prenom] {
  <Bruyere, Veronique>
  <Wijsen, Jozef>
  <Mens, Tom>
}

% les espaces sont optionnelles entre les elements
@let PROFS2 = @relation [Nom,Prenom]{<Bruyere,Veronique><Wijsen,Jozef><Mens,Tom>}

% autre exemple de convention d'ecriture pour la definition de relation
@let PROFS3 = @relation [   Nom,        Prenom    ] { 
                < Bruyere,    Veronique >
                < Wijsen,     Jozef     >
                < Mens,       Tom       > 
              }
              
% les valeurs d'un tuple sont separees par des virgules
@let ECRIVAIN = @relation [Nom, Prenom] {
  < de la Fontaine, Jean >
  < de Musset, Alfred >
  < Higgins Clark, Mary >
  < Doyle, Arthur Conan >
}

@print PROFS1, PROFS2, PROFS3, ECRIVAIN


% les valeurs d'un tuple sont "trimmees", ce qui offre de la souplesse pour les conventions d'ecriture
% si des espaces sont significatives au debut ou a la fin d'une valeur, la valeur doit etre entouree de guillemets doubles ou simples (apostrophes)
@let R1 = @relation [Titre, Annee] {
  < "   espaces avant",               1995 >
  < "espaces apres      ",            2000 >
  < "    espaces avant et apres   ",  2000 >
}

@let R2 = @relation [Titre, Annee] {
  < '   espaces avant'                  , 1995 >
  < 'espaces apres      '               , 2000 >
  < '    espaces avant et apres   '     , 2000 >
}

@print R1, R2


% les valeurs d'un tuple sont delimitees par une virgule ou le signe '>'
% si une valeur contient des virgules ou des signes '>', on peut soit :
%   - entourer la valeur de guillemets (simples ou doubles)
%   - echapper le caractere avec un backslash
@let CITATION = @relation [Citation, Auteur] {
  < "Les cons ca ose tout, c'est meme a ca qu'on les reconnait", Audiard >
  < "Je suis contre les femmes, tout contre", Sacha Guitry >
  < Les francais ont du vin\, les Anglais de l'humour, Roland Topor >
}

@print CITATION

@let EXPRESSION_MATHEMATIQUE = @relation [expression] {
  < x1 < y1 >
  < x2 \> y2 >
  < "x3 > y3" >
  < "forall x1, x2, x3" >
}

@print EXPRESSION_MATHEMATIQUE

% echappement dans les valeurs d'un tuple :
%  \"   :     "
%  \'   :     '
%  \,   :     ,
%  \>   :     >
%  \\   :     \
% un backslash suivi d'un autre caractere que ceux qui precedent n'est pas interprete
@let ECHAPPEMENT = @relation [exemple] {
  < c:\java >
  < c:\\windows >
  < Lundi\, j'ai repondu : "non\, non !" > 
  < "Mardi, j'ai repondu : \"non, non !\"" >
  < 'Jeudi, j\'ai repondu : "non, non !"' >
  < "une chaine qui se termine par un backslash \\" >
  < une autre chaine qui se termine par un backslash \ >
}

@print ECHAPPEMENT

% une relation peut ne contenir aucun tuple
@let VIDE1 = @relation [nom, prenom] {}

% pour une valeur d'attribut vide, il est necessaire d'utiliser des guillemets (simple ou double)
@let EMPTY_VALUES = @relation [Nom, Prenom, Telephone] {
  <Wijsen, Jozef, "" >
  <Bruyere, Veronique, '' >
}

@print EMPTY_VALUES

% une relation peut ne pas avoir d'attribut et etre vide
@let VIDE2 = @relation [] {}

@print VIDE1, VIDE2

% une relation peut ne pas avoir d'attribut et contenir un seul tuple, le tuple vide
@let SANS_ATTR = @relation [] { < > }

% une relation avec un attribut et un seul tuple, dont la valeur d'attribut est la chaine vide
@let AVEC_ATTR = @relation [a1] { < "" > }

@print SANS_ATTR, AVEC_ATTR


% NOTE : on fait l'hypothese que tous les attributs appartiennent a un seul domaine, par exemple le domaine des chaines de caractere