#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('fornitore_id')
        r.fieldcell('data')
        r.fieldcell('doc_n')
        r.fieldcell('descrizione',width='50em')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('tot_pag', totalize=True)
        r.fieldcell('saldo', totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo',semaphore=True)
        
    def th_order(self):
        return 'data:d'

    #def th_query(self):
    #    return dict(column='id', op='contains', val='')

    def th_options(self):
        return dict(partitioned=True)

    #@metadata(variable_struct=True)
    def th_sections_fatforn(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![en]Paid',condition='$saldo=0')]
    
    def th_top_toolbarsuperiore(self,top):
        top.slotToolbar('5,sections@fatforn,10,sections@volumeacquisti,5',
                        childname='superiore',_position='<bar')
                        #,gradient_from='#999',gradient_to='#888')

    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val=''),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val=''),
                            dict(field='data', lbl='!![en]Invoice date',width='10em'),
                            dict(field='descrizione', lbl='!![en]Description',width='10em')],
                            cols=4, isDefault=True)    
class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.fatforn(bc.roundedGroupFrame(title='!![en]Supplier invoices',region='top',datapath='.record',height='300px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.paym_fatforn(tc.contentPane(title='!![en]Payments'))

    def fatforn(self,pane):
        #pane = form.record
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('fornitore_id', lbl='!![en]Supplier', hasDownArrow=True, colspan=3, width='100%' )
        fb.field('data' )
        fb.field('doc_n' )
        fb.field('importo',font_weight='bold')
        fb.field('descrizione',width='100%', colspan=3, tag='textarea')

    def paym_fatforn(self,pane):
        pane.inlineTableHandler(relation='@paym_fat_forn',
                                viewResource='ViewFromPayments')

    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px' )
