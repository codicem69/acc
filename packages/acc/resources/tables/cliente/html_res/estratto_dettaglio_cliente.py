from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrbag import Bag
from decimal import Decimal

class Main(TableScriptToHtml):

    row_table = 'acc.fatt_emesse'
    page_width = 297
    page_height = 210
    page_margin_top = 5
    page_margin_left = 3
    page_margin_right = 5
    page_margin_bottom = 5
    doc_header_height = 28
    doc_footer_height = 10
    grid_header_height = 5
    grid_row_height = 4.5
    totalize_footer = 'Totale'
    totalize_class = 'head_gold'
    empty_row = dict()
    virtual_columns = '$tot_pag,$saldo'
    css_requires = 'estratto_cliente'

    # altezza in mm di ogni subriga pagamento
    pag_subrow_height = 3.5

    def mainLayoutParameters(self):
        # Azzeriamo i margini interni: la classe base usa top=1,left=1,right=1,bottom=1
        # che sottraggono spazio dal calcolo della larghezza utile in structAnalyze,
        # facendo scattare erroneamente la divisione in sheet multipli.
        return dict(font_family='Arial Narrow', font_size='9pt',
                    name='mainLayout', top=0, left=0, right=0, bottom=0, border_width=0)

    def gridLayoutParameters(self):
        # FIX CHIAVE: top=0, bottom=0 per non ridurre la larghezza utile calcolata
        # in structAnalyze (copyWidth - layout margins). Con i valori default 0.1
        # la somma colonne (287mm) supera la larghezza utile percepita dal framework
        # e scatta il multi-sheet che spezza le righe.
        # Aggiungiamo anche overflow:hidden sul contenitore griglia così le righe
        # in eccesso non sfondano sul footer.
        return dict(name='gridLayout', um='mm', border_color='#e0e0e0',
                    top=0, bottom=0, left=0, right=0,
                    font_size='9pt',
                    border_width=0.3, lbl_class='caption',
                    text_align='left',
                    overflow='hidden')

    def defineCustomStyles(self):
        self.body.style("""
            .caption {
                text-align: center;
                color: white;
                background: #1a2744;
                font-weight: bold;
                font-size: 8pt;
                height: 4mm;
                line-height: 4mm;
            }
            .smallCaption {
                font-size: 7pt;
                text-align: left;
                color: gray;
                text-indent: 1mm;
                width: auto;
                font-weight: normal;
                line-height: 3mm;
                height: 3mm;
            }
            .totalizer_row {
                color: #f9f7f2 !important;
                background: #1a2744 !important;
                font-weight: bold !important;
                border-top: 0.5pt solid #c8a84b !important;
            }
            .totalize_caption {
                text-align: right;
                padding-right: 2mm;
                font-weight: bold;
                font-style: italic;
                color: #f9f7f2 !important;
                letter-spacing: 0.5px;
                text-transform: uppercase;
            }
            .totalizer_row .cell_num,
            .totalizer_row .cell_pagato,
            .totalizer_row .cell_saldo {
                color: white !important;
                background: #1a2744 !important;
                font-weight: bold !important;
                border-top: 0.5pt solid #c8a84b !important;
                border-bottom: none !important;
            }
            .layout_row:nth-child(even) {
                background-color: #f2f2f2;
            }
            .layout_row:nth-child(odd) {
                background-color: #ffffff;
            }
            .totalizer_row {
                color: #c8a84b !important;
                background: #1a2744 !important;
                font-weight: bold !important;
            }
            .grid_header_row {
                background-color: #dddddd !important;
                color: black;
            }
            /* ── Riga totali: sovrascrive le classi colonna ── */
            .totalizer_row .cell_num,
            .totalizer_row .cell_pagato,
            .totalizer_row .cell_saldo,
            .totalizer_row .cell_base {
                color: #c8a84b !important;
                background: #1a2744 !important;
                font-weight: bold !important;
                font-size: 9pt !important;
                font-style: normal !important;
                font-family: Arial Narrow, sans-serif !important;
                border-top: 0.5pt solid #c8a84b !important;
                border-bottom: none !important;
            }
            .totalizer_row td,
            .totalizer_row div {
                color: #c8a84b !important;
                background: #1a2744 !important;
            }
            /* ── Sottorighe pagamenti ── */
            .pag_subrow td {
                background-color: #f7f5ef !important;
                border-top: 0.3pt dashed #c8a84b !important;
                font-size: 7pt !important;
                height: 3.5mm !important;
                line-height: 3.5mm !important;
            }
            .cell_pag_label {
                color: #5a5a5a !important;
                font-style: italic !important;
                text-indent: 4mm;
                white-space: nowrap;
                overflow: hidden;
            }
            .cell_pag_importo {
                color: #1a6b3c !important;
                font-weight: bold !important;
                text-align: right !important;
                padding-right: 1mm;
            }
            .cell_pag_empty {
                color: transparent !important;
            }
        """)

    def docHeader(self, header):
        agency_id = self.db.currentEnv.get('current_agency_id')
        tbl_agency = self.db.table('agz.agency')
        self.agency_name, self.bank, self.iban, self.bic = tbl_agency.readColumns(
            columns='$agency_name,$bank,$iban,$bic',
            where='$id =:ag_id',
            ag_id=agency_id
        )

        head = header.layout(name='doc_header', border_width=0)
        row = head.row()

        row.cell("""
            <table style='border-collapse:collapse;width:100%;'>
              <tr>
                <td style='width:4px;background:#c8a84b;border-radius:2px;'>&nbsp;</td>
                <td style='padding-left:8px;'>
                    <div style='
                        font-family:"Century Gothic","Futura","Trebuchet MS",sans-serif;
                        font-size:18pt;
                        font-weight:bold;
                        color:#1a2744;
                        letter-spacing:0.5px;
                        line-height:1.15;
                    '>{agency_name}</div>
                    <div style='
                        font-family:"Century Gothic","Futura",sans-serif;
                        font-size:6pt;
                        color:#5a5a5a;
                        letter-spacing:3px;
                        text-transform:uppercase;
                        margin-top:3px;
                    '>Account Statement</div>
                </td>
              </tr>
            </table>
        ::HTML""".format(agency_name=self.agency_name))

        if self.parameter('anno'):
            periodo = """
                <div style='
                    font-family:"Century Gothic","Futura",sans-serif;
                    font-size:8pt;
                    color:#c8a84b;
                    letter-spacing:2px;
                    text-transform:uppercase;
                    margin-top:5px;
                '>Anno {anno}</div>
            """.format(anno=self.parameter('anno'))
        elif self.parameter('dal'):
            periodo = """
                <div style='
                    font-family:"Roboto Mono","Courier New",monospace;
                    font-size:8pt;
                    color:#c8a84b;
                    letter-spacing:0.5px;
                    margin-top:5px;
                '>from {dal} &nbsp;&rsaquo;&nbsp; {al}</div>
            """.format(
                dal=self.parameter('dal').strftime("%d %b %Y"),
                al=self.parameter('al').strftime("%d %b %Y"))
        elif self.parameter('al'):
            periodo = """
                <div style='
                    font-family:"Roboto Mono","Courier New",monospace;
                    font-size:8pt;
                    color:#c8a84b;
                    letter-spacing:0.5px;
                    margin-top:5px;
                '>&rsaquo;&nbsp; {al}</div>
            """.format(
                al=self.parameter('al').strftime("%d %b %Y"))
        else:
            periodo = ""

        row.cell("""
            <div style='text-align:right;'>
                <div style='
                    font-family:"Century Gothic","Futura",sans-serif;
                    font-size:6pt;
                    color:#5a5a5a;
                    letter-spacing:3px;
                    text-transform:uppercase;
                    margin-bottom:5px;
                '>Estratto Contabile</div>
                <div style='
                    font-family:"Century Gothic","Futura",sans-serif;
                    font-size:13pt;
                    font-weight:bold;
                    color:#1a2744;
                    border-bottom:1.5pt solid #c8a84b;
                    padding-bottom:3px;
                '>{cliente}</div>
                {periodo}
            </div>
        ::HTML""".format(
            cliente=self.field('rag_sociale'),
            periodo=periodo
        ))

    def gridStruct(self, struct):
        r = struct.view().rows()

        # Larghezza utile = 297 - 5(sx) - 5(dx) = 287mm
        # 18 + 20 + 173 + 22 + 10 + 22 + 22 = 287mm esatti
        # IMPORTANTE: con gridLayoutParameters top=bottom=left=right=0
        # la larghezza utile è esattamente 287mm, nessuno sheet multiplo.

        r.fieldcell('data',
                    mm_width=18,
                    name='Data',
                    lbl_class='head_base',
                    content_class='cell_base')

        r.fieldcell('doc_n',
                    mm_width=20,
                    name='Documento',
                    lbl_class='head_base',
                    content_class='cell_base')

        r.fieldcell('descrizione',
                    mm_width=173,
                    name='Descrizione',
                    lbl_class='head_base',
                    content_class='cell_base')

        r.fieldcell('importo',
                    mm_width=22,
                    name='Importo',
                    totalize=True,
                    lbl_class='head_right',
                    content_class='cell_num')

        r.fieldcell('insda_x',
                    mm_width=10,
                    name='Ins.D/A',
                    lbl_class='head_base',
                    content_class='cell_base')

        r.fieldcell('tot_pag',
                    mm_width=22,
                    name='Pagato',
                    totalize=True,
                    lbl_class='head_right',
                    content_class='cell_pagato')

        r.fieldcell('saldo',
                    mm_width=22,
                    name='Saldo',
                    totalize=True,
                    lbl_class='head_base',
                    content_class='cell_saldo')

    def gridData(self):
        """Override: filtra le righe con balance dopo aver calcolato il saldo reale."""
        data = super(Main, self).gridData()
        if not self.parameter('balance'):
            return data
        # Filtriamo tenendo solo le fatture con saldo != 0 (positivo o negativo)
        filtered = Bag()
        for node in data:
            row = node.attr
            fatt_id = row.get('_pkey')
            if not fatt_id:
                continue
            pagamenti = self._getPagamentiPerFattura(fatt_id)
            importo_raw = row.get('importo') or '0'
            if isinstance(importo_raw, str):
                importo = round(Decimal(float(importo_raw.replace('.', '').replace(',', '.') or '0')), 2)
            else:
                importo = round(Decimal(str(importo_raw)), 2)
            tot_pag = round(sum(Decimal(str(p.get('importo') or 0)) for p in pagamenti), 2)
            saldo = round(importo - tot_pag, 2)
            if saldo != 0:
                filtered.setItem(node.label, node.value, **node.attr)
        return filtered

    def gridQueryParameters(self):
        condition = []

        if self.parameter('anno'):
            condition.append('$anno_doc=:anno')
        if self.parameter('dal') and self.parameter('al'):
            condition.append('$data BETWEEN :dal AND :al')
        if self.parameter('al'):
            condition.append('$data <= :al')

        return dict(
            condition=' AND '.join(condition) if condition else None,
            condition_anno=self.parameter('anno'),
            condition_dal=self.parameter('dal'),
            condition_al=self.parameter('al'),
            relation='@fatt_cliente',
            order_by='$data, $doc_n'
        )

    # ── Pagamenti: cache per riga corrente ───────────────────────────────────
    #
    # Il flow di gnrbaghtml per ogni riga è:
    #   lineIterator():
    #     1. onNewRow()        ← qui precarichiamo i pagamenti e salviamo in cache
    #     2. calcRowHeight()   ← qui restituiamo altezza riga + subrows
    #     3. (calcola doNewPage e grid_body_used)
    #     4. prepareRow(row)   ← qui disegniamo riga + subrows usando la cache
    #
    # Così la query viene fatta una sola volta per riga e il salto pagina
    # avviene nel punto giusto, tenendo conto dell'altezza totale.

    def _getPagamentiPerFattura(self, fatt_id):
        """
        ⚠️  Adatta al tuo modello:
              tabella  → 'acc.pag_fat_emesse'
              FK       → 'fatt_emesse_id'
              colonne  → data_pagamento, importo, modalita, note
        """
        if not fatt_id:
            return []
        try:
            pag_tbl = self.db.table('acc.pag_fat_emesse')
            if self.parameter('al'):

                sel = pag_tbl.query(
                    columns='$data,$importo,$note',
                    where='$fatt_emesse_id=:_fid AND $data<=:al',
                    _fid=fatt_id,al=self.parameter('al'),
                    order_by='$data'
                ).selection()
            else:
                sel = pag_tbl.query(
                    columns='$data,$importo,$note',
                    where='$fatt_emesse_id=:_fid',
                    _fid=fatt_id,
                    order_by='$data'
                ).selection()

            return sel.output('dictlist')
        except Exception:
            return []

    def onRecordLoaded(self):
        """Inizializza il totale saldo per il totalizzatore."""
        self._totale_saldo = Decimal('0')

    def onNewRow(self):
        """
        Precarica i pagamenti e calcola il saldo della singola fattura.
        Ogni fattura è indipendente: nessun riporto dalle righe precedenti.
          - _importo_fattura   : importo lordo della fattura
          - _saldo_riga_fattura: importo - somma pagamenti (residuo della fattura)
        Le subrows partiranno da _importo_fattura e scaleranno verso _saldo_riga_fattura.
        """
        fatt_id = self.rowField('_pkey')
        self._current_pagamenti = self._getPagamentiPerFattura(fatt_id)

        # Importo lordo fattura
        self._importo_fattura = round(
            Decimal(float(self.rowField('importo').replace('.', '').replace(',', '.') or '0')), 2)

        # Totale pagamenti di questa fattura
        tot_pag = round(sum(Decimal(str(p.get('importo') or 0)) for p in self._current_pagamenti), 2)

        # Saldo residuo della fattura
        self._saldo_riga_fattura = round(self._importo_fattura - tot_pag, 2)
        # Accumula per il totalizzatore manuale
        self._totale_saldo += self._saldo_riga_fattura
        # *** FIX TOTALIZZATORE ***
        # updateRunningTotals() viene chiamato subito DOPO onNewRow() e legge
        # self.rowData['saldo'] per sommarlo. Scriviamo qui il valore corretto
        # così il framework totalizza il saldo reale e non il valore grezzo del DB.
        self.rowData['saldo'] = float(self._saldo_riga_fattura)


    def renderGridCell_saldo(self, col=None, rowData=None, parentRow=None, **cell_kwargs):
        """Override: mostra il saldo netto sulla riga fattura.
        Quando renderMode è 'footer' o 'carry' mostra il totale accumulato."""
        if self.renderMode in ('footer', 'carry', 'subtotal'):
            saldo = rowData.get('saldo', Decimal('0')) if rowData else self._totale_saldo
        else:
            saldo = getattr(self, '_saldo_riga_fattura', Decimal('0'))
        if not isinstance(saldo, Decimal):
            saldo = Decimal(str(saldo))
        val = self.toText(saldo,
                          format=col.get('format') or '#,###.00',
                          locale=self.locale)
        css = ('cell_saldo_zero aligned_right' if saldo == 0
               else ('cell_saldo_negativo' if saldo < 0
                     else 'cell_saldo aligned_right'))
        cell_kwargs['width'] = cell_kwargs.pop('mm_width', None)
        cell_kwargs['content_class'] = css
        cell_kwargs.pop('align_class', None)
        blacklist = ['field', 'field_getter', 'sqlcolumn', 'totalize', 'dtype',
                     'subtotal', 'subtotal_order_by', 'formula', 'background',
                     'color', 'hidden', 'columnset', 'sheet', 'style',
                     'white_space', 'format', 'mask', 'currency', 'locale']
        clean_kw = {k: v for k, v in cell_kwargs.items() if v and k not in blacklist}
        return parentRow.cell(val, overflow='hidden', white_space='nowrap', **clean_kw)

    def calcRowHeight(self):
        """Restituisce l'altezza TOTALE (fattura + subrighe pagamento)
        usata dal framework per calcolare lo spazio di paginazione."""
        n_pag = len(self._current_pagamenti) if hasattr(self, '_current_pagamenti') else 0
        return self.grid_row_height + n_pag * self.pag_subrow_height

    def prepareRow(self, row):
        """
        Disegna la riga normale della fattura con altezza FISSA (grid_row_height),
        poi aggiunge una subrow per ogni pagamento usando la cache di onNewRow().

        Le subrows mostrano il saldo che scala progressivamente da (saldo_riga + tot_pag)
        fino a saldo_riga_fattura, mostrando il dettaglio dei pagamenti intermedi.
        _saldo_progressivo è già stato aggiornato correttamente in onNewRow().
        """
        row.height = self.grid_row_height

        # 1) Riga normale (chiama renderGridCell_saldo che usa _saldo_riga_fattura)
        self.fillGridRow()

        # 2) Subrows pagamenti dalla cache (nessuna query aggiuntiva)
        pagamenti = getattr(self, '_current_pagamenti', [])
        if not pagamenti:
            return

        COL_WIDTHS = [
            ('data',        18,  'cell_pag_label'),
            ('doc_n',       20,  'cell_pag_empty'),
            ('descrizione', 173, 'cell_pag_label'),
            ('importo',     22,  'cell_pag_empty'),
            ('insda_x',     10,  'cell_pag_empty'),
            ('tot_pag',     22,  'cell_pag_importo'),
            ('saldo',       22,  'cell_pag_saldo'),
        ]

        body_grid = row.parent

        # Le subrows partono dall'importo lordo della fattura e scalano
        # con ogni pagamento fino al saldo residuo.
        saldo_corrente = self._importo_fattura

        for pag in pagamenti:
            importo_pag = round(Decimal(str(pag.get('importo') or 0)), 2)
            saldo_corrente -= importo_pag
            subrow = body_grid.row(height=self.pag_subrow_height, _class='pag_subrow')

            for col_name, mm_w, css_class in COL_WIDTHS:
                if col_name == 'data':
                    data_pag = pag.get('data')
                    val = self.toText(data_pag) if data_pag else ''
                elif col_name == 'descrizione':
                    note = pag.get('note') or ''
                    val = '\u21b3 ' + note if note else '\u21b3 Pagamento'
                elif col_name == 'tot_pag':
                    val = self.toText(importo_pag, format='#,###.00') if importo_pag else ''
                elif col_name == 'saldo':
                    val = self.toText(saldo_corrente, format='#,###.00')
                    css_class = ('cell_pag_saldo_zero aligned_right' if saldo_corrente == 0
                                 else ('cell_pag_saldo_negativo' if saldo_corrente < 0
                                       else 'cell_pag_saldo aligned_right'))
                else:
                    val = ''

                subrow.cell(val,
                            width=mm_w,
                            overflow='hidden',
                            white_space='nowrap',
                            content_class=css_class)

        # _saldo_progressivo è già al valore corretto (aggiornato in onNewRow),
        # non serve aggiornarlo qui.

    # ── Footer ───────────────────────────────────────────────────────────────

    def docFooter(self, footer, lastPage=None):
        foo = footer.layout(
            'footer_estratto',
            top=1, left=1,
            lbl_class='cell_label',
            content_class='footer_content',
            border_color='#c8a84b'
        )
        r = foo.row()
        today = self.db.workdate.strftime("%d %b %Y")
        r.cell(
            'Bank: {bank}  \u00b7  IBAN: {iban}  \u00b7  BIC/SWIFT: {bic}'.format(
                bank=self.bank, iban=self.iban, bic=self.bic),
            content_class='left',
            font_size='8pt'
        )
        r.cell('Printed on {oggi}'.format(oggi=today))

    def outputDocName(self, ext=''):
        cliente = self.field('rag_sociale').replace(":", " ").strip()
        if ext and not ext[0] == '.':
            ext = '.%s' % ext

        if self.parameter('anno'):
            return 'Statement_{anno}_{cliente}{ext}'.format(
                anno=self.parameter('anno'), cliente=cliente, ext=ext)
        elif self.parameter('dal') and self.parameter('al'):
            return 'Statement_{dal}_{al}_{cliente}{ext}'.format(
                dal=self.parameter('dal').strftime("%d%m%Y"),
                al=self.parameter('al').strftime("%d%m%Y"),
                cliente=cliente, ext=ext)
        else:
            return 'Statement_{cliente}{ext}'.format(cliente=cliente, ext=ext)
