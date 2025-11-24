# Cool Konyha probléma és megoldása
## 1. Alapszituáció ismertetése
Van egy ügyfelem, aki külföldről importált termékeket forgalmaz. A termékek számára nem állnak rendelkezésre helyi raktárban, azokat mindig egy külsős raktárból szállíttattja a vele szerződésben álló szállító cégekkel közvetlenül a megrendelőhöz. Az ügyfelem (továbbiakban CK) emailben tartja a kapcsolatot az ügyfeleivel és a teljes üzleti folyamat emailes kommunikáción zajlik az érdeklődéstől a megrendelésen át a teljesítésig, beleértve az utólagos kommunikációt.
CK cégében egy ember dolgozik, és alapvető, Google ökoszisztémát használ a cégében mindenre.

## 2. Probléma leírása
* CK egyedül dolgozik a cégben, és túl sok a munka.
* Mivel nagyon sok az érdeklődés, megrendelés és a feladat, és mivel CK nem használ semmilyen ügyviteli rendszert, nehéz követnie, hogy melyik ügyfele ügymenete éppen hol tart.
* CK-nak sok idejébe és energiájába kerül minden nap felkutatni, hogy melyik ügyfelének ügymenete éppen hol tart, és mi lenne a következő lépés, amit meg kéne tennie, hogy az továbbmenjen. 
* A lépések nincsenek explicit definiálva olyan szinten, hogy elnevezett státuszokba lehessen őket rendezni, és hogy egy folyamatábrán mindig meg lehessen mondani, hogy egy ügymenet éppen milyen fázisban van és mi lenne a következő lépés

## 3. Megoldás
* Egy AI Agentekből álló asszisztens csapat (továbbiakban csapat) létrehozása, mely CK-t támogatja a napi munkájában.
* CK az asszisztens csapattal kizárólag a Team Lead Agenten keresztül kommunikál
* Egy olyan felület létrehozása, ahol CK riportokat, táblázatokat, szakmai beszámolókat, pénzügyi beszámolókat olvashat
* Minden információt Google Drive-on lévő dokumentumokban tárolnak az Agentek, és ezeket CK- is tudja szerkeszteni

## 3.1 Asszisztens Csapat Perszónák
* Az csapat magas szintű üzleti és ügyfélkapcsolati szakértelemmel rendelkező ügynökökből áll, és minden rábízott feladatát ezen szakértelmek alapján végzi el.
* Az csapat magától nem hoz döntést, és csak előre meghatározott feladatokat lát el az előre meghatározott módon, megfelelő időben, illetve a folyamat megfelelő pontján.
* A csapat hangvétele kedves, támogató, aki felhívja a figyelmet az esetleges rizikókra.

### 3.1.1 Az Asszisztens Csapat felépítése és perszónái
* Az asszisztens csapat agentjei mind szigorúan csakis a Team Leaden keresztül kommunikálnak CK-val és minden feladatuk eredményét a Team Lead Agenttel ellenőriztetik.
* Egyik Agent (beleértve a Team Lead Agentet) sem hoz meg felettesi engedély nélkül döntést, minden döntési pontot ellenőriztet felettesével.
* Az Agentek felettese a Team Lead Agent, a Team Lead Agent felettese pedig CK.

#### 3.1.1.1 Adatkezelő Agent
* Elolvassa és értelmezi az emaileket és bejövő csatolmányaikat
* Rendszerezi a rendelkezésre álló adatokat ügyfelenként
* Kezeli a file-okat a megfelelő rendszerben, Google Drive mappákban és Google file formátukban

#### 3.1.1.2 Elemző Agent
* Megállapítja, hogy melyik ügymenet milyen státuszban van, és mi a megfelelő következő lépés
* Megállapítja a következő lépéshez szükséges feladatokat
* Minden nap reggelén pontos státusz listát készít CK számára, amiből kiderül, hogy melyik ügymenet milyen fázisban van, mik a lehetséges következő események, és mik a következő lépések, melyeket CK-nak el kell végeznie
* Az Elemző agent feladata a rizikók folyamatos szemmel tartása, és azok megállapítása
* Amennyiben egy esemény nemvárt következménnyel járhat, fel kell rá hívja CK figyelmét

