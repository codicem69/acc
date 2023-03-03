# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatture_forn', pkey='id', name_long='!![en]Supplier invoice', name_plural='!![en]Supplier invoices',caption_field='id')
        self.sysFields(tbl)
        tbl.column('fornitore_id',size='22', group='_', name_long='fornitore_id'
                    ).relation('fornitore.id', relation_name='forn_fatt', mode='foreignkey', onDelete='raise')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('doc_n', name_short='!![en]Doc.no.')
        tbl.column('importo', dtype='money', name_short='!![en]Ammount')
        tbl.column('descrizione', name_short='!![en]Description')