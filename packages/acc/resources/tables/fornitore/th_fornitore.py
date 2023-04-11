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
        r.fieldcell('balance', width='20em',totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='font-weight:bold;color:black;')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_supplier', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.fornitore(bc.roundedGroupFrame(title='!![en]Supplier',region='top',datapath='.record',height='180px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_forn(tc.contentPane(title='!![en]Invoices'))
        self.bank_forn(tc.contentPane(title='!![en]Bank details'))

    def fornitore(self, pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=2, border_spacing='4px',colswidth='auto',fld_width='100%')
        #fb = pane.formbuilder(cols=2, border_spacing='4px', fld_width='30em')
        fb.field('rag_sociale')
        fb.field('address')
        fb.field('cap' )
        fb.field('city')
        fb.field('tel')
        fb.field('email')
        fb.field('balance',font_weight='bold',color ="^#FORM.record.balance?=#v>0?'red':'black'")

    def fat_forn(self,pane):
        pane.dialogTableHandler(relation='@forn_fatt',
                                viewResource='View',extendedQuery=True)
    def bank_forn(self,pane):
        pane.dialogTableHandler(relation='@forn_bank',
                                viewResource='View')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
