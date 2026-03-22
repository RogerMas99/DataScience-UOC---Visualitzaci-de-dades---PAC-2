# DataScience-UOC---Visualitzaci-de-dades---PAC-2

Aquest repositori recull tres visualitzacions creades per avaluar l'adequació de diferents representacions gràfiques segons la naturalesa de les dades i l'objectiu comunicatiu.

## 1. Force-Directed Graph: Interaccions (Xarxa de Dofins)
[**Obrir Visualització Interactiva**](ForceDirected_Graph_Dolphins.html) | [Codi Font](Codi_ForceDirected_Graph.py)

**Tècnica i Origen:** Els grafs dirigits per forces posicionen els nodes d'una xarxa simulant sistemes físics (repulsió entre nodes i atracció entre arestes). Aquesta aproximació prové de la integració d'algorismes de simulació física a la teoria de grafs durant els anys vuitanta (ex. Fruchterman-Reingold).
**Característiques i Dades:** Requereixen dades relacionals (nodes i enllaços, sovint ponderats o direccionals). Són òptims per revelar l'estructura topològica, clústers i nodes influents en xarxes complexes. El seu principal inconvenient és el risc d'esdevenir inintel·ligibles (efecte *hairball*) quan el volum de nodes i arestes és massa elevat.
**Anàlisi:** [Escriu breument què representa aquesta xarxa concreta, l'objectiu de descobriment i què hi destaques].

---

## 2. Sparklines: Evolució Borsa (Top 10 IBEX 35)
![Sparklines IBEX 35](Sparklines_Top10_IBEX35.png)
[Codi Font](Codi_Sparkline.py)

**Tècnica i Origen:** Terme formalitzat per Edward Tufte l'any 2006, definint-los com a gràfics de mida paraula, intensos en dades i sense marcs de coordenades explícits.
**Característiques i Dades:** Utilitzen dades quantitatives estructurades en sèries temporals. La seva gran fortalesa és la capacitat de mostrar la variància i les tendències generals de múltiples variables simultàniament ocupant un espai mínim (alta densitat de dades). La limitació inherent és la impossibilitat d'extreure valors absoluts precisos, ja que prescindeixen d'eixos detallats.
**Anàlisi:** [Escriu aquí la justificació de l'ús d'aquesta tècnica per a les cotitzacions i la conclusió extreta].

---

## 3. Timeline: Cronologia (Cursa Espacial)
![Timeline Space Race](Timeline_Space_Race.png)
[Codi Font](Codi_Timeline.py)

**Tècnica i Origen:** Tècnica clàssica de representació cronològica lineal que va ser popularitzada a gran escala per figures com Joseph Priestley al segle XVIII per mapejar la història.
**Característiques i Dades:** Consumeixen dades temporals (marques de temps discretes o intervals) vinculades a variables qualitatives (esdeveniments). Faciliten enormement la comprensió de relacions de precedència, ritme i simultaneïtat. L'inconvenient principal és la dificultat de gestió de l'espai quan els esdeveniments s'aglomeren en finestres de temps molt curtes.
**Anàlisi:** [Comenta què emfatitza aquesta línia de temps concreta i per què és la representació adequada].
