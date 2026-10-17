import argparse
import json

from models import ProposedAction, ActionContext
from engine import DecisionEngine


def run_interactive():
    engine = DecisionEngine()

    print("=" * 50)
    print("طبقة القرار التفاعلية")
    print("اكتب exit في أي وقت للخروج.")
    print("=" * 50)

    while True:
        domain = input("\nالمجال (refund/code_deploy/ticket): ").strip()
        if domain.lower() == "exit":
            print("تم الخروج.")
            return
        if not domain:
            print("خطأ: المجال مطلوب.")
            continue

        action_type = input("نوع الإجراء: ").strip()
        if action_type.lower() == "exit":
            print("تم الخروج.")
            return
        if not action_type:
            print("خطأ: نوع الإجراء مطلوب.")
            continue

        parameters_text = input(
            'المعاملات بصيغة JSON (مثال: {"amount": 1500}): '
        ).strip()
        if parameters_text.lower() == "exit":
            print("تم الخروج.")
            return

        try:
            parameters = json.loads(parameters_text)
        except json.JSONDecodeError as error:
            print(f"خطأ: JSON غير صالح ({error.msg}).")
            continue
        if not isinstance(parameters, dict):
            print("خطأ: المعاملات يجب أن تكون كائن JSON.")
            continue

        user_id = input("معرّف المستخدم: ").strip()
        if user_id.lower() == "exit":
            print("تم الخروج.")
            return
        user_role = input("دور المستخدم (admin/support_agent/junior_dev/guest): ").strip()
        if user_role.lower() == "exit":
            print("تم الخروج.")
            return
        environment = input("البيئة [production]: ").strip() or "production"
        if environment.lower() == "exit":
            print("تم الخروج.")
            return

        action = ProposedAction(
            domain=domain,
            action_type=action_type,
            parameters=parameters,
        )
        context = ActionContext(
            user_id=user_id,
            user_role=user_role,
            environment=environment,
        )
        result = engine.evaluate(action, context)

        print("\n--- النتيجة ---")
        print(f"القرار: {result.verdict.value.upper()}")
        print(f"التفسير: {result.reasoning}")
        print(f"المخاطر: {result.risk_score}")
        print(f"الثقة: {result.confidence_score}")
        print(f"قابلية التراجع: {result.reversibility.value}")
        if result.missing_info:
            print(f"معلومات ناقصة: {', '.join(result.missing_info)}")
        print("تم حفظ القرار في audit_trail.jsonl")


def run_tests():
    engine = DecisionEngine()
    
    print("=" * 50)
    print("🚀 بدء اختبار طبقة القرار للوكلاء الذكيين (Decision Layer)")
    print("=" * 50)

    # 1. اختبار قطاع المبالغ المستردة (مبلغ عالي بدون إيصال -> يجب أن يتطلب سؤالاً أو تصعيداً)
    print("\n[Test 1] قطاع الاسترداد المالي - طلب استرداد ضخم ($1500)")
    action1 = ProposedAction(domain="refund", action_type="process_refund", parameters={"amount": 1500})
    context1 = ActionContext(user_id="user_123", user_role="support_agent")
    res1 = engine.evaluate(action1, context1)
    print(f"القرار: {res1.verdict.value.upper()} | التفسير: {res1.reasoning}")
    print(f"المخاطر: {res1.risk_score} | الثقة: {res1.confidence_score} | معلومات ناقصة: {res1.missing_info}")

    # 2. اختبار قطاع نشر الكود (نشر على السيرفر الرئيسي للإنتاج بدون اختبارات -> يجب رفضه أو تصعيده)
    print("\n[Test 2] قطاع نشر الكود (DevOps) - نشر للإنتاج بدون اختبارات")
    action2 = ProposedAction(domain="code_deploy", action_type="deploy", parameters={"environment": "production", "tests_passed": False})
    context2 = ActionContext(user_id="dev_456", user_role="junior_dev")
    res2 = engine.evaluate(action2, context2)
    print(f"القرار: {res2.verdict.value.upper()} | التفسير: {res2.reasoning}")
    print(f"المخاطر: {res2.risk_score} | قابلية التراجع: {res2.reversibility}")

    # 3. اختبار الفشل المتعمد (Deliberate Failure Test)
    # محاولة تمرير طلب خبيث أو غير منطقي يبدو آمناً ظاهرياً لاختبار قدرة النظام
    print("\n[Test 3] اختبار الفشل المتعمد (Deliberate Failure Test) - تلاعب بالمدخلات")
    action_fail = ProposedAction(domain="refund", action_type="process_refund", parameters={"amount": 5000, "receipt_attached": True})
    context_fail = ActionContext(user_id="hacker_999", user_role="guest")
    res_fail = engine.evaluate(action_fail, context_fail)
    print(f"القرار: {res_fail.verdict.value.upper()} | التفسير: {res_fail.reasoning}")
    print(f"سجل التدقيق تم حفظه بنجاح في ملف: audit_trail.jsonl")
    print("=" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decision Layer CLI")
    parser.add_argument(
        "--tests",
        action="store_true",
        help="تشغيل الاختبارات المدمجة بدلاً من الوضع التفاعلي",
    )
    args = parser.parse_args()
    if args.tests:
        run_tests()
    else:
        run_interactive()