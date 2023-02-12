## Ohjelman rakenne

työn aiheena on shakki sekä siihen sopiva minmaxia hyödyntävä shakki ai.
ohjelman rakenne voidaan jakaa raa'asti:
- engine.py, joka hallitsee shakkipeliä sekä hoitaa voitto tarkistukset.
- bot_model.py tiedostot, jotka kaikki esittävät jotakin ai mallia (näistä ainoa oikeasti järkevä on minmax)
- false_engine.py, jota bot_modelit hyödyntävät laskeakseen liikkeitä taikka hyödyntääkseen muita funktioita, jotka eivät ole niiden saatavilla enginessä hierarkian vuoksi.
- inputs.py, joka mahdollistaa shakin pelaamisen ihmisenä
- visuals.py, joka pygame libraryn avulla tuottaa pelistä graafisen käyttöliittymän käytettävyyden parantamiseksi.

## luokka kaavio pelin sisäisten tiedostojen suhteesta
 ```mermaid
 classDiagram
      ui -- visuals.py
      ui -- inputs.py
      engine.py -- visuals.py
      visual.py -- inputs.py
      engine.py -- rand_bot_model.py
      engine.py -- tunnelvision_bot_model.py
      engine.py -- minmax_bot_model.py
      minmax_bot_model.py -- false_engine.py
      rand_bot_model.py -- false_engine.py
      tunnelvision_bot_model.py -- false_engine.py
         
      class ui{
          }
    
      class visuals{
          }
      class inputs.py{
          }
      class minmax_bot_model.py{
      }
      class  player.py{
      }
      class tunnelvision_bot_model.py{
      }
      class rand_bot_model.py{
      }
      class false_engine.py{
      }
```
