## 23.1-29.1

vaihdoin aiheen shakkipeliin ja sen bottiin. Asetin tavoitteeksi saada toimivan shakkipelin tällä viikolla. Onnistuin tekemään helposti pelattavan ja selvän käyttöliittymän pygamella. Pelin sisäisestä logiikasta sain tehtyä suurimman osan jo nyt, mutta shakkimatille ei vielä ole kattavaa tarkistusmetodia. nappuloiden liikkeiden laskenta sujuu kuitenkin hyvin ja ne noudattavat shakin sääntöjä. erikoissäännöistä puuttuu vielä tornitus, en passant ja tasapelin huomiointi.

shakin check tapahtuessa peli huomaa kuninkaan olevan uhanalaisena tarkistamalla kaikki mahdolliset uhka ruudut kuninkaalle. Myös kuninkaan liikkuessa huomioidaan kaikki ruudut, joita uhataan (kuninkaalla ei voi liikkua niihin). check tarkastus, joka on melko työläs, kuitenkin tehdään aina kun pelaaja haluaa liikuttaa nappulaa. (hidas) Ensi viikolle siis jää tämän prosessin optimointi sekä pelin koodin optimointi yleisellä tasolla. check tarkastusta ei tarvitsi tehdä useampaan otteeseen, jos kriittiset nappulat (nappulat, jotka ovat uhkaavan nappulan sekä kuninkaan välissä) laitetaan listaan muistiin (niitä liikutettaessa täytyy huomioidan avautuva käytävä, ja vihollisen hevosen uhkaa ei tarvitse huomoida muulloin, kun vihollisen viime liikkeen ollessa hevonen (tälle myös oma algo). Ensi viikolle jää myös testien tekeminen Game_Engine-luokalle.

Ensi viikolla on myös tarkoitus tutustua tarkemmin botin vaatimiin algoritmeihin, mutta oletan algoritmin tekemisen olevan helpompaa itse pelin koodin ollessa optimoitua joten panostan siihen ensin.

pelin voi käynnistää engine.py tiedostolla, ja ruudun kokoa voi muokata arvolla self.game_size. Ruudukon kokoa voi muokata komennolla self.table_size, mutta peli ei vielä skaalaannu käsittelemään erilaisia ruudukoita.
