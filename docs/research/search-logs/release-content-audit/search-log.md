# Search log: opposing evidence on the weight-bearing claims (S23, release content audit)

Source Scout and Verifier, 2026-10-15. Times are UTC. The audit that reads this log is
[`release-content-audit.md`](../../release-content-audit.md) (Part 5, roadmap point 4). Search results and snippets
are finding aids only (RA-1, D-014); nothing here is evidence until a text is retrieved and read, and nothing found
here is recorded as canonical (S23 prompt §08: a found counter-source is a finding, not a claim).

## What was searched, and why these claims

Of the 59 weight-bearing claims, 37 quote official legal texts or definitions whose wording cannot be contested by
another source (an official text says what it says). The searches target the claims whose content another source
could contradict: the two supplier fields (who makes the HBM in the H100 and in Trainium2) and the AI Diffusion
rule's status, which the pages derive from its own dated events.

| Query | Mode | Target | Results read (titles only) | Outcome |
|---|---|---|---|---|
| `Trainium2 HBM3E supplier SK hynix Samsung Micron` | standard | Trainium2 supplier (`claim-semianalysis-trn2-hbm-samsung-2025`) | DIGITIMES 2023-12-07; TrendForce 2024-03-13 reposts; Korea JoongAng Daily (Micron, H200) | DIGITIMES retrieved (below); the rest repost `src-054` or concern other products |
| `NVIDIA H100 HBM3 supplier Samsung Micron SK hynix sole supplier 2023` | standard | H100 supplier (`claim-trendforce-h100-hbm3-primarily-sk-hynix-2024`) | TrendForce 2024-03-13 and its reposts (Business Wire, Design & Reuse, I-Connect007); DRAMeXchange | every result is the registered source `src-054` or a copy of it; no other statement about the H100's memory maker |
| `BIS rescission AI diffusion rule Federal Register rescind 2025-00636` | standard | the AI Diffusion rule's status (`policy-us-fr-2025-00636`) | BIS press release PDF (media.bis.gov); law-firm alerts (Baker McKenzie, Wiley, Kirkland, Steptoe, Hogan Lovells, Thompson Hine) | BIS release retrieved (below); law-firm alerts are secondary and not read as evidence |
| `Micron Technology Form 10-K fiscal year 2026 annual report filed October 2026` | standard | the four Micron values past the horizon (audit C-2) | an SEC EDGAR filing index entry titled "Form 10-K - FY2026"; third-party summaries | a pointer only: EDGAR is not retrieved without a declared identity (RA-3, RA-7); no company-hosted copy was sought |

## Retrievals

Plain curl 8.5.0 over HTTPS, default client identity (RA-1, RA-2). Bytes stay outside the repository.

| Time | URL | Status | Bytes | SHA-256 | Read |
|---|---|---|---|---|---|
| 2026-10-15T20:48:59Z | `https://apps.digitimes.com/news/a20231207PD211/samsung-sk-hynix-hbm3-aws.html` | 200 | 142531 | `d5edc2132ee075aa40421b31027c48335109bb1eac6374f8fc95113adfe1ba80` | headline only, "Samsung and SK Hynix will both supply HBM3 for AWS Trainium 2"; the body is paywalled (an access gap). The same article is T-21 / S-29 of S16.5 and S16.6, already recorded as a pointer that "disagrees in form" with SemiAnalysis (`hbm-supplier-research.md`) |
| 2026-10-15T20:49:00Z | `https://media.bis.gov/sites/default/files/documents/05.07%20Recission%20of%20AI%20Diffusion%20Press%20Release.pdf` | 200 | 162283 | `793bb718ba4358c4a928430c9f0bd3eeca6df9816d4360f59a4c416f32016b06` | read in full (pdftotext 24.02.0). Dated May 12, 2025: "the Department of Commerce (DOC) initiated a rescission of the Biden Administration's AI Diffusion Rule"; "BIS plans to publish a Federal Register notice formalizing the rescission"; the Under Secretary "has instructed BIS enforcement officials not to enforce" the rule |
| 2026-10-15T21:06:56Z | `https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens` (the address 2026-14132 prints on p.3, read across its line breaks) | 200 | 56313 | `aa94c08641fdc27c40300184825741b800b641ba370ced531fb409f00e93d5ec` | read in full. "FOR IMMEDIATE RELEASE | May 13, 2025"; "the Department of Commerce (DOC) announced a rescission"; "BIS plans to publish a regulation formalizing the rescission"; the same instruction not to enforce. **It differs from the PDF above** in its date (13, not 12 May), its verb ("announced", not "initiated"), what BIS plans ("a regulation", not "a Federal Register notice") and one guidance bullet; the PDF's own metadata gives a creation date of 2026-10-13. The page is the one the official text cites, so it is the source the audit proposes (`src-065` after the human's verdict, D-220); the PDF is not registered |
| 2026-10-15T20:51:25Z | `https://www.bis.gov/media/documents/bis-guidance-may-312026.pdf` (the address as 2026-14132 prints it, p.3) | 404 | 3736 | `3f0e979438990c1dda29ab284940ea624102be7d24f14a9080f4611a8bd2815f` | not found at the printed address; the printed address may carry a line-break artefact. Not retried at another address (a later session decides) |

## Outcome

- **No source contradicts a weight-bearing claim.** No retrieved text gives the H100 or Trainium2 a memory maker
  incompatible with the recorded one; the DIGITIMES headline adds a second maker for Trainium2 as a 2023 plan, which
  the record already allows ("it does not say that Samsung was the only supplier") and S16.6 already recorded.
- **One opposing text bears on a page's framing:** BIS's own release of 13 May 2025 on the AI Diffusion rule (the bis.gov page; a PDF copy dated 12 May differs), held
  until now only as a pointer inside 2026-14132's sentence (CD-7). It does not change the rule's recorded dates or
  derived status (no Federal Register text rescinds the rule; D-209, `change-detection.md` §1), but it is the
  issuing agency's statement that it announced a rescission and does not enforce the rule. Audit finding C-1.
