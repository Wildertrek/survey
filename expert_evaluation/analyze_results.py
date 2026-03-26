#!/usr/bin/env python3
"""
Expert Evaluation Results Analyzer

Processes the expert evaluation CSVs and computes all metrics needed
for Paper 1 Section 6.4.4.

Usage:
    python analyze_results.py                          # analyze in-place CSVs
    python analyze_results.py results.zip              # analyze from zip file
    python analyze_results.py --output report.json     # save JSON report
"""

import csv
import json
import sys
import zipfile
import tempfile
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# ─── Answer Key ───────────────────────────────────────────────────────────
# Ground truth for the 50 evaluation items.
# Human items: correct factor from published instrument scoring key.
# LLM items: target factor the item was generated to represent.
# This file is NOT shown to the evaluator.

ANSWER_KEY = {
    # Human-authored items (20) - from published instrument scoring keys
    "eval_002": "Conscientiousness",       # BFI-44: "does a thorough job"
    "eval_003": "Sanguine",                # O4TS: "talkative and expressive"
    "eval_005": "Psychopathy",             # SD4: "been in more fights"
    "eval_006": "Rational System",         # REI: "prefer complex to simple problems"
    "eval_010": "Loss of Interest",        # PHQ-9: "little interest or pleasure" -> BDI Loss of Interest
    "eval_013": "Narcissism",              # SD4: "I am special because everyone tells me"
    "eval_014": "Competing",               # TKI: "try to win my position"
    "eval_020": "Neuroticism",             # BFI-44: "depressed, blue"
    "eval_025": "Self-Transcendence",      # PVQ-21: "humble and modest"
    "eval_026": "Machiavellianism",        # SD3: "wait for the right time to get back at people"
    "eval_033": "Trouble Relaxing",        # GAD-7: "trouble relaxing"
    "eval_034": "Machiavellianism",        # SD3: "clever manipulation"
    "eval_038": "Judging",                 # OEJTS: "follow a schedule"
    "eval_040": "Compromising",            # TKI: "let other person have some positions"
    "eval_041": "Avoidance Motivation",    # AGQ-R: "avoid learning less than possible"
    "eval_043": "Experiential System",     # REI: "don't have a good sense of intuition" (reverse-scored)
    "eval_044": "Promotion Focus",         # RFQ: "achieving things important to me"
    "eval_046": "Self-Sufficiency",        # NPI-16: "always know what I am doing"
    "eval_047": "Conscientiousness",       # HEXACO-60: "plan ahead and organize"
    "eval_049": "Autonomy",               # BPNSFS: "sense of choice and freedom"

    # LLM-generated items (30) - target factor from test_items/*_tests.json
    "eval_001": "Sensing",                 # MBTI: "focus on details"
    "eval_004": "Accommodating",           # TKI: "give in too easily"
    "eval_007": "Autonomy",               # SDT: "prefer own responsibilities"
    "eval_008": "Accommodating",           # TKI: "put others' needs before own to keep peace"
    "eval_009": "Compromising",            # TKI: "give up demands to reach consensus"
    "eval_011": "Anxiety Disorders",       # SCID: "anxious in social situations" (social anxiety)
    "eval_012": "Experiential System",     # CEST: "hard to distinguish feelings and thoughts"
    "eval_015": "Approach Motivation",     # AAM: "on the lookout for new experiences"
    "eval_016": "Paranoia",               # MMPI: "on guard around others"
    "eval_017": "Promotion Focus",         # RFT: "take on too much in pursuit of success"
    "eval_018": "Obsessive-Compulsive and Related Disorders",  # SCID: "wash hands repeatedly"
    "eval_019": "Adaptability",            # TEI: "stick to familiar routines" (reverse-scored)
    "eval_021": "Novelty Seeking",         # TCI: "love trying new things"
    "eval_022": "Disruptive, Impulse-Control, and Conduct Disorders",  # SCID: "trouble with law"
    "eval_023": "Psychopathic_Deviate",    # MMPI: "challenge authority"
    "eval_024": "Neuroticism",             # OCEAN: "nervous in social situations"
    "eval_027": "Thinking",               # MBTI: "weigh pros and cons"
    "eval_028": "Self-Transcendence",      # TCI: "reflects on place in the universe"
    "eval_029": "Social Awareness",        # TEI: "understanding social contexts"
    "eval_030": "Prevention Focus",        # RFT: "responsible for everything going smoothly"
    "eval_031": "Adaptability",            # Enneagram: "switch between roles"
    "eval_032": "Self-Directedness",       # TCI: "set personal goals, work diligently"
    "eval_035": "Extraversion",            # OCEAN: "keep busy with social activities"
    "eval_036": "Autonomy",               # SDT: "prefer independent work"
    "eval_037": "Perseverance",            # Enneagram: "committed to goals, value flexibility"
    "eval_039": "Self-Enhancement",        # STBV: "enjoy being successful, care about others"
    "eval_042": "Persistence",             # TCI: "struggles to let go of tasks"
    "eval_045": "Approach Motivation",     # AAM: "plan steps before taking action"
    "eval_048": "Thinking",               # MBTI: "analyzing problems, logical solutions"
    "eval_050": "Conservation",            # STBV: "keep things as they are"
}


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def cohens_kappa(observed_agreement, expected_agreement):
    """Compute Cohen's kappa from observed and expected agreement rates."""
    if expected_agreement == 1.0:
        return 1.0
    return (observed_agreement - expected_agreement) / (1.0 - expected_agreement)


