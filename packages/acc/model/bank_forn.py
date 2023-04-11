class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bank_forn', pkey='id', name_long='!![en]Supplier bank', name_plural='!![en]Suppliers bank',caption_field='banca')
        self.sysFields(tbl)

        tbl.column('fornitore_id',size='22', group='_', name_long='fornitore_id'
                    ).relation('fornitore.id', relation_name='forn_bank', mode='foreignkey', onDelete='cascade')
        tbl.column('banca', name_short='!![en]Bank name')
        tbl.column('iban', size='27', name_short='Iban', validate_notnull=True)
        tbl.column('swiftcode', name_short='!![en]Swift code')