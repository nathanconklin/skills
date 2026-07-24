---
name: nathan-whitepaper
description: Convert Markdown files into Word (.docx) whitepapers using Nathan's standard whitepaper template (Virginia Tech logo headers, "Page X of Y" footer, Times New Roman body, centered title and author block, syntax-highlighted code blocks). Use this skill whenever the user asks to turn a Markdown document, draft, paper, or report into a Word document, whitepaper, prelim document, or "my standard format" -- even if they don't say "template" explicitly. Also use it when regenerating or updating a whitepaper .docx from an edited .md source. This skill is fully self-contained in this single file; the converter script and the entire template (styles, headers, VT logo image) are embedded below.
---

# Nathan's Whitepaper (Markdown -> Word), single-file skill

Converts a Markdown document into a .docx matching Nathan's standard whitepaper
format. Everything -- the converter and the entire template (page geometry, VT-logo
headers, footer, styles, numbering, the logo image itself) -- is embedded in the
Python script at the bottom of this file. There are no other files to fetch.

## Workflow

1. Extract the converter: copy the entire contents of the python code fence at
   the bottom of this file, byte for byte, into `/home/claude/nathan_whitepaper.py`.
   Do not retype or reformat it; the base64 block near the top of the script is the
   embedded VT logo and must be preserved exactly.
2. Locate the source .md file (usually in /mnt/user-data/uploads). Skim its first
   ~15 lines for the title (first `# H1`) and the italic metadata lines under it
   (subtitle and/or author lines).
3. Write a small `config.json` (see below) filling in anything the Markdown does
   not carry -- most importantly `header_title` and author emails.
4. Run it:

   `python3 /home/claude/nathan_whitepaper.py input.md output.docx --config config.json`

   Add `--image-dir DIR` if the Markdown references images by relative paths that
   live somewhere other than next to the .md file.
5. Verify the result. Convert to PDF and check both the layout and the numbering:

   - `soffice --headless --convert-to pdf output.docx`
   - `pdftotext output.pdf - | grep -o "Page [0-9]* of [0-9]*"`

   The footers must read Page 1 of N through Page N of N with no gaps or
   repeats; if they do not, report it rather than shipping the file. Also
   rasterize (`pdftoppm -jpeg -r 60`) and confirm the header rule: page 1 shows
   the VT logo ONLY; page 2 and every later page shows the logo plus the
   right-aligned running title and author line. Check the code/table rendering
   on a later page while there.
6. Copy the .docx to /mnt/user-data/outputs and present it.

## Page numbering and headers (how they work, do not "fix" them)

- The footer's "Page X of Y" uses live PAGE and NUMPAGES field objects -- the
  identical construction Word inserts via Insert > Page Number > "Page X of Y".
  Word recomputes header/footer fields while it paginates, so the numbers stay
  correct as pages are added or removed, exactly like natively inserted ones.
- The document contains NO update-at-open trigger of any kind: no
  `updateFields` flag in settings.xml and no `w:dirty` attribute on any field.
  Both of those mechanisms cause Word's "this document contains fields that may
  refer to other files" prompt. Never add either back.
- The script bakes the rendered page count into the fields' cached values (it
  prints "Page count: N (baked into footer fields)"), so the file shows the
  right total everywhere from the moment it is delivered, including in viewers
  that never recalculate fields.
- Header/footer references and `titlePg` are stated explicitly on EVERY sectPr,
  never inherited across sections, so headers apply deterministically: VT logo
  only on page 1, logo + right-aligned running title and author line on every
  page after. Keep it that way if editing the script.

## config.json

All keys optional; the script infers what it can from the Markdown.

    {
      "title": "Override for the document title",
      "subtitle": "Centered italic line under the title",
      "header_title": "Short running title for the page header",
      "header_author": "Nathan Conklin, nathan.conklin@vt.edu",
      "authors": [
        {"name": "Nathan Conklin",
         "lines": ["nathan.conklin@vt.edu", "Department of Computer Science,", "Virginia Tech"]}
      ]
    }

Guidance:

- **header_title**: defaults to the full document title, which is often too long
  and wraps to two lines in the header. Craft a shortened form (<= ~75 characters);
  keeping the part before a colon plus a trimmed subtitle usually works well.
- **Nathan's defaults**: when the author is Nathan and the Markdown gives no email,
  fill in `nathan.conklin@vt.edu`, `Department of Computer Science,`,
  `Virginia Tech` (academic work) or `SEACORP` (work documents) -- infer from
  context or ask if unclear.
