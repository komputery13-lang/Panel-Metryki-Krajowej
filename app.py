from flask import Flask, render_template, request

app = Flask(__name__)

POPULACJA_POLSKI = 37376000
AKTUALNY_ROK = 2026

def pobierz_dokladne_dane(wiek):
    if wiek < 0 or wiek > 100: return 0
    if wiek == 0: return 255000
    if wiek == 1: return 260000
    if wiek == 2: return 268000
    if wiek == 3: return 280000
    if wiek == 4: return 295000
    if wiek == 5: return 310000
    if 6 <= wiek <= 9: return 380000 - (wiek - 6) * 5000
    if 10 <= wiek <= 13: return 360000 + (wiek - 10) * 8000
    if 14 <= wiek <= 18: return 375000 - (wiek - 14) * 6000
    if 19 <= wiek <= 22: return 345000 + (wiek - 19) * 3000
    if 23 <= wiek <= 25: return 355000 + (wiek - 23) * 12000
    if 26 <= wiek <= 29: return 390000 + (wiek - 26) * 15000
    if 30 <= wiek <= 32: return 440000 + (wiek - 30) * 20000
    if 33 <= wiek <= 39: return 510000 + (wiek - 33) * 12000
    if 40 <= wiek <= 44: return 610000 - (wiek - 40) * 8000
    if 45 <= wiek <= 46: return 570000 - (wiek - 45) * 15000
    if 47 <= wiek <= 52: return 540000 - (wiek - 47) * 10000
    if 53 <= wiek <= 59: return 490000 - (wiek - 53) * 7000
    if 60 <= wiek <= 65: return 450000 - (wiek - 60) * 4000
    if 66 <= wiek <= 70: return 440000 - (wiek - 66) * 6000
    if 71 <= wiek <= 76: return 410000 - (wiek - 71) * 25000
    if 77 <= wiek <= 84: return 260000 - (wiek - 77) * 20000
    if 85 <= wiek <= 89: return 110000 - (wiek - 85) * 12000
    return max(55000 - (wiek - 90) * 5000, 1200)

