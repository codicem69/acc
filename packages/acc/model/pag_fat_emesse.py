# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('pag_fat_emesse', pkey='id', name_long='!![en]Payment invoice issued', name_plural='!![en]Payment invoices issued',caption_field='id')
        self.sysFields(tbl)

        tbl.column('fatt_emesse_id',size='22', group='_', name_long='fatt_emesse_id'
                    ).relation('fatt_emesse.id', relation_name='paym_fat_emesse', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('importo', dtype='money', size='10,3', name_short='!![en]Amount')
        tbl.column('note', name_short='!![en]Note')
        tbl.aliasColumn('impfatemessa','@fatt_emesse_id.importo')