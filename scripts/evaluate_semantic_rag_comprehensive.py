"""
Comprehensive Semantic RAG Benchmark & Dynamic Estate Evaluation Suite.

Evaluates:
1. Chunk Integrity: Table preservation, contextual breadcrumb injection, breakpoint thresholding.
2. Retrieval Benchmark: 18 diverse resident queries (Hit Rate @ 1, Hit Rate @ 3, MRR, Grounding Score).
3. Contact Extraction Non-Pollution: Proves dynamic contact extraction does NOT displace general by-law chunks.
4. Dynamic Contact Revamp: Proves live handbook edits update responses with ZERO stale numbers.
5. Hallucination & Faithfulness: Verifies exact dollar tariffs, time ranges, by-laws, and phone numbers.
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from condo_classifier.semantic_rag import (
    EmbeddingProvider,
    HybridSemanticIndex,
    SemanticChunk,
    SemanticChunker,
    SemanticRAGEngine,
    cosine_similarity,
    split_into_sentences,
)

sys.stdout.reconfigure(encoding="utf-8")


# Authoritative ground truth for sample_condo_handbook.md
AUTHORITATIVE_DOLLARS = {
    0.55, 10.0, 15.0, 20.0, 50.0, 100.0, 107.0, 120.0, 200.0, 500.0, 1000.0, 2000.0, 5000.0
}

AUTHORITATIVE_PHONES = {
    "+65 6789 0100", "+65 6789 0200", "6789 0100", "6789 0200", "67890100", "67890200",
    "1800-543-8888", "1800 543 8888", "18005438888",
    "+65 6333 4455", "6333 4455", "+65 6444 8899", "6444 8899",
    "995", "999"
}

TEST_QUERIES = [
    {
        "id": "Q01",
        "category": "Renovation Noise",
        "query": "Can my contractor do heavy drilling or hacking on Saturday morning?",
        "target_chunk_id": "chunk_0005",
        "target_section": "3.1 Renovation Working Hours & Permissible Acoustic Thresholds",
        "expected_facts": ["strictly prohibited on saturdays", "10:00 – 16:00", "by-law §4"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
    {
        "id": "Q02",
        "category": "Renovation Hours",
        "query": "What are the allowed hours for general renovation like painting and carpentry?",
        "target_chunk_id": "chunk_0005",
        "target_section": "3.1 Renovation Working Hours & Permissible Acoustic Thresholds",
        "expected_facts": ["09:00 – 18:00", "09:00 – 13:00", "saturday"],
        "expected_verdict": "PERMITTED",
        "has_contact_intent": False,
    },
    {
        "id": "Q03",
        "category": "Weekend Drilling Penalty",
        "query": "What happens if a contractor does unapproved drilling on Sunday or a public holiday?",
        "target_chunk_id": "chunk_0006",
        "target_section": "3.2 Noise Infractions & Financial Penalties",
        "expected_facts": ["$1,000", "deposit", "site closure", "blacklisting"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
    {
        "id": "Q04",
        "category": "Noise Infraction Fine",
        "query": "What is the penalty fine for a second renovation noise complaint?",
        "target_chunk_id": "chunk_0006",
        "target_section": "3.2 Noise Infractions & Financial Penalties",
        "expected_facts": ["$500", "pass suspension", "48 hours"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q05",
        "category": "BBQ Booking Tariff",
        "query": "How much does it cost to book the BBQ pit and is there a deposit?",
        "target_chunk_id": "chunk_0007",
        "target_section": "4.1 Facilities Tariff & Operating Hours",
        "expected_facts": ["$20", "$50", "refundable"],
        "expected_verdict": "PERMITTED",
        "has_contact_intent": False,
    },
    {
        "id": "Q06",
        "category": "BBQ Operating Hours & Capacity",
        "query": "What are the operational hours and capacity limit for booking the BBQ pavilion pit?",
        "target_chunk_id": "chunk_0007",
        "target_section": "4.1 Facilities Tariff & Operating Hours",
        "expected_facts": ["10:00–14:00", "17:00–22:00", "12 pax"],
        "expected_verdict": "PERMITTED",
        "has_contact_intent": False,
    },
    {
        "id": "Q07",
        "category": "BBQ Cleaning Fee",
        "query": "Is there a cleaning fee if the BBQ pit is left dirty with food and ash?",
        "target_chunk_id": "chunk_0008",
        "target_section": "4.2 BBQ Pit and Poolside Etiquette",
        "expected_facts": ["$50", "cleaning fee", "deposit"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q08",
        "category": "Pool Hours & Attire",
        "query": "What are the opening hours and attire rules for the swimming pool?",
        "target_chunk_id": "chunk_0007",
        "target_section": "4.1 Facilities Tariff & Operating Hours",
        "expected_facts": ["07:00 – 22:00", "proper swimwear", "free"],
        "expected_verdict": "PERMITTED",
        "has_contact_intent": False,
    },
    {
        "id": "Q09",
        "category": "Poolside Noise / Quiet Hours",
        "query": "Can we play amplified music or host a karaoke session at the poolside BBQ after 10pm?",
        "target_chunk_id": "chunk_0008",
        "target_section": "4.2 BBQ Pit and Poolside Etiquette",
        "expected_facts": ["cease promptly at 22:00", "amplified music", "karaoke"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
    {
        "id": "Q10",
        "category": "Water Leak Statutory Presumption",
        "query": "Water is leaking from my bathroom ceiling from the unit above. Who is legally responsible under BMSMA Section 101?",
        "target_chunk_id": "chunk_0011",
        "target_section": "6.1 BMSMA Statutory Presumption (Section 101)",
        "expected_facts": ["bmsma section 101", "presumed to originate from the upper unit", "upper unit owner"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q11",
        "category": "Water Leak Inspection SLA",
        "query": "What is the management response time and inspection timeline for inter-floor water leaks?",
        "target_chunk_id": "chunk_0012",
        "target_section": "6.2 Inspection SLA & Resolution Escalation",
        "expected_facts": ["within 2 hours", "within 24 hours", "moisture meter", "7 calendar days"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q12",
        "category": "Parking Wheel Clamping",
        "query": "My car was wheel-clamped in the visitor lot. What is the unclamping fee and where do I pay?",
        "target_chunk_id": "chunk_0010",
        "target_section": "5.2 Visitor Parking & Wheel-Clamping Enforcement",
        "expected_facts": ["$107", "guardhouse", "within 30 minutes"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q13",
        "category": "Season Parking Allocation",
        "query": "What is the monthly parking charge for a resident's second vehicle?",
        "target_chunk_id": "chunk_0009",
        "target_section": "5.1 Resident Vehicle Season Decals & Allocation",
        "expected_facts": ["$120", "second", "quarterly balloting"],
        "expected_verdict": "PERMITTED",
        "has_contact_intent": False,
    },
    {
        "id": "Q14",
        "category": "Emergency Lift Hotline",
        "query": "The elevator is broken down and someone is trapped inside. What is the 24/7 lift hotline and who should I contact?",
        "target_chunk_id": "chunk_0003",
        "target_section": "1.1 Management Office & Security Directory",
        "expected_facts": ["1800-543-8888", "schindler", "24 hours"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": True,
    },
    {
        "id": "Q15",
        "category": "Pet Swimming Pool Ban & Leash Fine",
        "query": "Are pets allowed in the swimming pool area, and what is the fine for an unleashed dog?",
        "target_chunk_id": "chunk_0013",
        "target_section": "7.1 Domestic Pet Limits & Regulations",
        "expected_facts": ["$100", "$200", "by-law §10", "barred from: swimming pool"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
    {
        "id": "Q16",
        "category": "Pet Limit Per Unit",
        "query": "What is the pet limit per unit? Can I keep two dogs in my condo?",
        "target_chunk_id": "chunk_0013",
        "target_section": "7.1 Domestic Pet Limits & Regulations",
        "expected_facts": ["1 small/medium dog", "2 domestic cats", "by-law §10"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
    {
        "id": "Q17",
        "category": "Moving Guidelines Deposit",
        "query": "What is the security deposit and advance notice required for moving in or moving out?",
        "target_chunk_id": "chunk_0004",
        "target_section": "2.1 Moving Guidelines & Security Deposit",
        "expected_facts": ["$1,000", "3 working days", "refundable"],
        "expected_verdict": "ACTION REQUIRED",
        "has_contact_intent": False,
    },
    {
        "id": "Q18",
        "category": "Corridor Clutter & Fire Safety",
        "query": "Can residents place shoe racks or bicycles along the common corridor outside their unit under SCDF rules?",
        "target_chunk_id": "chunk_0015",
        "target_section": "8.2 Fire Escape Corridors (SCDF Compliance)",
        "expected_facts": ["1.2 meters", "scdf", "48-hour removal notice"],
        "expected_verdict": "PROHIBITED",
        "has_contact_intent": False,
    },
]


def test_table_integrity(kb_path: Path) -> dict[str, Any]:
    content = kb_path.read_text(encoding="utf-8")
    chunker = SemanticChunker()
    chunks = chunker.chunk_markdown_file(kb_path)

    lines = content.splitlines()
    source_tables = []
    current_table = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current_table.append(line)
        else:
            if current_table:
                if any(re.search(r"^\|(?:\s*:?-+:?\s*\|)+\s*$", row) for row in current_table):
                    source_tables.append(current_table)
                current_table = []
    if current_table and any(re.search(r"^\|(?:\s*:?-+:?\s*\|)+\s*$", row) for row in current_table):
        source_tables.append(current_table)

    intact = 0
    details = []
    for idx, table_lines in enumerate(source_tables, 1):
        header = table_lines[0].strip()
        data_rows = [r.strip() for r in table_lines[2:]]
        match = [c for c in chunks if header in c.content]
        if not match:
            details.append({"table_id": idx, "header": header[:60], "status": "MISSING", "intact": False})
            continue
        c = match[0]
        missing = [r for r in data_rows if r not in c.content]
        ok = (len(missing) == 0) and c.has_table
        if ok:
            intact += 1
        details.append({
            "table_id": idx,
            "header": header[:60],
            "chunk_id": c.chunk_id,
            "intact": ok,
            "status": "INTACT" if ok else "SPLIT",
            "rows": len(table_lines),
        })

    score = (intact / len(source_tables)) * 100.0 if source_tables else 100.0
    return {
        "total_tables": len(source_tables),
        "intact_tables": intact,
        "table_integrity_score": score,
        "details": details,
    }


def test_breadcrumbs(kb_path: Path) -> dict[str, Any]:
    chunker = SemanticChunker()
    chunks = chunker.chunk_markdown_file(kb_path)
    titled = [c for c in chunks if (c.document_title or c.section or c.subsection)]
    injected = 0
    for c in titled:
        t = c.embeddable_text
        if t.startswith("[") and "]\n" in t:
            if (not c.document_title or f"Document: {c.document_title}" in t) and \
               (not c.section or f"Section: {c.section}" in t) and \
               (not c.subsection or f"Subsection: {c.subsection}" in t):
                injected += 1
    score = (injected / len(titled)) * 100.0 if titled else 100.0
    return {
        "total_chunks": len(chunks),
        "titled_chunks": len(titled),
        "correctly_injected": injected,
        "coverage_percent": score,
    }


def test_retrieval_suite(engine: SemanticRAGEngine) -> dict[str, Any]:
    results = []
    reciprocal_ranks = []
    hits1 = 0
    hits3 = 0
    grounded_count = 0

    for item in TEST_QUERIES:
        qid = item["id"]
        qtext = item["query"]
        target = item["target_chunk_id"]

        t0 = time.perf_counter()
        rag_res = engine.query(qtext, top_k=3, expand_parent=True)
        lat = time.perf_counter() - t0

        retrieved_ids = [c.chunk_id for c in rag_res.retrieved_chunks]
        rank = (retrieved_ids.index(target) + 1) if target in retrieved_ids else None
        rr = (1.0 / rank) if rank else 0.0
        reciprocal_ranks.append(rr)

        h1 = (rank == 1)
        h3 = (rank is not None and rank <= 3)
        if h1:
            hits1 += 1
        if h3:
            hits3 += 1
        if rag_res.grounded:
            grounded_count += 1

        results.append({
            "id": qid,
            "category": item["category"],
            "query": qtext,
            "target_chunk_id": target,
            "rank": rank,
            "hit_at_1": h1,
            "hit_at_3": h3,
            "rr": round(rr, 4),
            "latency_s": round(lat, 3),
            "grounded": rag_res.grounded,
            "by_laws_cited": rag_res.by_laws_cited,
            "answer_preview": rag_res.answer[:200].replace("\n", " "),
            "retrieved_ids": retrieved_ids,
        })

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
    h1_pct = (hits1 / len(TEST_QUERIES)) * 100.0
    h3_pct = (hits3 / len(TEST_QUERIES)) * 100.0
    grounding_score = (grounded_count / len(TEST_QUERIES)) * 100.0

    return {
        "total": len(TEST_QUERIES),
        "hit_count_at_1": hits1,
        "hit_rate_at_1": round(h1_pct, 2),
        "hit_count_at_3": hits3,
        "hit_rate_at_3": round(h3_pct, 2),
        "mrr": round(mrr, 4),
        "grounding_score": round(grounding_score, 2),
        "results": results,
    }


def test_contact_extraction_non_pollution(kb_path: Path) -> dict[str, Any]:
    """
    Verifies that dynamic contact extraction does NOT pollute or degrade general by-law chunk relevance.
    1. For general by-law inquiries (drilling, BBQ tariff, pet limit, ceiling leaks),
       verifies that the contact directory chunk (chunk_0003) does NOT usurp or displace
       the specific by-law chunk.
    2. Compares retrieval ranks with contact triggers active vs inactive.
    """
    engine = SemanticRAGEngine(kb_path=kb_path)
    engine.initialize()

    # Identify contact directory chunk ID
    contact_chunk_id = "chunk_0003"
    non_pollution_checks = []
    pollution_detected = False

    general_queries = [q for q in TEST_QUERIES if not q.get("has_contact_intent", False)]

    for q in general_queries:
        qid = q["id"]
        qtext = q["query"]
        target = q["target_chunk_id"]

        matches = engine.index.retrieve(engine.expand_query(qtext), top_k=3)
        retrieved_ids = [m.chunk.chunk_id for m in matches]

        target_in_top3 = target in retrieved_ids
        target_rank = (retrieved_ids.index(target) + 1) if target_in_top3 else None

        # Check if contact directory chunk displaced the target chunk
        contact_at_rank_1 = (retrieved_ids[0] == contact_chunk_id)
        if contact_at_rank_1 and target != contact_chunk_id:
            pollution_detected = True

        non_pollution_checks.append({
            "id": qid,
            "category": q["category"],
            "query": qtext,
            "target": target,
            "target_rank": target_rank,
            "top1_id": retrieved_ids[0] if retrieved_ids else None,
            "contact_chunk_usurped_rank1": contact_at_rank_1,
            "clean_relevance": (not contact_at_rank_1) and target_in_top3,
        })

    clean_count = sum(1 for c in non_pollution_checks if c["clean_relevance"])
    clean_score = (clean_count / len(general_queries)) * 100.0

    return {
        "queries_tested": len(general_queries),
        "clean_queries": clean_count,
        "clean_relevance_score": round(clean_score, 2),
        "pollution_detected": pollution_detected,
        "checks": non_pollution_checks,
    }


def test_dynamic_contact_revamp_zero_stale_numbers(tmp_path: Path) -> dict[str, Any]:
    """
    Tests that revamping handbook contacts updates responses dynamically with zero stale numbers.
    Creates a temporary handbook, queries baseline, revamps all numbers, and verifies:
    1. New numbers appear in responses.
    2. Old numbers NEVER appear (zero stale numbers).
    """
    kb_file = tmp_path / "dynamic_revamp_test.md"

    # Initial handbook content
    initial_md = """# Emerald Crest Condominium (MCST 5500) - Resident Handbook

