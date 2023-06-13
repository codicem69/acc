from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Estratto Fornitore'

class Main(BaseResourcePrint):
    batch_title = 'Estratto Fornitore'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/estratto_fornitore'
    #Questo parametro indica la risorsa di stampa da utilizzare
    
    #con def_process decidiamo se utilizzare un'altra html_res. Inquesto caso estratto_dettaglio_forn
    #def pre_process(self):
    #    if self.batch_parameters['estratto_dett']:
    #        self.htmlMaker = self.page.site.loadTableScript(page=self.page, table='acc.fornitore',
    #                                                 respath='html_res/estratto_dettaglio_forn', class_name='Main')
    def table_script_parameters_pane(self, pane,**kwargs):
        #Questo metodo consente l'inserimento di alcuni parametri da utilizzare per la stampa
        #Prepariamo la stringa con gli ultimi 20 anni separati da virgola da passare alla filteringSelect
        current_year = datetime.today().year
        years=''
        for r in range(20):
            years += ',' + (str(current_year-r))
        
        fb = pane.formbuilder(cols=1, width='220px')
        fb.checkbox(value='^.balance', label='!![en]Only credits', lbl='Balance')
        fb.filteringSelect(value='^.anno', values=years, lbl='!![en]Year')
        fb.dateTextBox(value='^.dal',lbl='!![en]Date from',period_to='.al')
        fb.dateTextBox(value='^.al',lbl='!![en]Date to')
        #fb.filteringSelect(value='^.tip', values='cargo,cruise,ponton')
        #fb.div('Cargo',hidden="^.tip?=#v!='cargo'")
        #^.form_gdfdep?=#v==true?true:false
        #se volgliamo utilizzare una checkbox per selezionare un'altra risorsa
        #fb.checkbox(value='^.estratto_dett',label='!![en]Statement with payment details')
        #fb.div('!![en]Select the Supplier for single statement',hidden='^.estratto_dett?=!#v') #con hidden che punta al valore della checkbox visualizziamo il div
        #fb.dbselect(value='^.fornitore_id', table='acc.fornitore', lbl='Fornitore', selected_rag_sociale='.rag_sociale',hasDownArrow=True, hidden='^.estratto_dett?=!#v')
        #anche sulla dbSelect abbiamo il valore hidden che in caso di checkbox selezionata ci visualizza il widget