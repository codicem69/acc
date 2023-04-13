#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('fatture_forn_id')
        r.fieldcell('data')
        r.fieldcell('importo')
        r.fieldcell('note')

    def th_order(self):
        return 'data:a'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromPayments(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('fatture_forn_id')
        r.fieldcell('data', edit=True)
        r.fieldcell('importo',edit=True,totalize=True)
        r.fieldcell('impfatforn',hidden=True)
        r.cell('progressivo',formula='+=importo',format='#,###.00',dtype='N')
        r.cell('rimanenza fattura',formula='impfatforn-progressivo',format='#,###.00',dtype='N',
               range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('note',edit=True, width='100%',values='Bonifico,Contanti,Storno fat.',hasArrowDown=True)

    def th_order(self):
        return 'data:a'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('fatture_forn_id' )
        fb.field('data' )
        fb.field('importo')
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
