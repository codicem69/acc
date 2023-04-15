from __future__ import print_function
from gnr.web.batch.btcaction import BaseResourceAction
from decimal import Decimal
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
        nuovo_pagcliente=None
        for record in iteratore_fatforn:
            saldo = record['saldo']
            if saldo > 0:
                fatcliente_id = record['id']
                nuovo_pagcliente = self.db.table('acc.pag_fat_emesse').newrecord(fatt_emesse_id=fatcliente_id, data=data_saldo, importo=saldo, note=note)
                self.db.table('acc.pag_fat_emesse').insert(nuovo_pagcliente)
        if nuovo_pagcliente:
            self.db.commit()       

    def messaggio_termometro(self,record, curr, tot, **kwargs):
        return "Invoice %s %i/%i" %(record['doc_n'],curr,tot)

    def table_script_parameters_pane(self,pane,extra_parameters=None,record_count=None,**kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.dateTextBox(value='^.data_saldo',lbl='!![en]Payment date')
        fb.simpleTextArea(value='^.note',lbl='!![en]Note')
        fb.div(f'Applica il saldo a {record_count} fatture')