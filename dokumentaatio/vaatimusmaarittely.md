## Tehtävänä toteuttaa shakkipeli siihen kuuluvalla pelilogiikalla ja pelin sisäinen shakkibotti.

## Käyttöliittymä
- Käyttöliittymä toteutetaan python kirjaston pygame avulla. Pelissä tulee olla graafinen käyttöliittymä, joka päivittyy peli tilanteen mukaan.
- Pelaajan tulee voida pelata shakkia hiirellä robottia vastaan. Pelaajan valitessa nappulan täytyy sen mahdolliset liikkeet esittää ruudulla pelaajalle.
- Nappulat toteutetaan joko pikselitaiteena, joka liitetään pelin tiedostoihin tai matriisista lukemalla pygamen komennoilla.

## Pelin sisäinen logiikka
- Pelin tulee noudattaa shakin sääntöjä
- peli toteutetaan python koodilla hyödyntäen olio pohjaista koodia
- Pelin sisäinen shakkibotti toteutetaan min-max algoritmilla
- Voiton taikka shakin tapahtuessa pelin tulee ilmoittaa siitä käyttäjälle.
- Pelin voi aloittaa uudelleen r näppäimellä

## Testaus
- Pelin koodiin tehdään kattavat ja järkevät yksikkötestit sekä isompaa kokonaisuutta testaavat testit.

## Näkymät
- Pelin rakenne koostuu aloitusruudusta, josta pelaaja voi valita haluamansa pelitilan:
  - eri pelitiloja on joko yksinpeli bottia vastaan, pelaaja vastaan pelaaja tai botti vastaan botti
  - Pelaaja voi myös valita yksinpelissä onko tämä musta vai valkoinen
- Itse pelinäkymä tulee olla tavallisen shakin näköinen
