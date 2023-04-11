class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('fornitore', pkey='id', name_long='!![en]Supplier', name_plural='!![en]Suppliers',caption_field='full_supplier')
        self.sysFields(tbl)

        tbl.column('rag_sociale', name_short='!![en]Company name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('cap', name_short='!![en]CAP')
        tbl.column('city', name_short='!![en]City place')
        tbl.column('tel', name_short='!![en]Tel.')
        tbl.column('email', name_short='!![en]Email')
        tbl.formulaColumn('full_supplier',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') """ )
        tbl.aliasColumn('balance','@forn_fatt.saldo',dtype='N')
        tbl.formulaColumn('worktime', ':env_workdate')