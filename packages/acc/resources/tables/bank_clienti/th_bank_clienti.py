#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id')
        r.fieldcell('banca')
        r.fieldcell('iban')
        r.fieldcell('swiftcode')

    def th_order(self):
        return 'cliente_id'

    def th_query(self):
        return dict(column='banca', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px',colswidth='90%',fld_width='100%')
        fb.field('cliente_id' )
        fb.field('banca' )
        fb.field('iban' )
        fb.field('swiftcode' )


    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
