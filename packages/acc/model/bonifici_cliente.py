class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bonifici_cliente', pkey='id', name_long='!![en]Transfer', 
                        name_plural='!![en]Transfers',caption_field='causale')
        self.sysFields(tbl)
        
        tbl.column('data', dtype='D', name_short='!![en]Date')
        tbl.column('cliente_id',size='22', name_long='!![en]Customer'
                    ).relation('cliente.id', relation_name='bonifico_cliente', mode='foreignkey', onDelete='cascade')            
        tbl.column('causale', name_short='!![en]Reason')
        tbl.column('importo', dtype='money', name_short='!![en]Amount')