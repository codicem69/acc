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
        r.fieldcell('fornitore_id')
        r.fieldcell('causale', width='70em')
        r.fieldcell('importo', totalize=True)

    def th_order(self):
        return 'data:d'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):
    py_requires="""gnrcomponents/attachmanager/attachmanager:AttachManager"""
    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.bonifici_forn(bc.roundedGroup(title='!![en]Transfers supplier',region='top',datapath='.record',height='200px'))
        self.fatture_fornitore(bc.contentPane(title='!![en]Invoices supplier',margin='2px', region='left', width='30%', splitter=True))
        self.allegatiBonForn(bc.contentPane(title='!![en]Attachments',region='center',width='70%',splitter=True))

    def bonifici_forn(self,pane): 
        fb = pane.formbuilder(cols=1, border_spacing='4px')
        fb.field('data')
        fb.field('fornitore_id', hasDownArrow=True, width='30em' )
        fb.field('causale',tag='simpleTextArea', width='50em' )
        fb.field('importo' )

    def fatture_fornitore(self,pane):
        pane.inlineTableHandler(relation='@bonifici_forn',viewResource='ViewFromFatFornBonifici',
                                picker='fatture_forn_id',
                                picker_condition='fornitore_id=:fid and $saldo>0',# or $bonificato IS NULL',
                                picker_condition_fid='^#FORM.record.fornitore_id',
                                picker_viewResource='ViewFormFatFornBonifici_picker')#'ViewFromCargoLU_picker')
                           #,pbl_classes=True,margin='2px',addrow=True,picker='doc_n',
                           #picker_condition='$saldo>0',
                           #picker_viewResource=True)
    
    def allegatiBonForn(self,pane):
        pane.attachmentGrid(uploaderButton=True) 

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_bonifico,*,10')
        btn_bonifico_print=bar.stampa_bonifico.button('!![en]Print transfer')
        btn_bonifico_print.dataRpc('nome_temp', self.print_bonifico,record='=#FORM.record',nome_template = 'acc.bonifici_fornitore:bonifico_forn',format_page='A4')
    
    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )

    @public_method
    def print_bonifico(self, record, resultAttr=None, nome_template=None, format_page=None, **kwargs):
        #msg_special=None
        record_id=record['id']
        #print(x)
       #if selId is None:
       #    msg_special = 'yes'
       #    return msg_special

        tbl_bonifici_forn = self.db.table('acc.bonifici_fornitore')
        builder = TableTemplateToHtml(table=tbl_bonifici_forn)

        nome_temp = nome_template.replace('acc.bonifico_forn:','')
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