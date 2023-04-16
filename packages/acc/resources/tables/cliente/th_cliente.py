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

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')



class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.cliente(bc.roundedGroupFrame(title='!![en]Customer',region='top',datapath='.record',height='180px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_emesse(tc.contentPane(title='!![en]Invoices'))
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

    def fat_emesse(self,pane):
        pane.dialogTableHandler(relation='@fatt_cliente',
                                viewResource='View',extendedQuery=True,pbl_classes=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )