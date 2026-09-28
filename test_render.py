from schema import (
    DocumentAnnotation, BequestLanguage, IncomeBeneficiaries,
    RestrictionsContingencies, Finding, DefinedTerm, UMMention,
    UncategorizedFinding,
)
from render import render_to_workbook

annotation = DocumentAnnotation(
    document_name="Herrold Interim Trust — 5th Amendment Herrold Trust (Package B, 10 pp.)",
    bequest_language=BequestLanguage(
        location=Finding(status="Found", answer=None,
            citation="Article 11 / §1 / Page 2; Article 6 / §2 / Page 1"),
        verbatim_text=Finding(status="Found", answer=(
            "Beneficiary Name: UNIVERSITY OF MIAMI, FROST SCHOOL OF MUSIC, "
            "FEIN #59-0621158, TO BE USED FOR STUDENT SCHOLARSHIP FUND. Share: 100%. "
            "Also: my Trustee shall deliver possession of Trustor's cello to her for "
            "the express purpose of hand delivering it to the UNIVERSITY OF MIAMI, "
            "SCHOOL OF MUSIC."),
            citation="Article 11 / §1 / Page 2; Article 6 / §2 / Page 1"),
        plain_english_summary=Finding(status="Found", answer=(
            "UM's Frost School of Music receives 100% of the residue for its "
            "Student Scholarship Fund, plus the Trustor's cello."),
            citation="Article 11 / §1 / Page 2"),
        trustee_executor_names=Finding(status="Found",
            answer="Trustee: Stephen George Herrold", citation="Preamble / Page 1"),
        trustee_executor_contact=Finding(status="Not in this document",
            note="Only the drafting attorney's contact info appears (Law Offices "
                 "of Roy W. Litherland); no contact info for Herrold himself."),
        um_receives=Finding(status="Found", answer=(
            "100% of the Survivor's/Family/Marital Balance residue, after the "
            "$50,000 distribution to Clarice Munn Burkhart; plus the Trustor's cello."),
            citation="Article 11 / §1 / Page 2; Article 6 / §4 / Page 2"),
        trigger_event=Finding(status="Found",
            answer="Death of the Surviving Trustor, Stephen George Herrold.",
            citation="Article 11 / §1 / Page 2"),
    ),
    income_beneficiaries=IncomeBeneficiaries(
        count=Finding(status="Found", answer="One", citation="Article 11 / §1(a)(1) / Page 3"),
        names_and_relationship=Finding(status="Found",
            answer="University of Miami, Frost School of Music — no relationship stated (institutional beneficiary).",
            citation="Article 11 / §1(a)(1) / Page 3"),
        timing_implication=Finding(status="Found",
            answer="UM receives 100% upon the surviving trustor's death; no other life beneficiary delays it.",
            citation="Article 11 / §1(a)(1) / Page 3"),
    ),
    restrictions=RestrictionsContingencies(
        primary_or_contingent=Finding(status="Found",
            answer="Primary, subject to the $50,000 specific distribution to Clarice Munn Burkhart.",
            citation="Article 11 / §1(a)(1) / Page 3; Article 6 / §4 / Page 2"),
        conditions_precedent=Finding(status="Found",
            answer="Stephen George Herrold must be deceased; the $50,000 distribution to Clarice Munn Burkhart must be satisfied first.",
            citation="Article 6 / §4 / Page 2"),
        other_restrictions=Finding(status="Found", answer=(
            "UM's school must remain tax-exempt; gift must be applied to the "
            "Student Scholarship Fund; trustee may postpone distribution for a "
            "'compelling reason'; a no-contest clause applies; interest lapses if "
            "the school is involved in more than a mere-form-change merger."),
            citation="Article 11 / §1(a)(2) / Page 3; Article 11 / §2 / Pages 4-5; Article 11 / §5 / Pages 7-8"),
    ),
    defined_terms=[
        DefinedTerm(term="Trustee", finding=Finding(status="Found",
            answer="Stephen George Herrold.", citation="Preamble / Page 1")),
        DefinedTerm(term="Trustor", finding=Finding(status="Found",
            answer="Stephen George Herrold (sole surviving Trustor after Rebecca Munn Herrold's death).",
            citation="Preamble / Page 1")),
        DefinedTerm(term="Compelling Reason", finding=Finding(status="Found",
            answer="Nine enumerated grounds for postponing a distribution, incl. "
                   "special needs, age under 25, undue influence, substance abuse, "
                   "pending divorce, financial difficulty, tax disadvantage, tax minimization.",
            citation="Article 11 / §2(e) / Page 5")),
    ],
    um_mentions=[
        UMMention(exact_text="...hand delivering it to the UNIVERSITY OF MIAMI, SCHOOL OF MUSIC.",
            finding=Finding(status="Found", citation="Article 6 / §2 / Page 1")),
        UMMention(exact_text="Beneficiary Name: UNIVERSITY OF MIAMI, FROST SCHOOL OF MUSIC, FEIN #59-0621158...",
            finding=Finding(status="Found", citation="Article 11 / §1 / Page 2")),
        UMMention(exact_text="...Distribution and Administration of Trust Share for UNIVERSITY OF MIAMI, FROST SCHOOL OF MUSIC...",
            finding=Finding(status="Found", citation="Article 11 / §1(a) / Page 3")),
        UMMention(exact_text="Our Trustee shall promptly pay to... the UNIVERSITY OF MIAMI, FROST SCHOOL OF MUSIC, the entire net income and principal...",
            finding=Finding(status="Found", citation="Article 11 / §1(a)(1) / Page 3")),
        UMMention(exact_text="If the UNIVERSITY OF MIAMI, FROST SCHOOL OF MUSIC is not in existence or has been involved in a merger...",
            finding=Finding(status="Found", citation="Article 11 / §1(a) / Page 3")),
    ],
    found_but_uncategorized=[
        UncategorizedFinding(text="This document revokes the Fourth Amendment in its entirety.",
            citation="Preamble / Page 1",
            note="The Fourth Amendment itself isn't in this file — its effect can't be assessed without it."),
        UncategorizedFinding(text="UM has a limited power of appointment over its share.",
            citation="Article 11 / §3 / Page 6"),
        UncategorizedFinding(text="No-contest clause: a beneficiary who contests the trust without probable cause forfeits their interest.",
            citation="Article 11, No Contest Clause / Pages 7-8"),
    ],
    judgment_calls=[
        "Treated the Article 11 §1 distribution language as the operative 'bequest language' even though the document never uses the word 'bequest'.",
        "Read the $50,000 distribution to Clarice Munn Burkhart as coming before UM's residuary share, based on document order rather than an express priority clause.",
    ],
    questions_for_client=[
        "Does the $50,000 distribution to Clarice Munn Burkhart affect the calculation of UM's residuary share?",
        "Do we have the original Fourth Amendment on file, to confirm what its revocation actually changes?",
    ],
)

render_to_workbook(
    annotation,
    template_path="/mnt/user-data/uploads/MiLA_Annotation_Template_v0.xlsx",
    out_path="/home/claude/mila_pipeline/out/Herrold_annotation_TEST.xlsx",
)
print("rendered OK")
