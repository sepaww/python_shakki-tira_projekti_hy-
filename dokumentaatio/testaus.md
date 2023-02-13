# Testaus
Ohjelman toiminnalisuudesta on tehty testit itse shakki pelin siirtojen toiminnan testaamiseen.
Yksi laajempi testi, jossa testataan kuninkaan uhkaamista, ja siihen liittyvien toimintojen toimintaa.
toinen testi, joka testaa kaikkien muiden, paitsi kuninkaan ja sotilaan liikkeitä
kolmas testi, joka testaa sotilaiden liikkeitä

![image](https://user-images.githubusercontent.com/117186747/216830037-0d4c6429-4655-4d57-9886-7a631c9ae096.png)

## Minmax
Minmaxiin perustuvan shakki ai:n tehokkuutta on testattu satunnaisilla pelitilanteilla, ja eri syvyyksillä stress_tests.py tiedoston avulla. Koodissa luodaan kuvitteellinen tilanne, ja minmax bottia pyydetään keksimään annettuun pelitilanteeseen paras mahdollinen liike eri syvyyksillä. testitulokset perustuvat 10 syklin keskiarvoihin syvyyksillä 1-5:

![image](https://user-images.githubusercontent.com/117186747/218524498-08f4c503-dd9b-4abf-bcbf-593807fbf3cb.png)

### Taulukko
kymmenen testauskerran keskiarvot järjestettynä laskenta tavan mukaan:
- tapa 1: pelilaudasta on täytetty noin 1/4 satunnaisilla nappuloilla
- tapa 2: pelilaudasta on täytetty noin 1/8 satunnaisilla nappuloilla
- tapa 3: laskenta on suoritettu perustuen bottia vastaan pelattujen botin käyttämien vuorojen ajan keskiarvo


| laskenta syvyys | laskenta tapa 1 | laskenta tapa 2 | laskenta tapa 3 |
|---|---|---|---|
| 1 | 0.0032   | 0.0100   | 0.004    |
| 2 | 0.0107   | 0.01384  | 0.00805  |
| 3 | 0.1384   | 0.0450   | 0.078    |
| 4 | 2.1726   | 0.5701   | 0.836    |
| 5 | 37.6610  | 6.3011   | 15.6196  |


