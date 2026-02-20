#!/usr/bin/env python3
"""
Personality Atlas — Expert Review

Interactive validation tool for the Computational Atlas of Personality Models.
Estimated time: 45-60 minutes.

Setup:
    pip install streamlit
    streamlit run evaluator.py
"""

import csv
import io
import json
import zipfile
import streamlit as st
from pathlib import Path
from urllib.parse import quote

DATA_DIR = Path(__file__).parent / "data"

# GitHub base URL for model cards
SURVEY_BASE = "https://github.com/Wildertrek/survey/blob/main/atlas"

MODEL_CARD_MAP = {
    "OCEAN":              ("01_trait_based", "ocean"),
    "HEXACO":             ("01_trait_based", "hexaco"),
    "HEX":                ("01_trait_based", "hexaco"),
    "MBTI":               ("01_trait_based", "mbti"),
    "Four Temperaments":  ("01_trait_based", "ftm"),
    "FTM":                ("01_trait_based", "ftm"),
    "EPM":                ("01_trait_based", "epm"),
    "16PF":               ("01_trait_based", "16pf"),
    "NPI":                ("02_narcissism_based", "npi"),
    "Dark Triad":         ("02_narcissism_based", "dtm"),
    "DTM":                ("02_narcissism_based", "dtm"),
    "DT3":                ("02_narcissism_based", "dtm"),
    "Dark Tetrad":        ("02_narcissism_based", "dt4"),
    "DT4":                ("02_narcissism_based", "dt4"),
    "FFNI":               ("02_narcissism_based", "ffni"),
    "FFNI-SF":            ("02_narcissism_based", "ffni_sf"),
    "HSNS":               ("02_narcissism_based", "hsns"),
    "IPN":                ("02_narcissism_based", "ipn"),
    "MCMI-N":             ("02_narcissism_based", "mcmin"),
    "NARQ":               ("02_narcissism_based", "narq"),
    "PNI":                ("02_narcissism_based", "pni"),
    "AAM":                ("03_motivational_value", "aam"),
    "SDT":                ("03_motivational_value", "sdt"),
    "RFT":                ("03_motivational_value", "rft"),
    "STBV":               ("03_motivational_value", "stbv"),
    "MST":                ("03_motivational_value", "mst"),
    "CS":                 ("03_motivational_value", "clifton"),
    "Clifton Strengths":  ("03_motivational_value", "clifton"),
    "CEST":               ("04_cognitive_learning", "cest"),
    "SCM":                ("04_cognitive_learning", "scm"),
    "FSLS":               ("04_cognitive_learning", "fsls"),
    "PCT":                ("04_cognitive_learning", "pct"),
    "MMPI":               ("05_clinical_health", "mmpi"),
    "SCID":               ("05_clinical_health", "scid"),
    "BDI":                ("05_clinical_health", "bdi"),
    "GAD-7":              ("05_clinical_health", "gad7"),
    "GAD7":               ("05_clinical_health", "gad7"),
    "TCI":                ("05_clinical_health", "tci"),
    "MCMI":               ("05_clinical_health", "mcmi"),
    "WAIS":               ("05_clinical_health", "wais"),
    "TMP":                ("05_clinical_health", "tmp"),
    "RIT":                ("05_clinical_health", "rit"),
    "TAT":                ("05_clinical_health", "tat"),
    "TKI":                ("06_interpersonal_conflict", "tki"),
    "DISC":               ("06_interpersonal_conflict", "disc"),
    "TEI":                ("07_application_holistic", "tei"),
    "Enneagram":          ("07_application_holistic", "em"),
    "EM":                 ("07_application_holistic", "em"),
    "RIASEC":             ("07_application_holistic", "riasec"),
    "CMOA":               ("07_application_holistic", "cmoa"),
    "BT":                 ("07_application_holistic", "bt"),
    "PAPC":               ("07_application_holistic", "papc"),
}


def model_card_url(name):
    entry = MODEL_CARD_MAP.get(name)
    if not entry:
        return ""
    return f"{SURVEY_BASE}/{entry[0]}/{entry[1]}/MODEL_CARD.md"


def model_card_link(name):
    url = model_card_url(name)
    return f"[{name}]({url})" if url else name


# ---------------------------------------------------------------------------
# Data loading & saving
# ---------------------------------------------------------------------------

@st.cache_data
def load_factor_guide():
    path = DATA_DIR / "factor_guide.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def load_items():
    rows = []
    with open(DATA_DIR / "item_classification_task.csv") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


