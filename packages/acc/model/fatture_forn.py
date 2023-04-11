# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatture_forn', pkey='id', name_long='!![en]Supplier invoice', name_plural='!![en]Supplier invoices',caption_field='inv')
        self.sysFields(tbl)
        tbl.column('fornitore_id',size='22', group='_', name_long='fornitore_id'
                    ).relation('fornitore.id', relation_name='forn_fatt', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('doc_n', name_short='!![en]Doc.no.')
        tbl.column('importo', dtype='money', name_short='!![en]Ammount')
        tbl.column('descrizione', name_short='!![en]Description')
        tbl.formulaColumn('inv',"$doc_n || ' - ' || $data")
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_forn',columns='SUM($importo)', where='$fatture_forn_id=#THIS.id'),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('saldo', '$importo-coalesce($tot_pag,0)',dtype='N',name_long='!![en]Balance',format='#,###.00')
        tbl.formulaColumn('semaforo',"""CASE WHEN $saldo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')
        tbl.aliasColumn('paym_details','@paym_fat_forn.paymdet', dtype='T')
        

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
