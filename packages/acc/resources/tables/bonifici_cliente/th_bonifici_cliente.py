#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('data')
        r.fieldcell('cliente_id')
        r.fieldcell('causale', width='70em')
        r.fieldcell('importo', totalize=True)

    def th_order(self):
        return 'data:d'

    def th_query(self):
        return dict(column='causale', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.bonifici_clienti(bc.roundedGroup(title='!![en]Transfers customer',region='top',datapath='.record',height='200px'))

    def bonifici_clienti(self,pane):    
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('data')
        fb.field('cliente_id', hasDownArrow=True, width='30em' )
        fb.field('causale',tag='simpleTextArea', width='50em' )
        fb.field('importo' )


    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px' )

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_bonifico,*,10')
        btn_bonifico_print=bar.stampa_bonifico.button('!![en]Print transfer')
        btn_bonifico_print.dataRpc('nome_temp', self.print_bonifico,record='=#FORM.record',nome_template = 'acc.bonifici_cliente:bonifico_cliente',format_page='A4')

    @public_method
    def print_bonifico(self, record, resultAttr=None, nome_template=None, format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_bonifici_forn = self.db.table('acc.bonifici_cliente')
        builder = TableTemplateToHtml(table=tbl_bonifici_forn)

        nome_temp = nome_template.replace('acc.bonifico_cliente:','')
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=nome_temp)

        template = self.loadTemplate(nome_template)  # nome del template
        pdfpath = self.site.storageNode('home:stampe_template', nome_file)

        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
        letterhead=''       
        for r in range(len(templates)):
            if templates[r][1] == 'A4_vert':
                letterhead = templates[r][0]    
            if format_page=='A3':
                if templates[r][1] == 'A3_orizz':
                    letterhead = templates[r][0]
          
        builder(record=record_id, template=template,letterhead_id=letterhead)
        
        result = builder.writePdf(pdfpath=pdfpath)

        self.setInClientData(path='gnr.clientprint',
                              value=result.url(timestamp=datetime.now()), fired=True)    