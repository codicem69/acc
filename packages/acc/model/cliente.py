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
        tbl.column('tel', name_short='Tel.')
        tbl.column('note', name_short='Note')

        tbl.aliasColumn('bank_details_cliente','@customer_bank.bank_details_cliente')
        tbl.formulaColumn('full_cliente',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') """ )
        
        tbl.formulaColumn('tot_impfat',select=dict(table='acc.fatt_emesse',columns='coalesce(SUM($importo),0) as tot_impfat', 
                                                   where='$cliente_id=#THIS.id and $insda is Null or $insda=false')
                          ,dtype='N',format='#,###.00',
                          name_long='!![en]Total invoices')
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_emesse',columns='coalesce(sum($importo),0)', where='@fatt_emesse_id.cliente_id=#THIS.id'),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('balance', '$tot_impfat-$tot_pag',dtype='N',name_long='!![en]Balance',format='#,###.00')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))