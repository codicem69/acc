#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from datetime import datetime
from collections import defaultdict

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('cliente_id', width='30em', name='!![en]Customer')
        r.fieldcell('data', width='5em')
        r.fieldcell('doc_n', width='5em')
        r.fieldcell('descrizione',width='40em')
        r.fieldcell('insda')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True,name='^name_totpag')
        r.fieldcell('saldo', totalize=True,name='^name_saldo',
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_al',semaphore=True)
        r.fieldcell('saldo_effettivo', totalize=True,name=f'Saldo al {self.db.workdate.strftime("%d/%m/%Y")}',
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_eff',semaphore=True)

    def th_order(self):
        return 'data:d,doc_n:d'

    def th_options(self):
        return dict(partitioned=True)
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='div_zero',caption='!![en]Not null',
                        condition='$saldo!=0'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![en]Paid',condition='$saldo=0'),
                dict(code='insda',caption='!![en]InsDA',condition='$insda=true'),
                dict(code='scaduti',caption='!![en]Expired',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![en]Not Expired',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![en]Without Expire',condition='$scadenza is null and $saldo!=0'),
                dict(code='over_paym',caption='!![en]Over payment',condition='$saldo<0')]
    
    #def th_sections_cliente_id(self):
    #    return [dict(code='cliente',caption='!![en]Customer',condition="$cliente_id!=''")]
                
    def th_top_toolbarsuperiore(self,top):
        bar=top.slotToolbar('5,sections@fatemesse,sections@cliente_id,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar',sections_cliente_id_multivalue=False,
                        sections_cliente_id_multiButton=False,sections_cliente_id_lbl='!![en]Customer',
                        sections_cliente_id_width='60em')
                        #,gradient_from='#999',gradient_to='#888')
        bar.actions.div('Actions')
        #settiamo nella env la data_saldo per i calcoli con la formulaColumn
        bar.data('^acc_fatt_emesse.view.queryBySample.c_0',serverpath='data_saldo',dbenv=True)
        bar.dataController("""if(data_saldo) {SET name_saldo='Saldo al '+ data_saldo; SET name_totpag = 'Tot.Pag. al '+data_saldo;} else 
                           {SET name_saldo='Saldo al '+ data_att; SET name_totpag='Tot.Pag. al '+ data_att;}""",
                           data_saldo='^acc_fatt_emesse.view.queryBySample.c_0',data_att=self.workdate.strftime("%d/%m/%Y"),_onStart=True)
    #def th_bottom_toolbarinferiore(self,bottom):
    #    bar=bottom.slotToolbar('5,sections@cliente_id,15',
    #                    childname='inferiore',_position='<bar',sections_cliente_id_multivalue=False,sections_cliente_id_multiButton=False)
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val='', tag='dateTextBox'),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val='', tag='dateTextBox'),
                            dict(field='data', lbl='!![en]Invoice date',width='10em', tag='dateTextBox'),
                            dict(field='descrizione', lbl='!![en]Description',width='20em')],
                            cols=4, isDefault=True) 

