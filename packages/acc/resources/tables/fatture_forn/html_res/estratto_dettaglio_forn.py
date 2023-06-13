from gnr.web.gnrbaseclasses import TableScriptToHtml
from datetime import datetime

class Main(TableScriptToHtml):
    maintable = 'acc.fatture_forn'
    row_table = 'acc.fatture_forn'
    css_requires='grid'
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
    virtual_columns = '@fatture_forn_id.tot_pag,@fatture_forn_id.saldo' #aggiungiamo le colonne calcolate

    def docHeader(self, header):
        #Questo metodo definisce il layout e il contenuto dell'header della stampa
        
        if self.parameter('fornitore_id'):
            fornitore=self.rowField('fornitore')
            self.fornitore=fornitore
        else:
            fornitore= ''  
        head = header.layout(name='doc_header', margin='5mm', border_width=0)
        row = head.row()
        if self.parameter('anno'):
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement <br>{forn}</strong></div>
                    <div style='font-size:10pt;'>{anno}</div></center>::HTML""".format(forn=fornitore,anno=self.parameter('anno')))
        elif self.parameter('dal'):
            row.cell("""<center><div style='font-size:12pt;'><strong>Estratto/Statement <br>{forn}</strong></div>
                    <div style='font-size:10pt;'>from {dal} to {al}</div></center>::HTML""".format(forn=fornitore,
                    dal=self.parameter('dal'),al=self.parameter('al')))            
        else:
            #row = head.row()
            row.cell("""<center><div style='font-size:14pt;'><strong>Estratto/Statement</strong></div>
                    <div style='font-size:12pt;'><strong>{forn}</strong></div></center>::HTML""".format(
                                forn=fornitore))

    def defineCustomStyles(self):
        #Questo metodo definisce gli stili del body dell'html
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
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
        if not self.parameter('fornitore_id'):
        #if len(self.fornid) > 1:
            r.cell('fornitore',mm_width=30, content_class="breakword")
            r.cell('fornitore', hidden=True, subtotal='Totali {breaker_value}',subtotal_order_by='$fornitore',subtotal_content_class='cell_pers')
        r.cell('data', mm_width=15, name='Data')
         #r.fieldcell('mese_fattura', hidden=True, subtotal='Totale {breaker_value}', subtotal_order_by="$data")
         #Questa formulaColumn verrà utilizzata per creare i subtotali per mese
        r.cell('doc_n', mm_width=15, name='Documento')
        #r.cell('doc_n', hidden=True, subtotal='{breaker_value}',subtotal_order_by='$fornitore')
        #r.fieldcell('cliente_id', mm_width=0)
        #r.cell('bal',mm_width=15)
        r.cell('descrizione',mm_width=0,name='Descrizione', content_class="breakword")
        r.cell('importo', mm_width=20, name='Importo doc.', totalize=True,format='#,###.00')
        r.cell('tot_pag', mm_width=20, name='Totale versamenti', totalize=True,format='#,###.00')
        
        r.cell('saldo',name='Balance doc.', mm_width=20, totalize=True,format='#,###.00',content_class='cell_pers')
        #r.cell('balance_fornitore',name='Balance totale',content_class='cell_pers',mm_width=20,format='#,###.00', totalize=True)
        #r.cell('balance_fornitore',  subtotal='Balance totale {breaker_value}', mm_width=20,format='#,###.00')
    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        fornitore_offset = 20
        descrizione_offset = 150
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        if not self.parameter('fornitore_id'):
            n_rows_forn = len(self.rowField('fornitore'))//fornitore_offset + 1.2
        else:
            n_rows_forn = len(self.rowField('fornitore'))//fornitore_offset     
        n_rows_descr = len(self.rowField('descrizione'))//descrizione_offset + 1.2
        
  #      n_rows_nome_provincia = len(self.rowField('_sigla_provincia_nome'))//nome_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_forn,n_rows_descr)#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows)
        return height
    
    def gridData(self): 
        condition = ['$fornitore_id=:forn_id']
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
        fornitori_pkeys = self.db.table('acc.fornitore').query(columns="$id", where='$balance >=0').selection().output('pkeylist')
        self.fornid=fornitori_pkeys
        if self.parameter('fornitore_id'):
            len_forn=1
        else:
            len_forn=len(fornitori_pkeys)    
        righe_fat=[]
        righe=[]
        for r in range(len_forn):
            #verifichiamo se alla stampa abbiamo scelto il singolo fornitore così passiamo la query giusta per la ricerca del singolo
            #altrimenti saranno selezionati tutti i fornitori e sarà passata la query per tutti
            if self.parameter('fornitore_id'):
                forn_id=self.parameter('fornitore_id')
                fornitori = self.db.table('acc.fornitore').query(columns="$id,$rag_sociale,sum($balance) as differenza", where='$id=:pkeys and $balance >=0',
                                                             order_by='$rag_sociale',
                                                             group_by='$id',
                                                  pkeys=forn_id).fetch()
            else:
                fornitori = self.db.table('acc.fornitore').query(columns="$id,$rag_sociale,sum($balance) as differenza", where='$id IN :pkeys and $balance >=0',
                                                             order_by='$rag_sociale',
                                                             group_by='$id',
                                                  pkeys=fornitori_pkeys).fetch()
                
                #forn_id=fornitori_pkeys[r]    
                forn_id=fornitori[r][0]
                
            fatforn = self.db.table('acc.fatture_forn').query(columns="""$fornitore_id,
                                            $data,$doc_n,$descrizione,$importo,$tot_pag,$saldo""",
                                            where=where,
                                            balance=balance,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al'),
                                            forn_id=forn_id, 
                                            order_by='$data'
                                            ).fetch()
           #pagfatforn = self.db.table('acc.pag_fat_forn').query(columns="""$fatture_forn_id,
           #                                $data,$importo,$note""",
           #                                where='').fetch()
            pagfatforn = self.db.table('acc.pag_fat_forn').query(columns="""$fatture_forn_id,
                                            $data,$importo,$note""",
                                            where=where_pag,
                                            anno=self.parameter('anno'),
                                            dal=self.parameter('dal'),
                                            al=self.parameter('al')
                                            ).fetch()
            
            fornitore=fornitori[r][1]
            balance_fornitore = fornitori[r][2]
            bal_forn=0
            righe_pag=[]
            for r in range(len(fatforn)):
                fat_id=fatforn[r][7]
                data_fat=fatforn[r][1]
                doc_n=fatforn[r][2]
                descrizione_fat=fatforn[r][3]
                importo_fat=fatforn[r][4]
                tot_pag=fatforn[r][5]
                saldo=fatforn[r][6]

                pag_progressivo=0          
                saldo_fat = importo_fat
                    
                for p in range(len(pagfatforn)):

                    if pagfatforn[p][0] == fat_id:
                        data=pagfatforn[p][1]
                        tot_pag=pagfatforn[p][2]
                        descrizione=pagfatforn[p][3]
                        if descrizione is not None:
                            descrizione='Versamento - ' + str(descrizione)
                        else:
                            descrizione='Versamento'    
                        pag_progressivo += tot_pag
                        saldo_fat = 0
                        saldo_fat = importo_fat-pag_progressivo

                        righe_pag.append(dict(data=data,doc_n=doc_n, descrizione=descrizione, importo='',
                                  tot_pag=tot_pag,saldo='',fornitore=fornitore))
                bal_forn+=saldo_fat
                #if r == len(fatforn)-1:
                #    righe_pag.append(dict(data='',doc_n='', descrizione='Balance '+ str(fornitore), importo='',
                #                  tot_pag='',saldo='',fornitore=fornitore,balance_fornitore=bal_forn))
                righe_fat.append(dict(data=data_fat,doc_n=doc_n, descrizione=descrizione_fat, importo=importo_fat,
                                  tot_pag='',saldo=saldo_fat,fornitore=fornitore)) 
                
                righe = []
                righe_fat.extend(righe_pag)
                for myDict in righe_fat:
                    if myDict not in righe:
                        righe.append(myDict)             
        
        return righe
        ##Facciamo anche una query sulla row_table, per individuare dalle pkeys i "clienti" oggetto della stampa
        #fornitori = self.db.table('acc.fornitore').query(columns='$id,$rag_sociale', where='$id IN :pkeys', 
        #                                            pkeys=self.record['selectionPkeys']).fetch()
        #
        #return fornitori
        
        #for prodotto in fatture_forn_grouped:
        #    categoria_principale = prodotto['prodotto_gerarchia'].split('/')[0]
        #    prodotto['categoria_principale'] = categoria_principale

        #return fatture_forn_grouped
    
    #def gridQueryParameters(self):
    #    
    #    condition=[]
    #    balance=0
    #    if self.parameter('balance') == True:
    #        condition.append('$saldo>:balance')
    #    else:
    #        condition.append('$saldo>=:balance')    
    #    if self.parameter('anno'):
    #        condition.append('$anno_doc=:anno')
    #    if self.parameter('dal') and self.parameter('al'):
    #        condition.append('$data BETWEEN :dal AND :al')
    #     
    #    return dict(condition=' AND '.join(condition), condition_anno=self.parameter('anno'), 
    #                condition_dal=self.parameter('dal'),condition_al=self.parameter('al'),
    #                condition_balance=balance,relation='@forn_fatt')
    
    

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
        #verifichiamo se in self.gridData abbiamo il record con il nome del fornitore e con replace sostituiamo gli spazi e punti
        if len(self.gridData())>0:
            fornitore=self.gridData()[0]['fornitore'].replace('.','').replace(' ','_')
        else:
            fornitore=''    
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.parameter('anno') and self.parameter('fornitore_id'):
            doc_name = 'Statement_{anno}_{fornitore}{ext}'.format(anno=self.parameter('anno'), 
                        fornitore=fornitore, ext=ext)
        elif self.parameter('anno'):
            doc_name = 'Statement_{anno}{ext}'.format(anno=self.parameter('anno'),ext=ext)
        elif self.parameter('dal') and self.parameter('al') and self.parameter('fornitore_id'):
            doc_name = 'Statement_from_{dal}_to_{al}_{fornitore}{ext}'.format(dal=self.parameter('dal'),
                        al=self.parameter('al'),
                        fornitore=fornitore, ext=ext)  
        elif self.parameter('dal') and self.parameter('al'):
            doc_name = 'Statement_from_{dal}_to_{al}'.format(dal=self.parameter('dal'),
                        al=self.parameter('al'), ext=ext)        
        elif self.parameter('fornitore_id'):
            doc_name = 'Statement_{fornitore}{ext}'.format(fornitore=fornitore, ext=ext)
        else: 
            doc_name = 'Statement'.format(ext=ext)    
        return doc_name
