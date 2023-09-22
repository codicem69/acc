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
        #r.fieldcell('tot_impfat',hidden=True)
        #r.fieldcell('totpag',hidden=True)
        r.fieldcell('balance', width='20em',totalize=True,
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='font-weight:bold;color:black;')
        #r.cell('balance_2',formula='tot_impfat-tot_pag', width='20em',totalize=True,
        #                  range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='font-weight:bold;color:black;')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='div_zero',caption='!![en]Not null',
                        condition='$balance!=0'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$balance>0'),
                dict(code='over_paym',caption='!![en]Over payment',
                        condition='$balance<0')]

    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@fornitore,15',
                        childname='superiore',_position='<bar',sections_fornitore_multiButton=False,
                        sections_fornitore_multivalue=True,
                        sections_fornitore_lbl='!![en]Supplier',
                        sections_fornitore_width='60em')

    def th_sections_fornitore(self):
        #prendiamo agency_id nel currentEnv
        ag_id=self.db.currentEnv.get('current_agency_id')
        #effettuaiamo la ricerca di tutti i fornitori filtrando quelli relativi all'agency_id
        f = self.db.table('acc.fornitore').query(where='agency_id=:ag_id',ag_id=ag_id,order_by='$rag_sociale').selection().output('records')#$agency_id=:ag_id',ag_id=self.db.currentEnv.get('current_agency_id')).fetch()
        #creaiamo una lista vuota dove andremo ad appendere i dizionari con il valore tutti e con i fornitori
        result=[]
        result.append(dict(code='tutti',caption='!![en]All'))
        for r in f:
            result.append(dict(code=r['id'], caption=r['rag_sociale'],
                     condition='$id=:fornitore',condition_fornitore=r['id']))
        return result
        
    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_supplier', op='contains', val='')

    def th_options(self):
        return dict(partitioned=True)

class Form(BaseComponent):

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.fornitore(bc.roundedGroupFrame(title='!![en]Supplier',region='top',datapath='.record',height='220px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.fat_forn(tc.contentPane(title='!![en]Invoices'))
        #self.note_forn(tc.contentPane(title='!!Note',datapath='.record'))
        self.bonifici(tc.contentPane(title='!![en]Transfers'))
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
        fb.field('note', tag='simpleTextArea', height='100px', colspan=2)
        #fb.field('balance',font_weight='bold',color ="^#FORM.record.balance?=#v>0?'red':'black'")
        
    def fat_forn(self,pane):
        pane.dialogTableHandler(relation='@forn_fatt',
                                viewResource='ViewFromFatForn',extendedQuery=True,pbl_classes=True, liveUpdated=True)
    #def note_forn(self,frame):
    #    frame.simpleTextArea(title='Note',value='^.note',editor=True)

    def bonifici(self,pane):
        pane.dialogTableHandler(relation='@bonifico_forn',
                                viewResource='View',extendedQuery=True,pbl_classes=True)    
    def bank_forn(self,pane):
        pane.dialogTableHandler(relation='@forn_bank',
                                viewResource='View')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
