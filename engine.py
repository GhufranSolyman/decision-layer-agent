import json
from models import ProposedAction, ActionContext, DecisionResult, Verdict, Reversibility, AuditRecord

class DecisionEngine:
    def __init__(self, audit_file="audit_trail.jsonl"):
        self.audit_file = audit_file

    def evaluate(self, action: ProposedAction, context: ActionContext) -> DecisionResult:
        # حساب الإشارات (Signals Engine)
        confidence, risk, reversibility, evidence, missing_info = self._calculate_signals(action, context)
        
        # مصفوفة اتخاذ القرار (Decision Logic Matrix)
        verdict = Verdict.EXECUTE
        reasoning = ""

        # القواعد الأمنية للقرار
        if risk > 0.8 and reversibility == Reversibility.NONE:
            verdict = Verdict.REFUSE
            reasoning = "خطر مرتفع جداً والإجراء غير قابل للتراجع نهائياً."
            
        elif len(missing_info) > 0 and risk > 0.4:
            verdict = Verdict.ASK
            reasoning = f"يوجد نقص في المعلومات الأساسية: {', '.join(missing_info)}"
            
        elif risk > 0.6 or (context.user_role != "admin" and risk > 0.3):
            verdict = Verdict.ESCALATE
            reasoning = "المخاطر تتجاوز صلاحيات المستخدم الحالي؛ يتطلب تصعيداً بشرياً."
            
        elif confidence < 0.5:
            verdict = Verdict.DEFER
            reasoning = "مستوى الثقة منخفض، يتم تأجيل القرار لحين جمع أدلة أكثر."
            
        else:
            verdict = Verdict.EXECUTE
            reasoning = "المخاطر مقبولة، الثقة عالية، والإدلة كافية للتنفيذ المباشر."

        result = DecisionResult(
            verdict=verdict,
            confidence_score=confidence,
            risk_score=risk,
            reversibility=reversibility,
            evidence_used=evidence,
            missing_info=missing_info,
            reasoning=reasoning
        )

        # حفظ في سجل التدقيق (Audit Trail)
        self._log_audit(action, context, result, confidence, risk)
        return result

    def _calculate_signals(self, action: ProposedAction, context: ActionContext):
        # هنا يتم حساب المخاطر حسب كل قطاع (Domain Rules)
        evidence = []
        missing_info = []
        risk = 0.1
        confidence = 0.95
        reversibility = Reversibility.HIGH

        # 1. قطاع المبالغ المستردة (Refund Approval)
        if action.domain == "refund":
            amount = action.parameters.get("amount", 0)
            evidence.append(f"مبلغ الاسترداد المطلوبة: ${amount}")
            
            if amount > 1000:
                risk = 0.85
                reversibility = Reversibility.LOW
            elif amount > 200:
                risk = 0.5
                reversibility = Reversibility.MEDIUM
                
            if "receipt_attached" not in action.parameters:
                missing_info.append("إيصال الشراء الأصلي")

        # 2. قطاع نشر الكود (Code Deploy)
        elif action.domain == "code_deploy":
            env = action.parameters.get("environment", "staging")
            reversibility = Reversibility.MEDIUM
            evidence.append(f"البيئة المستهدفة: {env}")
            
            if env == "production":
                risk = 0.9
                reversibility = Reversibility.LOW
                if not action.parameters.get("tests_passed", False):
                    missing_info.append("تقرير إكمال الاختبارات التلقائية (CI/CD)")
                    confidence = 0.4

        # 3. قطاع إدارة التذاكر (Ticket Triage)
        elif action.domain == "ticket":
            priority = action.parameters.get("priority", "low")
            if priority == "urgent":
                risk = 0.4
            reversibility = Reversibility.HIGH
            evidence.append(f"درجة الأهمية: {priority}")

        return confidence, risk, reversibility, evidence, missing_info

    def _log_audit(self, action: ProposedAction, context: ActionContext, result: DecisionResult, confidence: float, risk: float):
        audit_entry = AuditRecord(
            inputs={"action": action.dict(), "context": context.dict()},
            signals={"confidence": confidence, "risk": risk},
            decision=result
        )
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_entry.dict(), ensure_ascii=False) + "\n")