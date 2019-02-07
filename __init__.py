import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_lexer_inspector.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

HOTSPOT_TAG=643

class Command:
    
    def __init__(self):
        self.shown=False
        ed.hotspots(HOTSPOT_ADD,
                         tag=HOTSPOT_TAG,
                         tag_str='{x:1,y:1}',
                         pos=(1,1,7,1)
                         )
        global option_int
        global option_bool
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):
        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)
        
    def on_open(self,ed_self):
        ed_self.hotspots(HOTSPOT_DELETE_ALL)
        for i in ed_self.get_token(TOKEN_LIST) :
            ed_self.hotspots(HOTSPOT_ADD,
                         tag=HOTSPOT_TAG,
                         tag_str=i['str'],
                         pos=(i['x1'],i['y1'],i['x2'],i['y2']))   
    
    def on_change_slow(self, ed_self):
        ed_self.hotspots(HOTSPOT_DELETE_ALL)
        for i in ed_self.get_token(TOKEN_LIST) :
            ed_self.hotspots(HOTSPOT_ADD,
                         tag=HOTSPOT_TAG,
                         tag_str=i['str'],
                         pos=(i['x1'],i['y1'],i['x2'],i['y2']))
        
    def on_hotspot(self, ed_self, entered, hotspot_index):
        hotspot=ed_self.hotspots(HOTSPOT_GET_LIST)[hotspot_index]
        token=ed.get_token(TOKEN_LIST)[hotspot_index]
        if self.shown:
            dlg_proc(self.h_tooltip,DLG_HIDE)
        self.shown=True
        self.h_tooltip = dlg_proc(0, DLG_CREATE)
        dlg_proc(self.h_tooltip,DLG_PROP_SET,prop={
          'x':hotspot['pos'][0],
          'y':hotspot['pos'][1],
          'h':100,
        })
        label = dlg_proc(self.h_tooltip,DLG_CTL_ADD,'label')
        strres=''
        for i in token:
            strres+=str(i)+': '+str(token[i])+'\n'
        dlg_proc(self.h_tooltip, DLG_CTL_PROP_SET, index=label, prop={
          'x':3,
          'y':3, 
          'cap':strres
        }) 
        dlg_proc(self.h_tooltip,DLG_DOCK,index=0,prop='B')
        dlg_proc(self.h_tooltip,DLG_SHOW_NONMODAL)
        pass
