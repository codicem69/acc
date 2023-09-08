# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        user=self.db.currentEnv.get('user')
        taguser = self.db.currentEnv.get('userTags')
        tag_user=taguser.split(',')
        
        if 'admin' in tag_user or 'superadmin' in tag_user or '_DEV_' in tag_user:
            acc = root.branch(u"acc", tags="")
            acc.packageBranch('Amministrazione sistema',pkg='adm')#, branchMethod='userSubmenu')
            acc.packageBranch('System',pkg='sys')
            acc.packageBranch('Email',pkg='email')
            acc.packageBranch('Unlocode',pkg='unlocode')
            acc.packageBranch('Agencies',pkg='agz')
            
            acc.thpage(u"!![en]Suppliers", table="acc.fornitore", tags="")
            acc.thpage(u"!![en]Supplier invoices", table="acc.fatture_forn", tags="")
            acc.thpage(u"!![en]Payment invoices supplier", table="acc.pag_fat_forn", tags="")
            acc.thpage(u"!![en]Transfers supplier", table="acc.bonifici_fornitore", tags="")
            acc.thpage(u"!![en]Invoices supplier on transfers", table="acc.fatforn_bonifici", tags="")
            acc.thpage(u"!![en]Supplier bank", table="acc.bank_forn", tags="")
            acc.thpage(u"!![en]Invoices issued", table="acc.fatt_emesse", tags="")
            acc.thpage(u"!![en]Payment invoices issued", table="acc.pag_fat_emesse", tags="")
            acc.thpage(u"!![en]Customers", table="acc.cliente", tags="")
            acc.thpage(u"!![en]Customer bank", table="acc.bank_clienti", tags="")
            acc.thpage(u"!![en]Transfers customer", table="acc.bonifici_cliente", tags="")
        else:
            acc = root.branch(u"acc", tags="")
            acc.thpage(u"!![en]Suppliers", table="acc.fornitore", tags="")
            acc.thpage(u"!![en]Supplier invoices", table="acc.fatture_forn", tags="")
            acc.thpage(u"!![en]Customers", table="acc.cliente", tags="")
            acc.thpage(u"!![en]Invoices issued", table="acc.fatt_emesse", tags="")
            unlocode = root.branch(u"Unlocode", tags="")
            unlocode.thpage(u"Località", table="unlocode.place", tags="")
            unlocode.thpage(u"Nazione", table="unlocode.nazione", tags="")
            agz = root.branch(u"Agencies", tags="")
            agz.thpage(u"Agencies", table="agz.agency", tags="")
            agz.thpage(u"Staff", table="agz.staff", tags="")
            email = root.branch(u"!![en]Email", tags="")
            email.thpage(u"!![en]Messages", table="email.message", tags="")

