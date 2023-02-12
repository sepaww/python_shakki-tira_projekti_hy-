## 6.1-12.1
- maanantaina ensimmäinen minmax versio. äärimmäisen hidas versio, joka onnistui laskemaa kolmen syvyyteen hikisesti
- tiistaina paranteluja minmaxiin
- lauantaina lisää minmax hommailua sekä muutaman bugin poisto shakista (minmax rikkoi muutaman shakin oman rakenteen)
- sunnuntaina uusi paranneltu systeemi minmaxiin, jossa lasketaan rekursiivisesti liikkeitä make_move ja unmake_move funktioiden avulla vähentäen laskennan määrää. vaihdettu liikkeiden laskemisen logiikkaa. kaunisteltu koodin rakennetta ja vähennetty turhaa koodia. lisätty kommentointi minmax koodiin.
vaikeaa on ollut minmaxin optimisointi tai sen ratkaisijen ajatteleminen. itse koodin kirjoittamiseen on kulunut vain pieni aika verrattuna ratkaisujen harkitsemiseen.

seuraavaksi dokumentoinnin ajantasalle tuonti, testien tekeminen min_maxiin jo(i)llakin valmiilla liikesarja koodilla sekä shakin parempi testaaminen vaikkapa random_bot_modelilla
