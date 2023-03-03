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
        r.fieldcell('importo')
        r.fieldcell('descrizione')

    def th_order(self):
        return 'fornitore_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('fornitore_id', lbl='!![en]Supplier', hasDownArrow=True, colspan=3, width='100%' )
        fb.field('data' )
        fb.field('doc_n' )
        fb.field('importo' )
        fb.field('descrizione',width='100%', colspan=3, tag='textarea')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
