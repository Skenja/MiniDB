from QueryEngine import QueryEngine
from Minibaza import Baza, Kolekcija

QE = QueryEngine()

query = "(def osobe (bp 'test'))(def dok {'ime' 'Pero' 'prihod' 5000})(def dok2 {'ime' 'Ivo' 'prihod' 2000})(?+ osobe 'kolekcija' dok)(?+ osobe 'kolekcija' dok2)(za-svaki d (?> osobe 'kolekcija' {'prihod' 7000})(print d))(ako (> 1 2) 'rrr' (za-svaki d (?> osobe 'kolekcija' {'prihod' 1000})(print d)))"
QE.newQuery(query)