- **Authors**: one author renders as a single centered block; two or more render
  side by side in columns. Each author is name + up to ~3 lines (email,
  department, institution).
- The script auto-detects author lines among the italic metadata (they contain an
  `@`, "Department", "University", etc.); other italic lines become the subtitle.

## What the template produces

- US Letter, 1" top/bottom and 0.75" side margins.
- Page 1 header: VT logo only. Every page after page 1: logo left, running
  title + author line right-aligned. Footer: "Page X of Y" right-aligned, as
  live auto-updating fields (see above).
- Title 18pt bold centered; Heading1/2/3 for `##`/`###`/`####`; body is Times New
  Roman 10pt, 1.15 line spacing. The first `# H1` is consumed as the document
  title and does not repeat as a body heading; `---` rules are dropped.
- Code fences -> bordered, light-gray-shaded box in Consolas 8pt with pygments
  syntax highlighting (falls back to plain monospace without pygments). The fence
  language tag never leaks into the document.
- Markdown tables -> bordered tables with a bold, shaded header row and column
  widths proportioned to content.
- Bullet/numbered lists (2 nesting levels), **bold**, *italic*, `inline code`
  (Consolas), links as real hyperlinks, `>` blockquotes as indented italic.
- Standalone images -> centered figure with an auto-numbered italic
  "Figure N: alt text" caption. Missing image paths are skipped with a stderr
  warning -- check it and tell the user if a figure was dropped.

## Limitations

- Footnotes, task lists, HTML blocks, and multi-paragraph list items are not
  supported; flag anything that gets dropped rather than silently shipping it.
- If wanted figures exist only in a previous .docx (not the .md), extract them
  from that docx (`unzip`, `word/media/`) and reference them from the Markdown as
  `![caption](path.png)` before converting.

## Converter script

Save everything inside this fence verbatim as `/home/claude/nathan_whitepaper.py`:

````python
#!/usr/bin/env python3
"""Convert a Markdown file into a Word whitepaper in Nathan's standard format.

Fully self-contained: the whitepaper template (VT-logo headers, "Page X of Y"
footer, Times New Roman styles, list numbering) is embedded in this script, so
no external template file is needed.

Usage:
    python3 nathan_whitepaper.py input.md output.docx [--config config.json] [--image-dir DIR]

Optional config.json keys (all optional; inferred from the markdown otherwise):
    title          document title (default: first H1)
    subtitle       centered italic line under the title
    header_title   short running title for the page header (default: title)
    header_author  author line in the page header, e.g. "Nathan Conklin, nathan.conklin@vt.edu"
    authors        list of {"name": ..., "lines": ["email", "Dept", "University"]}
                   Two or more authors render side by side in columns.
"""
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

EMU_PER_INCH = 914400
CONTENT_WIDTH_DXA = 10080  # 12240 - 1080*2 (US Letter, 0.75" side margins)
CONTENT_WIDTH_EMU = 7 * EMU_PER_INCH

try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.token import Token
    HAVE_PYGMENTS = True
except ImportError:
    HAVE_PYGMENTS = False

# ============================================================ embedded template
VT_LOGO_B64 = """
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
iqCqqv8HnvpGremFBRgAAAAASUVORK5CYII=
"""

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

STYLES_XML = XML_DECL + f'<w:styles {W_NS}>' + '''<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="200" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="10"/><w:qFormat/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:bCs/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="200" w:after="0"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:bCs/><w:color w:val="4F81BD"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="34"/><w:qFormat/><w:pPr><w:ind w:left="720"/><w:contextualSpacing/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="35"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepLines/><w:jc w:val="center"/></w:pPr><w:rPr><w:i/><w:iCs/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="10080"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="10080"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="39"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''

NUMBERING_XML = XML_DECL + f'<w:numbering {W_NS}>' + '''<w:abstractNum w:abstractNumId="90"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#61623;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr></w:lvl><w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="o"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:hint="default"/></w:rPr></w:lvl><w:lvl w:ilvl="2"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#61607;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="2160" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Wingdings" w:hAnsi="Wingdings" w:hint="default"/></w:rPr></w:lvl></w:abstractNum><w:abstractNum w:abstractNumId="91"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl><w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="lowerLetter"/><w:lvlText w:val="%2."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr></w:lvl><w:lvl w:ilvl="2"><w:start w:val="1"/><w:numFmt w:val="lowerRoman"/><w:lvlText w:val="%3."/><w:lvlJc w:val="right"/><w:pPr><w:ind w:left="2160" w:hanging="180"/></w:pPr></w:lvl></w:abstractNum><w:num w:numId="100"><w:abstractNumId w:val="90"/></w:num><w:num w:numId="101"><w:abstractNumId w:val="91"/></w:num></w:numbering>'''