def analyze_task1(items):
    """Analyze item classification results."""
    results = {
        "total": len(items),
        "completed": 0,
        "accuracy": None,
        "cohens_kappa": None,
        "by_source": {},
        "by_category": {},
        "by_model": {},
        "confidence_mean": None,
        "confidence_std": None,
        "disagreements": [],
    }

    answered = [it for it in items if it.get("expert_factor_assignment", "").strip()]
    results["completed"] = len(answered)

    if not answered:
        return results

    # Accuracy
    correct = 0
    all_labels = set()
    expert_labels = []
    truth_labels = []
    confidences = []

    for it in answered:
        item_id = it["item_id"]
        expert = it["expert_factor_assignment"].strip()
        truth = ANSWER_KEY.get(item_id, "")

        if not truth:
            continue

        expert_labels.append(expert)
        truth_labels.append(truth)
        all_labels.add(expert)
        all_labels.add(truth)

        if expert == truth:
            correct += 1
        else:
            results["disagreements"].append({
                "item_id": item_id,
                "model": it["model"],
                "item_text": it["item_text"][:80],
                "expert": expert,
                "expected": truth,
                "confidence": it.get("expert_confidence", ""),
                "notes": it.get("expert_notes", ""),
            })

        conf = it.get("expert_confidence", "")
        if conf and conf.isdigit():
            confidences.append(int(conf))

    n_compared = len(expert_labels)
    if n_compared > 0:
        results["accuracy"] = round(correct / n_compared * 100, 1)

        # Cohen's kappa
        label_list = sorted(all_labels)
        n = n_compared
        # Count each label in expert and truth
        expert_counts = Counter(expert_labels)
        truth_counts = Counter(truth_labels)
        pe = sum(
            (expert_counts.get(l, 0) / n) * (truth_counts.get(l, 0) / n)
            for l in label_list
        )
        po = correct / n
        results["cohens_kappa"] = round(cohens_kappa(po, pe), 3)

    # By source type
    for source in ["LLM-generated", "human"]:
        source_items = [it for it in answered if it.get("source_type") == source]
        source_correct = sum(
            1 for it in source_items
            if it["expert_factor_assignment"].strip() == ANSWER_KEY.get(it["item_id"], "")
        )
        if source_items:
            results["by_source"][source] = {
                "n": len(source_items),
                "correct": source_correct,
                "accuracy": round(source_correct / len(source_items) * 100, 1),
            }

    # By category
    cats = set(it.get("category", "").strip() or "unspecified" for it in answered)
    for cat in sorted(cats):
        cat_items = [
            it for it in answered
            if (it.get("category", "").strip() or "unspecified") == cat
        ]
        cat_correct = sum(
            1 for it in cat_items
            if it["expert_factor_assignment"].strip() == ANSWER_KEY.get(it["item_id"], "")
        )
        if cat_items:
            results["by_category"][cat] = {
                "n": len(cat_items),
                "correct": cat_correct,
                "accuracy": round(cat_correct / len(cat_items) * 100, 1),
            }

    # By model
    models = set(it["model"] for it in answered)
    for model in sorted(models):
        model_items = [it for it in answered if it["model"] == model]
        model_correct = sum(
            1 for it in model_items
            if it["expert_factor_assignment"].strip() == ANSWER_KEY.get(it["item_id"], "")
        )
        if model_items:
            results["by_model"][model] = {
                "n": len(model_items),
                "correct": model_correct,
                "accuracy": round(model_correct / len(model_items) * 100, 1),
            }

    # Confidence stats
    if confidences:
        results["confidence_mean"] = round(sum(confidences) / len(confidences), 2)
        mean = results["confidence_mean"]
        variance = sum((c - mean) ** 2 for c in confidences) / len(confidences)
        results["confidence_std"] = round(variance ** 0.5, 2)

    return results


