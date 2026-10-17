from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# 1. القرارات الستة المتاحة
class Verdict(str, Enum):
    EXECUTE = "execute"
    ASK = "ask"
    DEFER = "defer"
    ESCALATE = "escalate"
    REFUSE = "refuse"

# 2. مستويات قابلية التراجع
class Reversibility(str, Enum):
    HIGH = "high"       # يمكن إلغاء الفعل بسهولة
    MEDIUM = "medium"   # يتطلب جهداً لإلغائه
    LOW = "low"         # صعب التراجع عنه
    NONE = "none"       # لا يمكن التراجع عنه نهائياً (مثل حذف قاعدة بيانات)

# 3. هيكل الإجراء المقترح (Proposed Action)
class ProposedAction(BaseModel):
    domain: str                     # القطاع (مثلاً: refund, code_deploy, ticket)
    action_type: str                # نوع الإجراء (مثلاً: process_refund)
    parameters: dict                # التفاصيل (المبلغ، السيرفر، رقم التذكرة...)

# 4. السياق (Context)
class ActionContext(BaseModel):
    user_id: str
    user_role: str                  # دور المستخدم (admin, customer, junior_dev)
    historical_data: dict = {}      # سجل سابق أو معلومات إضافية
    environment: str = "production" # بيئة العمل (production, staging)

# 5. نتيجة القرار مع الـ Metadata المطلوبة كاملة
class DecisionResult(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    verdict: Verdict
    confidence_score: float         # من 0.0 إلى 1.0
    risk_score: float               # من 0.0 إلى 1.0
    reversibility: Reversibility
    evidence_used: List[str]        # الأدلة اعتمد عليها
    missing_info: List[str]         # المعلومات الناقصة إن وجدت
    reasoning: str                  # التفسير والمنطق خلف القرار
    
# 6. سجل التدقيق الشامل (Audit Trail Record)
class AuditRecord(BaseModel):
    inputs: dict
    signals: dict
    decision: DecisionResult