# NOTE: deliberately no <w:updateFields/> here — that flag makes Word show
# "This document contains fields that may refer to other files..." on open.
# PAGE/NUMPAGES recalculate automatically during pagination, and correct cached
# values are baked in by the page-count pass below, so the prompt is unnecessary.
SETTINGS_XML = XML_DECL + f'<w:settings {W_NS}>' + ('<w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/>'
    '<w:characterSpacingControl w:val="doNotCompress"/>'
    '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
    '</w:settings>')

LOGO_DRAWING = ('<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="114300" distR="114300" simplePos="0" relativeHeight="251655168" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">'
    '<wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="margin"><wp:posOffset>0</wp:posOffset></wp:positionH>'
    '<wp:positionV relativeFrom="page"><wp:posOffset>457200</wp:posOffset></wp:positionV>'
    '<wp:extent cx="1408176" cy="265176"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
    '<wp:docPr id="10" name="VT logo"/>'
    '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="10" name="VT logo"/><pic:cNvPicPr/></pic:nvPicPr>'
    '<pic:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
    '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="1408176" cy="265176"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
    '</pic:pic></a:graphicData></a:graphic></wp:anchor></w:drawing></w:r>')

HEADER_DEFAULT_XML = XML_DECL + f'<w:hdr {W_NS}>' + ('<w:p><w:pPr><w:pStyle w:val="Header"/><w:jc w:val="right"/></w:pPr>'
    '<w:r><w:t xml:space="preserve">{{HEADER_TITLE}}</w:t></w:r><w:r><w:br/></w:r>'
    '<w:r><w:t xml:space="preserve">{{HEADER_AUTHOR}}</w:t></w:r>' + LOGO_DRAWING + '</w:p></w:hdr>')

HEADER_FIRST_XML = XML_DECL + f'<w:hdr {W_NS}>' + ('<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr>'
    + LOGO_DRAWING + '</w:p></w:hdr>')

def footer_xml(numpages="1"):
    """Right-aligned "Page X of Y" footer built from live PAGE and NUMPAGES field
    objects -- the identical construction Word itself inserts via Insert > Page
    Number > "Page X of Y". Word recomputes header/footer fields during
    pagination (that is layout behavior, not an "update fields at open" action),
    so numbers stay correct as pages are added or removed.

    Deliberately NO w:dirty attribute on any field and NO updateFields flag in
    settings.xml: both of those trigger Word's "this document contains fields
    that may refer to other files" prompt at open. Do not add either back.
    numpages is the cached value, patched to the true count by the render pass
    so the file is correct the moment it is delivered."""
    return XML_DECL + f'<w:ftr {W_NS}>' + ('<w:p><w:pPr><w:pStyle w:val="Footer"/><w:jc w:val="right"/></w:pPr>'
        '<w:r><w:t xml:space="preserve">Page </w:t></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>1</w:t></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
        '<w:r><w:t xml:space="preserve"> of </w:t></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>{numpages}</w:t></w:r>'
        '<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p></w:ftr>')

HEADER_REL_XML = XML_DECL + ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vtlogo.png"/>'
    '</Relationships>')

ROOT_RELS_XML = XML_DECL + ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>')

DOC_RELS_BASE = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
    '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    '<Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
    '<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
    '<Relationship Id="rId10" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header2.xml"/>'
    '<Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer2.xml"/>')

CONTENT_TYPES = XML_DECL + ('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '{{EXTRA_DEFAULTS}}'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
    '<Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
    '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
    '<Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
    '</Types>')

DOC_ROOT_OPEN = XML_DECL + f'<w:document {W_NS}>'

# Colors chosen to read well on the light-gray code background
if HAVE_PYGMENTS:
    TOKEN_COLORS = [
        (Token.Comment, ("6A9955", False, True)),
        (Token.Keyword, ("0000CC", True, False)),
        (Token.Name.Tag, ("00509E", True, False)),
        (Token.Name.Attribute, ("00509E", False, False)),
        (Token.Name.Function, ("795E26", False, False)),
        (Token.Name.Class, ("267F99", True, False)),
        (Token.Name.Builtin, ("267F99", False, False)),
        (Token.Name.Decorator, ("AF00DB", False, False)),
        (Token.Literal.String, ("A31515", False, False)),
        (Token.Literal.Number, ("098658", False, False)),
        (Token.Operator, ("444444", False, False)),
        (Token.Punctuation, ("444444", False, False)),
    ]
