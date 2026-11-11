"""Explainable, deterministic demonstration model; NOT evidence of luck or career success."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import json
import re
import unicodedata

BASE = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def config():
    rules = json.loads((BASE / "rulebook.json").read_text(encoding="utf-8"))
    careers = json.loads((BASE / "careers.json").read_text(encoding="utf-8"))
    attribute_ids = {a["id"] for a in careers["attributes"]}
    keys = set()
    for c in careers["careers"]:
        assert sum(c["weights"].values()) == 100, c["id"]
        assert set(c["weights"]) == attribute_ids, c["id"]
    for rule in rules["rules"]:
        assert re.fullmatch(r"\d\d",rule["pair"])
        assert rule["pair"] not in keys
        assert set(rule["deltas"]) <= attribute_ids
        keys.add(rule["pair"])
    return rules, careers


def normalize_number(value: str) -> str:
    """Convert Thai/ASCII digits, strip cosmetic separators and +66 country prefix."""
    if not isinstance(value, str):
        raise ValueError("กรุณาระบุหมายเลขโทรศัพท์เป็นข้อความ")
    try:
        txt = "".join(str(unicodedata.decimal(char)) if char.isdecimal() else char for char in value.strip())
    except (ValueError, TypeError):
        raise ValueError("รูปแบบหมายเลขไม่ถูกต้อง")
    if not re.fullmatch(r"[+\d\s.()\-]+", txt):
        raise ValueError("หมายเลขมีอักขระที่ไม่รองรับ")
    digits = re.sub(r"\D", "", txt)
    if digits.startswith("66") and len(digits) == 11:
        digits = "0" + digits[2:]
    if not re.fullmatch(r"0[689]\d{8}", digits):
        raise ValueError("รองรับเบอร์มือถือไทย 10 หลักที่ขึ้นต้นด้วย 06, 08 หรือ 09")
    return digits


def analyze(value: str) -> dict:
    rules, career_config = config()
    number = normalize_number(value)
    core = number[2:]
    by_pair = {r["pair"]: r for r in rules["rules"]}
    attrs = {a["id"]: float(rules["baseline"]) for a in career_config["attributes"]}
    matches = []
    for index in range(7):
        pair = core[index:index+2]
        rule = by_pair.get(pair)
        if rule:
            for trait, delta in rule["deltas"].items():
                attrs[trait] += float(delta)
            matches.append({"pair":pair,"position":index+1,"theme":rule["theme"],
                            "reason":rule["reason"],"deltas":rule["deltas"]})
    scores = {a: round(max(0, min(100, v))) for a,v in attrs.items()}
    rankings = []
    for career in career_config["careers"]:
        fit = sum(scores[k] * w for k,w in career["weights"].items()) / 100
        rankings.append({"career_id":career["id"],"name":career["name"],
                         "group":career["group"],"score":round(fit)})
    rankings.sort(key=lambda row: (-row["score"], row["career_id"]))
    return {"number":number,"formatted":f"{number[:3]}-{number[3:6]}-{number[6:]}",
            "core":core,"pairs":[core[i:i+2] for i in range(7)],
            "matched_rules":matches,"matched_count":len(matches),"trait_scores":scores,
            "careers":rankings,"rulebook_version":rules["version"],
            "disclaimer":"คะแนนเชิงกฎจำลองตามความเชื่อ ไม่ใช่โอกาสสำเร็จหรือการพิสูจน์คุณสมบัติของบุคคล"}
