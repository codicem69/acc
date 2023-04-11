class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cliente', pkey='id', name_long='!![en]Customer', name_plural='!![en]Customers',caption_field='full_cliente')
        self.sysFields(tbl)

        tbl.column('rag_sociale', name_short='!![en]Company name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('cap', name_short='!![en]CAP')
        tbl.column('city', name_short='!![en]City place')
        tbl.column('vat', name_short='!![en]Vat number')
        tbl.column('cf', name_short='!![en]Fiscal code')
        tbl.column('cod_univoco',size='7', name_short='!![en]Unique code')
        tbl.column('pec', name_short='Email pec')
        
        tbl.formulaColumn('full_cliente',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') """ )