else:
    TOKEN_COLORS = []


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def token_style(ttype):
    for base, style in TOKEN_COLORS:
        if ttype in base:
            return style
    return None


# ---------------------------------------------------------------- inline markdown
INLINE_RE = re.compile(
    r"(?P<img>!\[(?P<imgalt>[^\]]*)\]\((?P<imgsrc>[^)\s]+)[^)]*\))"
    r"|(?P<link>\[(?P<ltext>[^\]]+)\]\((?P<lurl>[^)\s]+)[^)]*\))"
    r"|(?P<bi>\*\*\*(?P<bitext>.+?)\*\*\*)"
    r"|(?P<b>\*\*(?P<btext>.+?)\*\*)"
    r"|(?P<i>\*(?P<itext>[^*]+?)\*)"
    r"|(?P<i2>_(?P<i2text>[^_]+?)_)"
    r"|(?P<c>`(?P<ctext>[^`]+?)`)"
)


class DocBuilder:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.rels = []            # extra rels appended to document.xml.rels
        self.media = []           # (src_path, target_name)
        self.next_rid = 100
        self.fig_count = 0
        self.need_jpeg_ct = False

    def new_rid(self):
        self.next_rid += 1
        return f"rId{self.next_rid}"

    # ---------- runs
    def run(self, text, bold=False, italic=False, code=False, color=None, sz=None):
        rpr = ""
        if code:
            rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
        if bold:
            rpr += "<w:b/><w:bCs/>"
        if italic:
            rpr += "<w:i/><w:iCs/>"
        if color:
            rpr += f'<w:color w:val="{color}"/>'
        if sz:
            rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        space = ' xml:space="preserve"' if text != text.strip() or "  " in text else ""
        return f"<w:r>{rpr}<w:t{space}>{esc(text)}</w:t></w:r>"

    def inline_runs(self, text, bold=False, italic=False):
        out = []
        pos = 0
        for m in INLINE_RE.finditer(text):
            if m.start() > pos:
                out.append(self.run(text[pos:m.start()], bold, italic))
            if m.group("img"):
                out.append(self.image_run_inline(self.resolve(m.group("imgsrc")), m.group("imgalt")))
            elif m.group("link"):
                out.append(self.hyperlink(m.group("ltext"), m.group("lurl"), bold, italic))
            elif m.group("bi"):
                out.append(self.run(m.group("bitext"), True, True))
            elif m.group("b"):
                out.append(self.run(m.group("btext"), True, italic))
            elif m.group("i"):
                out.append(self.run(m.group("itext"), bold, True))
            elif m.group("i2"):
                out.append(self.run(m.group("i2text"), bold, True))
            elif m.group("c"):
                out.append(self.run(m.group("ctext"), bold, italic, code=True))
            pos = m.end()
        if pos < len(text):
            out.append(self.run(text[pos:], bold, italic))
        return "".join(out)

    def resolve(self, src):
        if os.path.isabs(src) or re.match(r"^[a-z]+://", src):
            return src
        return os.path.join(self.image_dir, src)

    def hyperlink(self, text, url, bold=False, italic=False):
        rid = self.new_rid()
        self.rels.append(
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{esc(url)}" TargetMode="External"/>'
        )
        rpr = '<w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/>'
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        rpr += "</w:rPr>"
        return f'<w:hyperlink r:id="{rid}"><w:r>{rpr}<w:t>{esc(text)}</w:t></w:r></w:hyperlink>'

    # ---------- paragraphs
    def para(self, style, runs, extra_ppr=""):
        ppr = ""
        if style or extra_ppr:
            ppr = "<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "") + extra_ppr + "</w:pPr>"
        return f"<w:p>{ppr}{runs}</w:p>"

    def body_para(self, text):
        return self.para("BodyText", self.inline_runs(text))

    def heading(self, level, text):
        style = {1: "Title", 2: "Heading1", 3: "Heading2", 4: "Heading3"}.get(level, "Heading3")
        return self.para(style, self.inline_runs(text))

    def list_item(self, text, ordered, ilvl):
        num_id = 101 if ordered else 100
        ppr = f'<w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>'
        return self.para("ListParagraph", self.inline_runs(text), ppr)

    def blockquote(self, text):
        ppr = '<w:ind w:left="720" w:right="720"/>'
        return self.para("BodyText", self.inline_runs(text, italic=True), ppr)

    # ---------- code blocks: bordered, shaded single-cell table, Consolas 8pt, highlighted
    def code_block(self, code, lang):
        lines_runs = []
        if HAVE_PYGMENTS:
            lexer = None
            if lang:
                try:
                    lexer = get_lexer_by_name(lang, stripnl=False)
                except Exception:
                    lexer = None
            if lexer is None:
                try:
                    lexer = guess_lexer(code, stripnl=False)
                except Exception:
                    lexer = None
            if lexer is not None:
                cur = []
                for ttype, value in lex(code, lexer):
                    style = token_style(ttype)
                    parts = value.split("\n")
                    for i, part in enumerate(parts):
                        if i > 0:
                            lines_runs.append(cur)
                            cur = []
                        if part:
                            cur.append((part, style))
                if cur:
                    lines_runs.append(cur)
        if not lines_runs:
            lines_runs = [[(ln, None)] for ln in code.split("\n")]
        while lines_runs and not any(t for t, _ in lines_runs[-1]):
            lines_runs.pop()

        paras = []
        for line in lines_runs:
            runs = []
            for text, style in line:
                color, bold, italic = (style if style else (None, False, False))
                rpr = ('<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
                       + ("<w:b/>" if bold else "")
                       + ("<w:i/>" if italic else "")
                       + (f'<w:color w:val="{color}"/>' if color else "")
                       + '<w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr>')
                runs.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>')
            if not runs:
                runs = ['<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="16"/></w:rPr><w:t xml:space="preserve"> </w:t></w:r>']
            ppr = ('<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
                   '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="16"/></w:rPr></w:pPr>')
            paras.append(f"<w:p>{ppr}{''.join(runs)}</w:p>")

        border = ('<w:top w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
                  '<w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
                  '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
                  '<w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>')
        return (
            f'<w:tbl><w:tblPr><w:tblW w:w="{CONTENT_WIDTH_DXA}" w:type="dxa"/>'
            f"<w:tblBorders>{border}</w:tblBorders>"
            '<w:tblCellMar><w:top w:w="115" w:type="dxa"/><w:left w:w="144" w:type="dxa"/><w:bottom w:w="115" w:type="dxa"/><w:right w:w="144" w:type="dxa"/></w:tblCellMar>'
            '<w:tblLook w:val="04A0" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/></w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{CONTENT_WIDTH_DXA}"/></w:tblGrid>'
            f'<w:tr><w:tc><w:tcPr><w:tcW w:w="{CONTENT_WIDTH_DXA}" w:type="dxa"/>'
            '<w:shd w:val="clear" w:color="auto" w:fill="F5F5F5"/></w:tcPr>'
            + "".join(paras) + "</w:tc></w:tr></w:tbl>"
            '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="8"/></w:rPr></w:pPr></w:p>'
        )

    # ---------- tables
    def table(self, header_cells, rows):
        ncols = max(len(header_cells), max((len(r) for r in rows), default=0))
        weights = []
        for c in range(ncols):
            longest = max([len(header_cells[c]) if c < len(header_cells) else 0]
                          + [len(r[c]) if c < len(r) else 0 for r in rows])
            weights.append(max(longest, 4))
        total = sum(weights)
        widths = [max(700, int(CONTENT_WIDTH_DXA * w / total)) for w in weights]
        widths[-1] = CONTENT_WIDTH_DXA - sum(widths[:-1])

        def row_xml(cells, header=False):
            tcs = []
            for c in range(ncols):
                text = cells[c] if c < len(cells) else ""
                runs = self.inline_runs(text, bold=header)
                shd = '<w:shd w:val="clear" w:color="auto" w:fill="EDEDED"/>' if header else ""
                tcs.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="{widths[c]}" w:type="dxa"/>{shd}</w:tcPr>'
                    f'<w:p><w:pPr><w:spacing w:after="60" w:line="240" w:lineRule="auto"/></w:pPr>{runs}</w:p></w:tc>'
                )
            trpr = "<w:trPr><w:tblHeader/></w:trPr>" if header else ""
            return f"<w:tr>{trpr}{''.join(tcs)}</w:tr>"

        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        body = (row_xml(header_cells, header=True) if header_cells else "") + "".join(
            row_xml(r) for r in rows
        )
        return (
            '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
            f'<w:tblW w:w="{CONTENT_WIDTH_DXA}" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
            f"<w:tblGrid>{grid}</w:tblGrid>{body}</w:tbl>"
            '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="8"/></w:rPr></w:pPr></w:p>'
        )

    # ---------- images
    def _register_image(self, src):
        ext = os.path.splitext(src)[1].lower().lstrip(".")
        if ext == "jpeg":
            ext = "jpg"
        if ext == "jpg":
            self.need_jpeg_ct = True
        name = f"mdimage{len(self.media) + 1}.{ext}"
        self.media.append((src, name))
        rid = self.new_rid()
        self.rels.append(
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{name}"/>'
        )
        return rid, ext

    def _image_size_emu(self, src, max_w_emu):
        try:
            out = subprocess.run(["identify", "-format", "%w %h", src],
                                 capture_output=True, text=True, timeout=30)
            w_px, h_px = (int(x) for x in out.stdout.split()[:2])
        except Exception:
            w_px, h_px = 1600, 900
        w = min(max_w_emu, int(w_px * EMU_PER_INCH / 96))
        h = int(w * h_px / w_px)
        return w, h

    def drawing_xml(self, rid, w, h, name):
        did = self.next_rid
        return (
            '<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{w}" cy="{h}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{did}" name="{esc(name)}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{did}" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>"
        )

    def image_run_inline(self, src, alt):
        if not os.path.isfile(src):
            sys.stderr.write(f"WARNING: image not found, skipped: {src}\n")
            return self.run(f"[missing image: {alt or src}]", italic=True)
        rid, _ = self._register_image(src)
        w, h = self._image_size_emu(src, CONTENT_WIDTH_EMU)
        return f"<w:r>{self.drawing_xml(rid, w, h, alt or os.path.basename(src))}</w:r>"

    def figure(self, src, alt):
        """Standalone image paragraph -> centered image + Caption."""
        if not os.path.isfile(src):
            sys.stderr.write(f"WARNING: image not found, skipped: {src}\n")
            return ""
        self.fig_count += 1
        rid, _ = self._register_image(src)
        w, h = self._image_size_emu(src, CONTENT_WIDTH_EMU)
        img_p = ('<w:p><w:pPr><w:keepNext/><w:spacing w:after="60"/><w:jc w:val="center"/></w:pPr>'
                 f"<w:r>{self.drawing_xml(rid, w, h, alt or f'Figure {self.fig_count}')}</w:r></w:p>")
        cap = self.para("Caption", self.run(f"Figure {self.fig_count}: {alt}" if alt
                                            else f"Figure {self.fig_count}"))
        return img_p + cap


