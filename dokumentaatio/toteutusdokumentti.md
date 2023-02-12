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
      ui -- visuals
      ui -- inputs
      engine -- visuals
      visual -- inputs
      engine -- rand_bot_model
      engine -- tunnelvision_bot_model
      engine -- minmax_bot_model
      minmax_bot_model -- false_engine
      rand_bot_model -- false_engine
      tunnelvision_bot_model -- false_engine
         
      class ui{
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
