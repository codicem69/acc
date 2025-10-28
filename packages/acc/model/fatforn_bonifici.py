# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fatforn_bonifici', pkey='id', name_long='Fatture bonifici fornitore', name_plural='Fatture bonifici fornitori',caption_field='id')
        self.sysFields(tbl)
        tbl.column('bonifici_forn_id',size='22', group='_', name_long='!![en]Transfers supplier'
                    ).relation('bonifici_fornitore.id', relation_name='bonifici_forn', mode='foreignkey', onDelete='cascade')
        tbl.column('fatture_forn_id',size='22', group='_', name_long='!![en]Supplier invoice'
                    ).relation('fatture_forn.id', relation_name='inv_supplier', mode='foreignkey', onDelete='cascade')
        tbl.aliasColumn('importo','@fatture_forn_id.importo')
        tbl.aliasColumn('saldo','@fatture_forn_id.saldo')

