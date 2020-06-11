import database as db
import remi.gui as gui
from remi import start, App


data = db.get()
dates, names = [], []
for line in data:
    if line[0] not in names:
        names.append(line[0])
    if line[2] not in dates:
        dates.append(line[2])
filt = {}


class Dashboard(App):
    def __init__(self, *args):
        super(Dashboard, self).__init__(*args)

    def main(self):
        menuBar = gui.MenuBar(width='100%', height='50px')
        menu = gui.Menu(width='100%', height='50px')
        diag = gui.MenuItem('Filters', width=100, height=50)
        diag.onclick.do(self.filtersMenu)
        menu.append(diag)
        menuBar.append(menu)
        return menuBar

    def checkbox(self, chb, val):
        print(chb._label.get_text(), val)
        filt[chb._label.get_text()] = val

    def filtersMenu(self, widget):
        self.dialog = gui.GenericDialog(title='Filters Menu', message='Click Ok To Confirm Selection',
                                        width='300px')
        self.main_cont = gui.HBox(width=300)
        dates_cont = gui.VBox(width='50%')
        for date in dates[:-1]:
            chb = gui.CheckBoxLabel(date, False)
            chb.onchange.do(self.checkbox)
            dates_cont.append(chb)
        chb = gui.CheckBoxLabel(dates[-1], False)
        chb.onchange.do(self.checkbox)
        dates_cont.append(chb)
        self.main_cont.append(dates_cont)
        names_cont = gui.VBox(width='50%')
        for name in names:
            chb = gui.CheckBoxLabel(name, False)
            chb.onchange.do(self.checkbox)
            names_cont.append(chb)
        self.main_cont.append(names_cont)
        names_cont.style['align-items'] = 'flex-start'
        dates_cont.style['align-items'] = 'flex-start'
        names_cont.style['justify-content'] = 'flex-start'
        dates_cont.style['justify-content'] = 'flex-start'
        self.dialog.add_field('main_cont', self.main_cont)
        self.dialog.confirm_dialog.do(self.diag_conf)
        self.dialog.show(self)

    def diag_conf(self, widget):
        pass  # Plotting with matplotlib in process



start(Dashboard, debug=True, address='0.0.0.0', port=8081)