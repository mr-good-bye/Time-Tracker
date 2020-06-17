import database as db
import remi.gui as gui
from remi import start, App
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from matplotlib.figure import Figure


data = db.get()
dates, names = [], []
filt = {}
for line in data:
    if line[0] not in names:
        names.append(line[0])
        filt[line[0]] = True
    if line[2] not in dates:
        dates.append(line[2])
        filt[line[2]] = False
filt[dates[-1]] = True
print(filt)


class Dashboard(App):
    def __init__(self, *args):
        super(Dashboard, self).__init__(*args)

    def main(self):
        self.fig = ''
        self.ax = ''
        self.plt = ''
        self.datarom = ''
        menuBar = gui.MenuBar(width='100%', height='50px')
        menu = gui.Menu(width='100%', height='50px')
        diag = gui.MenuItem('Filters', width=100, height=50)
        diag.onclick.do(self.filtersMenu)
        menu.append(diag)
        menuBar.style['align-items'] = 'flex-start'
        menuBar.style['align-items'] = 'flex-start'
        menu.style['justify-content'] = 'flex-start'
        menu.style['justify-content'] = 'flex-start'

        #menuBar.style['align-items'] = 'center'
        #menu.style['align-items'] = 'center'
        menuBar.append(menu)
        self.menu = menu
        self.hbox = gui.VBox(width=600)
        self.hbox.style['margin'] = 'auto'
        #self.hbox.style['align-items'] = 'center'
        self.hbox.append(menuBar)
        fig, ax = plt.subplots()
        lbls, sizes = [], []
        for i in data:
            if filt[i[0]] and filt[i[2]]:
                lbls.append(i[0] + ':' + i[2])
                sizes.append(i[1])
        ax.pie(sizes, labels=lbls)
        ax.axis('equal')
        self.fig = fig
        self.ax = ax
        self.plt = plt
        self.canv = FigureCanvasAgg(self.fig)
        plt.savefig('temp.png')
        self.img = gui.Image(self.draw())
        self.hboxIMG = gui.VBox(width=600)
        self.hboxIMG.append(self.img)
        self.hbox.append(self.hboxIMG)
        return self.hbox

    def checkbox(self, chb, val):
        filt[chb._label.get_text()] = val

    def filtersMenu(self, widget):
        self.dialog = gui.GenericDialog(title='Filters Menu', message='Click Ok To Confirm Selection',
                                        width='300px')
        self.main_cont = gui.HBox(width=300)
        dates_cont = gui.VBox(width='50%')
        for date in dates:
            chb = gui.CheckBoxLabel(date, filt[date])
            chb.onchange.do(self.checkbox)
            dates_cont.append(chb)
        chb.onchange.do(self.checkbox)
        dates_cont.append(chb)
        self.main_cont.append(dates_cont)
        names_cont = gui.VBox(width='50%')
        for name in names:
            chb = gui.CheckBoxLabel(name, filt[name])
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
        fig,ax = plt.subplots()
        lbls, sizes = [], []
        for i in data:
            if filt[i[0]] and filt[i[2]]:
                lbls.append(i[0]+':'+i[2])
                sizes.append(i[1])
        ax.pie(sizes, labels=lbls)
        ax.axis('equal')
        self.fig = fig
        self.ax = ax
        self.plt = plt
        self.canv = FigureCanvasAgg(self.fig)
        plt.savefig('temp.png')
        self.img = gui.Image(gui.load_resource('temp.png'))
        self.hboxIMG.empty()
        self.hboxIMG.append(self.img)

    def draw(self):
        fig, ax = plt.subplots()
        lbls, sizes = [], []
        for i in data:
            if filt[i[0]] and filt[i[2]]:
                lbls.append(i[0] + ':' + i[2])
                sizes.append(i[1])
        ax.pie(sizes, labels=lbls)
        ax.axis('equal')
        self.fig = fig
        self.ax = ax
        self.plt = plt
        self.canv = FigureCanvasAgg(self.fig)
        plt.savefig('temp.png')
        return gui.load_resource('temp.png')



start(Dashboard, debug=False, address='0.0.0.0', port=8081)