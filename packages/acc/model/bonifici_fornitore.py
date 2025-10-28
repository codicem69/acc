from gnr.core.gnrbag import Bag

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
        tbl.formulaColumn('tot_balance_bonifico',select=dict(table='acc.fatforn_bonifici',
                                                columns='SUM($saldo)',
                                                where='$bonifici_forn_id=#THIS.id'),
                                    dtype='N',name_long='Tot.Balance',format='#,###.00')

        tbl.pyColumn('events_rows',dtype='X',required_columns='$data',name_long='fat_forn')

    def pyColumn_events_rows(self,record=None,field=None):

        if not record.get('data'):
            return Bag(dict(error='Missing data'))


        tbl_fatfornbon = self.db.table('acc.fatforn_bonifici')
        pkey=record.get('id') or record.get('pkey') #se lanciata in una view vuole record['id] se in un template vuole record['pkey] - con il get nel caso non esiste la key non torna l'errore

        recordsRate = tbl_fatfornbon.query(columns='@fatture_forn_id.doc_n as doc_n_fat,@fatture_forn_id.data as data_fat,@fatture_forn_id.importo as importo_fat,@fatture_forn_id.saldo as balance_fat,@fatture_forn_id.descrizione as descrizione_fat',
                                                    where='$bonifici_forn_id = :bon_id',
                                                    bon_id=pkey, order_by='data_fat,doc_n ASC').fetch()

        #convertiamo dal risultato della query gli importi decimal con due cifre dopo la virgola
        #for a in recordsRate:
        #    a['importo_fat']=round(a['importo_fat'],2)
        #    a['balance_fat']=round(a['balance_fat'],2)

        #creiamo la bag e aggiungiamo l'attributo format per visualizzare correttamente le cifre con la virgola
        rows = Bag()
        for n,r in enumerate(recordsRate,1):
            #print(X)
            rows['r_%s'%(n)]=Bag(r)
            rows.setAttr('r_%s'%(n)+'.importo_fat',format='#,###.00')
            rows.setAttr('r_%s'%(n)+'.balance_fat',format='#,###.00')

        return rows
