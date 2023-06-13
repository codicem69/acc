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
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '$tot_pag,$saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>{anno}</div></center>::HTML""".format(cliente=self.field('@cliente_id.rag_sociale'),anno=self.parameter('anno')))
        elif self.parameter('dal'):
            row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>from {dal} to {al}</div></center>::HTML""".format(cliente=self.field('@cliente_id.rag_sociale'),
                    dal=self.parameter('dal'),al=self.parameter('al')))            
        else:
            #row = head.row()
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement</strong></div>
                    <div style='font-size:12pt;'><strong>{cliente}</strong></div></center>::HTML""".format(
                                cliente=self.field('@cliente_id.rag_sociale')))

    def defineCustomStyles(self):
        #Questo metodo definisce gli stili del body dell'html
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
                            color:grey;
                            text-indent:1mm;}

                            .footer_content{
                            text-align:right;
                            margin:2mm;
                            font-size:8pt;
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
        r.cell('Document printed on {oggi}'.format(oggi=today))
        
    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno'):
            doc_name = 'Statement_{anno}_{fornitore}{ext}'.format(anno=self.parameter('anno'), 
                        fornitore=self.field('rag_sociale'), ext=ext)
        elif self.parameter('dal') and self.parameter('al'):
            doc_name = 'Statement_from_{dal}_to_{al}_{fornitore}{ext}'.format(dal=self.parameter('dal'),
                        al=self.parameter('al'),
                        fornitore=self.field('rag_sociale'), ext=ext)    
        else: 
            doc_name = 'Statement_{fornitore}{ext}'.format(fornitore=self.field('rag_sociale'), ext=ext)
        return doc_name
