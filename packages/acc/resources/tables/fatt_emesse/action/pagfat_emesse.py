from __future__ import print_function
from gnr.web.batch.btcaction import BaseResourceAction
from decimal import Decimal
from time import sleep
import os 
from gnr.core.gnrnumber import floatToDecimal,decimalRound

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
        nuovo_pagcliente=None
        for record in iteratore_fatforn:
            saldo = record['saldo']
            cliente_id = record['cliente_id']
            if saldo > 0:
                fatcliente_id = record['id']
                nuovo_pagcliente = self.db.table('acc.pag_fat_emesse').newrecord(fatt_emesse_id=fatcliente_id, data=data_saldo, importo=saldo, note=note)
                self.db.table('acc.pag_fat_emesse').insert(nuovo_pagcliente)
        #verifichiamo il totale delle fatture cliente poi preleviamo tutti gli id delle fatture cliente che con un ciclo for nella tbl 
        # pagamenti cliente andremo a calcolare il totale pagato per poi calcolare il saldo
        totale_fatture = self.db.table('acc.fatt_emesse').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$cliente_id=:c_id and $insda is not true',c_id=cliente_id)
        fatture_cliente_id = self.db.table('acc.fatt_emesse').query(columns='$id',where='$cliente_id=:c_id', c_id=cliente_id).fetchAsDict('id')
        totale_pagato = 0
        for r in fatture_cliente_id:
            pagamenti = self.db.table('acc.pag_fat_emesse').query(columns='$importo',
                                                                where='$fatt_emesse_id=:fe_id', fe_id=r).fetch()
            for a in range(len(pagamenti)):
                totale_pagato += pagamenti[a][0]
        #prendiamo il record della tabella cliente e con for_update=True successivamente faremo l'aggiornamento con il nuovo saldo 
        tbl_cliente = self.db.table('acc.cliente')
        record_cliente = tbl_cliente.record(where='$id=:id_cliente', 
                                  id_cliente=cliente_id,
                                  for_update=True).output('dict')
        old_record = dict(record_cliente)
        if totale_fatture is not None:
            nuovo_record = dict(id=cliente_id,balance=floatToDecimal(totale_fatture - totale_pagato or 0))
            tbl_cliente.update(nuovo_record,old_record)
       
        if nuovo_pagcliente:
            self.db.commit()       

    def messaggio_termometro(self,record, curr, tot, **kwargs):
        return "Invoice %s %i/%i" %(record['doc_n'],curr,tot)

    def table_script_parameters_pane(self,pane,extra_parameters=None,record_count=None,**kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.dateTextBox(value='^.data_saldo',lbl='!![en]Payment date')
        fb.simpleTextArea(value='^.note',lbl='!![en]Note')
        fb.div(f'Applica il saldo a {record_count} fatture')
