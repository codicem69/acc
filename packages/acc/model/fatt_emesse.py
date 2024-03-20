# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatt_emesse', pkey='id', name_long='!![en]Invoice issued', name_plural='!![en]Invoices issued',caption_field='id')
        self.sysFields(tbl)
        tbl.column('cliente_id',size='22', group='_', name_long='cliente_id',batch_assign=True
                    ).relation('cliente.id', relation_name='fatt_cliente', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('doc_n', name_short='!![en]Doc.no.', dtype='T')
        tbl.column('importo', dtype='money', name_short='!![en]Ammount')
        tbl.column('descrizione', name_short='!![en]Description', dtype='T')
        tbl.column('insda', dtype='B', name_short='InsDA')
        tbl.column('scadenza', dtype='D', name_short='!![en]Due Date')
        tbl.formulaColumn('giorni_scadenza',"""CASE WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo>0 THEN 'Scadenza tra giorni ' || cast(($scadenza - CURRENT_DATE) as varchar)
                                        WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo<=0  THEN '!![en]PAYED' 
                                        WHEN ($scadenza - CURRENT_DATE)<0 AND $saldo<=0 THEN '!![en]PAYED' ELSE 'Scaduta da giorni ' || cast((CURRENT_DATE-$scadenza) as varchar) END """,
                                        name_long='!![en]Expire days', dtype='T')
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_emesse',columns='coalesce(SUM($importo),0)', where="$fatt_emesse_id=#THIS.id"),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('saldo', "CASE WHEN ($insda is not null) AND ($insda=true) THEN 0 ELSE $importo-coalesce($tot_pag,0) END",dtype='N',name_long='!![en]Balance',format='#,###.00')
        tbl.formulaColumn('semaforo',"""CASE WHEN $saldo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')
        tbl.formulaColumn('anno_doc',"date_part('year', $data)", dtype='D')
        tbl.formulaColumn('insda_x',"CASE WHEN $insda = True THEN 'x' ELSE '' END", dtype='T')
        
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))

    def aggiornaCliente(self,record):
        cliente_id = record['cliente_id']
        self.db.deferToCommit(self.db.table('acc.cliente').ricalcolaBalanceCliente,
                                    cliente_id=cliente_id,
                                    _deferredId=cliente_id)

    def trigger_onInserted(self,record=None):
        self.aggiornaCliente(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaCliente(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaCliente(record)