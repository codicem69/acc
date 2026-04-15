#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrbag import Bag
from collections import defaultdict

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
                                picker_condition='fornitore_id=:fid and $saldo>0',# and $bonificato IS NULL',
                                picker_condition_fid='^#FORM.record.fornitore_id',
                                picker_viewResource='ViewFormFatFornBonifici_picker')#'ViewFromCargoLU_picker')
                           #,pbl_classes=True,margin='2px',addrow=True,picker='doc_n',
                           #picker_condition='$saldo>0',
                           #picker_viewResource=True)
    
    def allegatiBonForn(self,pane):
        pane.attachmentGrid(uploaderButton=True) 

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('10,stampa_bonifico,10,email_bonifico,*,10')
        btn_bonifico_print=bar.stampa_bonifico.button('!![en]Print transfer')
        btn_bonifico_print.dataRpc('nome_temp', self.print_bonifico,record='=#FORM.record',nome_template = 'acc.bonifici_fornitore:bonifico_forn_new',format_page='A4')
        btn_email_bonifico=bar.email_bonifico.button('!![en]Email transfer')
        btn_email_bonifico.dataRpc('invio_bonifico', self.email_bonifico,record='=#FORM.record',
                _onResult="""if(result.getItem('messaggio')) {genro.publish("floating_message",{message:result.getItem('messaggio'), messageType:"message"})};
                if(result.getItem('invio_email')) {genro.wdgById('fat').hide();}
                """)

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

    @public_method
    def email_bonifico(self, record, **kwargs):
        bon_id=record['id']
        fattureBonifico = self.db.table('acc.fatforn_bonifici').query(
            columns='$fatture_forn_id,@fatture_forn_id.data as data,@fatture_forn_id.doc_n as doc_n,$importo,@fatture_forn_id.tot_pag as tot_pag,$saldo',
            where='$bonifici_forn_id = :bon_id',
            bon_id=bon_id).fetch()
        # Verifica email cliente
        forn_id=record['fornitore_id']
        email_forn,email_forn_cc,ragione_sociale = self.db.table('acc.fornitore').readColumns(
            columns='$email,$email_cc,$rag_sociale',
            where='id=:forn_id',
            forn_id=forn_id)
        invio_bonifico = Bag()

        # Recupera i pagamenti collegati alle fatture trovate
        pkeys_list=[]
        for f in fattureBonifico:
            pkeys_list.append(f['fatture_forn_id'])
        pagamenti = self.db.table('acc.pag_fat_forn').query(columns='$fatture_forn_id,$data,$importo,$note',
                        where='$fatture_forn_id IN :pkeys_list',
                        pkeys_list=pkeys_list,
                        order_by='$fatture_forn_id,$data').fetch()
       
        # Organizza i pagamenti per fattura
        pagamenti_per_fattura = defaultdict(list)
        for p in pagamenti:
            pagamenti_per_fattura[p['fatture_forn_id']].append(p)


        #print(c)
        if not email_forn:
            invio_bonifico['messaggio']=f'Invio annullato: il cliente {ragione_sociale} non ha email.'
            return invio_bonifico
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,agency_name,user_fullname,agency_fullstyle,bank,iban,bic = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,@agency_id.agency_name,$fullname,@agency_id.fullstyle,@agency_id.bank,,@agency_id.iban,@agency_id.bic',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        #Impostiamo i dati per il saluto
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            sal='Buon pomeriggio,'
        elif cur_time < '24:00:00':
            sal = 'Buonasera,' 
        elif cur_time < '04:00:00':        
            sal = 'Buona notte,' 
        
        int_email = 'Bonifico - ' + agency_name
        testo='in allegato inviamo copia bonifico a saldo fatture come da elenco'
        data_pag = 'Data'
        importo_pag = 'Importo'
        note_pag = 'Note'
        nessun_pag = 'Nessun pagamento registrato'
        pag_label = 'Pagamenti'
        saluti='Cordiali saluti'
        # Costruisci le righe HTML
        righe_html = ''
        totale_complessivo = 0
        saldo_complessivo = 0

        for i, r in enumerate(fattureBonifico):
            bg = 'background:#f9f9f9;' if i % 2 == 0 else ''
            righe_html += f"""
            <tr style="{bg}">
                <td style="padding:8px; border:1px solid #ddd;">{r['doc_n']}</td>
                <td style="padding:8px; border:1px solid #ddd;">{r['data'].strftime("%d/%m/%Y")}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['importo']:,.2f}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['tot_pag']:,.2f}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['saldo']:,.2f}</td>
            </tr>"""
            # Riga con sotto-tabella pagamenti
            pags = pagamenti_per_fattura.get(r['fatture_forn_id'], [])
            if pags:
                righe_pag_html = ''
                for p in pags:
                    note_txt = p['note'] or ''
                    righe_pag_html += f"""
                    <tr>
                        <td style="padding:4px 8px;color:#555;">{p['data'].strftime("%d/%m/%Y")}</td>
                        <td style="padding:4px 8px;color:#555;text-align:right;white-space:nowrap;">€ {p['importo']:,.2f}</td>
                        <td style="padding:4px 8px;color:#555;">{note_txt}</td>
                    </tr>"""
            else:
                righe_pag_html = f"""
                    <tr>
                        <td colspan="3" style="padding:4px 8px;color:#aaa;font-style:italic;">{nessun_pag}</td>
                    </tr>"""
            if pags:
                righe_html += f"""
                <tr style="{bg}">
                    <td colspan="6" style="padding:4px 16px 10px 24px;border:1px solid #eee;background:#fafafa;">
                        <span style="font-size:11px;font-weight:bold;color:#2c3e50;text-transform:uppercase;
                                     letter-spacing:.5px;">{pag_label}</span>
                        <table style="width:auto;border-collapse:collapse;font-size:12px;margin-top:4px;">
                            <thead>
                                <tr>
                                    <th style="padding:3px 8px;text-align:left;color:#888;font-weight:normal;
                                               border-bottom:1px solid #ddd;">{data_pag}</th>
                                    <th style="padding:3px 8px;text-align:right;color:#888;font-weight:normal;
                                               border-bottom:1px solid #ddd;">{importo_pag}</th>
                                    <th style="padding:3px 8px;text-align:left;color:#888;font-weight:normal;
                                               border-bottom:1px solid #ddd;">{note_pag}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {righe_pag_html}
                            </tbody>
                        </table>
                    </td>
                </tr>"""    
            totale_complessivo += r['importo']
            saldo_complessivo += r['saldo']
            body_html = f"""
                <div style="font-family:Arial,sans-serif;font-size:14px;color:#333;max-width:780px;">

                    <div style="background:#2c3e50;color:#ffffff;padding:12px 32px;border-radius:6px 6px 0 0;">
                        <h2 style="margin:0;font-weight:normal;">{int_email}</h2>
                    </div>

                    <div style="background:#ffffff;padding:28px 32px;">
                        <p style="font-size:15px;">
                            to: <strong>{ragione_sociale}</strong>
                        </p>
                        <p style="color:#555;line-height:1.6;">
                            {sal}<br>
                            {testo}.<br>
                        </p>

                        <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px;">
                            <thead>
                                <tr>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:left;border:1px solid #2c3e50;">Fatt.n.</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:left;border:1px solid #2c3e50;">data</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">importo</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">Totale pagato</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">Saldo</th>
                                </tr>
                            </thead>
                            <tbody>
                                {righe_html}
                            </tbody>
                        </table>

                        <div style="text-align:right;font-size:15px;font-weight:bold;color:#2c3e50;
                                    padding:10px 0;border-top:2px solid #2c3e50;margin-bottom:28px;">
                            Totale Complessivo: &euro; {totale_complessivo:,.2f}
                        </div>
                        <p style="color:#555;">{saluti}</p>
                        <p style="color:#555;font-size:13px;">{user_fullname}</p>
                        <p style="color:#555;font-size:13px;">{agency_fullstyle}</p>
                        
                    </div>
                </div>
                    <div style="max-width:780px;border-top:1px solid #ddd;margin:0;font-size:10px;text-align:justify;">
                    <div style="padding:12px 24px;">
                        {self.getPreference('privacy_email', pkg='acc')}
                    </div>
                    </div>      
                """
        # Carica allegati dalla tabella bonifici_fornitore_atc
        tbl_atc = self.db.table('acc.bonifici_fornitore_atc')
        
        allegati = tbl_atc.query(
            columns='$maintable_id, $filepath, $mimetype, $description, $text_content',
            where='$maintable_id = :bon_id',
            bon_id=bon_id).fetch()
        allegati_da_inviare = []
        if allegati:
            for row in allegati:
                fileSn = self.site.storageNode(row['filepath'])
                allegati_da_inviare.append(fileSn.internal_path)
        self.db.table('email.message').newMessage(account_id=account_email,
                    from_address=email_mittente,
                    to_address=email_forn,
                    cc_address=email_forn_cc,
                    subject=f'{int_email}',
                    body=body_html, html=True,attachments=allegati_da_inviare)
        self.db.commit()

        invio_bonifico['invio_email']='ok'
        invio_bonifico['messaggio']=f'Email creata per {email_forn} ({len(fattureBonifico)} fatture).'  
        return invio_bonifico