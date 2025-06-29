# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatture_forn', pkey='id', name_long='!![en]Supplier invoice', name_plural='!![en]Supplier invoices',caption_field='inv')
        self.sysFields(tbl)
        tbl.column('fornitore_id',size='22', group='_', name_long='fornitore_id',batch_assign=True
                    ).relation('fornitore.id', relation_name='forn_fatt', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('doc_n', name_short='!![en]Doc.no.')
        tbl.column('importo', dtype='money', name_short='!![en]Ammount')
        tbl.column('descrizione', name_short='!![en]Description')
        tbl.column('scadenza', dtype='D', name_short='!![en]Due Date')
        tbl.column('note', name_short='!![en]Note')
        tbl.formulaColumn('giorni_scadenza',"""CASE WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo>0 THEN 'Scadenza tra giorni ' || cast(($scadenza - CURRENT_DATE) as varchar)
                                        WHEN ($scadenza - CURRENT_DATE)>0 AND $saldo<=0 THEN '!![en]PAYED' 
                                        WHEN ($scadenza - CURRENT_DATE)<0 AND $saldo<=0 THEN '!![en]PAYED' ELSE 'Scaduta da giorni ' || cast((CURRENT_DATE-$scadenza) as varchar) END """,
                                        name_long='!![en]Expire days')
        tbl.formulaColumn('inv',"$doc_n || ' - ' || to_char($data, :df)",var_df='DD/MM/YYYY')
        tbl.formulaColumn('inv_fornitore',"$doc_n || '-' || @fornitore_id.rag_sociale")
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_forn',columns='coalesce(SUM($importo),0)', where='$fatture_forn_id=#THIS.id'),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('saldo', 'coalesce($importo,0)-coalesce($tot_pag,0)',dtype='N',name_long='!![en]Balance',format='#,###.00')
        tbl.formulaColumn('semaforo',"""CASE WHEN $saldo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')
        tbl.formulaColumn('anno_doc',"date_part('year', $data)", dtype='D')
        tbl.formulaColumn('bonificato',select=dict(table='acc.fatforn_bonifici',
                                                columns="CASE WHEN $fatture_forn_id <> '' THEN true END",
                                                where='$fatture_forn_id=#THIS.id',group_by='$fatture_forn_id'),
                                                limit=1,dtype='B')
        tbl.aliasColumn('paym_details','@paym_fat_forn.paymdet', dtype='T')
        
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))

    def aggiornaFornitore(self,record):
        fornitore_id = record['fornitore_id']
        self.db.deferToCommit(self.db.table('acc.fornitore').ricalcolaBalance,
                                    fornitore_id=fornitore_id,
                                    _deferredId=fornitore_id)

    def trigger_onInserted(self,record=None):
        self.aggiornaFornitore(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaFornitore(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaFornitore(record)

    