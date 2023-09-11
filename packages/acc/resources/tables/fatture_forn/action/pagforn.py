from __future__ import print_function
from gnr.web.batch.btcaction import BaseResourceAction
from decimal import Decimal
from gnr.core.gnrnumber import floatToDecimal,decimalRound
from time import sleep
import os 

caption = 'Saldo multiplo' #nome nel menu dei batch
tags = 'admin,user'  #autorizzazione al batch
description =  'Saldo di più fatture' #nome piu completo

class Main(BaseResourceAction):
    batch_prefix = 'agg' #identificatore di batch (univoco)
    batch_title = 'Saldo fatture' #titolo all'interno del visore del batch
    batch_delay = 0.5  #periodo campionamento termometro
    batch_steps='main'
    batch_cancellable = True
    virtual_columns = '$saldo'
    #batch_selection_savedQuery = 'testbatch'

    def step_main(self):
        print('page_id',self.db.currentPage.page_id)
        selection = self.get_selection()#(columns='$id,$doc_n,$importo,$saldo')
        
        if not selection:
            self.batch_debug_write('Nessun record trovato')
            return
        data_saldo = self.batch_parameters.get('data_saldo')
        note = self.batch_parameters.get('note')
        records = self.get_records(for_update=True) #dalla selezione corrente ottiene un iteratore in formato record
        maximum = len(self.get_selection())
        iteratore_fatforn = self.btc.thermo_wrapper(records,message=self.messaggio_termometro, maximum=maximum) 
        
        #il metodo thermo_wrapper ottiene un iteratore che scorrendo ogni elemento aggiorna il termometro 
        #con il ciclo for successivo aggiorniamo il pagamento delle fatture selezionate
        nuovo_pagforn=None
        for record in iteratore_fatforn:
            saldo = record['saldo']
            if saldo > 0:
                fatforn_id = record['id']
                fornitore_id = record['fornitore_id']
                nuovo_pagforn = self.db.table('acc.pag_fat_forn').newrecord(fatture_forn_id=fatforn_id, data=data_saldo, importo=saldo, note=note)
                self.db.table('acc.pag_fat_forn').insert(nuovo_pagforn)
        #verifichiamo il totale delle fatture fornitore poi preleviamo tutti gli id delle fatture fornitori che con un ciclo for nella tbl 
        # pagamenti fornitori andremo a calcolare il totale pagato per poi calcolare il saldo
        totale_fatture = self.db.table('acc.fatture_forn').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$fornitore_id=:f_id',f_id=fornitore_id)
        fatture_forn_id = self.db.table('acc.fatture_forn').query(columns='$id',where='$fornitore_id=:f_id', f_id=fornitore_id).fetchAsDict('id')
        totale_pagato = 0
        for r in fatture_forn_id:
            pagamenti = self.db.table('acc.pag_fat_forn').query(columns='$importo',
                                                                     where='$fatture_forn_id=:ff_id', ff_id=r).fetch()
            for a in range(len(pagamenti)):
                totale_pagato += pagamenti[a][0]
        #prendiamo il record della tabella fornitore e con for_update=True successivamente faremo l'aggiornamento con il nuovo saldo 
        tbl_fornitore = self.db.table('acc.fornitore')
        record_fornitore = tbl_fornitore.record(where='$id=:id_forn', 
                                  id_forn=fornitore_id,
                                  for_update=True).output('dict')
        old_record = dict(record_fornitore)
           
        if totale_fatture is not None:
            nuovo_record = dict(id=fornitore_id,balance=floatToDecimal(totale_fatture - totale_pagato or 0))
            tbl_fornitore.update(nuovo_record,old_record)

        if nuovo_pagforn:
            self.db.commit() 

    def messaggio_termometro(self,record, curr, tot, **kwargs):
        return "Invoice %s %i/%i" %(record['doc_n'],curr,tot)

    def table_script_parameters_pane(self,pane,extra_parameters=None,record_count=None,**kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.dateTextBox(value='^.data_saldo',lbl='!![en]Payment date')
        fb.simpleTextArea(value='^.note',lbl='!![en]Note')
        fb.div(f'Applica il saldo a {record_count} fatture')