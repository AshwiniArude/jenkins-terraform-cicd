"""Fill docs/Report_Template.docx with your screenshots -> docs/Final_Report.docx

Usage (from the project root):
    pip install python-docx
    python scripts/build_report.py
    python scripts/build_report.py --repo https://github.com/<you>/jenkins-terraform-cicd \
                                   --video https://youtu.be/xxxx --date "05 Nov 2026"

Screenshots go in screenshots/ named SS-01.png, SS-02.jpg ... (png/jpg/jpeg).
Each [[SS-xx]] placeholder in the template is replaced by that image; missing ones stay as placeholders.
"""
import argparse
import re
from pathlib import Path

from docx import Document
from docx.image.image import Image
from docx.oxml.ns import qn
from docx.shared import Inches

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "docs" / "Report_Template.docx"
OUTPUT = ROOT / "docs" / "Final_Report.docx"
SHOTS = ROOT / "screenshots"
TOKEN = re.compile(r"\[\[(SS-\d{2})\]\]")
MAX_W, MAX_H = 6.2, 7.6  # inches


def find_shot(ss_id):
    for ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"):
        p = SHOTS / f"{ss_id}{ext}"
        if p.exists():
            return p
    return None


def fit(path):
    img = Image.from_file(str(path))
    w, h = img.px_width, img.px_height
    width = MAX_W
    if h / w * width > MAX_H:
        width = MAX_H * w / h
    return Inches(width)


def iter_paragraphs(doc):
    yield from doc.paragraphs
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                yield from cell.paragraphs


def replace_text(doc, mapping):
    for p in iter_paragraphs(doc):
        for r in p.runs:
            for k, v in mapping.items():
                if v and k in r.text:
                    r.text = r.text.replace(k, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="GitHub repository URL")
    ap.add_argument("--video", help="Demo video URL")
    ap.add_argument("--date", help="Submission date text")
    args = ap.parse_args()

    doc = Document(str(TEMPLATE))
    inserted, missing = [], []

    for p in list(doc.paragraphs):
        m = TOKEN.search(p.text)
        if not m:
            continue
        ss = m.group(1)
        path = find_shot(ss)
        if path is None:
            missing.append(ss)
            continue
        # clear placeholder text and its dashed box/shading, then insert the image
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        pPr = p._p.get_or_add_pPr()
        for tag in ("w:pBdr", "w:shd"):
            el = pPr.find(qn(tag))
            if el is not None:
                pPr.remove(el)
        p.add_run().add_picture(str(path), width=fit(path))
        inserted.append(ss)

    replace_text(doc, {"<<REPO_LINK>>": args.repo, "<<VIDEO_LINK>>": args.video, "<<DATE>>": args.date})
    doc.save(str(OUTPUT))

    print(f"Saved: {OUTPUT}")
    print(f"Inserted {len(inserted)} screenshot(s): {', '.join(inserted) or '-'}")
    if missing:
        print(f"Missing {len(missing)} (placeholders kept): {', '.join(missing)}")
    left = [k for k, v in {"<<REPO_LINK>>": args.repo, "<<VIDEO_LINK>>": args.video,
                            "<<DATE>>": args.date}.items() if not v]
    print("Still to fill by hand in Word: " + ", ".join(left + ["<<COURSE NAME / CODE>>", "<<FACULTY NAME>>"]))
    print("Tip: open in Word, right-click the Table of Contents -> Update Field.")


if __name__ == "__main__":
    main()
