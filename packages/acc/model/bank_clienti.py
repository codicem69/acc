class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bank_clienti', pkey='id', name_long='!![en]Customer bank', name_plural='!![en]Customers bank',caption_field='banca')
        self.sysFields(tbl)

        tbl.column('cliente_id',size='22', group='_', name_long='cliente_id'
                    ).relation('cliente.id', relation_name='customer_bank', mode='foreignkey', onDelete='cascade')
        tbl.column('banca', name_short='!![en]Bank name')
        tbl.column('iban', size='27', name_short='Iban', validate_notnull=True)
        tbl.column('swiftcode', name_short='!![en]Swift code')
        tbl.formulaColumn('bank_details_cliente',"coalesce('Banca: '|| $banca,'') || '<br>' || coalesce('Iban: ' || $iban,'') || '<br>' || coalesce('Swift code: ' || $swiftcode, '')")