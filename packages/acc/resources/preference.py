# preference.py
from gnr.app.gnrapp import GnrApp
from gnr.core.gnrdecorator import public_method


class AppPref(object):

    def permission_acc(self, **kwargs):
        return 'admin'
        
    def prefpane_acc(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.privacy(tc.borderContainer(title='!!Email Privacy'))
        #self.extra(tc.borderContainer(title='!!Extra'))

    #def data(self,pane):
    #    fb = pane.formbuilder(cols=1,border_spacing='3px', margin='10px')
    #    fb.div('Press button to load/save default data')
    #    fb.button('Load data',action="""genro.mainGenroWindow.genro.publish('open_batch');
    #                                    genro.serverCall('_package.shipsteps.loadStartupData',null,function(){});
    #                                    """,_tags='_DEV_')
    #    fb.button('Save data',action="""genro.mainGenroWindow.genro.publish('open_batch');
    #                                    genro.serverCall('_package.shipsteps.createStartupData',null,function(){});
    #                                """,_tags='_DEV_')



    def privacy(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
        fb = pane.formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='100em')
        fb.simpleTextArea('^.privacy_email',lbl='Email Privacy',width='100em', height='200px',editor=True)
    
