from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable = 'acc.fatt_emesse'
    row_table = 'acc.fatt_emesse'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    doc_header_height = 30
    doc_footer_height = 15
    grid_header_height = 5
    totalize_footer='Totale'
    totalize_class ='head_gold'
    css_requires = 'estratto_cliente'
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '$tot_pag,$saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        agency_id=self.db.currentEnv.get('current_agency_id')
        tbl_agency = self.db.table('agz.agency')
        self.agency_name,self.bank,self.iban,self.bic = tbl_agency.readColumns(columns='$agency_name,$bank,$iban,$bic', where = '$id =:ag_id', ag_id=agency_id)

        head = header.layout(name='doc_header', margin='5mm',right=5, border_width=0)
        row = head.row()
        # ── Colonna sinistra: nome azienda ──────────────────────────────
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
        #row.cell("""<center><div style='font-size:20pt;'><strong>{agency_name}</strong></div></center>::HTML""".format(
        #                        agency_name=self.agency_name))
         # ── Colonna destra: cliente + periodo ───────────────────────────
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
                '>dal {dal} &nbsp;&rsaquo;&nbsp; {al}</div>
            """.format(
                dal=self.parameter('dal').strftime("%d %b %Y"),
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
        #if self.parameter('anno'):
        #    row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
        #            <div style='font-size:10pt;'>{anno}</div></center>::HTML""".format(cliente=self.field('@cliente_id.rag_sociale'),anno=self.parameter('anno')))
        #elif self.parameter('dal'):
        #    row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
        #            <div style='font-size:10pt;'>from {dal} to {al}</div></center>::HTML""".format(cliente=self.field('@cliente_id.rag_sociale'),
        #            dal=self.parameter('dal').strftime("%d-%m-%Y"),al=self.parameter('al').strftime("%d-%m-%Y")))
        #else:
        #    #row = head.row()
        #    row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement</strong></div>
        #            <div style='font-size:12pt;'><strong>{cliente}</strong></div></center>::HTML""".format(
        #                        cliente=self.field('@cliente_id.rag_sociale')))

    def defineCustomStyles(self):
        # Stili layout generati dal framework (caption, smallCaption).
        # I totalizer (totalizer_row, totalize_caption, head_gold) sono ora
        # definiti in estratto_cliente.css — qui li ripetiamo solo come
        # fallback nel caso il CSS esterno non venga caricato (html_res locale).
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
            /* fallback totalizer — sovrascritti dal CSS esterno se caricato */
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
            /* Colore per le righe PARI */
        .layout_row:nth-child(even) {
            background-color: #f2f2f2;
        }

        /* Colore per le righe DISPARI */
        .layout_row:nth-child(odd) {
            background-color: #ffffff;
        }

        /* Escludi la barra dei totali che hai già personalizzato */
        /* Usiamo !important per assicurarci che il colore dei totali vinca sulle righe alternate */
        .totalizer_row {
            color: #c8a84b !important;
            background: #1a2744 !important;
            font-weight: bold !important;
        }

        /* Se vuoi evitare che le righe dell'header (titoli) vengano colorate */
        .grid_header_row {
            background-color: #dddddd !important;
            color: black;
        }
            """)


    def gridStruct(self,struct):
        #Questo metodo definisce la struttura della griglia di stampa definendone colonne e layout
        r = struct.view().rows()
        r.fieldcell('@cliente_id.rag_sociale', mm_width=62, subtotal='Totale documento {breaker_value}',subtotal_order_by='@cliente_id.rag_sociale,$data,$doc_n')
        r.fieldcell('data', mm_width=15)
        #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
        #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.fieldcell('doc_n', mm_width=15, name='Documento')
        #r.fieldcell('cliente_id', mm_width=0)
        r.fieldcell('descrizione',mm_width=0)
        r.fieldcell('importo', mm_width=20, totalize=True)
        r.fieldcell('insda_x',mm_width=10, name='ins_d/a')
        r.fieldcell('tot_pag', mm_width=20, totalize=True)
        r.fieldcell('saldo', mm_width=20, totalize=True)
        
    def gridQueryParameters(self):
        
        condition=[]
        balance=0
        if self.parameter('balance') == True:
            condition.append('$saldo>:balance')
        #else:
        #    condition.append('$saldo>=:balance')    
        if self.parameter('anno'):
            condition.append('$anno_doc=:anno')
        if self.parameter('dal') and self.parameter('al'):
            condition.append('$data BETWEEN :dal AND :al')

        result = dict(table='acc.fatt_emesse',condition=' AND '.join(condition), condition_anno=self.parameter('anno'), 
                    condition_dal=self.parameter('dal'),condition_al=self.parameter('al'),
                    condition_balance=balance)#,order_by='@cliente_id.rag_sociale DESC')#,relation='@fatt_cliente')
        #print(x)
        return result

    def docFooter(self, footer, lastPage=None):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        foo = footer.layout('totali_fattura',top=1,
                           lbl_class='cell_label', 
                           content_class = 'footer_content',border_color='white')
        r = foo.row()
        today = self.db.workdate.strftime("%d/%m/%Y")
        r.cell('Bank details: {bank} - IBAN: {iban} - BIC: {bic}'.format(bank=self.bank,iban=self.iban,bic=self.bic),content_class='left',font_size='8pt')
        r.cell('Document printed on {oggi}'.format(oggi=today))
        
    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        fornitore=self.field('rag_sociale').replace(":", " ")
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno'):
            doc_name = 'Statement_{anno}_{fornitore}{ext}'.format(anno=self.parameter('anno'), 
                        fornitore=fornitore, ext=ext)
        elif self.parameter('dal') and self.parameter('al'):
            doc_name = 'Statement_from_{dal}_to_{al}_{fornitore}{ext}'.format(dal=self.parameter('dal').strftime("%d-%m-%Y"),
                        al=self.parameter('al').strftime("%d-%m-%Y"),
                        fornitore=fornitore, ext=ext)    
        else: 
            doc_name = 'Statement_{fornitore}{ext}'.format(fornitore=fornitore, ext=ext)
        return doc_name
        #if ext and not ext[0] == '.':
        #    ext = '.%s' % ext
        #if self.parameter('anno'):
        #    doc_name = 'Statement_{anno}_{fornitore}{ext}'.format(anno=self.parameter('anno'), 
        #                fornitore=self.field('rag_sociale'), ext=ext)
        #elif self.parameter('dal') and self.parameter('al'):
        #    doc_name = 'Statement_from_{dal}_to_{al}_{fornitore}{ext}'.format(dal=self.parameter('dal'),
        #                al=self.parameter('al'),
        #                fornitore=self.field('rag_sociale'), ext=ext)    
        #else: 
        #    doc_name = 'Statement_{fornitore}{ext}'.format(fornitore=self.field('rag_sociale'), ext=ext)
        #return doc_name