@st.cache_data
def load_constructs():
    rows = []
    with open(DATA_DIR / "construct_review_task.csv") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


@st.cache_data
def load_categories():
    rows = []
    with open(DATA_DIR / "category_taxonomy_review.csv") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def save_items(rows):
    fieldnames = [
        "item_id", "item_text", "model", "category", "n_factors",
        "available_factors", "source_type", "instrument",
        "expert_factor_assignment", "expert_confidence", "expert_notes",
    ]
    with open(DATA_DIR / "item_classification_task.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def save_constructs(rows):
    fieldnames = ["model", "factor", "n_schema_rows", "sample_entries",
                  "appropriateness_rating", "notes"]
    with open(DATA_DIR / "construct_review_task.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def save_categories(rows):
    fieldnames = ["category", "n_models", "models", "description",
                  "theoretical_basis", "distinguishing_criteria",
                  "key_considerations",
                  "expert_appropriate", "models_miscategorized",
                  "missing_models", "notes"]
    with open(DATA_DIR / "category_taxonomy_review.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def init_state():
    if "eval_items" not in st.session_state:
        st.session_state.eval_items = load_items()
    if "eval_constructs" not in st.session_state:
        st.session_state.eval_constructs = load_constructs()
    if "eval_categories" not in st.session_state:
        st.session_state.eval_categories = load_categories()
    if "factor_guide" not in st.session_state:
        st.session_state.factor_guide = load_factor_guide()
    if "task1_idx" not in st.session_state:
        st.session_state.task1_idx = 0
    if "task2_idx" not in st.session_state:
        st.session_state.task2_idx = 0


# ---------------------------------------------------------------------------
# Task 1: Item-Factor Classification
# ---------------------------------------------------------------------------

def render_task1():
    items = st.session_state.eval_items
    n = len(items)
    idx = st.session_state.task1_idx

    completed = sum(1 for it in items if it.get("expert_factor_assignment", "").strip())
    st.progress(completed / n, text=f"Progress: {completed}/{n} items completed")

    col_prev, col_num, col_next, col_skip = st.columns([1, 2, 1, 2])
    with col_prev:
        if st.button("Previous", disabled=idx == 0, key="t1_prev"):
            st.session_state.task1_idx = max(0, idx - 1)
            st.rerun()
    with col_next:
        if st.button("Next", disabled=idx >= n - 1, key="t1_next"):
            st.session_state.task1_idx = min(n - 1, idx + 1)
            st.rerun()
    with col_num:
        st.markdown(f"**Item {idx + 1} of {n}**")
    with col_skip:
        if st.button("Jump to next unanswered", key="t1_next_empty"):
            for i in range(idx + 1, n):
                if not items[i].get("expert_factor_assignment", "").strip():
                    st.session_state.task1_idx = i
                    st.rerun()
            for i in range(0, idx):
                if not items[i].get("expert_factor_assignment", "").strip():
                    st.session_state.task1_idx = i
                    st.rerun()
            st.info("All items answered!")

    st.divider()
    item = items[idx]
    st.markdown(f"### {item['item_id']}")

    col_meta, col_item = st.columns([1, 3])
    with col_meta:
        st.markdown(f"**Model:** {model_card_link(item['model'])}")
        if item.get("category"):
            st.markdown(f"**Category:** {item['category']}")
        st.markdown(f"**Source:** {item.get('source_type', 'unknown')}")
        if item.get("instrument"):
            st.markdown(f"**Instrument:** {item['instrument']}")
        st.markdown(f"**# Factors:** {item['n_factors']}")
    with col_item:
        st.info(f'"{item["item_text"]}"')

    factors = [f.strip() for f in item["available_factors"].split("|")]
    current_assignment = item.get("expert_factor_assignment", "").strip()

    # Build radio labels with inline definitions
    guide = st.session_state.factor_guide.get(item["model"], {})
    factor_labels = {}
    for factor in factors:
        descriptors = guide.get(factor, "")
        if descriptors:
            factor_labels[factor] = f"{factor} — {descriptors}"
        else:
            factor_labels[factor] = factor

    default_idx = factors.index(current_assignment) if current_assignment in factors else None

    st.markdown("**Assign the most appropriate factor:**")
    selected = st.radio("Factor:", options=factors,
                        format_func=lambda f: factor_labels[f],
                        index=default_idx, key=f"t1_factor_{idx}",
                        label_visibility="collapsed")

    current_conf = item.get("expert_confidence", "")
    conf_val = int(current_conf) if current_conf and current_conf.isdigit() else 3
    confidence = st.slider("Confidence (1=guessing, 5=certain):",
                           min_value=1, max_value=5, value=conf_val, key=f"t1_conf_{idx}")

    notes = st.text_area("Notes (optional):", value=item.get("expert_notes", ""),
                         key=f"t1_notes_{idx}", height=80)

    if st.button("Save & Continue", type="primary", key="t1_save"):
        items[idx]["expert_factor_assignment"] = selected
        items[idx]["expert_confidence"] = str(confidence)
        items[idx]["expert_notes"] = notes
        save_items(items)
        if idx < n - 1:
            st.session_state.task1_idx = idx + 1
            st.rerun()
        else:
            st.success("All items complete!")


# ---------------------------------------------------------------------------
# Task 2: Construct Validity Review
# ---------------------------------------------------------------------------

def render_task2():
    constructs = st.session_state.eval_constructs
    n = len(constructs)
    idx = st.session_state.task2_idx

    completed = sum(1 for c in constructs if c.get("appropriateness_rating", "").strip())
    st.progress(completed / n, text=f"Progress: {completed}/{n} factor entries rated")

    models = []
    seen = set()
    for c in constructs:
        if c["model"] not in seen:
            models.append(c["model"])
            seen.add(c["model"])

    col_model, col_nav = st.columns([2, 2])
    with col_model:
        current_model = constructs[idx]["model"]
        selected_model = st.selectbox("Jump to model:", models,
                                      index=models.index(current_model), key="t2_model_select")
        if selected_model != current_model:
            for i, c in enumerate(constructs):
                if c["model"] == selected_model:
                    st.session_state.task2_idx = i
                    st.rerun()

    with col_nav:
        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if st.button("Prev", disabled=idx == 0, key="t2_prev"):
                st.session_state.task2_idx = max(0, idx - 1)
                st.rerun()
        with nav2:
            st.markdown(f"**{idx + 1}/{n}**")
        with nav3:
            if st.button("Next", disabled=idx >= n - 1, key="t2_next"):
                st.session_state.task2_idx = min(n - 1, idx + 1)
                st.rerun()

    row = constructs[idx]
    st.divider()

    url = model_card_url(row['model'])
    if url:
        st.markdown(f"### [{row['model']}]({url}) / {row['factor']}")
    else:
        st.markdown(f"### {row['model']} / {row['factor']}")
    st.markdown(f"**Schema rows:** {row['n_schema_rows']}")

    entries = [e.strip() for e in row.get("sample_entries", "").split(" || ") if e.strip()]
    st.markdown(f"**Lexical schema** ({len(entries)} unique adjectives from {row['n_schema_rows']} rows):")
    table = "| Adjective | Synonym | Verb | Noun |\n|---|---|---|---|\n"
    for entry in entries:
        parts = [p.strip() for p in entry.split(" / ")]
        while len(parts) < 4:
            parts.append("")
        table += f"| {parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} |\n"
    st.markdown(table)

    current_rating = row.get("appropriateness_rating", "").strip()
    rating_val = int(current_rating) if current_rating and current_rating.isdigit() else 0

    rating_labels = {
        0: "-- Select rating --", 1: "1 - Inappropriate", 2: "2 - Poor",
        3: "3 - Adequate", 4: "4 - Good", 5: "5 - Excellent",
    }

    rating = st.radio("Appropriateness rating:", options=[0, 1, 2, 3, 4, 5],
                      format_func=lambda x: rating_labels[x],
                      index=rating_val, key=f"t2_rating_{idx}", horizontal=True)

    notes = st.text_area("Notes (suggested replacements, concerns):",
                         value=row.get("notes", ""), key=f"t2_notes_{idx}", height=80)

    col_save, col_skip = st.columns(2)
    with col_save:
        if st.button("Save & Continue", type="primary", key="t2_save"):
            if rating == 0:
                st.warning("Please select a rating.")
            else:
                constructs[idx]["appropriateness_rating"] = str(rating)
                constructs[idx]["notes"] = notes
                save_constructs(constructs)
                if idx < n - 1:
                    st.session_state.task2_idx = idx + 1
                    st.rerun()
                else:
                    st.success("All factor entries rated!")
    with col_skip:
        if st.button("Skip", key="t2_skip"):
            if idx < n - 1:
                st.session_state.task2_idx = idx + 1
                st.rerun()


# ---------------------------------------------------------------------------
# Task 3: Category Taxonomy Review
# ---------------------------------------------------------------------------

def render_task3():
    categories = st.session_state.eval_categories
    n = len(categories)

    completed = sum(1 for c in categories if c.get("expert_appropriate", "").strip())
    st.progress(completed / n, text=f"Progress: {completed}/{n} categories reviewed")

    for i, cat in enumerate(categories):
        with st.expander(
            f"{'[done]' if cat.get('expert_appropriate', '').strip() else '[   ]'} "
            f"{cat['category']} ({cat['n_models']} models)",
            expanded=not cat.get("expert_appropriate", "").strip(),
        ):
            st.markdown(f"**Description:** {cat['description']}")

            model_names = [m.strip() for m in cat['models'].split(",")]
            linked = ", ".join(model_card_link(m) for m in model_names)
            st.markdown(f"**Models:** {linked}")

            if cat.get("theoretical_basis", "").strip():
                st.markdown(f"**Theoretical Basis:** {cat['theoretical_basis']}")
            if cat.get("distinguishing_criteria", "").strip():
                st.markdown(f"**Inclusion Criteria:** {cat['distinguishing_criteria']}")
            if cat.get("key_considerations", "").strip():
                st.info(f"**Questions to Consider:** {cat['key_considerations']}")

            st.divider()
            current_appropriate = cat.get("expert_appropriate", "").strip()
            app_options = ["Yes", "Partially", "No"]
            app_idx = app_options.index(current_appropriate) if current_appropriate in app_options else None

            appropriate = st.radio("Is this a reasonable grouping?", app_options,
                                   index=app_idx, key=f"t3_app_{i}", horizontal=True)

            miscategorized = st.text_input("Models that belong elsewhere:",
                                           value=cat.get("models_miscategorized", ""), key=f"t3_miscat_{i}")
            missing = st.text_input("Important models missing from this category:",
                                    value=cat.get("missing_models", ""), key=f"t3_missing_{i}")
            notes = st.text_area("Notes:", value=cat.get("notes", ""),
                                 key=f"t3_notes_{i}", height=80)

            if st.button("Save", key=f"t3_save_{i}"):
                if appropriate is None:
                    st.warning("Please select Yes/No/Partially.")
                else:
                    categories[i]["expert_appropriate"] = appropriate
                    categories[i]["models_miscategorized"] = miscategorized
                    categories[i]["missing_models"] = missing
                    categories[i]["notes"] = notes
                    save_categories(categories)
                    st.success(f"Saved: {cat['category']}")
                    st.rerun()

    st.divider()
    st.text_area("Overall taxonomy observations (optional):", key="t3_general",
                 height=100, label_visibility="collapsed")


# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------

def render_submit():
    items = st.session_state.eval_items
    constructs = st.session_state.eval_constructs
    categories = st.session_state.eval_categories

    n_items = len(items)
    n_constructs = len(constructs)
    t1_done = sum(1 for it in items if it.get("expert_factor_assignment", "").strip())
    t2_done = sum(1 for c in constructs if c.get("appropriateness_rating", "").strip())
    t3_done = sum(1 for c in categories if c.get("expert_appropriate", "").strip())

    st.markdown("### Completion Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Task 1: Items", f"{t1_done}/{n_items}", f"{t1_done/n_items:.0%}" if n_items else "0%")
    with col2:
        st.metric("Task 2: Constructs", f"{t2_done}/{n_constructs}", f"{t2_done/n_constructs:.0%}" if n_constructs else "0%")
    with col3:
        st.metric("Task 3: Taxonomy", f"{t3_done}/7", f"{t3_done/7:.0%}")

    all_done = t1_done == n_items and t2_done == n_constructs and t3_done == 7
    if not all_done:
        incomplete = []
        if t1_done < n_items:
            incomplete.append(f"Task 1 ({n_items - t1_done} items remaining)")
        if t2_done < n_constructs:
            incomplete.append(f"Task 2 ({n_constructs - t2_done} factors remaining)")
        if t3_done < 7:
            incomplete.append(f"Task 3 ({7 - t3_done} categories remaining)")
        st.warning(f"Incomplete: {', '.join(incomplete)}. You can still submit a partial evaluation.")

    st.divider()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in ["item_classification_task.csv", "construct_review_task.csv",
                      "category_taxonomy_review.csv"]:
            fpath = DATA_DIR / fname
            if fpath.exists():
                zf.write(fpath, fname)
    zip_buffer.seek(0)

    st.markdown("### Download & Send")
    st.markdown("**Step 1:** Download the zip file containing your completed evaluation.")

    st.download_button(
        label="Download evaluation_results.zip",
        data=zip_buffer.getvalue(),
        file_name="expert_evaluation_results.zip",
        mime="application/zip",
        type="primary",
    )

    st.markdown("**Step 2:** Email the zip file to the researcher.")

    subject = quote("Expert Evaluation Results - TIST-2025-12-1243")
    body = quote(
        "Dear Joseph,\n\n"
        "Please find attached my completed expert evaluation for the "
        "Personality Atlas validation study (TIST-2025-12-1243).\n\n"
        f"Completion: Task 1 ({t1_done}/{n_items}), "
        f"Task 2 ({t2_done}/{n_constructs}), "
        f"Task 3 ({t3_done}/7)\n\n"
        "Best regards"
    )
    mailto = f"mailto:jraetano@utk.edu?subject={subject}&body={body}"

    st.markdown(
        f'<a href="{mailto}" target="_blank">'
        '<button style="background-color:#FF4B4B; color:white; border:none; '
        'padding:0.5rem 1rem; border-radius:0.3rem; font-size:1rem; cursor:pointer;">'
        'Open Email to jraetano@utk.edu</button></a>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Click above to open your email client with the recipient and subject "
        "pre-filled. Attach the downloaded zip file before sending."
    )

    st.divider()
    st.markdown(
        "Thank you for your time and expertise. Your evaluation will be "
        "acknowledged in the paper's acknowledgments section."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title="Personality Atlas — Expert Review",
        page_icon="clipboard",
        layout="wide",
    )

    st.title("Personality Atlas — Expert Review")
    st.caption("Validation Study for the Computational Atlas of Personality Models (TIST-2025-12-1243)")

    init_state()

    with st.sidebar:
        st.markdown("## Navigation")
        task = st.radio(
            "Select task:",
            ["Instructions", "Task 1: Items", "Task 2: Constructs",
             "Task 3: Taxonomy", "Submit"],
            key="task_nav",
        )

        st.divider()

        items = st.session_state.eval_items
        constructs = st.session_state.eval_constructs
        categories = st.session_state.eval_categories

        n_items = len(items)
        n_constructs = len(constructs)
        t1_done = sum(1 for it in items if it.get("expert_factor_assignment", "").strip())
        t2_done = sum(1 for c in constructs if c.get("appropriateness_rating", "").strip())
        t3_done = sum(1 for c in categories if c.get("expert_appropriate", "").strip())

        st.markdown("### Completion")
        st.markdown(f"- Task 1: **{t1_done}/{n_items}** items")
        st.markdown(f"- Task 2: **{t2_done}/{n_constructs}** factors")
        st.markdown(f"- Task 3: **{t3_done}/7** categories")

        total = n_items + n_constructs + 7
        overall = (t1_done + t2_done + t3_done) / total if total else 0
        st.progress(overall, text=f"Overall: {overall:.0%}")

    if task == "Instructions":
        instructions = (DATA_DIR / "expert_evaluation_instructions.txt").read_text()
        st.markdown("```\n" + instructions + "\n```")
        st.divider()
        st.markdown("**Recommended order:** Task 3 (10 min) → Task 2 (15 min) → Task 1 (25 min)")
        st.markdown("Use the sidebar to navigate between tasks.")

    elif task == "Task 1: Items":
        st.header("Task 1: Item-Factor Classification")
        st.markdown(
            "For each item, assign the most appropriate factor from the model's factor list. "
            "Some items are reverse-scored — classify by the construct being measured, not the "
            "direction of the statement."
        )
        render_task1()

    elif task == "Task 2: Constructs":
        st.header("Task 2: Construct Validity Review")
        st.markdown(
            "Rate the appropriateness of the lexical schema (Adjective → Synonym → Verb → Noun) "
            "for each factor on a 1-5 scale."
        )
        render_task2()

    elif task == "Task 3: Taxonomy":
        st.header("Task 3: Category Taxonomy Review")
        st.markdown(
            "Review whether the 7-category structure is appropriate. "
            "For each category, indicate if the grouping is reasonable and note any issues."
        )
        render_task3()

    elif task == "Submit":
        st.header("Submit Your Evaluation")
        render_submit()


if __name__ == "__main__":
    main()
