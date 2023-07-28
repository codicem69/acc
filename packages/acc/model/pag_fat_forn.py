# encoding: utf-8
from gnr.core.gnrbag import Bag
from datetime import datetime

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('pag_fat_forn', pkey='id', name_long='!![en]Payment invoice supplier', name_plural='!![en]Payment invoices suppliers',caption_field='id')
        self.sysFields(tbl)

        tbl.column('fatture_forn_id',size='22', group='_', name_long='fatture_forn_id'
                    ).relation('fatture_forn.id', relation_name='paym_fat_forn', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('importo', dtype='N', size='10,2', name_short='!![en]Amount',format='#,###.00')
        tbl.column('note', name_short='!![en]Note')
        tbl.aliasColumn('impfatforn','@fatture_forn_id.importo')
        tbl.formulaColumn('paymdet',"to_char($data, :df) || ': € ' || $importo || ' ' || $note", dtype='T',var_df='DD/MM/YYYY')
        tbl.formulaColumn('anno_doc',"date_part('year', $data)", dtype='D')
      

