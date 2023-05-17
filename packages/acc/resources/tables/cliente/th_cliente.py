#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale', width='30em')
        r.fieldcell('address', width='30em')
        r.fieldcell('cap')
        r.fieldcell('city', width='20em')
        r.fieldcell('vat')
        r.fieldcell('cf')
        r.fieldcell('cod_univoco')
        r.fieldcell('pec')
        r.fieldcell('balance', width='20em',totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='font-weight:bold;color:black;')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='div_zero',caption='!![en]Not null',
                        condition='$balance!=0'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$balance>0'),
                dict(code='over_paym',caption='!![en]Over payment',
                        condition='$balance<0')]

    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,15',
                        childname='superiore',_position='<bar')
            
    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')



class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.cliente(bc.roundedGroupFrame(title='!![en]Customer',region='top',datapath='.record',height='210px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_emesse(tc.contentPane(title='!![en]Invoices'))
        self.bonifici(tc.contentPane(title='!![en]Transfers'))
        self.banca_cliente(tc.contentPane(title='!![en]Bank details'))
        #self.bank_forn(tc.contentPane(title='!![en]Bank details'))
    
    def cliente(self, pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=2, border_spacing='4px',colswidth='auto',fld_width='100%')
        #fb = pane.formbuilder(cols=2, border_spacing='4px', fld_width='30em')
        fb.field('rag_sociale' )
        fb.field('address' )
        fb.field('cap' )
        fb.field('city' )
        fb.field('vat' )
        fb.field('cf' )
        fb.field('cod_univoco' )
        fb.field('pec' )
        fb.field('note', tag='simpleTextArea', height='70px', colspan=2)

    def fat_emesse(self,pane):
        pane.dialogTableHandler(relation='@fatt_cliente',
                                viewResource='ViewFromFatture',extendedQuery=True,pbl_classes=True)
    
    def bonifici(self,pane):
        pane.dialogTableHandler(relation='@bonifico_cliente',
                                viewResource='View',extendedQuery=True,pbl_classes=True)  
        
    def banca_cliente(self,pane):
        pane.dialogTableHandler(relation='@customer_bank',
                                viewResource='View',extendedQuery=True,pbl_classes=True)    

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