def generuj_pelna_baze_historyczna():
    baza = {}
    wydarzenia_szczegolowe = {
        2026: "Polska i świat wkraczają w nową erę sztucznej inteligencji i robotyki.",
        2025: "Historyczny przełom w fuzji jądrowej – kontrolowany zysk energetyczny net-gain.",
        2024: "Igrzyska Olimpijskie w Paryżu. Startuje kosmiczna misja NASA Europa Clipper.",
        2023: "Indyjska sonda Chandrayaan-3 bezpiecznie ląduje na biegunie Księżyca.",
        2022: "Teleskop Jamesa Webba przesyła pierwsze najgłębsze zdjęcia wszechświata.",
        2021: "Łazik Perseverance ląduje na Marsie i wysyła pierwsze próbki dźwiękowe.",
        2020: "Wybuch globalnej pandemii COVID-19. Świat zamyka się w masowych lockdownach.",
        2019: "Opublikowano pierwsze w historii ludzkości zdjęcie cienia czarnej dziury (M87).",
        2018: "SpaceX wystrzeliwuje rakietę Falcon Heavy z samochodem Tesla w kosmos.",
        2017: "Odkrycie pierwszego międzygwiezdnego obiektu 'Oumuamua w Układzie Słonecznym.",
        2016: "Naukowcy z projektu LIGO ogłaszają pierwsze wykrycie fal grawitacyjnych.",
        2015: "Sonda New Horizons dokonuje historycznego zbliżenia do powierzchni Plutona.",
        2014: "Lądownik Philae wykonuje pierwsze lądowanie na powierzchni jądra komety.",
        2013: "Edward Snowden ujawnia tajne programy inwigilacji internetowej przez NSA.",
        2012: "Odkrycie Bozonu Higgsa w Wielkim Zderzaczu Cząstek CERN pod Genewą.",
        2011: "Trzęsienie ziemi w Japonii i katastrofa w elektrowni atomowej Fukushima.",
        2010: "Katastrofa polskiego samolotu prezydenckiego Tu-154 w Smoleńsku.",
        2009: "Satoshi Nakamoto uruchamia sieć Bitcoin i generuje pierwszy blok kryptowaluty.",
        2008: "Upadek banku Lehman Brothers wywołuje gigantyczny globalny kryzys finansowy.",
        2007: "Steve Jobs prezentuje pierwszego iPhone'a, rewolucjonizując telekomunikację.",
        2006: "Pluton zostaje oficjalnie zdegradowany do statusu planety karłowatej.",
        2005: "Uruchomienie serwisu YouTube. Śmierć papieża Jana Pawła II w Watykanie.",
        2004: "Wielkie rozszerzenie UE – Polska oficjalnie staje się członkiem Unii Europejskiej.",
        2003: "Zakończenie projektu Human Genome – zsekwencjonowano cały ludzki genom.",
        2002: "Waluta Euro wchodzi do obiegu gotówkowego w krajach strefy euro.",
        2001: "Atak terrorystyczny na World Trade Center w Nowym Yorku zmienia bieg historii.",
        2000: "Świat wkracza w nowe tysiąclecie, bezbłędnie mijając zagrożenie błędu Y2K.",
        1999: "Polska oficjalnie przystępuje do struktur obronnych NATO.",
        1998: "Wystrzelenie pierwszego modułu Międzynarodowej Stacji Kosmicznej (ISS).",
        1997: "Uchwalenie Konstytucji RP. Katastrofalna Powódź Tysiąclecia w Polsce.",
        1996: "Ogłoszenie sukcesu pierwszego sklonowania ssaka – owcy Dolly.",
        1995: "Premiera systemu Windows 95, który zrewolucjonizował obsługę PC.",
        1994: "Oficjalne otwarcie Eurotunelu łączącego Wielką Brytanię z Francją.",
        1993: "Wejście w życie Traktatu z Maastricht tworzącego Unię Europejską.",
        1992: "Powstaje powszechny format plików dźwiękowych MP3.",
        1991: "Oficjalny rozpad ZSRR. Polska uzyskuje dostęp do globalnej sieci Internet.",
        1990: "Lech Wałęsa zostaje pierwszym prezydentem III RP wybranym demokratycznie.",
        1989: "Obrady Okrągłego Stołu w Polsce oraz zburzenie Muru Berlińskiego.",
        1988: "Fala strajków w Polsce, która wymusiła transformację ustrojową.",
        1987: "Ronald Reagan wzywa w Berlinie do zburzenia muru dzielącego Europę.",
        1986: "Eksplozja reaktora atomowego w Elektrowni w Czarnobylu.",
        1985: "Michaił Gorbaczow obejmuje władzę w ZSRR i rozpoczyna 'Pierestrojkę'.",
        1984: "Premiera pierwszego komputera Apple Macintosh z myszką i interfejsem graficznym.",
        1983: "Wprowadzenie protokołu TCP/IP – oficjalne narodziny technologii Internetu.",
        1982: "Trwa stan wojenny w Polsce. Oficjalne zdelegalizowanie 'Solidarności'.",
        1981: "Wprowadzenie stanu wojennego w Polsce przez generała Wojciecha Jaruzelskiego.",
        1980: "Powstanie Niezależnego Samorządnego Związku Zawodowego 'Solidarność'.",
        1979: "Pierwsza pielgrzymka papieża Jana Pawła II do ojczystej Polski.",
        1978: "Kardynał Karol Wojtyła zostaje wybrany na papieża (Jan Paweł II).",
        1977: "Premiera kultowego filmu 'Gwiezdne Wojny: Część IV' w reżyserii George'a Lucasa.",
        1976: "Robotnicze protesty w Radomiu i Ursusie. Powstanie KOR.",
        1975: "Podpisanie Aktu Końcowego Konferencji Bezpieczeństwa i Współpracy w Helsinkach.",
        1974: "Reprezentacja Polski w piłce nożnej zajmuje 3. miejsce na Mistrzostwach Świata.",
        1973: "Zakończenie bezpośredniego zaangażowania militarnego USA w wojnie w Wietnamie.",
        1972: "Ostatnia załogowa misja na Księżyc – Apollo 17 opuszcza orbitę satelity.",
        1971: "Firma Intel wprowadza na rynek pierwszy komercyjny mikroprocesor Intel 4004.",
        1970: "Tragiczne Wydarzenia Grudniowe na Wybrzeżu. Ustąpienie Władysława Gomułki.",
        1969: "Neil Armstrong i Buzz Aldrin jako pierwsi ludzie lądują na Księżycu (Apollo 11).",
        1968: "Protesty studenckie w Polsce (Wydarzenia Marcowe). Kryzys polityczny.",
        1967: "Pierwszy udany przeszczep ludzkiego serca przeprowadzony przez Christiaana Barnarda.",
        1966: "Oficjalne obchody Tysiąclecia Państwa Polskiego.",
        1965: "Wojna w Wietnamie – pierwsze amerykańskie jednostki bojowe lądują w Da Nang.",
        1964: "Uchwalenie Kodeksu cywilnego oraz Kodeksu postępowania cywilnego w Polsce.",
        1963: "Zamach w Dallas – ginie prezydent Stanów Zjednoczonych John F. Kennedy.",
        1962: "Kryzys kubański stawia świat na krawędzi totalnej wojny nuklearnej.",
        1961: "Jurij Gagarin zostaje pierwszym człowiekiem w przestrzeni kosmicznej. Budowa Muru Berlińskiego.",
        1960: "Początek budowy Huty Katowice. Afrykański Rok Niepodległości (17 nowych państw).",
        1959: "Fidel Castro przejmuje władzę na Kubie w wyniku rewolucji kubańskiej.",
        1958: "Uruchomienie pierwszego polskiego reaktora badawczego 'Ewa' w Świerku.",
        1957: "ZSRR wystrzeliwuje Sputnika 1 – pierwszego sztucznego satelitę Ziemi.",
        1956: "Poznański Czerwiec – pierwsze masowe wystąpienia robotnicze w PRL.",
        1955: "Podpisanie Układu Warszawskiego. Oficjalne otwarcie Pałacu Kultury i Nauki w Warszawie.",
        1954: "Uruchomienie pierwszej na świecie elektrowni atomowej w Obninsku.",
        1953: "Śmierć Józefa Stalina wywołuje odwilż polityczną w krajach bloku wschodniego.",
        1952: "Wejście w życie Konstytucji PRL – formalne powstanie Polskiej Rzeczypospolitej Ludowej.",
        1951: "Polska i ZSRR dokonują największej powojennej wymiany terytoriów granicznych.",
        1950: "Rozpoczęcie budowy socjalistycznego miasta i kombinatu Nowa Huta.",
        1949: "Powstanie Organizacji Traktatu Północnoatlantyckiego (NATO) oraz bloku NRD i RFN.",
        1948: "Powstanie PZPR (Polska Zjednoczona Partia Robotnicza). Zjednoczenie ruchu robotniczego.",
        1947: "Wprowadzenie Planu Marshalla w celu odbudowy zniszczonej gospodarczo Europy.",
        1946: "Krajowe referendum w Polsce ('3xTAK') sankcjonuje nowe granice i ustrój.",
        1945: "Koniec II Wojny Światowej. Konferencja w Jałcie i Poczdamie ustala nowy ład i granice Polski.",
        1944: "Wybuch Powstania Warszawskiego przeciwko okupantowi niemieckiemieccemu.",
        1943: "Odkrycie masowych grobów polskich oficerów w Katyniu. Powstanie w getcie warszawskim.",
        1942: "Niemiecka konferencja w Wannsee – decyzja o masowej zagładzie Żydów (Endlösung).",
        1941: "Atak Niemiec na ZSRR (Plan Barbarossa) oraz japoński nalot na bazę Pearl Harbor.",
        1940: "Zbrodnia Katyńska – masowy mord polskich jeńców. Bitwa o Anglię w powietrzu.",
        1939: "Atak Niemiec i ZSRR na Polskę – oficjalny wybuch II Wojny Światowej.",
        1938: "Aneksja Austrii przez Niemcy (Anschluss) oraz układ monachijski rozbijający Czechosłowację.",
        1937: "Otwarcie zapory wodnej w Porąbce – początek modernizacji hydroenergetycznej.",
        1936: "Rozpoczęcie budowy Centralnego Okręgu Przemysłowego (COP) w widłach Wisły i Sanu.",
        1935: "Uchwalenie Konstytucji kwietniowej w Polsce oraz śmierć marszałka Józefa Piłsudskiego.",
        1934: "Podpisanie polsko-niemieckiej deklaracji o niestosowaniu przemocy.",
        1933: "Adolf Hitler obejmuje urząd kanclerza Niemiec, co kończy erę Republiki Weimarskiej.",
        1932: "Polska podpisuje pakt o nieagresji ze Związkiem Radzieckim na okres 3 lat.",
        1931: "Otwarcie Magistrali Węglowej Śląsk-Gdynia – kluczowej inwestycji kolejowej II RP.",
        1930: "Wybory brzeskie w Polsce – zaostrzenie kursu politycznego sanacji.",
        1929: "Krach na giełdzie w Nowym Jorku (Czarny Czwartek) rozpoczyna Wielki Kryzys gospodarczy.",
        1928: "Ignacy Mościcki otwiera Państwową Fabrykę Związków Azotowych w Mościcach.",
        1927: "Mazurek Dąbrowskiego zostaje oficjalnie uznany za hymn narodowy Rzeczypospolitej Polski.",
        1926: "Przewrót majowy przeprowadzony przez Józefa Piłsudskiego wprowadza rządy sanacji."
    }
    for r in range(1926, AKTUALNY_ROK + 1):
        if r not in baza:
            baza[r] = wydarzenia_szczegolowe.get(r, "Czas głębokiej transformacji ustrojowej i społeczno-gospodarczej kraju.")
    return baza

