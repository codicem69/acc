from gnr.core.gnrnumber import floatToDecimal,decimalRound

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
        tbl.column('email', name_short='Email')
        tbl.column('tel', name_short='Tel.')
        tbl.column('note', name_short='Note')
        tbl.column('balance', dtype='N', name_short='!![en]Balance',format='#,###.00')
        tbl.aliasColumn('bank_details_cliente','@customer_bank.bank_details_cliente')
        tbl.formulaColumn('full_cliente',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') || coalesce(' Vat: ' || $vat,'') || 
                                     coalesce(' - unique code: ' || $cod_univoco,'') || coalesce(' - pec: ' || $pec,'') """ )
        
        tbl.formulaColumn('tot_impfat',select=dict(table='acc.fatt_emesse',columns='coalesce(SUM($importo),0) as tot_impfat', 
                                                   where='$cliente_id=#THIS.id and $insda is Null or $insda=false')
                          ,dtype='N',format='#,###.00',
                          name_long='!![en]Total invoices')
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_emesse',columns='coalesce(sum($importo),0)', where='@fatt_emesse_id.cliente_id=#THIS.id'),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        tbl.formulaColumn('balance2', '$tot_impfat-$tot_pag',dtype='N',name_long='!![en]Balance_FC',format='#,###.00')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))
    
    def ricalcolaBalanceCliente(self,cliente_id=None):
        with self.recordToUpdate(cliente_id) as record:
            totale_fatture = self.db.table('acc.fatt_emesse').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$cliente_id=:c_id and $insda is not true',c_id=cliente_id)
            fatture_cliente_id = self.db.table('acc.fatt_emesse').query(columns='$id',where='$cliente_id=:c_id', c_id=cliente_id).fetchAsDict('id')
            totale_pagato = 0
            for r in fatture_cliente_id:
                pagamenti = self.db.table('acc.pag_fat_emesse').query(columns='$importo',
                                                                     where='$fatt_emesse_id=:fe_id', fe_id=r).fetch()
                for a in range(len(pagamenti)):
                    totale_pagato += pagamenti[a][0]
           
            if totale_fatture is None:
                record['balance'] = None
            else:    
                record['balance'] = floatToDecimal(totale_fatture - totale_pagato or 0) 
