from abc import ABC, abstractmethod
from datetime import datetime


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
        self.foglalva = {}

    @abstractmethod
    def ar_szamolas(self):
        pass

    def foglalas(self, datum):
        if datum in self.foglalva:
            print("Ez a szoba már foglalt ezen a napon!")
            return False
        else:
            self.foglalva[datum] = True
            print("Sikeres foglalás!")
            return True

    def foglalas_lemondas(self, datum):
        if datum in self.foglalva:
            del self.foglalva[datum]
            print("Foglalás sikeresen törölve!")
            return True
        else:
            print("Nincs ilyen foglalás ezen a napon!")
            return False

    def listaz_foglalasok(self):
        print(f"Foglalások a szobában {self.szobaszam}:")
        for datum in self.foglalva:
            print(f"  - Dátum: {datum}")


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=5000, szobaszam=szobaszam)

    def ar_szamolas(self):
        return self.ar


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=8000, szobaszam=szobaszam)

    def ar_szamolas(self):
        return self.ar


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def szoba_foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                szoba.foglalas(datum)
                return

    def szoba_foglalas_lemondas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                szoba.foglalas_lemondas(datum)
                return

    def listaz_foglalasok(self):
        print(f"{self.nev} foglalások:")
        for szoba in self.szobak:
            szoba.listaz_foglalasok()


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


def main():
    szalloda = Szalloda("Példa Szálloda")

    # Szobák inicializálása és hozzáadása
    szoba1 = EgyagyasSzoba(szobaszam=101)
    szoba2 = EgyagyasSzoba(szobaszam=102)
    szoba3 = KetagyasSzoba(szobaszam=201)
    szoba4 = KetagyasSzoba(szobaszam=202)
    szoba5 = EgyagyasSzoba(szobaszam=103)

    szalloda.add_szoba(szoba1)
    szalloda.add_szoba(szoba2)
    szalloda.add_szoba(szoba3)
    szalloda.add_szoba(szoba4)
    szalloda.add_szoba(szoba5)

    # Szobák foglalása
    szoba1.foglalas(datetime(2024, 5, 21))
    szoba2.foglalas(datetime(2024, 5, 22))
    szoba3.foglalas(datetime(2024, 5, 23))
    szoba4.foglalas(datetime(2024, 5, 24))
    szoba5.foglalas(datetime(2024, 5, 25))

    felhasznaloi_interfesz(szalloda)


def felhasznaloi_interfesz(szalloda):
    print("Üdvözöljük a Berger Szállodában!")
    while True:
        print("\nVálasszon egy műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Adja meg a választott művelet számát: ")

        if valasztas == "1":
            # Foglalás funkció
            print("Hány ágyas szobát szeretne foglalni?")
            print("1. Egyágyas")
            print("2. Kétágyas")
            szobatipus_valasztas = input("Adja meg a választott szobatípus számát: ")

            if szobatipus_valasztas not in ["1", "2"]:
                print("Érvénytelen választás.")
                continue

            szobatipus = EgyagyasSzoba if szobatipus_valasztas == "1" else KetagyasSzoba

            while True:
                datum_input = input("Adja meg a foglalás dátumát (éééé-hh-nn formátumban): ")
                try:
                    datum = datetime.strptime(datum_input, "%Y-%m-%d")
                    if datum < datetime.combine(datetime.now().date(), datetime.min.time()):
                        raise ValueError("Csak jövőbeli dátumokra lehet foglalni!")
                except ValueError as e:
                    print(f"Hiba: {e}")
                    print("Kérem, adjon meg egy új, jövőbeli dátumot.")
                    continue

                break

            szabad_szobak = []
            for szoba in szalloda.szobak:
                if isinstance(szoba, szobatipus) and datum not in szoba.foglalva:
                    szabad_szobak.append(szoba)

            if szabad_szobak:
                elso_szoba = szabad_szobak[0]
                elso_szoba.foglalas(datum)
                print(f"A foglalt szoba: {elso_szoba.szobaszam}, {szobatipus.__name__}")
                print(f"Foglalás dátuma: {datum.strftime('%Y-%m-%d')}")
                print(f"A foglalás ára: {elso_szoba.ar_szamolas()} Ft")
                while True:
                    helyes = input("Helyesek a foglalás adatai? (igen/nem): ")
                    if helyes.lower() == "igen":
                        print("Foglalás megerősítve!")
                        break
                    elif helyes.lower() == "nem":
                        elso_szoba.foglalas_lemondas(datum)
                        print("Foglalás megszakítva.")
                        break
                    else:
                        print("Érvénytelen válasz. Kérjük, válasszon 'igen' vagy 'nem'.")
            else:
                print("Minden szoba foglalt ezen a napon!")

        elif valasztas == "2":
            # Lemondás funkció
            print("Lemondási funkció")
            print("A foglalt szobák ezen a napon:")
            for szoba in szalloda.szobak:
                szoba.listaz_foglalasok()
            szobaszam = int(input("Adja meg a lemondani kívánt szoba számát: "))
            datum_input = input("Adja meg a lemondás dátumát (éééé-hh-nn formátumban): ")
            try:
                datum = datetime.strptime(datum_input, "%Y-%m-%d")
                if datum < datetime.combine(datetime.now().date(), datetime.min.time()):
                    raise ValueError("Csak jövőbeli dátumra lehet lemondani!")
            except ValueError as e:
                print(f"Hiba: {e}")
                print("Kérem, adjon meg egy érvényes dátumot.")
                continue

            szalloda.szoba_foglalas_lemondas(szobaszam, datum)

        elif valasztas == "3":
            szalloda.listaz_foglalasok()

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás, kérem, válasszon újra.")


if __name__ == "__main__":
    main()