# ---------------------------------------------------------------- markdown parsing
IMG_ONLY_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)[^)]*\)\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
AUTHOR_HINT = re.compile(r"@|Department|University|Institute|College|Laboratory|Lab\b", re.I)


def parse_markdown(md_text):
    """Return (title, meta_lines, blocks). blocks: list of (kind, payload)."""
    lines = md_text.replace("\r\n", "\n").split("\n")
    i, n = 0, len(lines)
    title, meta = None, []
    blocks = []

    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].startswith("# ") and not lines[i].startswith("## "):
        title = lines[i][2:].strip()
        i += 1
        while i < n:
            s = lines[i].strip()
            if not s or s == "---":
                i += 1
                if s == "---":
                    break
                continue
            m = re.fullmatch(r"\*([^*].*?)\*", s) or re.fullmatch(r"_(.*?)_", s)
            if m:
                meta.append(m.group(1).strip())
                i += 1
            else:
                break

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s in ("---", "***", "___"):
            i += 1
            continue
        if s.startswith("```"):
            lang = s[3:].strip() or None
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", ("\n".join(code_lines), lang)))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            blocks.append(("heading", (len(m.group(1)), m.group(2).strip())))
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1].strip()):
            header = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(("table", (header, rows)))
            continue
        m = IMG_ONLY_RE.match(s)
        if m:
            blocks.append(("figure", (m.group("src"), m.group("alt"))))
            i += 1
            continue
        m = LIST_RE.match(line)
        if m:
            items = []
            while i < n:
                lm = LIST_RE.match(lines[i])
                if not lm:
                    break
                indent = len(lm.group(1).replace("\t", "    "))
                ordered = bool(re.match(r"\d", lm.group(2)))
                items.append((min(indent // 2, 2) if indent < 4 else min(indent // 4, 2),
                              ordered, lm.group(3).strip()))
                i += 1
            blocks.append(("list", items))
            continue
        if s.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("quote", " ".join(q for q in quote if q)))
            continue
        para = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("#", "```", "|", ">", "---"))
                    or LIST_RE.match(lines[i]) or IMG_ONLY_RE.match(nxt)):
                break
            para.append(nxt)
            i += 1
        blocks.append(("para", " ".join(para)))
    return title, meta, blocks


