"""
Konuşma diline yakın metin: eksik noktalama, nadiren yazım hatası.
"""
from __future__ import annotations

import random
import re
from typing import Optional

# Dokunulmayacak teknik anahtarlar (prompt/kod)
_SKIP = frozenset(
    w.lower()
    for w in (
        "solidity", "function", "mapping", "require", "modifier", "contract",
        "uint256", "address", "bytes32", "openzeppelin", "erc-721", "erc-20",
        "natSpec", "tokenid", "verifyDiploma", "pragma", "external", "view",
    )
)

_TYPO_REPLACEMENTS = [
    ("bir", "bi"),
    ("için", "icin"),
    ("gibi", "gii"),
    ("oldu", "olduu"),
    ("çok", "cok"),
    ("şey", "sey"),
    ("öğren", "ogren"),
    ("üzerinde", "uzerinde"),
    ("persona", "persona"),  # bazen
    ("persona", "persone"),
    ("modda", "moda"),
    ("görev", "gorev"),
    ("kod", "kodd"),
    ("ama", "amma"),
    ("sanırım", "sanirim"),
    ("belki", "belkii"),
    ("platform", "platfom"),
    ("blockchain", "blokzincir"),  # nadiren karışık
    ("Solidity", "Solidty"),
]

_PUNCT_DROP_CHANCE = 0.22
_TYPO_WORD_CHANCE = 0.09
_RUNON_CHANCE = 0.18  # cümle sonu nokta kaldır + küçük harf devam


def humanize(text: str, rng: random.Random, *, intensity: float = 1.0) -> str:
    """Metni daha doğal (kusurlu) hale getir. intensity 0–1."""
    if not text or intensity <= 0:
        return text

    out = text

    # Bazen çift boşluk / başta/sonda düzensizlik
    if rng.random() < 0.12 * intensity:
        out = re.sub(r"\s+", "  ", out, count=rng.randint(1, 2))

    # Noktalama düşür (sondaki . , ;)
    if rng.random() < _PUNCT_DROP_CHANCE * intensity:
        out = re.sub(r"([.!?])(\s+)([A-ZÇĞİÖŞÜa-zçğıöşü])", r"\1\2\3", out)
        out = re.sub(r"\.(\s*)$", r"\1", out)
        out = re.sub(r",(\s)", r"\1", out, count=rng.randint(0, 2))

    # Kelime bazlı yazım hatası
    words = out.split()
    new_words = []
    for w in words:
        core = re.sub(r"^[^\wçğıöşüÇĞİÖŞÜ]+|[^\wçğıöşüÇĞİÖŞÜ]+$", "", w)
        if not core or core.lower() in _SKIP:
            new_words.append(w)
            continue
        if rng.random() < _TYPO_WORD_CHANCE * intensity:
            prefix = w[: len(w) - len(core)] if w.endswith(core) else ""
            suffix = w[len(prefix) + len(core) :] if prefix else ""
            low = core.lower()
            for a, b in _TYPO_REPLACEMENTS:
                if a in low and rng.random() < 0.35:
                    low = low.replace(a, b, 1)
                    break
            else:
                # harf atlama / tekrar
                if len(low) > 4 and rng.random() < 0.5:
                    i = rng.randint(1, len(low) - 2)
                    low = low[:i] + low[i + 1 :]
                elif len(low) > 3:
                    i = rng.randint(1, len(low) - 1)
                    low = low[:i] + low[i - 1] + low[i:]
            # orijinal büyük/küçük kabaca koru
            if core[0].isupper():
                core = low.capitalize()
            else:
                core = low
            w = prefix + core + suffix
        new_words.append(w)
    out = " ".join(new_words)

    # Run-on: ara cümlelerde nokta kaldır
    if rng.random() < _RUNON_CHANCE * intensity:
        parts = re.split(r"(\.\s+)", out)
        if len(parts) >= 3:
            idx = rng.randrange(0, len(parts) // 2) * 2
            if parts[idx].strip().endswith("."):
                parts[idx] = parts[idx].rstrip(".")
                if idx + 2 < len(parts) and parts[idx + 2]:
                    parts[idx + 2] = parts[idx + 2][:1].lower() + parts[idx + 2][1:]
            out = "".join(parts)

    # Sonda nokta yok (insansı)
    if rng.random() < 0.35 * intensity and out.rstrip().endswith("."):
        out = out.rstrip()[:-1]

    return out


def humanize_prompt(text: str, seed: Optional[int] = None) -> str:
    rng = random.Random(seed)
    return humanize(text, rng, intensity=1.0)
