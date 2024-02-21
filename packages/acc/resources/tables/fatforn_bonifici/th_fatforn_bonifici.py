#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('bonifici_forn_id')
        r.fieldcell('fatture_forn_id')

    def th_order(self):
        return 'bonifici_forn_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromFatFornBonifici(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('bonifici_forn_id',edit=True)
        r.fieldcell('fatture_forn_id',edit=True,width='20em')
        r.fieldcell('importo',totalize=True)
        r.fieldcell('saldo',totalize=True)

    def th_order(self):
        return '@fatture_forn_id.data'
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('bonifici_forn_id' )
        fb.field('fatture_forn_id' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
