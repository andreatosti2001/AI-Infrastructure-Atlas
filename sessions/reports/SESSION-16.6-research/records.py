"""S16.6: the records the human approved on 2026-10-07 (H-2), written by the Extractor after the Verifier's re-read.

Adds 3 sources (D-146: registered when retrieved), 6 claims, and the Samsung Electronics company record (ID by ID-1 from its legal name: "Co., Ltd." is not on the
legal-form list, so it stays in the slug; recorded as debt).
The two supplier values are NOT set here: they wait for the presentation the human approves (H-3), because
both page builds stop when a supplier is named (D-130).

Run once, from the repository root: python sessions/reports/SESSION-16.6-research/records.py
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
REVIEW = {"verdict": "accepted", "reviewer": "human", "reviewed_on": "2026-10-07",
          "recorded_in": "sessions/reports/SESSION-16.6-REPORT.md"}


def read(at, sha):
    return {"accessed_at": at, "sha256": sha}


TRENDFORCE = read("2026-10-07T16:44Z", "bc09c9b87630057287f07954a07427f1888518dbd64f5fda30ca9af72b97abd7")
SEMIANALYSIS = read("2026-10-07T16:45Z", "f5516abea183865b8a650bbb62040ea7fed56dec5263272a2e2b6d1c04bacf79")
SAMSUNG = read("2026-10-07T15:27Z", "626dd527bb25dc1ffd7ce72d84a0ded10f4d8f3daa0352d6c6b6be07c3eae73a")

SOURCES = [
    {"id": "src-054", "source_class": "market_research_consultancy",
     "title": "HBM3 Initially Exclusively Supplied by SK Hynix, Samsung Rallies Fast After AMD Validation, Says TrendForce",
     "publisher": "TrendForce (Press Center)", "publisher_entity": {"state": "not_applicable"}, "authors": "Avril Wu",
     "url": "https://www.trendforce.com/presscenter/news/20240313-12075.html",
     "stated_dates": [{"kind": "published", "date": "2024-03-13"}],
     "retrieval": {"method": "automated", **TRENDFORCE}},
    {"id": "src-055", "source_class": "market_research_consultancy",
     "title": "AWS Trainium3 Deep Dive | A Potential Challenger Approaching",
     "publisher": "SemiAnalysis", "publisher_entity": {"state": "not_applicable"},
     "authors": "Dylan Patel, Daniel Nishball, Wega Chu, and others",
     "url": "https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential",
     "stated_dates": [{"kind": "published", "date": "2025-12-04"}],
     "retrieval": {"method": "automated", **SEMIANALYSIS}},
    {"id": "src-056", "source_class": "company_filing",
     "title": "2025 Business Report, for the year ended December 31, 2025 (English)",
     "publisher": "Samsung Electronics Co., Ltd.", "publisher_entity": "company-samsung-electronics-co-ltd",
     "authors": {"state": "not_researched"},
     "url": "https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_Interim_Report.pdf",
     "stated_dates": {"state": "undated"},
     "retrieval": {"method": "automated", **SAMSUNG}, "filing_copy": "filer_hosted_not_checked"},
]

CLAIMS = [
    {"id": "claim-trendforce-h100-hbm3-primarily-sk-hynix-2024", "claim_type": "ATTRIBUTION",
     "statement": "TrendForce stated on 13 March 2024 that the current HBM3 supply for NVIDIA's H100 solution was primarily met by SK hynix. It is TrendForce's own assessment; the release names no source for it.",
     "evidence_status": "supported",
     "citations": [{"source_id": "src-054", "locator": "the release body, the paragraph beginning 'The current HBM3 supply', its first sentence",
                    "anchor": "The current HBM3 supply for NVIDIA’s H100 solution is primarily met by SK hynix",
                    "standing": "originator", "read": TRENDFORCE,
                    "third_party_criteria": {
                        "recognised": {"met": True, "reason": "an established, independent market-research firm on S16.6's list of recognised analysis firms (plan.md), approved by the human on 2026-10-07; citation by parties or governments was not checked"},
                        "independent": {"met": True, "reason": "the release states no sponsor, commission or tie to NVIDIA or SK hynix; the firm's ownership was not researched"}}}],
     "as_of": {"state": "not_stated"}, "review": REVIEW, "verified_on": "2026-10-07"},
    {"id": "claim-semianalysis-trn2-hbm-samsung-2025", "claim_type": "ATTRIBUTION",
     "statement": "SemiAnalysis stated on 4 December 2025 that the 5.7 Gbps HBM pin speed used in Trn2 (AWS Trainium2) was due to using memory supplied by Samsung. It is SemiAnalysis's own assessment; it names no source, and it does not say that Samsung was the only supplier.",
     "evidence_status": "supported",
     "citations": [{"source_id": "src-055", "locator": "the free part, the paragraph beginning 'The HBM3E is upgraded to 12-high for Trainium3', its third and fourth sentences",
                    "anchor": "the 5.7Gbps pin speed that was used in Trn2 is more in line with HBM3 speeds",
                    "standing": "originator", "read": SEMIANALYSIS,
                    "third_party_criteria": {
                        "recognised": {"met": False, "reason": "an independent semiconductor analysis firm widely read in the industry, but the Atlas found no evidence that parties, governments or intergovernmental bodies routinely cite it"},
                        "independent": {"met": True, "reason": "the text states no sponsor or tie to Amazon, Samsung, SK hynix or Micron; the firm sells research and consulting to the industry"}}},
                   {"source_id": "src-055", "locator": "the same paragraph, its fourth sentence",
                    "anchor": "The speed deficiency was due to using memory supplied by Samsung",
                    "standing": "originator", "read": SEMIANALYSIS,
                    "third_party_criteria": {
                        "recognised": {"met": False, "reason": "as the citation above"},
                        "independent": {"met": True, "reason": "as the citation above"}}}],
     "as_of": {"state": "not_stated"}, "review": REVIEW, "verified_on": "2026-10-07"},
    {"id": "claim-samsung-electronics-legal-name", "claim_type": "FACT",
     "statement": "The company's legal and commercial name is Samsung Electronics Co., Ltd.",
     "evidence_status": "supported",
     "citations": [{"source_id": "src-056", "locator": "p.4, 'A. Legal, Commercial name', its line",
                    "anchor": "Samsung Electronics Co., Ltd.", "standing": "party", "read": SAMSUNG}],
     "as_of": "2025-12-31", "review": REVIEW, "verified_on": "2026-10-07"},
    {"id": "claim-samsung-electronics-head-office-address", "claim_type": "FACT",
     "statement": "Samsung Electronics' corporate headquarters address is 129, Samsung-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do, 16677, Korea.",
     "evidence_status": "supported",
     "citations": [{"source_id": "src-056", "locator": "p.4, 'C. Address, phone number, and English language website of the corporate headquarters', the address line",
                    "anchor": "Address: 129, Samsung-ro, Yeongtong-gu, Suwon-si, Gyeonggi-do, 16677, Korea",
                    "standing": "party", "read": SAMSUNG}],
     "as_of": "2025-12-31", "review": REVIEW, "verified_on": "2026-10-07"},
    {"id": "claim-samsung-electronics-headquartered-in-kr", "claim_type": "DERIVATION",
     "statement": "Samsung Electronics' headquarters is in the country with ISO 3166 code KR.",
     "evidence_status": "supported",
     "input_claim_ids": ["claim-samsung-electronics-head-office-address", "claim-iso-3166-2-kr-41", "claim-iso-3166-1-kr"],
     "reasoning": "The filing gives an address in Gyeonggi-do, Korea (claim-samsung-electronics-head-office-address). ISO 3166-2 lists Gyeonggi-do as KR-41, a subdivision of the entry whose alpha-2 code is KR (claim-iso-3166-2-kr-41, claim-iso-3166-1-kr). So the country is the one coded KR. The step is the Atlas's, not the filing's (D-057).",
     "review": REVIEW, "verified_on": "2026-10-07"},
    {"id": "claim-samsung-electronics-memory-products", "claim_type": "FACT",
     "statement": "Samsung Electronics states that its DS Division manufactures and sells DRAM, NAND flash and mobile APs.",
     "evidence_status": "supported",
     "citations": [{"source_id": "src-056", "locator": "p.22, the paragraph on the company's businesses, the sentence beginning 'For components'",
                    "anchor": "the DS Division manufactures and sells DRAM, NAND flash, and mobile APs",
                    "standing": "party", "read": SAMSUNG}],
     "as_of": "2025-12-31", "review": REVIEW, "verified_on": "2026-10-07"},
]

COMPANY = {
    "id": "company-samsung-electronics-co-ltd", "type": "company", "name": "Samsung Electronics",
    "aliases": ["Samsung Electronics Co., Ltd."],
    "identity_claim_ids": ["claim-samsung-electronics-legal-name"],
    "legal_name": [{"value": "Samsung Electronics Co., Ltd.", "claim_ids": ["claim-samsung-electronics-legal-name"]}],
    "incorporated_in": {"state": "not_researched"},
    "headquartered_in": [{"value": "jurisdiction-kr", "claim_ids": ["claim-samsung-electronics-headquartered-in-kr"]}],
    "roles": [{"value": "memory_manufacturer", "claim_ids": ["claim-samsung-electronics-memory-products"]}],
}


def append(name, records):
    p = R / "data" / name
    data = json.loads(p.read_text(encoding="utf-8"))
    ids = {r["id"] for r in data}
    assert not ids & {r["id"] for r in records}, f"{name}: already added"
    p.write_text(json.dumps(data + records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    append("sources.json", SOURCES)
    append("claims.json", CLAIMS)
    append("companies.json", [COMPANY])
    print("added: 3 sources, 6 claims, 1 company")