def split_meta(meta, config):
    """Separate metadata lines into subtitle + author entries."""
    subtitle = config.get("subtitle")
    authors = config.get("authors")
    if authors is None:
        authors = []
        leftovers = []
        for line in meta:
            if AUTHOR_HINT.search(line) or re.match(r"^[A-Z][a-z]+(\s[A-Z]\.?)?(\s[A-Z][a-z]+)+,", line):
                parts = [p.strip() for p in line.split(",")]
                authors.append({"name": parts[0], "lines": parts[1:]})
            else:
                leftovers.append(line)
        if subtitle is None and leftovers:
            subtitle = leftovers[0]
    elif subtitle is None:
        for line in meta:
            if not AUTHOR_HINT.search(line):
                subtitle = line
                break
    return subtitle, authors


# ---------------------------------------------------------------- assembly
SECT_BASE = ('<w:pgSz w:w="12240" w:h="15840"/>'
             '<w:pgMar w:top="1440" w:right="1080" w:bottom="1440" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/>')
HDRS = ('<w:headerReference w:type="default" r:id="rId8"/><w:footerReference w:type="default" r:id="rId9"/>'
        '<w:headerReference w:type="first" r:id="rId10"/><w:footerReference w:type="first" r:id="rId11"/>')


def build_document_xml(b, title, subtitle, authors, blocks):
    parts = [b.para("Title", b.inline_runs(title))]
    if subtitle:
        parts.append(b.para(None, b.inline_runs(subtitle, italic=True),
                            '<w:spacing w:after="120"/><w:jc w:val="center"/>'))
    author_section = len(authors) >= 2
    if authors:
        if author_section:
            # Close the title section (single column). Header/footer refs and
            # titlePg are stated explicitly on EVERY sectPr -- never inherited --
            # so Word applies first-page (logo-only) vs default (logo + running
            # title) headers deterministically.
            parts.append(f'<w:p><w:pPr><w:sectPr>{HDRS}<w:type w:val="continuous"/>{SECT_BASE}'
                         '<w:cols w:space="720"/><w:titlePg/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>')
        for idx, a in enumerate(authors):
            if author_section and idx > 0:
                parts.append('<w:p><w:pPr><w:spacing w:after="0"/><w:jc w:val="center"/></w:pPr>'
                             '<w:r><w:br w:type="column"/></w:r></w:p>')
            lines = [a.get("name", "")] + list(a.get("lines", []))
            for j, ln in enumerate(lines):
                if not ln:
                    continue
                after = "160" if j == len(lines) - 1 else "0"
                parts.append(b.para(None, b.inline_runs(ln),
                                    f'<w:spacing w:after="{after}"/><w:jc w:val="center"/>'))
        if author_section:
            ncols = min(len(authors), 3)
            parts.append(f'<w:p><w:pPr><w:sectPr>{HDRS}<w:type w:val="continuous"/>{SECT_BASE}'
                         f'<w:cols w:num="{ncols}" w:space="720"/><w:titlePg/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>')
    for kind, payload in blocks:
        if kind == "heading":
            parts.append(b.heading(*payload))
        elif kind == "para":
            parts.append(b.body_para(payload))
        elif kind == "code":
            parts.append(b.code_block(*payload))
        elif kind == "table":
            parts.append(b.table(*payload))
        elif kind == "list":
            for ilvl, ordered, text in payload:
                parts.append(b.list_item(text, ordered, ilvl))
        elif kind == "quote":
            parts.append(b.blockquote(payload))
        elif kind == "figure":
            parts.append(b.figure(b.resolve(payload[0]), payload[1]))
    # Final (body) section: explicit header/footer refs + titlePg always.
    # When a two-column author section precedes it, the body section must be
    # "continuous" so it flows on the same page; in the single-section case the
    # type is omitted (Word ignores it on a lone section, and a stray trailing
    # "continuous" is what confused Word's header assignment).
    final_type = '<w:type w:val="continuous"/>' if author_section else ''
    final_sect = (f'<w:sectPr>{HDRS}{final_type}{SECT_BASE}'
                  '<w:cols w:space="720"/><w:titlePg/><w:docGrid w:linePitch="360"/></w:sectPr>')
    return DOC_ROOT_OPEN + "<w:body>" + "".join(parts) + final_sect + "</w:body></w:document>"