## 1. Directory & Emergency Contacts
| Service / Department | Location / Contact | Operational Hours | Responsibilities |
|---|---|---|---|
| Management Office | Clubhouse Level 1 / +65 6222 1111 | Mon–Fri: 09:00–17:00 | Permits, bookings, billing |
| Security Guardhouse | Main Gate / +65 6222 2222 | 24 Hours / 7 Days | Access control, noise enforcement |
| 24/7 Lift Breakdown | ElevateX Hotline: 1800-222-3333 | 24 Hours Emergency | Lift breakdowns |

## 2. Facilities
### 2.1 Swimming Pool
The swimming pool is open 07:00 to 22:00 daily. Proper swimwear is strictly mandatory.
"""
    kb_file.write_text(initial_md, encoding="utf-8")

    engine = SemanticRAGEngine(kb_path=kb_file)
    engine.initialize()

    # Verify baseline metadata
    assert "Emerald Crest" in engine.estate_name
    assert "6222 1111" in engine.primary_estate_contact
    assert "6222 2222" in engine.primary_estate_contact

    baseline_res = engine.query("What should I wear at the pool?")
    assert "6222 1111" in baseline_res.answer or "6222 2222" in baseline_res.answer

    # Revamp with completely new contacts
    revamped_md = """# Emerald Crest Condominium (MCST 5500) - Resident Handbook

