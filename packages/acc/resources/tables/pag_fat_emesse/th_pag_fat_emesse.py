#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('fatt_emesse_id')
        r.fieldcell('data')
        r.fieldcell('importo')
        r.fieldcell('note')

    def th_order(self):
        return 'fatt_emesse_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('fatt_emesse_id' )
        fb.field('data' )
        fb.field('importo' )
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
