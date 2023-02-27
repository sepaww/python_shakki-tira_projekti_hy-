## Ohjelman rakenne

työn aiheena on shakki sekä siihen sopiva minmaxia hyödyntävä shakki ai.
ohjelman rakenne voidaan jakaa raa'asti:
- engine.py, joka hallitsee shakkipeliä sekä hoitaa voitto tarkistukset.
- bot_model.py tiedostot, jotka kaikki esittävät jotakin ai mallia (näistä ainoa oikeasti järkevä on minmax)
- false_engine.py, jota bot_modelit hyödyntävät laskeakseen liikkeitä taikka hyödyntääkseen muita funktioita, jotka eivät ole niiden saatavilla enginessä hierarkian vuoksi.
- inputs.py, joka mahdollistaa shakin pelaamisen ihmisenä
- visuals.py, joka pygame libraryn avulla tuottaa pelistä graafisen käyttöliittymän käytettävyyden parantamiseksi.

## luokkakaavio pelin sisäisten tiedostojen suhteesta
 ```mermaid
 classDiagram
      ui -- visuals
      ui -- inputs
      engine -- visuals
      visuals -- inputs
      engine -- minmax_bot_model
      engine -- tunnelvision_bot_model
      engine -- rand_bot_model
      minmax_bot_model -- visuals
      engine -- player
      minmax_bot_model -- false_engine
      rand_bot_model -- false_engine
      tunnelvision_bot_model -- false_engine
         
      class ui{
          }
      class tests{
      }
      class visuals{
          }
      class inputs{
          }
      class minmax_bot_model{
      }
      class  player{
      }
      class tunnelvision_bot_model{
      }
      class rand_bot_model{
      }
      class false_engine{
      }
```
## Toiminta selitettynä lyhyesti
Engine.py on korkeimmalla sovelluksen hierarkiassa. sen tehtäviä on muunmuassa pelin ylläpito, liikkeiden haku, muiden tiedostojen kutsuminen sekä bottien antamien liikkeiden (tai pelaajan) toteuttaminen. Kun siirto on toteutettu engine.py tarkastaa onko liikkeestä seurannut shakki (uhka). Jos on, tarkastetaan onko kyseessä matti vai voiko uhattu pelaaja selvitä shakista jollakin liikkeellä. engine.py myös tarkastaa voiko pelaaja liikkua vai ei. Jollei, niin seuraa tasapeli. engine.py ilmoittaa havainnoistaan komentoriville. Huom! engine.py ei tarkasta vastaanottamansa botin liikkeen laillisuutta, vaan olettaa sen olevan laillinen. engine.py:n voi käynnistää eri tavoin riippuen millä arvoilla GameEngine luokka käynnistetään. pelaajat määritetään "bot" stringin avulla voidaan ilmoittaa, että pelaaja on botti ja seuraavalla numero arvolla, mikä malli. minmaxin saa arvolla 2.

minmax_bot_model.py perustuu minmax algoritmin perusteella toimivaan parhaan liikkeen etsintään. minmax käy läpi kaikki mahdolliset liikkeet, ja valitsee niistä parhaan lopputuloksen annettuun syvyyteen asti. syvyyttä voi muokata muuttamalla arvoa self.depth (suositellaan 3 tai 4 tai 5. mitä suurempi sitä hitaampi). Minmaxia on kuitenkin optimoitu alpha-beta karsinnalla, joka poistaa turhien liikkeiden läpikäyntiä. Näin tapahtuu kun tiedetään, että on jo olemassa parempi vaihtoehto kyseisen liikkeen sijaan. jokainen mahdollinen alkuperäisen syvyyden nappulan paras liike talletetaan self.best_moves listaan, josta heapq:n avulla valitaan parhaan arvon tuottava siirto. valittu siirto palautetaan tietyssä tuple muodossa engine.py:lle, josta voidaan lukea siirrettävä nappula sekä sen päämäärä.

false_engine.py on suurimmilta osiltaan täysi kopio engine.py:stä, mistä on poistettu osa enginen funktioista. sen tehtävä on tarjota engine.py funktioita, kuten liikeiden löytämistä boteille. Hierarkian takia botit eivät pääse käsiksi enginen ominaisuuksiin, joten false_engine.py korjaa tämän virheen.

## Puutteet
- Minmax botti ei huomioi tiettyjä shakin erikoissiirtoja. Esimerkiksi tornittaminen.
- Alpha-Beta karsinnan ansiosta laskenta syvyyttä on voitu nostaa viiteen. Se kuitenkin saattaa aiheuttaa kriittisiä mokia. Esimerkiksi tilanteessa, jossa vihollisen paras liike on välttää sotilaan syöminen omalla sotilaallaan jää huomioimatta, sillä botti arvioi sotilaan syömisen olevan paras mahdollinen siirto. Tästä syystä syömisen välttämistä seuraavan tilanteen paremmuutta ei ikinä tulla huomioimaan, koska sitä pidetään turhana laskentana.
- Koodin hierarkisuuden takia tiedosto false_engine on hieman epäselvä Yleisesti myös engine on melko kookas ja vaikka olen yrittänyt käyttää järkevää nimentää on se loppujen lopuksi melko epäselvä.
- Tilanteissa, joissa ei laskentasyvyyden riittämättömyyden takia löydetä yhtään hyviä siirtoja, tai kaikki siirrot ovat yhtä hyviä, botti voi tehdä älyttömiltä tuntuvia päätöksiä, esim siirtää yhden verran lähettiä reunaan järkevän keskustaa valloittavan siirron sijaan.

## Lähteet
- kurssimateriaali, erityisesti pdf minmaxista
