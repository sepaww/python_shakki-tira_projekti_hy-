## 20.2-26.2
- tällä viikolla ei hirveästi uutta. aikaa mennyt muihin kursseihin ja peli ja botti ovat jo hyvällä mallilla
- lauantaina muutama bugifiksi ja yksi testi korjattu toimivaksi. shakkiin lisätty myös undo ominaisuus, jolla voi perua kaikki tehdyt liikkeet 2 kerrallaan. vertaisarviointi.
- haastavaa oli huomioida tornitus undon liike historiassa. ratkaistu lisäämällä vuoron liikkeet listaan, jossa ne ovat tuplejen sisällä. yleensä vuoron listan sisällä vain yksi liike mutta tornittaessa vuoron listaan lisätään myös tornin liike.
