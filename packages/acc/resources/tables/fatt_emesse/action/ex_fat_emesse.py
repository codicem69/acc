# -*- coding: UTF-8 -*-

from gnr.web.batch.btcexport import BaseResourceExport

caption = 'Export Fatture'
description='Export Fatture'

class Main(BaseResourceExport):
    batch_prefix = 'EFE'
    batch_title = 'Export Fatture Emesse'
    batch_cancellable = False
    batch_delay = 0.5
    #export_mode = 'csv'

    def pre_process(self):
        self.file = self.batch_parameters['filename'] or 'Export fat_emesse %(anno)s' %self.batch_parameters
        self.columns=['cliente','data','doc_n','importo','descrizione','insda','scadenza']
        self.headers=['cliente','data','doc_n','importo','descrizione','insda','scadenza']


        self.coltypes={'cliente':'T','data':'A','doc_n':'T','importo':'N','descrizione':'A','ins_da':'A',
                        'scadenza':'A'}
        self.data = []
        f = self.tblobj.query(where='#PERIOD($data,:anno)',# AND $cliente_id=:clienteid',
                        columns="""@cliente_id.rag_sociale AS cliente,$data,$doc_n,$importo,$descrizione,$insda,$scadenza""",
                        order_by='$data,$doc_n',
                            anno=str(self.batch_parameters['anno'])).fetch()#,clienteid=str(self.batch_parameters['clienteid'])).fetch()
        for rec in f:
            self.data.append(dict(cliente=rec['cliente'],data=self.page.toText(rec['data']),doc_n=rec['doc_n'],importo=rec['importo'],
                                descrizione=rec['descrizione'],insda=rec['insda'],scadenza=self.page.toText(rec['scadenza'])))


    def table_script_parameters_pane(self,center,**kwargs):
        fb = center.formbuilder(cols=1,border_spacing='3px')
        fb.numberSpinner(value='^.anno',default_value=self.db.workdate.year,
                    validate_notnull=True,format='####',lbl='Anno',width='6em')
        #fb.dbSelect(value='^.clienteid',lbl='Cliente',table='acc.cliente')
        fb.textbox(value='^.filename',lbl='Salva col nome')
