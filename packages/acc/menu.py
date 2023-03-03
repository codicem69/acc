# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Suppliers", table="acc.fornitore", tags="")
        root.thpage(u"!![en]Supplier invoices", table="acc.fatture_forn", tags="")
