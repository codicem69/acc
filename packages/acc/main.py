#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='acc package',sqlschema='acc',sqlprefix=True,
                    name_short='Acc', name_long='Accounting', name_full='Acc')

    def custom_type_money(self):
        return dict(dtype='N',format='#,###.00')

    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
