class Kolekcija:
    def __init__ (self):
        self.docs = []

    def dodaj_doc (self, doc):
        self.docs.append (doc)

    def ukloni_doc_index (self, indeks):
        return self.docs.pop(indeks)

    def ukloni_doc (self, doc):
        self.docs.remove(doc)

    def nadji_doc (self, uzorak):
        for j in self.docs:
            if (j == uzorak):
                return j
        return None

    def print_sve (self):
        for j in self.docs:
            print ("   "+str(j))

class Baza:
    def __init__ (self, naziv):
        self.naziv = naziv
        self.kolekcije = {}

    def dodaj_kolekciju (self, ime):
        self.kolekcije[ime]=Kolekcija()

    def dodaj_dokument (self, ime_kol, dok):
        self.kolekcije[ime_kol].dodaj_doc (dok)

    def nadji_dokument (self, ime_kol, uzorak):
        return self.kolekcije[ime_kol].nadji_doc (uzorak)

    def ukloni_dokument (self, ime_kol, e):
        if isinstance (e, int):
            return self.kolekcije[ime_kol].ukloni_doc_index (e)
        else:
            self.kolekcije[ime_kol].ukloni_doc (e)
        
    def print_sve (self):
        for key, val in self.kolekcije.items():
            print (key+":")
            val.print_sve()