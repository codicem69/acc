from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable = 'acc.cliente'
    row_table = 'acc.cliente'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    
    doc_footer_height = 15
    doc_header_height = 16
    grid_row_height = 5
    grid_header_height = 5
    totalize_footer='Totale'
    cliente_height = 10
    #Fornendo a totalize_footer una stringa testuale, questa verrà usata come etichetta della riga di totalizzazione
    empty_row=dict()
    #Grazie a questo parametro in caso di mancanza di dati verrà stampata una griglia vuota invece di una pagina bianca
    virtual_columns = '@fatt_emesse_id.tot_pag,@fatt_emmese_id.saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        
        if len(self.cliente_id) > 1:
            cliente=''
        else:
            cliente= self.rowField('cliente')   
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>{anno}</div></center>::HTML""".format(cliente=cliente,anno=self.parameter('anno')))
        elif self.parameter('dal'):
            row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>from {dal} to {al}</div></center>::HTML""".format(cliente=cliente,
                    dal=self.parameter('dal'),al=self.parameter('al')))            
        else:
            #row = head.row()
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement</strong></div>
                    <div style='font-size:12pt;'><strong>{cliente}</strong></div></center>::HTML""".format(
                                cliente=cliente))

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
        
        if len(self.cliente_id) > 1:
            r.cell('cliente',mm_width=30)
        r.cell('data', mm_width=15, name='Data')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=15, name='Documento')
        r.cell('doc_n', hidden=True, subtotal='Totale documento {breaker_value}',subtotal_order_by='$cliente')
        #r.fieldcell('cliente_id', mm_width=0)
        
        r.cell('descrizione',mm_width=0,name='Descrizione')
        r.cell('importo', mm_width=20, name='Importo', totalize=True,format='#,###.00')
        r.cell('insda',mm_width=5, dtype='B')
        r.cell('tot_pag', mm_width=20, name='Totale versamenti', totalize=True,format='#,###.00')
        
        r.cell('saldo',name='Balance doc.', mm_width=20, totalize=True,format='#,###.00')
        r.cell('balance_cliente',name='Balance totale',mm_width=20,format='#,###.00', totalize=True)

    def gridData(self): 
        condition = ['$cliente_id=:cliente_id']
        condition_pag = []
        balance=0
        if self.parameter('balance') == True:
            condition.append('$saldo>:balance')
        else:
            condition.append('$saldo>=:balance')    
        if self.parameter('anno'):
            condition.append('$anno_doc=:anno')
            condition_pag.append('$anno_doc=:anno')
        if self.parameter('dal') and self.parameter('al'):
            condition.append('$data BETWEEN :dal AND :al')
            condition_pag.append('$data BETWEEN :dal AND :al')
         
        where = ' AND '.join(condition)
        where_pag = ' AND '.join(condition_pag)
                   # , condition_anno=self.parameter('anno'), 
                   #condition_dal=self.parameter('dal'),condition_al=self.parameter('al'),
                   #condition_balance=balance)
        #condition = ['$fornitore_id IN :pkeys AND $data <= :data_fine']
        #if self.parameter('dal'):
        #    condition.append('$data >= :data_inizio')
        #where = ' AND '.join(condition
        self.cliente_id=self.record('selectionPkeys')
        
        righe_fat=[]
        for r in range(len(self.record('selectionPkeys'))):
            cliente_id=self.record('selectionPkeys')[r]

            fat_emesse = self.db.table('acc.fatt_emesse').query(columns="""$cliente_id,
                                            $data,$doc_n,$descrizione,$importo,$tot_pag,$saldo,$insda""",
                                            where=where,
                                            balance=balance,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al'),
                                            cliente_id=cliente_id, 
                                            order_by='$data'
                                            ).fetch()
            pagfatEmesse = self.db.table('acc.pag_fat_emesse').query(columns="""$fatt_emesse_id,
                                            $data,$importo,$note""",
                                            where=where_pag,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al')).fetch()
        
            clienti = self.db.table('acc.cliente').query(columns="$id,$rag_sociale,sum($balance) as differenza", where='$id IN :pkeys',
                                                             order_by='$rag_sociale',
                                                             group_by='$id',
                                                  pkeys=self.record['selectionPkeys']).fetch()
            #print(x)
            cliente=clienti[r][1]
            #print(x)
            balance_cliente = clienti[r][2]
            bal_cliente=0
            righe_pag=[]
            for r in range(len(fat_emesse)):
                fat_id=fat_emesse[r][8]
                data_fat=fat_emesse[r][1]
                doc_n=fat_emesse[r][2]
                descrizione_fat=fat_emesse[r][3]
                importo_fat=fat_emesse[r][4]
                tot_pag=fat_emesse[r][5]
                saldo=fat_emesse[r][6]
                insda=fat_emesse[r][7]
                if insda == True:
                    insda = 'x'
                    saldo_fat = 0
                else:
                    insda = ''
                    saldo_fat=importo_fat

                pag_progressivo=0

                for p in range(len(pagfatEmesse)):

                    if pagfatEmesse[p][0] == fat_id:
                        data=pagfatEmesse[p][1]
                        tot_pag=pagfatEmesse[p][2]
                        descrizione=pagfatEmesse[p][3]
                        if descrizione is not None:
                            descrizione='Versamento - ' + str(descrizione)
                        else:
                            descrizione='Versamento'   
                        
                        pag_progressivo += tot_pag
                        saldo_fat = 0
                        saldo_fat = importo_fat-pag_progressivo
                        

                        righe_pag.append(dict(data=data,doc_n=doc_n, descrizione=descrizione, importo='',
                                  tot_pag=tot_pag,saldo=''))
                bal_cliente+=saldo_fat

                if r == len(fat_emesse)-1:
                    righe_pag.append(dict(data='',doc_n='Balance', descrizione='Totale ' + str(cliente), importo='',
                                  tot_pag='',saldo='',cliente='',balance_cliente=bal_cliente))    

                righe_fat.append(dict(data=data_fat,doc_n=doc_n, descrizione=descrizione_fat, importo=importo_fat,
                                  tot_pag='',saldo=saldo_fat,cliente=cliente,insda=insda))
                
                righe = []
                righe_fat.extend(righe_pag)
                for myDict in righe_fat:
                    if myDict not in righe:
                        righe.append(myDict)
                
        return righe    
    

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
