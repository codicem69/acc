# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatt_emesse', pkey='id', name_long='!![en]Invoice issued', name_plural='!![en]Invoices issued',caption_field='id')
        self.sysFields(tbl)
        tbl.column('cliente_id',size='22', group='_', name_long='cliente_id'
                    ).relation('cliente.id', relation_name='fatt_cliente', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('doc_n', name_short='!![en]Doc.no.')
        tbl.column('importo', dtype='money', name_short='!![en]Ammount')
        tbl.column('descrizione', name_short='!![en]Description')
        tbl.column('insda', dtype='B', name_short='InsDA')
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_emesse',columns='coalesce(SUM($importo),0)', where="$fatt_emesse_id=#THIS.id"),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('saldo', "CASE WHEN ($insda is not null) AND ($insda=true) THEN 0 ELSE $importo-coalesce($tot_pag,0) END",dtype='N',name_long='!![en]Balance',format='#,###.00')
        tbl.formulaColumn('semaforo',"""CASE WHEN $saldo = 0 THEN true ELSE false END""",dtype='B',name_long=' ')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