def main():
    args = sys.argv[1:]
    config_path = image_dir = None
    pos = []
    skip = -1
    for i, a in enumerate(args):
        if i == skip:
            continue
        if a == "--config":
            config_path = args[i + 1]; skip = i + 1
        elif a == "--image-dir":
            image_dir = args[i + 1]; skip = i + 1
        else:
            pos.append(a)
    if len(pos) != 2:
        sys.exit(__doc__)
    md_path, out_path = pos
    config = json.load(open(config_path)) if config_path else {}
    if image_dir is None:
        image_dir = os.path.dirname(os.path.abspath(md_path))

    md_text = open(md_path, encoding="utf-8").read()
    title, meta, blocks = parse_markdown(md_text)
    title = config.get("title") or title or "Untitled"
    subtitle, authors = split_meta(meta, config)

    header_title = config.get("header_title") or title
    header_author = config.get("header_author")
    if not header_author and authors:
        a0 = authors[0]
        email = next((l for l in a0.get("lines", []) if "@" in l), None)
        header_author = a0["name"] + (f", {email}" if email else "")
    header_author = header_author or ""

    b = DocBuilder(image_dir)
    document_xml = build_document_xml(b, title, subtitle, authors, blocks)

    header_default = (HEADER_DEFAULT_XML
                      .replace("{{HEADER_TITLE}}", esc(header_title))
                      .replace("{{HEADER_AUTHOR}}", esc(header_author)))

    extra_ct = ""
    if b.need_jpeg_ct:
        extra_ct = ('<Default Extension="jpg" ContentType="image/jpeg"/>'
                    '<Default Extension="jpeg" ContentType="image/jpeg"/>')
    content_types = CONTENT_TYPES.replace("{{EXTRA_DEFAULTS}}", extra_ct)

    doc_rels = (XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + DOC_RELS_BASE + "".join(b.rels) + "</Relationships>")

    out_path = os.path.abspath(out_path)
    logo = base64.b64decode("".join(VT_LOGO_B64.split()))
    parts = {
        "[Content_Types].xml": content_types,
        "_rels/.rels": ROOT_RELS_XML,
        "word/document.xml": document_xml,
        "word/_rels/document.xml.rels": doc_rels,
        "word/styles.xml": STYLES_XML,
        "word/settings.xml": SETTINGS_XML,
        "word/numbering.xml": NUMBERING_XML,
        "word/header1.xml": header_default,
        "word/header2.xml": HEADER_FIRST_XML,
        "word/footer1.xml": footer_xml(),
        "word/footer2.xml": footer_xml(),
        "word/_rels/header1.xml.rels": HEADER_REL_XML,
        "word/_rels/header2.xml.rels": HEADER_REL_XML,
        "word/media/vtlogo.png": logo,
    }

    def write_zip():
        if os.path.exists(out_path):
            os.remove(out_path)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in parts.items():
                z.writestr(name, data)
            for src, name in b.media:
                z.write(src, f"word/media/{name}")

    write_zip()

    # Page-count pass: render once, read the true page count, and bake it into the
    # NUMPAGES cached value so "Page X of Y" is correct without any field update.
    npages = count_pages(out_path)
    if npages:
        parts["word/footer1.xml"] = footer_xml(str(npages))
        parts["word/footer2.xml"] = footer_xml(str(npages))
        write_zip()
        print(f"Page count: {npages} (baked into footer fields)")
    else:
        print("NOTE: could not render to count pages; footer total will refresh when "
              "Word repaginates the document.")

    print(f"Wrote {out_path}")
    if not HAVE_PYGMENTS:
        print("NOTE: pygments not installed; code blocks rendered without syntax highlighting.")


def count_pages(docx_path):
    """Convert the docx to PDF with LibreOffice and return the page count, or None."""
    import tempfile
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    tmp = tempfile.mkdtemp(prefix="wp_pages_")
    try:
        env = dict(os.environ, HOME=tmp)
        r = subprocess.run([soffice, "--headless", "--norestore", "--convert-to", "pdf",
                            "--outdir", tmp, docx_path],
                           capture_output=True, text=True, timeout=180, env=env)
        pdfs = [f for f in os.listdir(tmp) if f.endswith(".pdf")]
        if not pdfs:
            return None
        pdf_path = os.path.join(tmp, pdfs[0])
        info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True, timeout=60)
        m = re.search(r"Pages:\s+(\d+)", info.stdout)
        if m:
            return int(m.group(1))
        # fallback: count page objects in the raw PDF
        raw = open(pdf_path, "rb").read()
        n = raw.count(b"/Type /Page") - raw.count(b"/Type /Pages")
        return n if n > 0 else None
    except Exception:
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
````
