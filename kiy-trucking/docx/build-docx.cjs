// Builds the editable Word version of the KIY Trucking letterhead.
// Run: node build-docx.cjs
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, VerticalAlign, WidthType, ShadingType, BorderStyle,
  TabStopType, PageBreak, LineRuleType,
} = require('docx');

// ---- identity -------------------------------------------------------------
const BLACK = '000000', RED = 'B5010D', HOT = 'E3121F', GREY = 'D6D6D6', STEEL = '4A4D52', INK = '1C1C1C';
const FONT = 'Arial';

// ---- geometry (DXA: 1440 = 1 inch, 56.69 = 1 mm) ---------------------------
const mm = (v) => Math.round(v * 56.6929);
const PAGE_W = mm(210), PAGE_H = mm(297);
const SIDE = mm(14);                // header/footer bands bleed to the page edge
const BODY_SIDE = mm(22);           // text margins
const FULL = PAGE_W;                // full-bleed table width

const img = (file, wMm, hMm) => new ImageRun({
  type: file.endsWith('.png') ? 'png' : 'jpg',
  data: fs.readFileSync(path.join(__dirname, file)),
  transformation: { width: Math.round(wMm * 3.7795), height: Math.round(hMm * 3.7795) }, // px at 96dpi
});

const noBorder = { style: BorderStyle.NONE, size: 0, color: 'auto' };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder, insideHorizontal: noBorder, insideVertical: noBorder };
const blackFill = { fill: BLACK, type: ShadingType.CLEAR, color: 'auto' };

const run = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 19, bold: o.bold, italics: o.italics, color: o.color || INK, characterSpacing: o.spacing || 0 });
const para = (children, o = {}) => new Paragraph({ children, alignment: o.align, spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 276, lineRule: LineRuleType.AUTO }, indent: o.indent, border: o.border, keepNext: o.keepNext });

// ---- header ---------------------------------------------------------------
function bandTable(rows, colWidths, indentMm, cellMargins) {
  return new Table({
    width: { size: colWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: colWidths,
    indent: { size: mm(indentMm), type: WidthType.DXA },
    borders: noBorders,
    rows,
  });
}

const whiteLine = (t, o = {}) => para([run(t, { color: o.color || GREY, size: o.size || 17, bold: o.bold, spacing: o.spacing || 20 })], { align: AlignmentType.RIGHT, line: 260 });

function makeHeader(compact) {
  const logoH = compact ? 13 : 27;
  const logoW = logoH * (424 / 179);
  const contact = compact
    ? [
        whiteLine('KIY TRUCKING (PTY) LTD', { color: 'FFFFFF', bold: true, size: 18, spacing: 50 }),
        whiteLine('+27 00 000 0000  ·  info@kiytrucking.co.za', { size: 16 }),
      ]
    : [
        whiteLine('KIY TRUCKING (PTY) LTD', { color: 'FFFFFF', bold: true, size: 20, spacing: 60 }),
        whiteLine('[Street address line 1]'),
        whiteLine('[Suburb, City, Postal code]'),
        whiteLine('+27 00 000 0000', { color: HOT, bold: true }),
        whiteLine('info@kiytrucking.co.za'),
        whiteLine('www.kiytrucking.co.za'),
      ];
  const margins = { top: mm(compact ? 3 : 6), bottom: mm(compact ? 3 : 6), left: SIDE, right: SIDE };
  const table = bandTable([
    new TableRow({ children: [
      new TableCell({ width: { size: mm(110), type: WidthType.DXA }, shading: blackFill, margins,
        children: [para([img('logo.png', logoW, logoH)], { line: 240 })] }),
      new TableCell({ width: { size: FULL - mm(110), type: WidthType.DXA }, shading: blackFill, margins, verticalAlign: VerticalAlign.CENTER, children: contact }),
    ] }),
  ], [mm(110), FULL - mm(110)], -14 - 8);
  return new Header({ children: [
    table,
    para([img('header-stripe.png', 210, 210 * 130 / 2480)], { indent: { left: -mm(22) }, line: 240 }),
    ...(compact ? [] : [para([], { before: mm(9), line: 240 })]),
  ] });
}

// ---- footer ---------------------------------------------------------------
function makeFooter() {
  const line = (t, o, align) => para([run(t, { size: 15, color: GREY, spacing: 10, ...o })], { align, line: 250 });
  const cell = (paras, width, ml, mr) => new TableCell({ width: { size: width, type: WidthType.DXA }, shading: blackFill, verticalAlign: VerticalAlign.BOTTOM,
    margins: { top: mm(3), bottom: mm(4.5), left: mm(ml), right: mm(mr) }, children: paras });
  const w1 = mm(66), w2 = mm(78), w3 = mm(66);
  const L = AlignmentType.LEFT, C = AlignmentType.CENTER, R = AlignmentType.RIGHT;
  const table = bandTable([
    new TableRow({ children: [
      cell([line('KIY TRUCKING (PTY) LTD', { color: 'FFFFFF', bold: true, spacing: 15 }, L), line('Reg. No. [0000/000000/07]', {}, L), line('VAT No. [0000000000]', {}, L)], w1, 12, 2),
      cell([para([
        run('BEYOND BORDERS. ', { color: 'FFFFFF', bold: true, italics: true, size: 18, spacing: 0 }),
        run('DELIVERING TRUST.', { color: HOT, bold: true, italics: true, size: 18, spacing: 0 }),
      ], { align: C, line: 250 })], w2, 2, 2),
      cell([line('SOUTH AFRICA » THE WORLD', { color: 'FFFFFF', bold: true, spacing: 15 }, R), line('Directors: [Name], [Name]', {}, R), line('www.kiytrucking.co.za', {}, R)], w3, 2, 12),
    ] }),
  ], [w1, w2, w3], -22);
  return new Footer({ children: [
    para([img('footer-stripe.png', 210, 210 * 130 / 2480)], { indent: { left: -mm(22) }, line: 240 }),
    table,
  ] });
}

// ---- body -----------------------------------------------------------------
const meta = new Table({
  width: { size: PAGE_W - 2 * BODY_SIDE, type: WidthType.DXA },
  columnWidths: [mm(83), mm(83)],
  borders: noBorders,
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: mm(83), type: WidthType.DXA }, children: [
      para([run('TO:', { bold: true, spacing: 30 })]),
      para([run('[Recipient name]')]), para([run('[Company]')]), para([run('[Address]')]),
    ] }),
    new TableCell({ width: { size: mm(83), type: WidthType.DXA }, children: [
      para([run('DATE: ', { bold: true }), run('[DD Month YYYY]', { color: STEEL })], { align: AlignmentType.RIGHT }),
      para([run('REF: ', { bold: true }), run('KIY/[0000]', { color: STEEL })], { align: AlignmentType.RIGHT }),
      para([run('ATT: ', { bold: true }), run('[Contact person]', { color: STEEL })], { align: AlignmentType.RIGHT }),
    ] }),
  ] })],
});