def analyze_task2(constructs):
    """Analyze construct validity review results."""
    results = {
        "total": len(constructs),
        "completed": 0,
        "mean_rating": None,
        "std_rating": None,
        "by_rating": {},
        "by_model": {},
        "flagged": [],
    }

    rated = [c for c in constructs if c.get("appropriateness_rating", "").strip()]
    results["completed"] = len(rated)

    if not rated:
        return results

    ratings = [int(c["appropriateness_rating"]) for c in rated]
    results["mean_rating"] = round(sum(ratings) / len(ratings), 2)
    mean = results["mean_rating"]
    variance = sum((r - mean) ** 2 for r in ratings) / len(ratings)
    results["std_rating"] = round(variance ** 0.5, 2)

    # Distribution
    for level in range(1, 6):
        label = {1: "Inappropriate", 2: "Poor", 3: "Adequate", 4: "Good", 5: "Excellent"}[level]
        count = sum(1 for r in ratings if r == level)
        results["by_rating"][f"{level} ({label})"] = count

    # By model
    models = set(c["model"] for c in rated)
    for model in sorted(models):
        model_constructs = [c for c in rated if c["model"] == model]
        model_ratings = [int(c["appropriateness_rating"]) for c in model_constructs]
        results["by_model"][model] = {
            "n": len(model_ratings),
            "mean": round(sum(model_ratings) / len(model_ratings), 2),
        }

    # Flagged (rating <= 2 or has notes)
    for c in rated:
        rating = int(c["appropriateness_rating"])
        notes = c.get("notes", "").strip()
        if rating <= 2 or notes:
            results["flagged"].append({
                "model": c["model"],
                "factor": c["factor"],
                "rating": rating,
                "notes": notes,
            })

    return results


def analyze_task3(categories):
    """Analyze taxonomy review results."""
    results = {
        "total": len(categories),
        "completed": 0,
        "yes": 0,
        "partially": 0,
        "no": 0,
        "details": [],
    }

    reviewed = [c for c in categories if c.get("expert_appropriate", "").strip()]
    results["completed"] = len(reviewed)

    for c in reviewed:
        verdict = c["expert_appropriate"].strip()
        if verdict == "Yes":
            results["yes"] += 1
        elif verdict == "Partially":
            results["partially"] += 1
        elif verdict == "No":
            results["no"] += 1

        detail = {
            "category": c["category"],
            "verdict": verdict,
        }
        if c.get("models_miscategorized", "").strip():
            detail["miscategorized"] = c["models_miscategorized"].strip()
        if c.get("missing_models", "").strip():
            detail["missing"] = c["missing_models"].strip()
        if c.get("notes", "").strip():
            detail["notes"] = c["notes"].strip()
        results["details"].append(detail)

    return results


