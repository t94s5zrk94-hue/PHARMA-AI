# ADR-006: Clinical Normalization Before Interaction

**Status**: Approved  
**Date**: 2026-07-05  
**Context**: Pharma AI Interaction Engine  

## 1. Context
વર્તમાન સિસ્ટમમાં પ્રોડક્ટના નામ કે સ્ટ્રેન્થના આધારે ઇન્ટરેક્શન તપાસવાની શક્યતા છે, જે ક્લિનિકલ રીતે જોખમી છે. ઇન્ટરેક્શન હંમેશા ઘટકો વચ્ચે હોય છે, ઉત્પાદનો વચ્ચે નહીં. ક્લિનિકલ સચોટતા જાળવવા માટે પ્રોડક્ટ-સેન્ટ્રિક અભિગમને નોલેજ-સેન્ટ્રિકમાં બદલવો અનિવાર્ય છે.

## 2. Decision
તમામ ડ્રગ ઇન્ટરેક્શન મૂલ્યાંકનો **નોર્મલાઇઝ્ડ જેનરિક ઘટકો (Normalized Generic Ingredients)** પર જ ચલાવવામાં આવશે.

### 2.1 Normalization Pipeline
કોઈપણ ઇન્ટરેક્શન તપાસતા પહેલા, ડેટા નીચેના પાઇપલાઇનમાંથી પસાર થશે:
`User Input` -> `Normalizer` -> `Alias Resolver` -> `Brand Resolver` -> `Generic Resolver` -> `Generic_ID` -> `Interaction Engine`

### 2.2 Combination Drugs Strategy
જો ઇનપુટમાં કોમ્બિનેશન ડ્રગ્સ (દા.ત. Telmisartan + Amlodipine) હોય, તો સિસ્ટમ દરેક ઘટકનું અલગ-અલગ મૂલ્યાંકન કરશે:
`Interaction([Telmisartan, Amlodipine], [Warfarin])` -> `(Telmisartan × Warfarin)` + `(Amlodipine × Warfarin)`

### 2.3 Confidence & Audit
* **Confidence Score**: ઇન્ટરેક્શન પહેલાં `Resolver` નો કોન્ફિડન્સ સ્કોર તપાસવામાં આવશે. જો સ્કોર લો હોય, તો યુઝર કન્ફર્મેશન લેવામાં આવશે.
* **Audit Trail**: દરેક ઇન્ટરેક્શન માટે: `Input` -> `Normalized To` -> `Generic_ID` -> `Interaction Rule` -> `Result` નું ઓડિટ લોગ જાળવવામાં આવશે.

## 3. Consequences

### Positive (ફાયદા)
* **Clinical Consistency**: બ્રાન્ડ કે ફોર્મ્યુલેશન બદલાવા છતાં ક્લિનિકલ પરિણામો સમાન રહેશે.
* **Scalability**: નવા ઇન્ટરેક્શન રૂલ્સ લખવાની જરૂર નહીં પડે, માત્ર જેનરિક મેપિંગ પૂરતું રહેશે.
* **Reduced Complexity**: એન્જિન ક્લિનિકલ નોલેજ પર ધ્યાન કેન્દ્રિત કરશે.

### Negative (પડકારો)
* **Mapping Overhead**: ડેટાબેઝ ક્લીનિંગ અને એક્યુરેટ મેપિંગ માટે પ્રારંભિક પ્રયત્નો જરૂરી છે.
* **Override Logic**: જે ડ્રગ્સ ફોર્મ્યુલેશન-સ્પેસિફિક ઇન્ટરેક્શન ધરાવે છે, તેના માટે અલગ ઓવરરાઈડ લોજિક ડેવલપ કરવું પડશે.

---