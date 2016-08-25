from shlex import split
from Minibaza import Baza, Kolekcija


class QueryEngine:
    def __init__(self, query = None):
        self.index = 0
        self.var = {}

        if query != None: self.newQuery(query)

    def newQuery(self, query):
        self.rezultat = self.parser(self.tokenizer(query))
        for i in range(len(self.rezultat)):
            self.rezultat[i] = self.interpreter(self.rezultat[i])

        if len(self.rezultat) > 1:
            print(self.rezultat)
        elif len(self.rezultat) == 1:
            print(self.rezultat[0])

    def tokenizer(self, query):
        return split(query.replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace('[', ' [ ').replace(']', ' ] '), False, False)

    def parser(self, query):
        lista = []
        i = 0
        while i < len(query):
            if (query[i] == '(' or query[i] == '['):
                lista = self.listexists(lista, self.parser(query[i+1:]))
                i = self.index + i + 1
            elif query[i] == '{':
                lista = self.listexists(lista, self.mapiraj(query[i+1:]))
                i = self.index + i + 1
            elif query[i] == ')' or query[i] == ']':
                self.index = i
                return lista
            elif query[i] != '}':
                lista = self.listexists(lista, query[i])
            i += 1

        return lista

    def mapiraj(self, query):
        lista = ['mapa']
        i = 0

        while i <= len(query):
            if (query[i] == '(' or query[i] == '['):
                lista = self.listexists(lista, self.parser(query[i+1:]))
                i = self.index + i + 1
            elif query[i] == '{':
                lista = self.listexists(lista, self.mapiraj(query[i+1:]))
                i = self.index + i +1
            elif query[i] == '}':
                self.index = i
                if len(lista) % 2 == 0:
                    return None
                return lista
            else:
                lista = self.listexists(lista, query[i])
            i += 1

    def interpreter(self, query):
        rez = None

        e = query[0]

        if e == '?+':
            rez = self.bp_plus(query)
        elif e == '?=' or e == '?>' or e == '?<':
            rez = self.bp_usporedba(query)
        elif e == 'def':
            rez = self.definiraj(query)
        elif e == '!':
            rez = self.postavi(query)
        elif e == 'bp':
            rez = self.baza(query)
        elif e == 'petlja':
            rez = self.petlja(query)
        elif e == 'za-svaki':
            rez = self.za_svaki(query)
        elif e == 'duljina':
            rez = self.duljina(query)
        elif e == '+':
            rez = self.plus(query)
        elif e == '-':
            rez = self.minus(query)
        elif e == '*':
            rez = self.puta(query)
        elif e == '/':
            rez = self.podjeljeno(query)
        elif e == 'kvadrat':
            rez = self.kvadrat(query)
        elif e == '<' or e == '>' or e == '=':
            rez = self.usporedba(query)
        elif e == 'ako' or e == 'if':
            rez = self.ako(query)
        elif e == '@':
            rez = self.indeks(query)
        elif e == 'print':
            rez = self.ispisi(query)
        elif e == 'mapa':
            rez = self.mapa(query)
        else:
            rez = self.lista(query)

        return rez

    #ISPIS
    def ispisi(self, query):
        e = self.jepodupit(query[1])
        if e in self.var:
            e = self.var[e]
        print(e)
        return e

    #HELPERI
    def listexists(self, lista, novo):
        if lista == None and isinstance(novo, (list)):
            lista = novo
        elif lista == None:
            lista = [novo]
        else:
            lista.append(novo)

        return lista

    def jebroj(self, e):
        e = self.jepodupit(e)

        if e == None:
            return None

        if isinstance(e, (list, dict, Baza, Kolekcija)):
            return e
        elif isinstance(e, (int, float)):
            return self.intfloat(float(e))
        elif e.replace('.', '', 1).replace('-', '', 1).isdigit():
            return self.intfloat(float(e))
        elif e in self.var:
            return self.intfloat(float(self.var[e]))
        else:
            return e

    def intfloat(self, e):
        if int(float("%0.2f" % e)) == e:
            return int(e)
        else:
            return float("%0.2f" % e)

    def jepodupit(self, e):
        if isinstance(e, (list)):
            return self.interpreter(e)
        else:
            return e

    def mapa(self, query):
        lista = None

        if len(query) % 2 != 0 and len(query) > 2:
            for e in query[1:]:
                temp = self.jebroj(self.jepodupit(e))

                if temp == None:
                    return None

                if isinstance(temp, (float, int, list, dict, Baza, Kolekcija)):
                    lista = self.listexists(lista, temp)
                elif temp[0] == "'":
                    lista = self.listexists(lista, temp[1:-1])
                elif temp in self.var:
                    lista = self.listexists(lista, self.var[temp])
                else:
                    lista = self.listexists(lista, temp)

            t = iter(lista)

            return dict(zip(t, t))

    def lista(self, query):
        lista = []
        temp = None
        for e in query:
            temp = self.jepodupit(e)
            if temp == None:
                return None

            n = self.jebroj(temp)
            if isinstance(temp, (list, dict)):
                lista.append(temp)
            elif isinstance(n, (float, int)):
                lista.append(n)
            elif temp[0] == "'":
                lista.append(temp[1:-1])
            else:
                lista.append(temp)
        return lista

    #ARITMETIKA
    def plus(self, query):
        rez = None

        for e in query[1:]:
            rez = self.aritmetika(rez, e, lambda x, y: x+y)

        return rez

    def minus(self, query):
        rez = None

        for e in query[1:]:
            rez = self.aritmetika(rez, e, lambda x, y: x-y)

        return rez

    def puta(self, query):
        rez = None

        for e in query[1:]:
            rez = self.aritmetika(rez, e, lambda x, y: x*y)

        return rez

    def podjeljeno(self, query):
        rez = None

        for e in query[1:]:
            rez = self.aritmetika(rez, e, lambda x, y: x/y)

        return rez

    def kvadrat(self, query):
        return self.aritmetika(query[1], query[1], lambda x, y: x*y)

    def aritmetika(self, baza, novo, f):
        e = self.jepodupit(novo)
        if e == None:
            return None

        e = self.jebroj(e)
        if isinstance(e, (int, float)):
            if baza != None:
                return self.intfloat(f(baza, e))
            else:
                return self.intfloat(e)

    #LOGIKA
    def usporedba(self, query):
        n1 = None
        n2 = None

        if len(query) == 3:
            n1 = self.jepodupit(query[1])
            n2 = self.jepodupit(query[2])

            if n1 == None or n2 == None:
                return None

            n1 = self.jebroj(n1)
            n2 = self.jebroj(n2)

            if isinstance(n1, (int, float)) and isinstance(n2, (int, float)):
                if query[0] == '>':
                    return n1 > n2
                elif query[0] == '<':
                    return n1 < n2
                elif query[0] == '=':
                    return n1 == n2

    #LISTE I MAPE
    def duljina(self, query):
        temp = None

        if len(query) == 2:
            temp = self.jepodupit(query[1])

            if isinstance(temp, (dict, list)):
                return len(temp)
            elif temp in self.var:
                return len(self.var[temp])

    def indeks(self, query):
        temp1 = None
        temp2 = None

        if len(query) == 3:
            temp1 = self.jepodupit(query[1])
            temp2 = self.jepodupit(query[2])

            if temp1 == None or temp2 == None:
                return None

            temp2 = self.jebroj(temp2)
            if not isinstance(temp2, (float, int)):
                return None

            if temp1 in self.var:
                temp1 = self.var[temp1]

            if isinstance(temp1, list):
                if len(temp1)-1 >= temp2:
                    return temp1[temp2]

    #VARIJABLE
    def definiraj(self, query):
        temp1 = None
        temp2 = None

        temp1 = self.jepodupit(query[1])
        temp2 = self.jepodupit(query[2])

        if temp1 == None or temp2 == None:
            return None

        if len(query) == 3 and temp1 not in self.var:
            n = self.jebroj(temp2)
            if isinstance(temp2, (float, int, Baza, dict, list)):
                self.var[temp1] = temp2
                return temp2
            elif isinstance(n, (float, int)):
                self.var[temp1] = n
                return n
            elif temp2[0] == "'":
                self.var[temp1] = temp2[1:-1]
                return temp2[1:-1]

    def postavi(self, query):
        temp1 = None
        temp2 = None
        temp3 = None

        if len(query) == 3:
            temp1 = self.jepodupit(query[1])
            temp2 = self.jepodupit(query[2])

            if temp1 == None or temp2 == None:
                return None

            if temp1[0] == "'":
                temp1 = temp1[1:-1]

            temp2 = self.jebroj(temp2)
            if not isinstance(temp2, (int, float)) and not isinstance(temp2, (list, dict)):
                if temp2[0] == "'":
                    temp2 = temp2[1:-1]

            if temp1 in self.var:
                self.var[temp1] = temp2
                return temp2
        elif len(query) == 4:
            temp1 = self.jepodupit(query[1])
            temp2 = self.jepodupit(query[2])
            temp3 = self.jepodupit(query[3])

            if temp1 == None or temp2 == None or temp3 == None:
                return None

            if temp1[0] == "'":
                temp1 = temp1[1:-1]

            temp2 = self.jebroj(temp2)
            if not isinstance(temp2, (float, int)):
                return None

            temp3 = self.jebroj(temp3)
            if not isinstance(temp2, (float, int)):
                if temp3[0] == "'":
                    temp3 = temp3[1:-1]

            if temp1 in self.var:
                if isinstance(self.var[temp1], list):
                    if len(self.var[temp1])-1 >= temp2:
                        self.var[temp1][temp2] = temp3
                        return self.var[temp1]

    #KONTROLA TOKA
    def ako(self, query):
        temp = None

        if len(query) == 4:
            temp = self.jepodupit(query[1])

            if temp == True or temp == 'True':
                temp = self.jepodupit(query[2])
            elif temp == False or temp == 'False':
                temp = self.jepodupit(query[3])

            if temp == None:
                return None

            temp = self.jebroj(temp)
            if not isinstance(temp, (int, float)):
                if temp[0] == "'":
                    temp = temp[1:-1]
            return temp

    def petlja(self, query):
        if len(query) >= 3:
            uvjet = query[1]

            while self.jepodupit(uvjet):
                for e in query[2:]:
                    rez = self.jepodupit(e)
        return rez

    def za_svaki(self, query):
        if len(query) >= 4:
            lista = self.jepodupit(query[2])

            if lista == None:
                return None

            if isinstance(lista, list):
                for e in lista:
                    self.var[query[1]] = e

                    for naredba in query[3:]:
                        self.jepodupit(naredba)
            return True

    #BAZA
    def baza(self, query):
        temp = None

        if len(query) == 2:
            temp = self.jepodupit(query[1])
            if temp == None:
                return None

            if temp[0] == "'":
                temp = temp[1:-1]
                if temp in self.var:
                    return self.var[temp]
                else:
                    return Baza(temp)

    def bp_plus(self, query):
        for i in range(len(query)):
            query[i] = self.jepodupit(query[i])
            if query[i] == None:
                return None

        bp_naziv = query[1]
        if bp_naziv[0] == "'":
            bp_naziv = bp_naziv[1:-1]
        if bp_naziv in self.var.keys():
            bp = self.var[bp_naziv]
            if not isinstance(bp, Baza):
                return False
        else:
            return False

        kol_naziv = query[2]
        if kol_naziv[0] == "'":
            kol_naziv = kol_naziv[1:-1]
        if not kol_naziv in bp.kolekcije.keys():
            bp.dodaj_kolekciju(kol_naziv)

        doc = query[3]
        if isinstance(doc, dict):
            bp.kolekcije[kol_naziv].dodaj_doc(doc)
            self.var[bp_naziv] = bp
            return True
        elif doc in self.var.keys():
            doc = self.var[doc]
            if isinstance(doc, dict):
                bp.kolekcije[kol_naziv].dodaj_doc(doc)
                self.var[bp_naziv] = bp
                return True
        return False

    def bp_usporedba(self, query):
        odstrel = []
        operator = query[0][1]

        for i in range(len(query)):
            query[i] = self.jepodupit(query[i])
            if query[i] == None:
                return None

        bp_naziv = query[1]
        if bp_naziv[0] == "'":
            bp_naziv = bp_naziv[1:-1]
        if bp_naziv in self.var.keys():
            bp = self.var[bp_naziv]
            if not isinstance(bp, Baza):
                return None
        else:
            return None

        kol_naziv = query[2]
        if kol_naziv[0] == "'":
            kol_naziv = kol_naziv[1:-1]
        if kol_naziv in bp.kolekcije.keys():
            kol = bp.kolekcije[kol_naziv]
        else:
            return None

        lista = kol.docs

        if isinstance(query[3], dict):
            for uvjet in query[3]:
                vrijednost = query[3][uvjet]

                for doc in lista:
                    if uvjet in doc:
                        if operator == '=':
                            if vrijednost != doc[uvjet]:
                                odstrel.append(doc)
                        elif operator == '<':
                            if isinstance(vrijednost, (int, float)) and isinstance(doc[uvjet], (int, float)):
                                if vrijednost <= doc[uvjet]:
                                    odstrel.append(doc)
                        elif operator == '>':
                            if isinstance(vrijednost, (int, float)) and isinstance(doc[uvjet], (int, float)):
                                if vrijednost >= doc[uvjet]:
                                    odstrel.append(doc)
                    else:
                        odstrel.append(doc)

            for e in odstrel:
                try:
                    lista.remove(e)
                except ValueError:
                    1
        return lista