from typing import List, Dict, Set
from pharma_ai.models.finding import Finding, FindingCategory, RecommendationStatus

class ConflictResolver:
    """
    Applies clinical precedence rules to a list of Findings.
    Uses a policy-driven approach to ensure deterministic outcomes.
    """
    
    # Priority Policy
    PRIORITY_MAP: Dict[FindingCategory, int] = {
        FindingCategory.CONTRAINDICATION: 100,
        FindingCategory.INTERACTION: 90,
        FindingCategory.PREGNANCY: 80,
        FindingCategory.LACTATION: 75,
        FindingCategory.RENAL: 70,
        FindingCategory.HEPATIC: 65,
        FindingCategory.DOSAGE: 60,
        FindingCategory.MONITORING: 40,
        FindingCategory.ADVERSE_EFFECT: 30,
    }

    def resolve(self, findings: List[Finding]) -> List[Finding]:
        if not findings:
            return []

        # 1. Group findings by category
        grouped: Dict[FindingCategory, List[Finding]] = {}
        for f in findings:
            grouped.setdefault(f.category, []).append(f)

        # 2. Identify all categories that contain a REJECTED finding
        # These act as 'blockers' for all lower-priority categories.
        veto_categories: Set[FindingCategory] = {
            cat for cat, items in grouped.items()
            if any(f.recommendation_status == RecommendationStatus.REJECTED for f in items)
        }

        # 3. Filter and resolve findings
        resolved_findings: List[Finding] = []
        for category, items in grouped.items():
            category_priority = self.PRIORITY_MAP.get(category, 0)
            
            # Check if any higher-priority category is currently a VETO blocker
            is_suppressed = False
            for blocker_cat in veto_categories:
                if self.PRIORITY_MAP.get(blocker_cat, 0) > category_priority:
                    is_suppressed = True
                    break
            
            if not is_suppressed:
                resolved_findings.extend(items)

        # 4. Return sorted by priority (Descending)
        return sorted(resolved_findings, key=lambda f: self.PRIORITY_MAP.get(f.category, 0), reverse=True)