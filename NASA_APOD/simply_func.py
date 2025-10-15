import string
from collections import Counter
# def analiza_tekstu(tekst):
def analiza_zdania(zdanie, wystapienia_uzytkownika=None):
    if not zdanie:
        return None
    else:

        # Ujednolicenie tekstu

        wpis = zdanie.lower()

        # Kopia tekstu

        wpis_nowy = wpis

        # Obliczanie ilości znaków interpunkcyjnych

        ilosc_znakow_interpunkcyjnych = 0
        for znak in wpis:
            if znak in string.punctuation:
                ilosc_znakow_interpunkcyjnych +=1


        # ILOŚĆ WYRAZÓW
        for znak in string.punctuation:
            wpis = wpis.replace(znak, "")
            
        lista = wpis.split()

        dlugosc_listy = len(lista)

        # ILOŚĆ ZNAKÓW
        znaki = wpis.replace(" ", "")
        ilosc_znakow = len(znaki)

        zliczenia = Counter(lista)

        czeste_slowa = zliczenia.most_common(1)

        # NAJCZĘSTSZE SŁOWO
        najczestsze_slowo = czeste_slowa[0][0]
        # najczestsze_slowa = [slowo for slowo, liczba in zliczenia]
        # print(najczestsze_slowa)

        znaki_konczace = ['!','?','.']

        for znak in znaki_konczace:
            tekst_z_kropkami = wpis_nowy.replace(znak, ".")
        
        # ILOSC ZDAŃ
        dzielenie_zdan = tekst_z_kropkami.split(".")
        ilosc_zdan = len([zdanie.strip() for zdanie in dzielenie_zdan if zdanie.strip()])

        # ŚREDNIA DŁUGOŚĆ SŁOWA
        if lista == 0:
            return None
        else:
            srednia_dlugosc = sum(len(s) for s in lista) / len(lista)
        # print(f'srednia dlugosc: {srednia_dlugosc}')
        if wystapienia_uzytkownika:
            wyraz = wystapienia_uzytkownika.lower()
            wystapienia = lista.count(wyraz)
        else:
            wystapienia = None


        wyniki = {
            "znaki_interpun": ilosc_znakow_interpunkcyjnych,
            "ilosc_wyrazow": dlugosc_listy, 
            "ilosc_znakow": ilosc_znakow,
            "najczestsze_slowo": najczestsze_slowo,
            "ilosc_zdan": ilosc_zdan, 
            "srednia_dlugosc": round(srednia_dlugosc, 0), 
            "lista": lista, 
            "wystapienia": wystapienia, 
            "wystapienia_uzytkownika": wystapienia_uzytkownika
        }
        return wyniki

    # LICZBA WYSTĄPIEŃ DANEGO SŁOWA + DODAC FUNKCJE Z TYM