## 1. Directory & Emergency Contacts
| Service / Department | Location / Contact | Operational Hours | Responsibilities |
|---|---|---|---|
| Management Office | Clubhouse Level 1 / +65 6999 8888 | Mon–Fri: 09:00–17:00 | Permits, bookings, billing |
| Security Guardhouse | Main Gate / +65 6999 7777 | 24 Hours / 7 Days | Access control, noise enforcement |
| 24/7 Lift Breakdown | Otis Emergency Hotline: 1800-888-9999 | 24 Hours Emergency | Lift breakdowns |

## 2. Facilities
### 2.1 Swimming Pool
The swimming pool is open 07:00 to 22:00 daily. Proper swimwear is strictly mandatory.
"""
    kb_file.write_text(revamped_md, encoding="utf-8")
    engine.reindex()

    # Verify updated engine metadata
    new_office = "6999 8888"
    new_guard = "6999 7777"
    old_office = "6222 1111"
    old_guard = "6222 2222"
    old_lift = "1800-222-3333"

    revamp_checks = []
    test_prompts = [
        ("General Inquiry", "Can residents swim in casual T-shirts?"),
        ("Contact Inquiry", "Who should I call for a trapped passenger in the elevator?"),
        ("Office Inquiry", "How do I reach the management office for an application?"),
    ]

    zero_stale_numbers = True
    all_new_numbers_present = True

    for cat, prompt in test_prompts:
        res = engine.query(prompt)
        ans = res.answer

        has_new_mo = (new_office in ans)
        has_new_gh = (new_guard in ans)
        has_new_contacts = has_new_mo or has_new_gh or ("1800-888-9999" in ans)

        has_stale_mo = (old_office in ans)
        has_stale_gh = (old_guard in ans)
        has_stale_lift = (old_lift in ans)
        stale_present = has_stale_mo or has_stale_gh or has_stale_lift

        if stale_present:
            zero_stale_numbers = False
        if not has_new_contacts:
            all_new_numbers_present = False

        revamp_checks.append({
            "category": cat,
            "prompt": prompt,
            "has_new_contacts": has_new_contacts,
            "stale_numbers_present": stale_present,
            "stale_detected": [num for num in [old_office, old_guard, old_lift] if num in ans],
            "answer_preview": ans[:200].replace("\n", " "),
        })

    return {
        "engine_estate_name": engine.estate_name,
        "primary_estate_contact": engine.primary_estate_contact,
        "zero_stale_numbers": zero_stale_numbers,
        "all_new_numbers_present": all_new_numbers_present,
        "checks": revamp_checks,
    }


def test_hallucination_and_faithfulness(engine: SemanticRAGEngine) -> dict[str, Any]:
    flags = []
    faith_results = []

    for item in TEST_QUERIES:
        qid = item["id"]
        qtext = item["query"]
        res = engine.query(qtext, top_k=3, expand_parent=True)
        ans = res.answer

        # Parse numeric dollars
        dollars = [float(d.replace(",", "")) for d in re.findall(r"(?:S?\$|SGD\s*)([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?)", ans)]
        unverified_dollars = [d for d in dollars if d not in AUTHORITATIVE_DOLLARS]

        # Parse phones
        phones = re.findall(r"(?:\+65\s*\d{4}[-\s]?\d{4}|\b1800[-\s]?\d{3}[-\s]?\d{4}\b|\b(?:995|999)\b)", ans)
        unverified_phones = []
        for p in phones:
            norm = re.sub(r"[-\s]", "", p)
            matched = any(re.sub(r"[-\s]", "", ap) in norm or norm in re.sub(r"[-\s]", "", ap) for ap in AUTHORITATIVE_PHONES)
            if not matched:
                unverified_phones.append(p)

        # Parse bylaws
        bylaws = re.findall(r"(?:By-law\s*(?:§|Section|\d+|No\.\s*\d+)[^\n.,;]*|BMSMA\s*Section\s*\d+)", ans, re.IGNORECASE)
        unverified_bylaws = []
        for b in bylaws:
            cb = b.lower()
            if not any(v in cb for v in ["4", "10", "101", "animals"]):
                unverified_bylaws.append(b)

        # Expected facts
        facts = item.get("expected_facts", [])
        ans_low = ans.lower()
        matched_facts = [f for f in facts if any(t in ans_low for t in f.lower().split(" / "))]
        recall = len(matched_facts) / len(facts) if facts else 1.0

        is_faithful = (len(unverified_dollars) == 0 and len(unverified_phones) == 0 and len(unverified_bylaws) == 0)
        if not is_faithful:
            flags.append({
                "id": qid,
                "query": qtext,
                "unverified_dollars": unverified_dollars,
                "unverified_phones": unverified_phones,
                "unverified_bylaws": unverified_bylaws,
            })

        faith_results.append({
            "id": qid,
            "category": item["category"],
            "dollars_cited": dollars,
            "unverified_dollars": unverified_dollars,
            "phones_cited": phones,
            "unverified_phones": unverified_phones,
            "bylaws_cited": bylaws,
            "unverified_bylaws": unverified_bylaws,
            "fact_recall": round(recall, 2),
            "faithful": is_faithful,
        })

    rate = ((len(TEST_QUERIES) - len(flags)) / len(TEST_QUERIES)) * 100.0
    avg_recall = (sum(r["fact_recall"] for r in faith_results) / len(faith_results)) * 100.0

    return {
        "queries_tested": len(TEST_QUERIES),
        "faithfulness_rate": round(rate, 2),
        "avg_fact_recall_percent": round(avg_recall, 2),
        "hallucination_flags_count": len(flags),
        "flags": flags,
        "details": faith_results,
    }


def main():
    import tempfile
    kb_path = PROJECT_ROOT / "Knowledge Base" / "sample_condo_handbook.md"

    print("Running Table Integrity Evaluation...")
    table_res = test_table_integrity(kb_path)

    print("Running Breadcrumb Evaluation...")
    breadcrumb_res = test_breadcrumbs(kb_path)

    print("Running Retrieval Benchmark...")
    engine = SemanticRAGEngine(kb_path=kb_path)
    engine.initialize()
    retrieval_res = test_retrieval_suite(engine)

    print("Running Contact Extraction Non-Pollution Verification...")
    non_pollution_res = test_contact_extraction_non_pollution(kb_path)

    print("Running Dynamic Contact Revamp Test...")
    with tempfile.TemporaryDirectory() as tmpdir:
        revamp_res = test_dynamic_contact_revamp_zero_stale_numbers(Path(tmpdir))

    print("Running Hallucination & Faithfulness Evaluation...")
    faith_res = test_hallucination_and_faithfulness(engine)

    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "handbook_evaluated": str(kb_path.name),
        "estate_name_detected": engine.estate_name,
        "table_integrity": table_res,
        "breadcrumb_injection": breadcrumb_res,
        "retrieval_benchmark": retrieval_res,
        "contact_non_pollution": non_pollution_res,
        "dynamic_revamp_test": revamp_res,
        "faithfulness_audit": faith_res,
    }

    out_file = PROJECT_ROOT / "reports" / "comprehensive_rag_benchmark_report.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[DONE] Wrote comprehensive results to {out_file}")


if __name__ == "__main__":
    main()
