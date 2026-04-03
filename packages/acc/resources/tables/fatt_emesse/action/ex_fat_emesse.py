from gnr.web.batch.btcexport import BaseResourceExport

caption = 'Export Fatture Emesse'
description='Export Fatture Emesse'

class Main(BaseResourceExport):
    batch_prefix = 'EFE'
    batch_title = 'Export Fatture Emesse'
    batch_cancellable = False
    batch_delay = 0.5

    def pre_process(self):
        #impostiamo il nome del file
        if self.batch_parameters['clienteid']:
            cliente=self.tblobj.query(where='$cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente""",
                        clienteid=str(self.batch_parameters['clienteid'])).fetch()
            cliente=' ' + cliente[0]['cliente'].replace(' ','_').replace('.','')
        else:
            cliente=''
        if self.batch_parameters['anno']:
            anno=' '+ self.batch_parameters['anno']
        else:
            anno=''
        self.batch_parameters['filename']=self.batch_parameters['filename'] or 'Export fat_emesse%s%s' %(anno,cliente)[:64]
        #self.batch_parameters['filename']=self.batch_parameters['filename'] or 'Export fat_emesse %(anno)s' %self.batch_parameters
        #impostiamo i dati
        self.columns=['cliente','data','doc_n','importo','descrizione','insda','scadenza','tot_pag','saldo']
        self.headers=['cliente','data','doc_n','importo','descrizione','insda','scadenza','tot_pag','saldo']

        self.coltypes={'cliente':'L','data':'A','doc_n':'A','importo':'N','descrizione':'A','insda':'A','scadenza':'A','tot_pag':'N','saldo':'N'}
        self.data = []
        if self.batch_parameters['anno'] and self.batch_parameters['clienteid']:
            f = self.tblobj.query(where='#PERIOD($data,:anno) AND $cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente,$data,$doc_n,$importo,$descrizione,$insda,$scadenza,$tot_pag,$saldo""",
                        order_by='$data,$doc_n',
                            anno=str(self.batch_parameters['anno']),clienteid=str(self.batch_parameters['clienteid'])).fetch()#,clienteid=str(self.batch_parameters['clienteid'])).fetch()
        elif self.batch_parameters['anno']:
            f = self.tblobj.query(where='#PERIOD($data,:anno)',# AND $cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente,$data,$doc_n,$importo,$descrizione,$insda,$scadenza,$tot_pag,$saldo""",
                        order_by='$data,$doc_n',
                            anno=str(self.batch_parameters['anno'])).fetch()#,clienteid=str(self.batch_parameters['clienteid'])).fetch()
        elif self.batch_parameters['clienteid']:
            f = self.tblobj.query(where='$cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente,$data,$doc_n,$importo,$descrizione,$insda,$scadenza,$tot_pag,$saldo""",
                        order_by='$data,$doc_n',
                            clienteid=str(self.batch_parameters['clienteid'])).fetch()#,clienteid=str(self.batch_parameters['clienteid'])).fetch()

        else:
            f = self.tblobj.query(where='',# AND $cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente,$data,$doc_n,$importo,$descrizione,$insda,$scadenza,$tot_pag,$saldo""",
                        order_by='$data,$doc_n').fetch()

        for rec in f:
            self.data.append(dict(cliente=rec['cliente'],data=self.page.toText(rec['data']),doc_n=rec['doc_n'],importo=rec['importo'],
                                descrizione=rec['descrizione'],insda=rec['insda'],scadenza=self.page.toText(rec['scadenza']),tot_pag=rec['tot_pag'],saldo=rec['saldo']))
        #print(x)

    def table_script_parameters_pane(self,center,**kwargs):
        anni = self.tblobj.query(
                    columns="EXTRACT(YEAR FROM $data) AS anno",
                    where="$data IS NOT NULL",
                    group_by="EXTRACT(YEAR FROM $data)",
                    order_by="EXTRACT(YEAR FROM $data)").fetch()
        anni_list = [r['anno'] for r in anni]
        fb = center.formbuilder(cols=1,border_spacing='3px')
        center.div('Compilando nella view Date<= otterremo il filtro<br> sulle fatture con tot_pag e saldo alla data inseririta', font_weight='bold',style='margin-bottom:10px;text-align:left;')
        #fb.numberSpinner(value='^.anno',format='####',lbl='Anno',width='6em')
        fb.filteringSelect(value='^.anno',values=','.join(str(a) for a in anni_list),lbl='Anno')
        fb.dbSelect(value='^.clienteid',lbl='Cliente',table='acc.cliente',hasDownArrow=True)
        fb.textbox(value='^.filename',lbl='Salva col nome')