class ViewFromFatture(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id', width='30em', name='!![en]Customer')
        r.fieldcell('data', width='5em')
        r.fieldcell('doc_n', width='5em')
        r.fieldcell('descrizione',width='40em')
        r.fieldcell('insda')
        r.fieldcell('importo', totalize=True)
        r.fieldcell('scadenza')
        r.fieldcell('giorni_scadenza', width='11em')
        r.fieldcell('tot_pag', totalize=True,name='^name_totpag')
        r.fieldcell('saldo', totalize=True,name='^name_saldo',
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_al',semaphore=True)
        r.fieldcell('saldo_effettivo', totalize=True,name=f'Saldo al {self.db.workdate.strftime("%d/%m/%Y")}',
                          range_alto='value>0',range_alto_style='color:red;font-weight:bold;',range_basso='value<=0',range_basso_style='color:black;font-weight:bold;')
        r.fieldcell('semaforo_eff',semaphore=True)


    def th_order(self):
        return 'data:d'

    def th_options(self):
        return dict(partitioned=True)
    
    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_sections_fatemesse(self):
        return [dict(code='tutti',caption='!![en]All'),
                dict(code='da_saldare',caption='!![en]To be paid',
                        condition='$saldo>0'),
                dict(code='saldati',caption='!![en]Paid',condition='$saldo=0'),
                dict(code='insda',caption='!![en]InsDA',condition='$insda=true'),
                dict(code='scaduti',caption='!![en]Expired',condition='$scadenza<now() and $saldo>0'),
                dict(code='non_scadute',caption='!![en]Not Expired',condition='$scadenza>now() and $saldo>0'),
                dict(code='senza_scadenza',caption='!![en]Without Expire',condition='$scadenza is null and $saldo!=0')]
    
    #def th_sections_cliente_id(self):
    #    return [dict(code='cliente',caption='!![en]Customer',condition="$cliente_id!=''")]
                
    def th_top_toolbarsuperiore(self,top):
        py_requires = "gnrcomponents/framegrid:FrameGrid"
        bar=top.slotToolbar('5,sections@fatemesse,10,emailfat,10,actions,resourceActions,15',
                        childname='superiore',_position='<bar')
                    
        bar.actions.div('Actions')
        #settiamo nella env la data_saldo per i calcoli con la formulaColumn
        bar.data('^acc_cliente.form.acc_fatt_emesse.view.queryBySample.c_0',serverpath='data_saldo',dbenv=True)
        bar.dataController("""if(data_saldo) {SET name_saldo='Saldo al '+ data_saldo; SET name_totpag = 'Tot.Pag. al '+data_saldo;} else 
                           {SET name_saldo='Saldo al '+ data_att; SET name_totpag='Tot.Pag. al '+ data_att;}""",
                           data_saldo='^acc_cliente.form.acc_fatt_emesse.view.queryBySample.c_0',data_att=self.workdate.strftime("%d/%m/%Y"),_onStart=True)

        btn_emailfat=bar.emailfat.button('Invia Email Fatture',disabled='^#FORM.controller.locked')
        btn_emailfat.dataRpc('.emaildialog',           # dove scrive il risultato
                            self.load_email_preview,cliente_id='=#FORM.record.id',pkeys='=#FORM.acc_fatt_emesse.view.grid.currentSelectedPkeys',
                            _onResult="""if (result.getItem('result_message')) {genro.publish('floating_message',{message:result.getItem('result_message'), messageType:'error'})} 
                            else {genro.wdgById('fat').show();SET .emaildialog.pkeys = GET #FORM.acc_fatt_emesse.view.grid.currentSelectedPkeys;PUBLISH fat_open;}"""#'FIRE dlg.emailDialog.show',  # apre il dialog DOPO aver caricato
                            )
        top.data('.dati',{'id':1234})
        dlg = top.dialog(title='Invio Email Fatture',closable=True,
                      height='620px', 
                      width='620px',
                      #parentRatio=1,
                      openAt='center',
                      nodeId='fat', 
                      subscribe_fat_open="""
                     var grid = genro.nodeById('grid_fatture');
                     if(grid && grid.widget){
                         setTimeout(function(){
                             grid.widget.resize();
                             grid.widget.render();
                         }, 100);
                     }
                 """)

        bc = dlg.borderContainer(height='100%')

        # ── ZONA TOP: form con i bottoni ──────────────────────────────
        top_pane = bc.contentPane(region='top', height='130px', 
                                   splitter=True, style='padding:8px;border-bottom:1px solid #ddd;')

        fb = top_pane.formbuilder(cols=2, border_spacing='4px', 
                                   width='100%', fld_width='100%')
        fb.div('^.emaildialog.count_label', font_weight='bold',style='margin-bottom:10px;text-align:left;')
        fb.br()
        fb.checkbox(value='^eng', lbl='Language: ', label='English', edit=True)
        fb.checkbox(value='^fda', lbl='', label='FDA', edit=True)

        # Bottoni nella zona top
        btn_bar = top_pane.div(style='margin-top:10px;text-align:left;')
        btn_bar.button('Conferma e Invia', fire='.emaildialog.sendemail')
        btn_bar.button('Annulla',
                action="genro.wdgById('fat').hide();",
                margin_left='8px')
        fb.textBox(value='^extra_ogg', lbl='Descrizione extra oggetto email')
        top.dataRpc('.emaildialog.result_message',self.send_emails,
                    _fired='^.emaildialog.sendemail',                          # senza underscore
                    pkeys='=.emaildialog.pkeys',                  # passa i pkeys salvati dal primo RPC
                    cliente_id='=#FORM.record.id',eng='=eng',fda='=fda',extra_ogg='=extra_ogg',allegati='=.emaildialog.allegati_preview',
                    _onResult="""if(result.getItem('messaggio')) {genro.publish("floating_message",{message:result.getItem('messaggio'), messageType:"message"})};
                    if(result.getItem('invio_email')) {genro.wdgById('fat').hide();}
                    """)

        center_pane = bc.contentPane(region='center', style='padding:4px;')
        inner_bc = center_pane.borderContainer(height='100%')
        # -- Griglia fatture --
        main_pane = inner_bc.contentPane(region='center', style='padding:4px;')
        grid = main_pane.quickGrid(value='^.emaildialog.fatture_preview',
            height='100%',
            selectionMode='multirow',
            nodeId='grid_fatture'
        )
        grid.column('numero',name='Fattura N.', width='80px')
        grid.column('data_fattura',name='Data',width='90px')
        grid.column('descrizione',name='Descrizione', width='200px')
        grid.column('totale',name='Importo', width='100px', format='€ #,##0.00', style='text-align:right;', totalize=True)
        grid.column('saldo',name='Saldo', width='100px', format='€ #,##0.00', style='text-align:right;')
        # -- Pannello allegati --
        att_pane = inner_bc.contentPane(region='bottom', height='180px',
                                         splitter=True,
                                         style='padding:4px;border-top:1px solid #ddd;')
        att_pane.div('Allegati', font_weight='bold', style='margin-bottom:6px;')

        att_grid = att_pane.quickGrid(
            value='^.emaildialog.allegati_preview',
            height='150px',
            selectionMode='multirow',
            nodeId='grid_allegati'
        )
        att_grid.column('includi', name='Includi', width='50px', 
                        dtype='B', edit=True)
        att_grid.column('description', name='Descrizione', width='auto')
        
    def th_queryBySample(self):
        return dict(fields=[dict(field='data', lbl='Date <=',width='10em', op='lesseq', val=''),
                            dict(field='data', lbl='Date >=',width='10em', op='greatereq', val=''),
                            dict(field='data', lbl='!![en]Invoice date',width='10em'),
                            dict(field='descrizione', lbl='!![en]Description',width='20em')],
                            cols=4, isDefault=True)      

    @public_method
    def load_email_preview(self,cliente_id=None,pkeys=None, **kwargs):
        """Solo dati — nessun accesso all'albero UI."""
        db = self.db
        result = Bag()
        if not pkeys:
            result['result_message']='Devi selezionare le fatture che vuoi inviare nella tabella'
            #print(X)
            return result
        fatture = db.table('acc.fatt_emesse').query(
            columns='$pkey,$doc_n,$data,$importo,$saldo,$descrizione,@cliente_id.rag_sociale,@cliente_id.email',
            where='$pkey IN :pkeys',pkeys=pkeys,
            #where='$cliente_id=:c_id',
            c_id=cliente_id, order_by='$data DESC'
            #where='$email_inviata IS NULL OR $email_inviata = FALSE',
        ).fetch()

        preview = Bag()
        for i, r in enumerate(fatture):
            row = Bag()
            row['numero'] = r['doc_n']
            row['data_fattura'] = r['data'].strftime("%d/%m/%Y")
            row['descrizione'] = r['descrizione']
            row['totale'] = r['importo']
            row['saldo'] = r['saldo']
            preview['fatture_preview.'f'r_{i}'] = row
        preview['count_label']=f'{len(fatture)} fatture pronte per l\'invio'

        # Carica allegati dalla tabella fatt_emesse_atc
        tbl_atc = self.db.table('acc.fatt_emesse_atc')
        pkeys_list = pkeys.split(',') if isinstance(pkeys, str) else list(pkeys)

        allegati = tbl_atc.query(
            columns='$maintable_id, $filepath, $mimetype, $description, $text_content',
            where='$maintable_id IN :pkeys',
            pkeys=pkeys_list
        ).fetch()

        for i, r in enumerate(allegati):
            row = Bag()
            row['includi'] =True
            row['description'] = r['description']
            row['filepath'] = r['filepath']
            preview['allegati_preview.'f'r_{i}'] = row
        
        return preview

    @public_method
    def send_emails(self, pkeys=None,eng=None,fda=None,extra_ogg=None,allegati=None, **kwargs):
        if not pkeys:
            return
        
        # pkeys arriva come lista da GenroPy, non come stringa
        if isinstance(pkeys, str):
            pkeys_list = [p.strip() for p in pkeys.split(',') if p.strip()]
        else:
            pkeys_list = list(pkeys)  # già lista, tuple, o altro iterabile

        fatture = self.db.table('acc.fatt_emesse').query(
            columns='$pkey,$doc_n,$data,$descrizione,$importo,$tot_pag,$saldo,@cliente_id.rag_sociale,@cliente_id.email,@cliente_id.email_cc',
            where='$pkey IN :pkeys_list',
            pkeys_list=pkeys_list,).fetch()
        
        dati_invio = Bag()
        if not fatture:
            dati_invio['messaggio']='Nessuna fattura trovata.'
            return dati_invio
            return 'Nessuna fattura trovata.'

        # Recupera i pagamenti collegati alle fatture trovate
        pagamenti = self.db.table('acc.pag_fat_emesse').query(columns='$fatt_emesse_id,$data,$importo,$note',
                        where='$fatt_emesse_id IN :pkeys_list',
                        pkeys_list=pkeys_list,
                        order_by='$fatt_emesse_id,$data').fetch()
       
        # Organizza i pagamenti per fattura
        pagamenti_per_fattura = defaultdict(list)
        for p in pagamenti:
            pagamenti_per_fattura[p['fatt_emesse_id']].append(p)

        # Verifica email cliente
        email_dest = fatture[0]['_cliente_id_email']
        email_dest_cc = fatture[0]['_cliente_id_email_cc']
        ragione_sociale = fatture[0]['_cliente_id_rag_sociale']
        
        if not email_dest:
            dati_invio['messaggio']=f'Invio annullato: il cliente {ragione_sociale} non ha email.'
            return dati_invio
        
        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,agency_name,user_fullname,agency_fullstyle,bank,iban,bic = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,@agency_id.agency_name,$fullname,@agency_id.fullstyle,@agency_id.bank,,@agency_id.iban,@agency_id.bic',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))
        #Impostiamo i dati per il saluto
        now = datetime.now()
        cur_time = now.strftime("%H:%M:%S")    
        if cur_time < '13:00:00':
            if eng==True:
                sal='Good day'
            else:
                sal='Buongiorno,'  
        elif cur_time < '17:00:00':
            if eng==True:
                sal='Good afternoon,'
            else:
                sal='Buon pomeriggio,'
        elif cur_time < '24:00:00':
            if eng==True:
                sal='Good evening,'
            else:
                sal = 'Buonasera,' 
        elif cur_time < '04:00:00':
            if eng==True:
                sal='Good night,'
            else:
                sal = 'Buona notte,' 
        
        # Costruisci le righe HTML
        righe_html = ''
        totale_complessivo = 0
        saldo_complessivo = 0
        if eng==True:
            if fda==True:
                int_email='Final D/A - ' + agency_name
                doc='FDA Inv.no.'
                testo='please find attached copies of our invoices/FDA, as listed'
            else:
                int_email='Invoice - ' + agency_name
                doc='Invoice no.'
                testo='please find attached copies of our invoices, as listed'
            data='Date'
            descr='Description'
            imp='Amount'
            pag='Tot. payment'
            saldo='Balance'
            tot_compl='Grand Total'
            
            saluti='Brgds'
            coordinate='Bank Details'
            banca_int='Account holder'
            banca='Bank'
            pag_label = 'Payments'
            data_pag = 'Date'
            importo_pag = 'Amount'
            note_pag = 'Note'
            nessun_pag = 'No payments recorded'
        else:
            if fda==True:
                int_email = 'Conto esborsi - ' + agency_name
                doc='C/E Fattura n.'
                testo='in allegato inviamo copie ns. fatture C/E emesse come da elenco'
            else:
                int_email = 'Fatture - ' + agency_name
                doc='Fattura n.'
                testo='in allegato inviamo copie ns. fatture emesse come da elenco'
            data='Data'
            descr='Descrizione'
            imp='Importo'
            pag='Totale pagato'
            saldo='Saldo'
            tot_compl='Totale Complessivo'
            
            saluti='Cordiali saluti'
            coordinate='Coordinate Bancarie'
            banca_int='Intestatario'
            banca='Banca'
            pag_label = 'Pagamenti'
            data_pag = 'Data'
            importo_pag = 'Importo'
            note_pag = 'Note'
            nessun_pag = 'Nessun pagamento registrato'

        
        
        for i, r in enumerate(fatture):
            bg = 'background:#f9f9f9;' if i % 2 == 0 else ''
            righe_html += f"""
            <tr style="{bg}">
                <td style="padding:8px; border:1px solid #ddd;">{r['doc_n']}</td>
                <td style="padding:8px; border:1px solid #ddd;">{r['data'].strftime("%d/%m/%Y")}</td>
                <td style="padding:8px; border:1px solid #ddd;">{r['descrizione']}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['importo']:,.2f}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['tot_pag']:,.2f}</td>
                <td style="padding:8px; border:1px solid #ddd; text-align:right;white-space:nowrap;">€ {r['saldo']:,.2f}</td>
            </tr>"""
            # Riga con sotto-tabella pagamenti
            pags = pagamenti_per_fattura.get(r['pkey'], [])
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
        
        numeri = ', '.join([r['doc_n'] for r in fatture])
        if saldo_complessivo == 0:
            frame_banca=''
        elif saldo_complessivo < 0:
            saldo_pos = saldo_complessivo.copy_abs() #trasformo in positivo il valore negativo
            if eng == True:
                frame_banca=f'Please let us know your bank details in order to remit the balance of € {saldo_pos} in your favor.'
            else:
                frame_banca=f'Gentilmente fateci avere i Vs. dettagli bancari per la rimessa del saldo di € {saldo_pos} in Vs. favore.'
        else:
            frame_banca=f"""<div style="margin:24px 0;padding:16px;background:#f8f8f8;border-left:4px solid #2c3e50;">
                                <p style="margin:0 0 10px 0;font-weight:bold;color:#2c3e50;">{coordinate}</p>
                                <table style="border-collapse:collapse;font-size:13px;">
                                    <tr>
                                        <td style="padding:4px 16px 4px 0;color:#888;white-space:nowrap;">{banca_int}</td>
                                        <td style="padding:4px 0;font-weight:bold;white-space:nowrap;">{agency_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:4px 16px 4px 0;color:#888;white-space:nowrap;">{banca}</td>
                                        <td style="padding:4px 0;white-space:nowrap;">{bank}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:4px 16px 4px 0;color:#888;white-space:nowrap;">IBAN</td>
                                        <td style="padding:4px 0;font-weight:bold;white-space:nowrap;">{iban}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:4px 16px 4px 0;color:#888;white-space:nowrap;">BIC/SWIFT</td>
                                        <td style="padding:4px 0;white-space:nowrap;">{bic}</td>
                                    </tr>
                                </table>
                            </div>"""
        
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
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:left;border:1px solid #2c3e50;">{doc}</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:left;border:1px solid #2c3e50;">{data}</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:left;border:1px solid #2c3e50;">{descr}</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">{imp}</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">{pag}</th>
                                    <th style="background:#2c3e50;color:#fff;padding:10px 8px;text-align:right;border:1px solid #2c3e50;">{saldo}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {righe_html}
                            </tbody>
                        </table>

                        <div style="text-align:right;font-size:15px;font-weight:bold;color:#2c3e50;
                                    padding:10px 0;border-top:2px solid #2c3e50;margin-bottom:28px;">
                            {tot_compl}: &euro; {saldo_complessivo:,.2f}
                        </div>
                        {frame_banca}
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
        if extra_ogg:
            extra_ogg = '- ' + extra_ogg
        else:
            extra_ogg = ''
        # Filtra solo gli allegati con includi=True
        allegati_da_inviare = []
        if allegati:
            for row in allegati.values():
                d = row.asDict() if hasattr(row, 'asDict') else dict(row)
                if d.get('includi'):
                    #allegati_da_inviare.append(d['filepath'])
                    fileSn = self.site.storageNode(d['filepath'])
                    allegati_da_inviare.append(fileSn.internal_path)
        
        self.db.table('email.message').newMessage(account_id=account_email,
                    from_address=email_mittente,
                    to_address=email_dest,
                    cc_address=email_dest_cc,
                    subject=f'{int_email} {extra_ogg}',
                    body=body_html, html=True,attachments=allegati_da_inviare)
        self.db.commit()

        dati_invio['invio_email']='ok'
        dati_invio['messaggio']=f'Email creata per {email_dest} ({len(fatture)} fatture).'  
        return dati_invio
   
class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor,gnrcomponents/attachmanager/attachmanager:AttachManager'
    def th_form(self, form):
        bc = form.center.borderContainer()
        self.fatEmesse(bc.roundedGroupFrame(title='!![en]Invoices issued',region='top',datapath='.record',height='300px', splitter=True))
        tc = bc.tabContainer(margin='2px',region='center')
        self.paym_fatEmesse(tc.contentPane(title='!![en]Payments'))
        self.att_fatEmesse(tc.contentPane(title='!![en]Attachments'))
        

    def fatEmesse(self,pane):
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('cliente_id', lbl='!![en]Customer', hasDownArrow=True, colspan=3, width='100%' )
        fb.field('data' )
        fb.field('doc_n' )
        fb.field('importo',font_weight='bold')
        fb.field('descrizione',width='100%', colspan=3, tag='textarea')
        fb.field('insda')
        fb.field('scadenza')
        fb.br()
        fb.field('note',width='100%', colspan=3, tag='textarea')
        

    def paym_fatEmesse(self,pane):
        pane.inlineTableHandler(relation='@paym_fat_emesse',
                                viewResource='ViewFromPayments')
    def att_fatEmesse(self,pane):
        pane.attachmentGrid(uploaderButton=True)

    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True )
        #return dict(dialog_height='400px', dialog_width='600px' )

