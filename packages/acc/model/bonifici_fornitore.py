class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bonifici_fornitore', pkey='id', name_long='!![en]Transfer', 
                        name_plural='!![en]Transfers',caption_field='causale')
        self.sysFields(tbl)
        
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('fornitore_id',size='22', name_long='!![en]Supplier'
                    ).relation('fornitore.id', relation_name='bonifico_forn', mode='foreignkey', onDelete='cascade')            
        tbl.column('causale', name_short='!![en]Reason')
        tbl.column('importo', dtype='money', name_short='!![en]Amount')
        tbl.formulaColumn('tot_fat_bonifico',select=dict(table='acc.fatforn_bonifici',
                                                columns='SUM($importo)',
                                                where='$bonifici_forn_id=#THIS.id'),
                                    dtype='N',name_long='Tot.Fatture',format='#,###.00')
 