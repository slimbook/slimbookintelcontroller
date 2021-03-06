from configparser import ConfigParser

import gi
import os
import re
import utils

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

USER_NAME = utils.get_user()
HOMEDIR = os.path.expanduser('~')

CONFIG_FILE = '{}/.config/slimbookintelcontroller/slimbookintelcontroller.conf'.format(
    HOMEDIR)
PROCESSORS_FILE = '{}/processors/available'.format(CURRENT_PATH)

config = ConfigParser()
config.read(CONFIG_FILE)

_ = utils.load_translation('slimbookintelcontroller')

CPU = utils.get_cpu_info('name')

patron = re.compile('(\w\d)[-]([0-9]{4,5})(\w*)[ ]')
version = patron.search(CPU).group(1)
number = patron.search(CPU).group(2)
line_suffix = patron.search(CPU).group(3)

MODEL_CPU = version+'-'+number+line_suffix

class Add_processor_dialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog",transient_for=parent)
        self.set_name('dialog')
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(500, 100)

        label = Gtk.Label(label=_(
            "Your processor is not supported yet. Do you want to add {} to the list?\n"+
            "If this is the case, you should go to the Intel page and get information about your TDP values.").format(MODEL_CPU))
        label.set_line_wrap(True)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class Settings_dialog(Gtk.Dialog):
    FIELDS = {
                'H': '35@40/40@45/45@54/35/45/54/',
                'U': '10@12/12@18/15@28/10/15/25/'
            }


    def __init__(self, parent):
        
        if config.has_option('CONFIGURATION', 'cpu-parameters') and config['CONFIGURATION']['cpu-parameters']!= '':
            values = config['CONFIGURATION']['cpu-parameters'].split('/')
            print('Loads:  '+str(values)+' from file.')
        else:
            try:
                values = self.FIELDS.get(line_suffix).split('/')
            except:
                values = ['0@0', '0@0', '0@0', '0', '0', '0']
            
            self.val = '{}/{}/{}/{}/{}/{}/?'.format(values[0],values[1],values[2],values[3],values[4],values[5])
            print('Creates loads:  '+self.val+'.')

        self.lowmode = (values[0].split('@'))
        self.midmode = (values[1].split('@'))
        self.highmode = (values[2].split('@'))


        self.low_default = float(values[3])
        self.mid_default = float(values[4])
        self.high_default = float(values[5])

        super().__init__(title="Slimbook Intel Controller Settings", transient_for=parent)
        self.set_name('dialog')
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        # WINDOW
        self.set_name('settings')

        center = Gtk.Align.CENTER
        left = Gtk.Align.START
        right = Gtk.Align.END

        win_grid = Gtk.Grid(column_homogeneous=False,
                            row_homogeneous=True,
                            column_spacing=10,
                            row_spacing=10)

        grid = Gtk.Grid(column_homogeneous=False,
                        row_homogeneous=True,
                        column_spacing=20,
                        row_spacing=10)

        self.get_content_area().add(win_grid)

        # Mantained TDP Column

        label1 = Gtk.Label(label=_('Mantained TDP'))

        self.entry1 = _create_gui_element(
            float(self.lowmode[0]), self.low_default - self.low_default/2, self.high_default + 10)

        self.entry2 = _create_gui_element(
            float(self.midmode[0]), self.low_default - self.low_default/2, self.high_default + 10)

        self.entry3 = _create_gui_element(
            float(self.highmode[0]), self.low_default - self.low_default/2, self.high_default + 10)

        grid.attach(self.entry1, 1, 1, 1, 1)
        grid.attach(self.entry2, 1, 2, 1, 1)
        grid.attach(self.entry3, 1, 3, 1, 1)
        grid.attach(label1, 1, 0, 1, 1)

        # High Power TDP Column

        label2 = Gtk.Label(_('High Power TDP'))

        self.entry4 = _create_gui_element(
            float(self.lowmode[1]), self.low_default - self.low_default/2, self.high_default + 10)

        self.entry5 = _create_gui_element(
            float(self.midmode[1]), self.low_default - self.low_default/2, self.high_default + 10)

        self.entry6 = _create_gui_element(
            float(self.highmode[1]), self.low_default - self.low_default/2, self.high_default + 10)

        grid.attach(self.entry4, 2, 1, 1, 1)
        grid.attach(self.entry5, 2, 2, 1, 1)
        grid.attach(self.entry6, 2, 3, 1, 1)
        grid.attach(label2, 2, 0, 1, 1)

        # Modes Column
        
        low_lbl = Gtk.Label(label=_('Low'), halign=left)

        mid_lbl = Gtk.Label(label=_('Medium'), halign=left)

        high_lbl = Gtk.Label(label=_('High'), halign=left)

        grid.attach(low_lbl, 0, 1, 1, 1)
        grid.attach(mid_lbl, 0, 2, 1, 1)
        grid.attach(high_lbl, 0, 3, 1, 1)

        separator = Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL)
        win_grid.attach(separator, 0, 4, 5, 1)

        # Recommended Values

        recommended_lbl = Gtk.Label(
            label=_('Recommended values:'), halign=left)

        win_grid.attach(recommended_lbl, 0, 5, 1, 1)

        low_lbl = Gtk.Label(
            label=_('Low: {} watts'.format(self.low_default)), halign=left)

        mid_lbl = Gtk.Label(
            label=_('Medium: {} watts'.format(self.mid_default)), halign=left)

        high_lbl = Gtk.Label(
            label=_('High: {} watts.'.format(self.high_default)), halign=left)

        values_box = Gtk.VBox()
        values_box.add(low_lbl)
        values_box.add(mid_lbl)
        values_box.add(high_lbl)

        win_grid.attach(values_box, 0, 6, 2, 2)

        win_grid.attach(grid, 0, 0, 5, 4)

        self.show_all()


