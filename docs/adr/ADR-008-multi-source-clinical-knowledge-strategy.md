# ADR-008: Multi-Source Clinical Knowledge Strategy

**Status**: Approved (Knowledge Architecture Freeze)  
**Date**: 2026-07-05  
**Context**: Pharma AI Knowledge Integrity & Governance  

## 1. Context
Pharma AI અનેક સ્ત્રોતોમાંથી ક્લિનિકલ ડેટા મેળવે છે. વિસંગત ડેટા અને ડાયરેક્ટ API કોલિંગ ક્લિનિકલ જોખમ નોતરી શકે છે. સિસ્ટમને વિશ્વસનીય બનાવવા માટે નોલેજ સોર્સિંગ અને વેલિડેશન લેયર અનિવાર્ય છે.

## 2. Decision
તમામ ક્લિનિકલ નોલેજ એક 'Local Master Repository' દ્વારા જ મેનેજ થશે.

### 2.1 Authorized Sources & Priority
ડેટા વિવાદ સમયે નીચે મુજબની પ્રાથમિકતા (Priority) રહેશે:
1. **PMBJK** (Primary Authority)
2. **CDSCO** (Legal Validation)
3. **WHO ATC** (Clinical Classification)
4. **OpenFDA** (Enrichment)

### 2.2 Golden Rule of Truth
**કોઈપણ external source ને "truth" માનવામાં આવશે નહીં.** ડેટા સ્થાનિક લેવલ પર વેલિડેશન પાસ કર્યા પછી જ Pharma AI નોલેજ બેઝનો ભાગ બનશે.

### 2.3 Conflict Resolution & Lifecycle
* **Conflict Resolution**: જો સોર્સ વચ્ચે વિવાદ હોય, તો ઉચ્ચ પ્રાથમિકતા (Priority) ધરાવતો સોર્સ માન્ય રહેશે.
* **Data Lifecycle**: દરેક રેકોર્ડ `NEW -> VALIDATED -> REVIEWED -> ACTIVE -> DEPRECATED` સ્ટેજમાંથી પસાર થશે.
* **Traceability**: દરેક ડેટા પોઈન્ટ માટે `Last Sync`, `Evidence Level`, અને `Reviewer` ટ્રેક કરવામાં આવશે.

## 3. Knowledge Layer Architecture
ડેટા ફ્લો નીચે મુજબ રહેશે:
`PMBJK` -> `Canonical Builder` -> `CDSCO Validation` -> `WHO Mapping` -> `OpenFDA Enrichment` -> `Clinical Validation` -> **Local Master Repository** -> `Resolver/Interaction/AI`

## 4. Future Roadmap
* **RxNorm**: આંતરરાષ્ટ્રીય મેપિંગ માટે ભવિષ્યમાં RxNorm સપોર્ટ ઉમેરવો.

## 5. Consequences
* **Clinical Integrity**: ડેટાની વિશ્વસનીયતામાં વધારો.
* **Offline Capability**: સિસ્ટમ સ્થાનિક ડેટા પર ડિપેન્ડન્ટ હોવાથી API ડાઉન હોવા છતાં કાર્યરત રહેશે.
* **Auditability**: દરેક ક્લિનિકલ નિર્ણય પાછળનો સ્ત્રોત (Provenance) ટ્રેક કરી શકાશે.

---