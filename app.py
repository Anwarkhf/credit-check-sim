
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        card = request.form.get("cardNumber", "")
        cvv = request.form.get("cvv", "")
        address = request.form.get("address", "")
        zipcode = request.form.get("zipcode", "")

        score = 0
        reasons = []

        def luhn_check(card):
            total = 0
            reverse = card[::-1]
            for i, d in enumerate(reverse):
                n = int(d)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n -= 9
                total += n
            return total % 10 == 0

        if not luhn_check(card):
            result = {"valid": False, "message": "❌ رقم البطاقة غير صالح (Luhn Failed)"}
        else:
            if cvv != "123":
                score += 30
                reasons.append("❌ CVV غير صحيح")
            else:
                reasons.append("✅ CVV صحيح")

            if "main" not in address.lower() or zipcode != "12345":
                score += 20
                reasons.append("⚠️ AVS غير مطابق")
            else:
                reasons.append("✅ AVS مطابق")

            import random
            if random.random() > 0.7:
                score += 40
                reasons.append("❗ الدولة مصنفة عالية الخطورة (محاكاة)")

            level = "🔒 آمن" if score <= 20 else "⚠️ متوسط الخطورة" if score <= 50 else "🚨 عالي الخطورة"
            level_class = "safe" if score <= 20 else "medium" if score <= 50 else "high"

            result = {
                "valid": True,
                "score": score,
                "level": level,
                "level_class": level_class,
                "reasons": reasons
            }
    return render_template("index.html", result=result)
