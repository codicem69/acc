#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('fornitore_id')
        r.fieldcell('banca',width='50em')
        r.fieldcell('iban', width='30em')
        r.fieldcell('swiftcode')

    def th_order(self):
        return 'fornitore_id'

    def th_query(self):
        return dict(column='banca', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px',colswidth='90%',fld_width='100%')
        fb.field('fornitore_id' )
        fb.field('banca' )
        fb.field('iban' )
        fb.field('swiftcode' )


    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px' )
