# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Suppliers", table="acc.fornitore", tags="")
        root.thpage(u"!![en]Supplier invoices", table="acc.fatture_forn", tags="")
        root.thpage(u"!![en]Payment invoices supplier", table="acc.pag_fat_forn", tags="")
        root.thpage(u"!![en]Supplier bank", table="acc.bank_forn", tags="")
        root.thpage(u"!![en]Invoices issued", table="acc.fatt_emesse", tags="")
        root.thpage(u"!![en]Payment invoices issued", table="acc.pag_fat_emesse", tags="")
        root.thpage(u"!![en]Customers", table="acc.cliente", tags="")

