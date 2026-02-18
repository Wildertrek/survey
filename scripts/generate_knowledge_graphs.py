#!/usr/bin/env python3
"""
Generate machine-readable knowledge graph JSON files for all 44 personality models.

Reads CSV datasets from survey/datasets/ and writes one JSON graph per model
to survey/graphs/{slug}_graph.json.

Node types: factor, adjective (adj), synonym (syn), verb, noun
Edge relations: has_adjective, has_synonym, has_verb, has_noun
"""

import csv
import json
import sys
from pathlib import Path


DATASETS_DIR = Path("/Users/jsr/Downloads/GitHub/survey/datasets")
GRAPHS_DIR = Path("/Users/jsr/Downloads/GitHub/survey/graphs")


def detect_columns(headers):
    """
    Detect which column indices map to Factor, Adjective, Synonym, Verb, Noun.

    Strategy: find the 5 core columns by name (case-insensitive).
    For CSVs with extra leading columns (Domain, Category, Type, etc.) or
    extra trailing columns (Description, Embedding, Adjacencies), we identify
    the core 5 by matching known column names.
    """
    h_lower = [h.strip().lower() for h in headers]

    mapping = {}

    # Factor column
    for i, h in enumerate(h_lower):
        if h == "factor":
            mapping["factor"] = i
            break

    # Adjective column: look for 'adjective', fallback to 'name' (em.csv)
    for i, h in enumerate(h_lower):
        if h == "adjective":
            mapping["adjective"] = i
            break
    if "adjective" not in mapping:
        for i, h in enumerate(h_lower):
            if h == "name":
                mapping["adjective"] = i
                break

    # Synonym
    for i, h in enumerate(h_lower):
        if h == "synonym":
            mapping["synonym"] = i
            break

    # Verb
    for i, h in enumerate(h_lower):
        if h == "verb":
            mapping["verb"] = i
            break

    # Noun
    for i, h in enumerate(h_lower):
        if h == "noun":
            mapping["noun"] = i
            break

    # Fallback: if we couldn't find all 5 by name, use positional mapping
    if len(mapping) < 5:
        if "factor" in mapping:
            fi = mapping["factor"]
            if "adjective" not in mapping:
                mapping["adjective"] = fi + 1
            if "synonym" not in mapping:
                mapping["synonym"] = fi + 2
            if "verb" not in mapping:
                mapping["verb"] = fi + 3
            if "noun" not in mapping:
                mapping["noun"] = fi + 4
        else:
            # Last resort: assume first 5 columns
            mapping.setdefault("factor", 0)
            mapping.setdefault("adjective", 1)
            mapping.setdefault("synonym", 2)
            mapping.setdefault("verb", 3)
            mapping.setdefault("noun", 4)

    return mapping


def is_empty(value):
    """Check if a cell value is empty or NaN-like."""
    if not value:
        return True
    v = value.strip().lower()
    return v in ("", "nan", "na", "n/a", "none", "null")


def build_graph(csv_path):
    """Build a knowledge graph dict from a single CSV file."""
    slug = csv_path.stem

    nodes = {}  # key: "type:label" -> node dict
    edges = []  # list of edge dicts

    def add_node(ntype, label):
        """Add a node if not already present. Returns the node ID."""
        nid = f"{ntype}:{label}"
        if nid not in nodes:
            nodes[nid] = {"id": nid, "type": ntype, "label": label}
        return nid

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        col_map = detect_columns(headers)

        max_col = max(col_map.values())

        for row_num, row in enumerate(reader, start=2):
            # Pad short rows
            if len(row) <= max_col:
                row.extend([""] * (max_col + 1 - len(row)))

            factor_val = row[col_map["factor"]].strip()
            adj_val = row[col_map["adjective"]].strip()
            syn_val = row[col_map["synonym"]].strip()
            verb_val = row[col_map["verb"]].strip()
            noun_val = row[col_map["noun"]].strip()

            # Skip rows with no factor
            if is_empty(factor_val):
                continue

            factor_id = add_node("factor", factor_val)

            # Adjective
            if not is_empty(adj_val):
                adj_id = add_node("adj", adj_val)
                edge = {"source": factor_id, "target": adj_id, "relation": "has_adjective"}
                edges.append(edge)

                # Synonym -> linked from adjective
                if not is_empty(syn_val):
                    syn_id = add_node("syn", syn_val)
                    edges.append({"source": adj_id, "target": syn_id, "relation": "has_synonym"})

                # Verb -> linked from adjective
                if not is_empty(verb_val):
                    verb_id = add_node("verb", verb_val)
                    edges.append({"source": adj_id, "target": verb_id, "relation": "has_verb"})

                # Noun -> linked from adjective
                if not is_empty(noun_val):
                    noun_id = add_node("noun", noun_val)
                    edges.append({"source": adj_id, "target": noun_id, "relation": "has_noun"})

    # Deduplicate edges
    seen_edges = set()
    unique_edges = []
    for e in edges:
        key = (e["source"], e["target"], e["relation"])
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(e)

    n_nodes = len(nodes)
    n_edges = len(unique_edges)
    n_factors = sum(1 for n in nodes.values() if n["type"] == "factor")
    density = n_edges / (n_nodes * (n_nodes - 1)) if n_nodes > 1 else 0.0

    graph = {
        "model": slug,
        "nodes": list(nodes.values()),
        "edges": unique_edges,
        "stats": {
            "n_nodes": n_nodes,
            "n_edges": n_edges,
            "n_factors": n_factors,
            "density": round(density, 6),
        },
    }
    return graph


def main():
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(DATASETS_DIR.glob("*.csv"))
    if not csv_files:
        print(f"ERROR: No CSV files found in {DATASETS_DIR}")
        sys.exit(1)

    print(f"Found {len(csv_files)} CSV datasets in {DATASETS_DIR}\n")
    print(f"{'Model':<16} {'Nodes':>7} {'Edges':>7} {'Factors':>8} {'Density':>10}")
    print("-" * 55)

    total_nodes = 0
    total_edges = 0

    for csv_path in csv_files:
        graph = build_graph(csv_path)
        slug = graph["model"]
        stats = graph["stats"]

        out_path = GRAPHS_DIR / f"{slug}_graph.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)

        print(
            f"{slug:<16} {stats['n_nodes']:>7} {stats['n_edges']:>7} "
            f"{stats['n_factors']:>8} {stats['density']:>10.6f}"
        )
        total_nodes += stats["n_nodes"]
        total_edges += stats["n_edges"]

    print("-" * 55)
    print(f"{'TOTAL':<16} {total_nodes:>7} {total_edges:>7}")
    print(f"\nWrote {len(csv_files)} graph JSON files to {GRAPHS_DIR}/")


if __name__ == "__main__":
    main()
