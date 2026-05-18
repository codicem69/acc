# -*- coding: utf-8 -*-
from pathlib import Path
import time
from gnr.core.gnrdecorator import public_method
class GnrCustomWebPage(object):
    py_requires = 'frameindex'


    @property
    def index_url(self):
        return None

    def index_dashboard(self, root):
        port_id = self.db.currentEnv.get('current_port')
        agency_id = self.db.currentEnv.get('current_agency_id')
        agency_name = ''
        if agency_id:
            agency_name = self.db.table('agz.agency').readColumns(
                where='$id=:agency_id',
                agency_id=agency_id,
                columns='$agency_name'
            ) or ''

        port_name = ''
        if port_id:
            port_name = self.db.table('unlocode.place').readColumns(
                where='$id=:port_id',
                port_id=port_id,
                columns='$descrizione'
            ) or ''

        wrapper = root.div(width='100%', height='100%', 
                           text_align='center', background='white',
                           padding_top='30px')
        wrapper.img(src='/_pkg/acc/resources/html_pages/images/logo_acc.png', 
                    style='width:30%;margin-top:30px;')
        wrapper.div(agency_name + ' - ' + port_name,
                    font_size='70px',font_weight='bold', color='#1d3355ff',#color='#384D63',
                    margin_top='20px', margin_bottom='30px')
        wrapper.img(src='/_rsrc/common/html_pages/images/splash_logo.png',
                    style='width:20%;margin-top:30px;')


















    #def main(self, root, **kwargs):
    #    port_id = self.db.currentEnv.get('current_port')
    #
    #    if port_id:
    #        # Utente già loggato con porto in env → vai direttamente a home
    #        root.script("genro.gotoURL('%s');" % self.site.url(
    #            '%s/home' % self.package.name
    #        ))
    #    else:
    #        # Nessun porto in env → mostra la plainIndex standard
    #        self.plainIndex(root, **kwargs)

    #def main(self, root, **kwargs):
    #
    #    port_id = self.db.currentEnv.get('current_port')
    #
    #    port = self.db.table('unlocode.place').readColumns(
    #        where='$id=:port_id',
    #        port_id=port_id,
    #        columns='$descrizione'
    #    )
    #
    #    # layout "splash dentro Genropy"
    #    # QUESTO è fondamentale: contentPane del frame
    #    pane = root.contentPane()
    #
    #    pane.div(
    #        f"Benvenuto nel porto di {port}",
    #        style="""
    #            font-size:40px;
    #            text-align:center;
    #            margin-top:120px;
    #        """
    #    )


    #@property
    #def index_url(self):
    #    port_id=(self.db.currentEnv.get('current_port'))
    #    port = self.db.table('unlocode.place').readColumns(where='$id=:port_id',
    #                        port_id=port_id, columns='$descrizione')
    #
    #     # leggo template html
    #    template_path = (
    #        Path(__file__).parent.parent /
    #        'resources' /
    #        'html_pages' /
    #        'splashscreen.html'
    #    )
    #
    #    print(template_path)
    #
    #    html = template_path.read_text(encoding='utf-8')
    #
    #    html = html.replace('{{PORT}}', port or '')
    #
    #    runtime_path = (
    #        Path(__file__).parent.parent /
    #        'resources' /
    #        'html_pages' /
    #        'runtime_splashscreen.html'
    #    )
    #
    #    runtime_path.write_text(html, encoding='utf-8')
    #
    #    return f'html_pages/runtime_splashscreen.html?ts={int(time.time())}'