const body = [
  meta,
  para([], { after: 120 }),
  para([run('SUBJECT: CROSS-BORDER FREIGHT PROPOSAL', { bold: true, italics: true, size: 28, spacing: 20 })],
    { before: 200, after: 280, border: { left: { style: BorderStyle.SINGLE, size: 28, color: RED, space: 10 } }, indent: { left: 0 } }),
  para([run('Dear [Recipient],')], { after: 200 }),
  para([run('Thank you for considering KIY Trucking for your cross-border freight requirements. We move cargo from South Africa into the SADC region and beyond, with a fleet of interlink and tautliner units, experienced long-haul drivers and full customs-clearing support at every port of entry.')], { after: 200 }),
  para([run('Every consignment is tracked in real time and backed by goods-in-transit cover, so you always know where your load is and when it will arrive. Our 24/7 operations desk coordinates loading, border documentation and delivery confirmation on your behalf.')], { after: 200 }),
  para([run('We would welcome the opportunity to discuss your routes and volumes in detail. Please contact our operations office at the number above to arrange a meeting or request a formal quotation.')], { after: 200 }),
  para([run('Yours faithfully,')], { after: 600 }),
  para([run('                                                  ')], { border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLACK, space: 1 } }, after: 100 }),
  para([run('[FULL NAME]', { bold: true, size: 22, spacing: 40 })]),
  para([run('[Designation]  ·  KIY Trucking (Pty) Ltd', { color: STEEL, size: 18 })]),
  para([new PageBreak()]),
  para([run('[Continuation sheet – body text continues here. This page carries a reduced header so long letters, quotations and schedules stay on brand without repeating the full contact block.]')], { after: 200 }),
];

const section = (firstPage) => ({
  properties: {
    page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: mm(38), bottom: mm(40), left: BODY_SIDE, right: BODY_SIDE, header: 0, footer: 0 },
    },
    titlePage: true,
  },
  headers: { first: makeHeader(false), default: makeHeader(true) },
  footers: { first: makeFooter(), default: makeFooter() },
  children: body,
});

const doc = new Document({
  creator: 'KIY Trucking',
  title: 'KIY Trucking Letterhead',
  styles: { default: { document: { run: { font: FONT, size: 19, color: INK } } } },
  sections: [section(true)],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(__dirname, '..', 'KIY-Trucking-Letterhead.docx'), buf);
  console.log('wrote KIY-Trucking-Letterhead.docx');
});
