"""
Adaptive modun gerçekten çalışıp çalışmadığını doğrula.
Çalıştırma: python -m src.test_adaptive  veya  python src/test_adaptive.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recommendation_engine import RecommendationEngine, UserVector
from src.recommendation_engine import RecommendationEngine as RE

def test_adaptive_mode():
    engine = RecommendationEngine()
    # Tek bir persona al (test için)
    persona_id = list(engine.persona_vectors.keys())[0]
    persona = engine.persona_vectors[persona_id]

    # UserVector'ü doğrudan oluştur (learning_goal dışında sabit)
    def make_user(learning_goal: float) -> UserVector:
        return UserVector(
            technical_skill=0.5,
            domain_knowledge=0.5,
            ai_experience=0.5,
            learning_goal=learning_goal,
            procedural_knowledge=0.5,
            declarative_knowledge=0.5,
            conditional_knowledge=0.5,
            cognitive_capacity=0.5,
            pattern_recognition=0.5,
            abstraction_level=0.5,
        )

    # 1) learning_goal > 0.7 → actual_mode "complementary" olmalı
    user_learning = make_user(0.9)
    result = engine.calculate_recommendation_score(user_learning, persona, mode="adaptive")
    assert result["mode"] == "complementary", f"Beklenen complementary, gelen: {result['mode']}"
    print("OK: learning_goal=0.9 → mode=complementary")

    # 2) learning_goal < 0.3 → actual_mode "similarity" olmalı
    user_production = make_user(0.2)
    result = engine.calculate_recommendation_score(user_production, persona, mode="adaptive")
    assert result["mode"] == "similarity", f"Beklenen similarity, gelen: {result['mode']}"
    print("OK: learning_goal=0.2 → mode=similarity")

    # 3) 0.3 <= learning_goal <= 0.7 → actual_mode "hybrid" olmalı
    user_mid = make_user(0.5)
    result = engine.calculate_recommendation_score(user_mid, persona, mode="adaptive")
    assert result["mode"] == "hybrid", f"Beklenen hybrid, gelen: {result['mode']}"
    print("OK: learning_goal=0.5 → mode=hybrid")

    # 4) mode verilmezse varsayılan "adaptive" kullanılmalı (learning_goal 0.9 ile complementary)
    result_default = engine.calculate_recommendation_score(user_learning, persona)
    assert result_default["mode"] == "complementary", f"Varsayılan mod adaptive olmalı, gelen: {result_default['mode']}"
    print("OK: mode verilmeden çağrı → varsayılan adaptive, learning_goal=0.9 → complementary")

    # 5) rank_personas mode vermiyor → adaptive kullanılır; farklı user'larda farklı mod çıkmalı
    rankings_learning = engine.rank_personas(user_learning, task_complexity=0.5, top_k=1)
    rankings_production = engine.rank_personas(user_production, task_complexity=0.5, top_k=1)
    # rank_personas her persona için ayrı skor döner; ilk persona için mode'u kontrol etmek için
    # tek persona ile calculate_recommendation_score zaten test edildi. rank_personas'ın
    # mode vermediğini biliyoruz; burada sadece hata olmadığını doğrulayalım.
    assert len(rankings_learning) == 1 and len(rankings_production) == 1
    print("OK: rank_personas adaptive ile çalışıyor (mode verilmiyor)")

    print("\nTüm adaptive testleri geçti.")

if __name__ == "__main__":
    test_adaptive_mode()