class Dialog(Gtk.Window):
    
    print(MODEL_CPU)
    # print(config.items('PROCESSORS'))
    def __init__(self):
        Gtk.Window.__init__(self, title="Slimbook Intel Controller")
        if not config.has_option('PROCESSORS',MODEL_CPU):
            
            dialog = Add_processor_dialog(self)
            response = dialog.run()

            if not response == Gtk.ResponseType.OK:     
                print("The Cancel button was clicked")
                exit()
            dialog.close()
            dialog.destroy()

        dialog = Settings_dialog(self)
        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            self.accept(dialog)
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        
        dialog.close()
        dialog.destroy()

    def accept(self, dialog):
        new_values = '{}@{}/{}@{}/{}@{}/  {}/{}/{}/'.format(dialog.entry1.get_text(),
                                           dialog.entry4.get_text(),
                                           dialog.entry2.get_text(),
                                           dialog.entry5.get_text(),
                                           dialog.entry3.get_text(),
                                           dialog.entry6.get_text(),
                                           dialog.low_default, dialog.mid_default, dialog.high_default)

        if config.has_option('PROCESSORS',MODEL_CPU):
            print('Processor values modified.')

            config.set('CONFIGURATION','cpu-parameters', new_values)

        else: 
            print('Processor added')
            config.set('PROCESSORS', MODEL_CPU, dialog.val)
            config.set('CONFIGURATION','cpu-parameters', new_values)
            print(config['PROCESSORS'][MODEL_CPU])

        with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

def _create_gui_element(value, low, max):

    spin_button = Gtk.SpinButton()
    spin_button.set_adjustment(Gtk.Adjustment(
        value=value,
        lower=low,
        upper=max,
        step_incr=1,
        page_incr=10,
    ))

    spin_button.set_numeric(True)

    return spin_button


style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH+'/css/style.css')

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
if __name__ == "__main__":
    Dialog()
    Gtk.main()
