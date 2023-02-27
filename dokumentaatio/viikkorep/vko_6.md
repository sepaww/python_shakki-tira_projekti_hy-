## 20.2-26.2
- tällä viikolla ei hirveästi uutta. aikaa mennyt muihin kursseihin ja peli ja botti ovat jo hyvällä mallilla
- lauantaina muutama bugifiksi ja yksi testi korjattu toimivaksi. shakkiin lisätty myös undo ominaisuus, jolla voi perua kaikki tehdyt liikkeet 2 kerrallaan. vertaisarviointi. minamx tajuaa nyt myös sotilaan toiseen päätyyn pääsyn uhan
- haastavaa oli huomioida tornitus undon liike historiassa. ratkaistu lisäämällä vuoron liikkeet listaan, jossa ne ovat tuplejen sisällä. yleensä vuoron listan sisällä vain yksi liike mutta tornittaessa vuoron listaan lisätään myös tornin liike.
- heitetään nyt tähän vielä maanantai: undossa oli useampi ajatusvirhe. se ei päivittänyt nappuloiden Tile() luokan .i ja .j koordinaatti muuttujia taikka päivittänyt kuninkaan uhan tarkistusta undon jälkeen. Yllämainitut ongelmat nyt toivonmukaan korjattu (ainakin omaan manuaaliseen testaukseen perustuen)
