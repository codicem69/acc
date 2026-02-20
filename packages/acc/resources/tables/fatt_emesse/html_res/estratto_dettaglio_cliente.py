from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable = 'acc.fatt_emesse'
    row_table = 'acc.fatt_emesse'
    css_requires='grid'
    page_width = 297
    page_height = 210
    page_margin_left = 5
    page_margin_right = 5
    
    doc_footer_height = 15
    doc_header_height = 18
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
        agency_id=self.db.currentEnv.get('current_agency_id')
        tbl_agency = self.db.table('agz.agency')
        self.agency_name,self.bank,self.iban,self.bic = tbl_agency.readColumns(columns='$agency_name,$bank,$iban,$bic', where = '$id =:ag_id', ag_id=agency_id)
        
        if self.parameter('cliente_id'):
            cliente=self.rowField('cliente')
        else:
            cliente= ''  
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        row.cell("""<center><div style='font-size:20pt;'><strong>{agency_name}</strong><br></div></center>::HTML""".format(
                                agency_name=self.agency_name))
        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>{anno}</div></center>::HTML""".format(cliente=cliente,anno=self.parameter('anno')))
        elif self.parameter('dal'):
            row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement <br>{cliente}</strong></div>
                    <div style='font-size:10pt;'>from {dal} to {al}</div></center>::HTML""".format(cliente=cliente,
                    dal=self.parameter('dal').strftime("%d-%m-%Y"),al=self.parameter('al').strftime("%d-%m-%Y")))            
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
        if not self.parameter('cliente_id'):
        #if len(self.cliente_id) > 1:
            r.cell('cliente',mm_width=30, content_class="breakword")
            r.cell('cliente', hidden=True, subtotal='Totali {breaker_value}',subtotal_order_by='$cliente',subtotal_content_class='cell_pers')
        r.cell('data', mm_width=15, name='Data')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=15, name='Documento')
        #r.cell('doc_n', hidden=True, subtotal='Totale documento {breaker_value}',subtotal_order_by='$cliente')
        #r.fieldcell('cliente_id', mm_width=0)
        
        r.cell('descrizione',mm_width=0,name='Descrizione', content_class="breakword")
        r.cell('importo', mm_width=20, name='Importo', totalize=True,format='#,###.00')
        r.cell('insda',mm_width=5, dtype='B')
        r.cell('tot_pag', mm_width=20, name='Totale versamenti', totalize=True,format='#,###.00')
        
        r.cell('saldo',name='Balance doc.', mm_width=20, totalize=True,format='#,###.00')
       # r.cell('balance_cliente',name='Balance totale',mm_width=20,format='#,###.00', totalize=True)

    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        cliente_offset = 20
        descrizione_offset = 150
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        if not self.parameter('cliente_id'):
            n_rows_cliente = len(self.rowField('cliente'))//cliente_offset + 1.2
        else:
            n_rows_cliente = len(self.rowField('cliente'))//cliente_offset     
        n_rows_descr = len(self.rowField('descrizione'))//descrizione_offset + 1.2

      
  #      n_rows_nome_provincia = len(self.rowField('_sigla_provincia_nome'))//nome_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_cliente,n_rows_descr)#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows)
        return height
    
    def gridData(self): 
        condition = ['$cliente_id=:cliente_id']
        condition_pag = []
        balance=0
        if self.parameter('balance') == True:
            condition.append('$saldo>:balance')
        #else:
        #    condition.append('$saldo>=:balance')    
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
        clienti_pkeys = self.db.table('acc.cliente').query(columns="$id", where='$balance >=0').selection().output('pkeylist')
        self.cliente_id=clienti_pkeys
        if self.parameter('cliente_id'):
            len_cliente=1
        else:
            len_cliente=len(clienti_pkeys)   

        righe_fat=[]
        righe=[]
        for r in range(len_cliente):
            #verifichiamo se alla stampa abbiamo scelto il singolo fornitore così passiamo la query giusta per la ricerca del singolo
            #altrimenti saranno selezionati tutti i fornitori e sarà passata la query per tutti
            if self.parameter('cliente_id'):
                cliente_id=self.parameter('cliente_id')
                clienti = self.db.table('acc.cliente').query(columns="$id,$rag_sociale,sum($balance) as differenza", where='$id=:pkeys and $balance >=0',
                                                             order_by='$rag_sociale',
                                                             group_by='$id',
                                                  pkeys=cliente_id).fetch()
            else:
                clienti = self.db.table('acc.cliente').query(columns="$id,$rag_sociale,sum($balance) as differenza", where='$id IN :pkeys and $balance >=0',
                                                             order_by='$rag_sociale',
                                                             group_by='$id',
                                                  pkeys=clienti_pkeys).fetch()

                #cliente_id=clienti_pkeys[r]
                cliente_id=clienti[r][0]

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
                                  tot_pag=tot_pag,saldo='',cliente=cliente))
                bal_cliente+=saldo_fat

                #if r == len(fat_emesse)-1:
                #    righe_pag.append(dict(data='',doc_n='Balance', descrizione='Totale ' + str(cliente), importo='',
                #                  tot_pag='',saldo='',cliente='',balance_cliente=bal_cliente))    

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
        r.cell('Bank details: {bank} - IBAN: {iban} - BIC: {bic}'.format(bank=self.bank,iban=self.iban,bic=self.bic),content_class='left',font_size='8pt')
        r.cell('Document printed on {oggi}'.format(oggi=today))
        
    def outputDocName(self, ext=''):
        #Questo metodo definisce il nome del file di output
        if len(self.gridData())>0:
            cliente=self.gridData()[0]['cliente'].replace('.','').replace(' ','_')
        else:
            cliente=''    
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno') and self.parameter('cliente_id'):
            doc_name = 'Statement_{anno}_{cliente}{ext}'.format(anno=self.parameter('anno'), 
                        cliente=cliente, ext=ext)
        elif self.parameter('anno'):
            doc_name = 'Statement_{anno}{ext}'.format(anno=self.parameter('anno'),ext=ext)    
        elif self.parameter('dal') and self.parameter('al') and self.parameter('cliente_id'):
            doc_name = 'Statement_from_{dal}_to_{al}_{cliente}{ext}'.format(dal=self.parameter('dal'),
                        al=self.parameter('al'),
                        cliente=cliente, ext=ext)   
        elif self.parameter('dal') and self.parameter('al'):
            doc_name = 'Statement_from_{dal}_to_{al}'.format(dal=self.parameter('dal'),
                        al=self.parameter('al'), ext=ext)
        elif self.parameter('cliente_id'):
            doc_name = 'Statement_{cliente}{ext}'.format(cliente=cliente, ext=ext)         
        else: 
            doc_name = 'Statement'.format(ext=ext)
        return doc_name
