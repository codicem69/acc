#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale')
        r.fieldcell('address')
        r.fieldcell('cap')
        r.fieldcell('city')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_supplier', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('rag_sociale' , width='30em')
        fb.field('address', width='30em')
        fb.field('cap' )
        fb.field('city', width='15em' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
