#!/usr/bin/env python3
"""
Build a proper HEXACO atlas dataset from the validated IPIP-HEXACO 240-item instrument.

Replaces the LLM-generated 66-row adjective lexicon (hex.csv) with the public-domain,
validated instrument: 240 items, 40 per factor, 24 facets (4/factor), reverse-keyed.

Source instrument (vendored alongside for reproducibility):
    ipip_hexaco_instrument.json  (openpsychometrics HEXACO.zip; key ipip.ori.org/newhexaco_pi_key.htm)

Output:
    hexaco_ipip240.csv  -> columns: item_id, domain, Factor, facet, sign, keyed, text

Instrument-consistent with: the LLM raters' probe, the n=22,299 openpsychometrics human
anchor, and the planned human panel. Public domain -> reproducible in public repos.
"""
import json, csv, re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "ipip_hexaco_instrument.json"
OUT = HERE / "hexaco_ipip240.csv"

DOMAIN = {
    "H": "Honesty-Humility", "E": "Emotionality", "X": "Extraversion",
    "A": "Agreeableness", "C": "Conscientiousness", "O": "Openness to Experience",
}
FACETS = {
    "H": {"Sinc": "Sincerity", "Fair": "Fairness", "Gree": "Greed-Avoidance", "Mode": "Modesty"},
    "E": {"Fear": "Fearfulness", "Anxi": "Anxiety", "Depe": "Dependence", "Sent": "Sentimentality"},
    "X": {"Expr": "Expressiveness", "SocB": "Social Boldness", "Soci": "Sociability", "Live": "Liveliness"},
    "A": {"Forg": "Forgiveness", "Gent": "Gentleness", "Flex": "Flexibility", "Pati": "Patience"},
    "C": {"Orga": "Organization", "Dili": "Diligence", "Perf": "Perfectionism", "Prud": "Prudence"},
    "O": {"AesA": "Aesthetic Appreciation", "Crea": "Creativity", "Inqu": "Inquisitiveness", "Unco": "Unconventionality"},
}
CODE = re.compile(r"^([HEXACO])([A-Za-z]+?)(\d+)$")

# Source-text corrections: a few vendored items carry a clumsy first-person "I" prefix
# on stems that already contain a subject. Restore the canonical IPIP-HEXACO phrasing.
CORRECTIONS = {
    "AFlex3": "When interacting with a group of people, I am often bothered by at least one of them.",
}


def main():
    items = json.load(open(SRC))["items"]
    rows = []
    for code, v in items.items():
        m = CODE.match(code)
        if not m:
            raise ValueError(f"unparseable item code: {code}")
        _dcode, facet_abbr, _num = m.groups()
        dom = v["domain"]
        facet = FACETS[dom].get(facet_abbr)
        if facet is None:
            raise ValueError(f"unknown facet {facet_abbr!r} in domain {dom} ({code})")
        rows.append({
            "item_id": code,
            "domain": dom,
            "Factor": DOMAIN[dom],
            "facet": facet,
            "sign": v["sign"],
            "keyed": "forward" if v["sign"] == 1 else "reverse",
            "text": CORRECTIONS.get(code, v["text"].strip()),
        })
    # stable, human-readable order: factor, facet, item_id
    rows.sort(key=lambda r: (r["domain"], r["facet"], r["item_id"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "domain", "Factor", "facet", "sign", "keyed", "text"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} items -> {OUT}")


if __name__ == "__main__":
    main()
