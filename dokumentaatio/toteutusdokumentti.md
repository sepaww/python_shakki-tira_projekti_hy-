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
      src "*" -- ui
       src "*" -- services
        src "*" -- repositories
        src "*" -- tests
         ui "*" -- screen
         ui "*" -- inputs
         ui "*" -- tools
         services "*" -- day_change_op
         services "*" -- ending_screen_op
         services "*" -- finance
         
      class src{
          }
      class tests{
      all tests
          }
      class ui{
          }
      class services{
          }
      class repositories{
      database_op.py
      stats.py
          }
      class day_change_op{
      day_change_operator.py
      day_change.py
          }
      class screen{
      draw_ending.py
      draw_screen.py
      draw_start_screen.py
          }
      class inputs{
      start_inputs.py
      end_inputs.py
      inputs.py
          }
      class tools{
      draw_highlight.py
      draw_normal.py
          }
      class ending_screen_op{
      ending_init.py
      
          }
      class finance{
      effects.py
      finance.py
      items.py
      stock_creator.py
      stock_history.py
          }
