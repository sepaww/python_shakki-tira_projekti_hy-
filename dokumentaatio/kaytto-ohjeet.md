## Käyttö ohjeet:

### asennus
- siirry valitsemaasi kansioon
- komennolla "git clone https://github.com/sepaww/tira_projekti" kloonaa tiedostot kansioon
- komennolla "poetry install" asennat pelin tarvitsemat riippuvuudet
- komennolla "poetry run invoke start" voit käynnistää pelin

### konfigurointi
- peliä voi pelata joko itsekseen molemmilla puolilla tai bottia vastaan. Myös kahden botin välinen peli on mahdollinen joskin saattaa jumittua johonkin tilanteeseen, jossa kumpikaan botti ei halua siirtää.
- engine.py viimeinen rivi käynnistää sovelluksen, ja muokkaamalla sen parametreja voi vaihtaa peli muotoa. Komento on muotoa: (eka pelaaja, toka pelaaja, käynnistetäänkö peli, aloittaja (0=valkoinen alhaalla, 1=valkoinen ylhäällä))
  - pelaajat koostuvat tiedoista (onko pelaaja botti ("bot") vai pelaata (mitä vain paitsi bot), mahdollisen botin mallin id (minmax id = 2)

### itse pelin pelaaminen
- peliä voi pelata hiirellä graafisen käyttöliittymän ansiosta.
- painamalla nappulaa hiirellä saa näkyviin sen mahdolliset liikkeet. painamalla mahdollisen liikkeen ruutua saa nappulan liikkumaan ruutuun.
- r näppäimellä voi palauttaa pelin lähtotilanteeseen
- u näppäimellä voi perua viimeisimmät 2 siirtoa kerrallaan
- peli ilmoittaa command riville pelin tilanteen, esim. onko tullut shakki tai shakkimatti