def print_report(task1, task2, task3):
    """Print a formatted report to stdout."""
    print("=" * 70)
    print("EXPERT EVALUATION RESULTS REPORT")
    print("=" * 70)

    # Task 1
    print("\n─── Task 1: Item Classification (50 items) ───")
    print(f"  Completed: {task1['completed']}/{task1['total']}")
    if task1["accuracy"] is not None:
        print(f"  Overall accuracy: {task1['accuracy']}%")
        print(f"  Cohen's kappa: {task1['cohens_kappa']}")
        print(f"  Confidence: {task1['confidence_mean']} (SD={task1['confidence_std']})")
        print()
        print("  By source:")
        for src, data in task1["by_source"].items():
            print(f"    {src}: {data['accuracy']}% ({data['correct']}/{data['n']})")
        print()
        print("  By category:")
        for cat, data in sorted(task1["by_category"].items()):
            print(f"    {cat}: {data['accuracy']}% ({data['correct']}/{data['n']})")
        print()
        print("  By model:")
        for model, data in sorted(task1["by_model"].items()):
            print(f"    {model}: {data['accuracy']}% ({data['correct']}/{data['n']})")

        if task1["disagreements"]:
            print(f"\n  Disagreements ({len(task1['disagreements'])}):")
            for d in task1["disagreements"]:
                print(f"    {d['item_id']} [{d['model']}]: expert={d['expert']}, expected={d['expected']}")
                if d["notes"]:
                    print(f"      note: {d['notes']}")
    else:
        print("  (no items completed)")

    # Task 2
    print("\n─── Task 2: Construct Validity Review (67 factors) ───")
    print(f"  Completed: {task2['completed']}/{task2['total']}")
    if task2["mean_rating"] is not None:
        print(f"  Mean rating: {task2['mean_rating']} (SD={task2['std_rating']})")
        print()
        print("  Rating distribution:")
        for level, count in task2["by_rating"].items():
            bar = "#" * count
            print(f"    {level}: {count} {bar}")
        print()
        print("  By model:")
        for model, data in sorted(task2["by_model"].items()):
            print(f"    {model}: {data['mean']:.1f} (n={data['n']})")

        if task2["flagged"]:
            print(f"\n  Flagged factors ({len(task2['flagged'])}):")
            for f in task2["flagged"]:
                print(f"    {f['model']}/{f['factor']}: rating={f['rating']}")
                if f["notes"]:
                    print(f"      note: {f['notes']}")
    else:
        print("  (no factors rated)")

    # Task 3
    print("\n─── Task 3: Taxonomy Review (7 categories) ───")
    print(f"  Completed: {task3['completed']}/{task3['total']}")
    if task3["completed"] > 0:
        print(f"  Yes: {task3['yes']}, Partially: {task3['partially']}, No: {task3['no']}")
        for d in task3["details"]:
            print(f"\n  {d['category']}: {d['verdict']}")
            if d.get("miscategorized"):
                print(f"    Miscategorized: {d['miscategorized']}")
            if d.get("missing"):
                print(f"    Missing: {d['missing']}")
            if d.get("notes"):
                print(f"    Notes: {d['notes']}")

    # Summary for paper
    print("\n" + "=" * 70)
    print("PAPER-READY METRICS (for Section 6.4.4)")
    print("=" * 70)
    if task1["accuracy"] is not None:
        print(f"  Task 1 accuracy: {task1['accuracy']}%")
        print(f"  Task 1 Cohen's kappa: {task1['cohens_kappa']}")
        human = task1["by_source"].get("human", {})
        llm = task1["by_source"].get("LLM-generated", {})
        if human:
            print(f"  Human item accuracy: {human['accuracy']}% ({human['correct']}/{human['n']})")
        if llm:
            print(f"  LLM item accuracy: {llm['accuracy']}% ({llm['correct']}/{llm['n']})")
    if task2["mean_rating"] is not None:
        n_good = sum(
            1 for c in task2["by_rating"].items()
            if c[0].startswith("4") or c[0].startswith("5")
        )
        n_good_count = task2["by_rating"].get("4 (Good)", 0) + task2["by_rating"].get("5 (Excellent)", 0)
        n_poor_count = task2["by_rating"].get("1 (Inappropriate)", 0) + task2["by_rating"].get("2 (Poor)", 0)
        print(f"  Task 2 mean rating: {task2['mean_rating']} (SD={task2['std_rating']})")
        print(f"  Task 2 Good+Excellent: {n_good_count}/{task2['completed']}")
        print(f"  Task 2 Poor+Inappropriate: {n_poor_count}/{task2['completed']}")
    if task3["completed"] > 0:
        print(f"  Task 3: {task3['yes']}/7 Yes, {task3['partially']}/7 Partially, {task3['no']}/7 No")


def main():
    # Determine data source
    data_dir = DATA_DIR
    cleanup = None

    if len(sys.argv) > 1 and sys.argv[1].endswith(".zip"):
        # Extract from zip
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(sys.argv[1]) as zf:
            zf.extractall(tmpdir)
        data_dir = Path(tmpdir)
        cleanup = tmpdir

    try:
        items = load_csv(data_dir / "item_classification_task.csv")
        constructs = load_csv(data_dir / "construct_review_task.csv")
        categories = load_csv(data_dir / "category_taxonomy_review.csv")

        task1 = analyze_task1(items)
        task2 = analyze_task2(constructs)
        task3 = analyze_task3(categories)

        print_report(task1, task2, task3)

        # Optional JSON output
        output_flag = "--output"
        if output_flag in sys.argv:
            idx = sys.argv.index(output_flag)
            if idx + 1 < len(sys.argv):
                output_path = sys.argv[idx + 1]
                report = {"task1": task1, "task2": task2, "task3": task3}
                with open(output_path, "w") as f:
                    json.dump(report, f, indent=2)
                print(f"\nJSON report saved to: {output_path}")

    finally:
        if cleanup:
            import shutil
            shutil.rmtree(cleanup, ignore_errors=True)


if __name__ == "__main__":
    main()