@app.route('/')
def strona_glowna():
    return render_template('index.html')

@app.route('/wynik', methods=['POST'])
def oblicz_wynik():
    try:
        wiek = int(request.form['wiek_uzytkownika'])
        brutto_input = request.form.get('wynagrodzenie_brutto', '0')
        # Zmiana na float pozwala przyjąć całkowicie dowolną wartość płacy (nawet z groszami)
        brutto = float(brutto_input) if brutto_input else 0.0
    except (ValueError, KeyError):
        return "Błąd danych.", 400

    if wiek < 0 or wiek > 100:
        return render_template('index.html', blad="Wprowadź wiek od 0 do 100 lat.")

    liczba_osob = pobierz_dokladne_dane(wiek)
    procent = (liczba_osob / POPULACJA_POLSKI) * 100
    rok_urodzenia = AKTUALNY_ROK - wiek
    
    baza_lat = generuj_pelna_baze_historyczna()
    wydarzenie = baza_lat.get(rok_urodzenia, "Zapis w rejestrach państwowych.")
    
    emerytalna = round(brutto * 0.0976, 2)
    zdrowotna = round(brutto * 0.0777, 2)
    rentowa = round(brutto * 0.015, 2)
    chorobowa = round(brutto * 0.0245, 2)
    pit = round(brutto * 0.065, 2)
    
    suma_podatkow = round(emerytalna + zdrowotna + rentowa + chorobowa + pit, 2)
    netto = round(brutto - suma_podatkow, 2) if brutto > 0 else 0.0

    podatki = {
        "netto": f"{netto:,.2f}".replace(",", " "),
        "suma_potracen": f"{suma_podatkow:,.2f}".replace(",", " "),
        "emerytalna": f"{emerytalna:,.2f}".replace(",", " "),
        "zdrowotna": f"{zdrowotna:,.2f}".replace(",", " "),
        "rentowa": f"{rentowa:,.2f}".replace(",", " "),
        "chorobowa": f"{chorobowa:,.2f}".replace(",", " "),
        "pit": f"{pit:,.2f}".replace(",", " ")
    }

    liczba_formatowana = f"{liczba_osob:,}".replace(",", " ")
    procent_formatowany = f"{procent:.4f}"
    procent_zycia = min(round((wiek / 78.0) * 100, 1), 100.0)

    statystyki_gus = {
        "stopa_bezrobocia": 5.9,
        "urodzenia_kwartal": 57500,
        "zgony_kwartal": 112000,
        "pensja_brutto": "8 410.00",
        "inflacja": 4.5,
        "pkb_wzrost": 3.2
    }

    tabela_rocznikow = []
    for w in range(0, 101):
        r_urodz = AKTUALNY_ROK - w
        tabela_rocznikow.append({
            "wiek": w,
            "rok": r_urodz,
            "populacja": f"{pobierz_dokladne_dane(w):,}".replace(",", " "),
            "wydarzenie_pelne": baza_lat.get(r_urodz, "Zapis historyczny w kronikach krajowych.")
        })

    return render_template(
        'wynik.html', 
        wiek=wiek, rok_urodzenia=rok_urodzenia, wydarzenie=wydarzenie,
        ile_osob=liczba_formatowana, proc=procent_formatowany,
        gus=statystyki_gus, podatki=podatki, brutto=f"{brutto:,.2f}".replace(",", " "), 
        procent_zycia=procent_zycia, tabela=tabela_rocznikow
    )

if __name__ == '__main__':
    app.run(debug=True)