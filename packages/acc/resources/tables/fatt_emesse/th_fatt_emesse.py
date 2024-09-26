#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('cliente_id', width='30em', name='!![en]Customer')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('descrizione',width='50em')
        r.fieldcell('insda')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True)
        r.fieldcell('saldo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo',semaphore=True)

    def th_order(self):
        return 'data:d,doc_n:d'

    def th_options(self):
        return dict(partitioned=True)
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![en]Paid',condition='$saldo=0'),
                dict(code='insda',caption='!![en]InsDA',condition='$insda=true'),
                dict(code='scaduti',caption='!![en]Expired',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![en]Not Expired',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![en]Without Expire',condition='$scadenza is null and $saldo!=0')]
    
    #def th_sections_cliente_id(self):
    #    return [dict(code='cliente',caption='!![en]Customer',condition="$cliente_id!=''")]
                
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@cliente_id,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar',sections_cliente_id_multivalue=False,
                        sections_cliente_id_multiButton=False,sections_cliente_id_lbl='!![en]Customer',
                        sections_cliente_id_width='60em')
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')
    
    #def th_bottom_toolbarinferiore(self,bottom):
    #    bar=bottom.slotToolbar('5,sections@cliente_id,15',
    #                    childname='inferiore',_position='<bar',sections_cliente_id_multivalue=False,sections_cliente_id_multiButton=False)
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val=''),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val=''),
                            dict(field='data', lbl='!![en]Invoice date',width='10em'),
                            dict(field='descrizione', lbl='!![en]Description',width='20em')],
                            cols=4, isDefault=True) 

class ViewFromFatture(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id', width='30em', name='!![en]Customer')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('descrizione',width='50em')
        r.fieldcell('insda')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True)
        r.fieldcell('saldo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo',semaphore=True)

    def th_order(self):
        return 'data:d'

    def th_options(self):
        return dict(partitioned=True)
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![en]Paid',condition='$saldo=0'),
                dict(code='insda',caption='!![en]InsDA',condition='$insda=true'),
                dict(code='scaduti',caption='!![en]Expired',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![en]Not Expired',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![en]Without Expire',condition='$scadenza is null and $saldo!=0')]
    
    #def th_sections_cliente_id(self):
    #    return [dict(code='cliente',caption='!![en]Customer',condition="$cliente_id!=''")]
                
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar')
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')
    
    #def th_bottom_toolbarinferiore(self,bottom):
    #    bar=bottom.slotToolbar('5,sections@cliente_id,15',
    #                    childname='inferiore',_position='<bar',sections_cliente_id_multivalue=False,sections_cliente_id_multiButton=False)
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val=''),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val=''),
                            dict(field='data', lbl='!![en]Invoice date',width='10em'),
                            dict(field='descrizione', lbl='!![en]Description',width='20em')],
                            cols=4, isDefault=True)      
    
class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.fatEmesse(bc.roundedGroupFrame(title='!![en]Invoices issued',region='top',datapath='.record',height='300px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.paym_fatEmesse(tc.contentPane(title='!![en]Payments'))
        

    def fatEmesse(self,pane):
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('cliente_id', lbl='!![en]Customer', hasDownArrow=True, colspan=3, width='100%' )
        fb.field('data' )
        fb.field('doc_n' )
        fb.field('importo',font_weight='bold')
        fb.field('descrizione',width='100%', colspan=3, tag='textarea')
        fb.field('insda')
        fb.field('scadenza')
        fb.br()
        fb.field('note',width='100%', colspan=3, tag='textarea')

    def paym_fatEmesse(self,pane):
        pane.inlineTableHandler(relation='@paym_fat_emesse',
                                viewResource='ViewFromPayments')

    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px' )