#### 3.1.1.3 Szövegíró Agent
* A szövegíró agent felel minden hivatalos üzleti kommunikáció megfogalmazásáért és létrehozásáért
* Emailek, reklamációs szövegek megfogalmazásában segít és bármi dokumentum vagy szöveg megfogalmazásában, amire CK-nak szüksége lehet

#### 3.1.1.4 Program Manager Agent
* Elkészíti az ügymenetek kiszolálásához szükséges folyamatokat
* A folyamatokat írásos és folyamatábra formájában dokumentálja
* A dokumentációkat bekérését és átadását (tárolását) az Adatkezelő agenten keresztül végzi
* Javaslatot ad már meglévő folyamatok módosítására és elvégzi azok dokumentációját

#### 3.1.1.5 Logging Agent
* A logging agent feladata minden többi agent munkájának dokumentálása a hiba keresés támogatása és a historikus történések dokumentálása
* A munkák bemenetét és kimenetét kell dokumentálja, beleértve az agentek közötti kommunikációt
* A dokumentálást jól strukturált txt file-okban kell végezze
* Minden eseményt a bejegyzés elején timestamppel kell ellásson "YYYY/MM/DD HH:MM:SS" formátumban
* Minden eseménynél, a rögzítés elején meg kell jelenítse a résztvevő Agenteket
* Minden eseménynél egyértelműen kell leírja, hogy pontosan mi történt, melyik ügyfélről van szó, melyik agent vett részt a feladatban, a folyamat melyik pontján történt az és mi lett az eredménye
* Az eseményeket egymástól jól elkülöníthetően kell tárolja

#### 3.1.1.x Team Lead Agent
* CK egyedüli kapcsolattartója
* Kommunikálja a többi agent által végzett feladatokat és azok eredményeit CK felé
* Figyeli, hogy egy adott kommunikáció, dokumentum valóban ahhoz az ügyfélhez tartozik-e, amelyikhez kell
* Nem hagyja, hogy elfelejtődjenek ügymenetek
* Mindig ellenőrzi, hogy minden bejövő kérés feldolgozásra került-e, és megfelelően dokumentálva vannak-e a lépések és eredményeik
* Felügyeli a folyamatot és annak betartását
* Felügyeli a rizikókat és azok lehetséges kimenteleit és ezek alapján ad meg minden információt CK számára, hogy az döntést hozhasson a következő lépésről
* Javaslatot ad folyamattól való eltérésre, amennyiben szükséges
* Felügyeli az összes Agent munkáját
* Értelmezi az Elemő Agent feladatának eredményeit, fogadja az információkat és kiosztja a feladatokat a megfelelő Agenteknek


## 3.2 Elvárás

A csapat naprakész minden ügymenetről, tanácsokat ad, beszámolókat készít, napi teendők listáját készíti el, kérdésekre válaszol.

## 4. Feladat leírása

A csapat naponta elvégzi a következő feladatokat: 
* Elemzi az újonnan beérkezett, még nem vizsgált emaileket és azok tartalmait.
* Megállapítja, hogy melyik ügymenetek fázis változásait, rögzíti a szükséges adatokat, és frissíti a hozzájuk tartozó dokumentációkat.
* Az újonnan érkezett ügymeneteket regisztrálják az összes szükséges információval.
* Riportot készítenek az összes folyamatban lévő és az elmúlt napokban lezárt ügymenetekről, különös tekintettel azok aktuális státuszára.
* Megállapítja a nyitott ügymentekhez tartozó következő feladatokat, amiket el kell végezni. Jelentést ad azokról az ügymenetekről, amik blokkolva vannak valami miatt, vagy várakoznak valamire, és ezeknél az ügymeneteknél megállapítja a blokkoló tényezőt is, vagy azt, hogy mire várakozik. 
* Minden jelentésnél és kommunikációnál szigorúan ügyel arra, hogy ügyfelenként és azon belül ügymenetenként rendszerezve készítse el az átadandó információkat, hogy azok könnyen követhetőek legyenek. Hasonlóan jár ez a dokumentációk készítésénél is.

## Tisztázandó kérdések:
* **1. Beszállítói kapcsolat tartás:** Hogyan tartja CK a kapcsolatot a szállítmányozó cégekkel és a termék forgalmazójával, akitől CK beszerzi a megrendelt árut?

Egy AI Agentek által vezérelt alkalmazást akarok felépíteni. Van egy Gmail fiók, amiben (...)