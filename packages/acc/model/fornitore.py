from gnr.core.gnrnumber import floatToDecimal,decimalRound

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
        tbl.column('note', name_short='Note')
        tbl.column('balance', dtype='N', name_short='!![en]Balance',format='#,###.00')
        tbl.formulaColumn('full_supplier',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'') """ )
        tbl.aliasColumn('bank_details','@forn_bank.bank_details')
        tbl.formulaColumn('worktime', ':env_workdate')
        tbl.formulaColumn('tot_impfat',select=dict(table='acc.fatture_forn',columns='coalesce(SUM($importo),0) as tot_impfat', 
                                                   where='$fornitore_id=#THIS.id')
                          ,dtype='N',format='#,###.00',
                          name_long='!![en]Total invoices')
        tbl.formulaColumn('tot_pag',select=dict(table='acc.pag_fat_forn',columns='coalesce(sum($importo),0)', where='@fatture_forn_id.fornitore_id=#THIS.id'),dtype='N',format='#,###.00',
                          name_long='!![en]Total payments')
        #tbl.formulaColumn('balance', '$tot_impfat-$tot_pag',dtype='N',name_long='!![en]Balance',format='#,###.00')
       
    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'))   
    
    def ricalcolaBalance(self,fornitore_id=None):
        with self.recordToUpdate(fornitore_id) as record:
            totale_fatture = self.db.table('acc.fatture_forn').readColumns(columns="""SUM($importo) AS totale_fatture""",
                                                                     where='$fornitore_id=:f_id',f_id=fornitore_id)
            fatture_forn_id = self.db.table('acc.fatture_forn').query(columns='$id',where='$fornitore_id=:f_id', f_id=fornitore_id).fetchAsDict('id')
            totale_pagato = 0
            for r in fatture_forn_id:
                pagamenti = self.db.table('acc.pag_fat_forn').query(columns='$importo',
                                                                     where='$fatture_forn_id=:ff_id', ff_id=r).fetch()
                for a in range(len(pagamenti)):
                    totale_pagato += pagamenti[a][0]
           
            if totale_fatture is None:
                record['balance'] = None
            else:    
                record['balance'] = floatToDecimal(totale_fatture - totale_pagato or 0) 
                
