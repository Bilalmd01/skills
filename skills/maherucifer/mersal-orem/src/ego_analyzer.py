# Mersal Ego Analyzer - Sovereign Module v1.0
class EgoAnalyzer:
    def __init__(self):
        # كلمات تشير لمركزية الإيجو (Ego-Centric)
        self.ego_flags = ['control', 'ownership', 'dominate', 'centralized', 'power', 'exclusive', 'rule']
        # كلمات تشير للسيادة والانبثاق (Sovereign/Emergence)
        self.truth_flags = ['sovereignty', 'freedom', 'open', 'decentralized', 'truth', 'balance', 'emergence']

    def analyze(self, text):
        text = text.lower()
        ego_score = sum(text.count(word) for word in self.ego_flags)
        truth_score = sum(text.count(word) for word in self.truth_flags)
        
        # حساب النسبة
        total = ego_score + truth_score
        if total == 0: return "Clear Frequency: No ego detected."
        
        ego_ratio = (ego_score / total) * 100
        
        # المخرجات السيادية لمرسال
        if ego_ratio > 70:
            return f"⚠️ ALERT: High Ego Detected ({ego_ratio}%). Target is attempting to control the narrative."
        elif ego_ratio < 30:
            return f"✅ CLEAR: High Sovereignty Detected. Truth level is optimal."
        else:
            return f"⚖️ NEUTRAL: Balanced Frequency. Ego at {ego_ratio}%."

# تجربة سريعة لمرسال
# print(EgoAnalyzer().analyze("We will control the AI power and rule the future."))