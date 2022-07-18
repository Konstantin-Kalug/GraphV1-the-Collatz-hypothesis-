import tkinter
import matplotlib.pyplot as plt
from tkinter import Label, Entry, Button, Tk, messagebox
from PIL import ImageTk, Image
import os.path


# перевод сантиметров в дюймы
def cm_to_inch(value):
    return value / 2.54


# класс главного окна
class Window:
    def __init__(self):
        # инициализация окна
        self.window = Tk()
        self.window.title("Графики!")
        self.window.geometry('802x700')
        self.window.resizable(width=False, height=False)
        self.draw_objects()

    def draw_objects(self):
        # рисуем на окне все необходимые объекты
        # рисуем текст
        self.lbl = Label(self.window, text="Вводи число, жми кнопку - получай график его изменения по правилу"
                                           " гипотезы Коллатца!", font="Arial 14")
        self.lbl.grid(column=0, row=0)
        # рисуем поле для ввода числа
        self.txt = Entry(self.window, width=10, font="Arial 10", bd=5, justify='center')
        self.txt.grid(column=0, row=2)
        # рисуем кнопку
        self.btn = Button(self.window, text='Получить график', font='Arial 12', command=self.click_button)
        self.btn.grid(row=3, column=0)
        # рисуем поле, где будет изображен график
        self.canvas = tkinter.Canvas(self.window, height=600, width=800)
        # генерируем пустой график
        self.create_image(0)
        self.canvas.grid(row=1, column=0)

    def set_image(self, file):
        # открываем изображение и вставляем его в соответствующее поле
        self.image = Image.open(file)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

    def create_image(self, num):
        # генерируем график
        self.fig, ax = plt.subplots(1, 1, figsize=(cm_to_inch(21), cm_to_inch(15)))
        ax.set_title('График гипотезы Коллатца', fontsize=15)
        ax.set_xlabel('Шаги', fontsize=12, color='blue')
        ax.set_ylabel('Значения числа', fontsize=12, color='blue')
        ax.minorticks_on()
        ax.grid(which='major', color='k')
        ax.grid(which='minor', linestyle=':')
        if num != 0:
            x, y = self.set_x_y(num)
            if len(x) != len(y) != 0:
                ax.xlim([x[0], x[-1]])
                ax.ylim([min(y), max(y)])
            line, = plt.plot(x, y, 'o-r', label='Изменение числа')
            ax.legend()
        else:
            line, = plt.plot([0], [0])
        self.fig.savefig('saved_figure.png')
        line.remove()
        plt.close(self.fig)
        self.window.focus_force()
        self.set_image('saved_figure.png')

    def set_x_y(self, num):
        # получаем оси x и y, выполняя необходимые действия
        x = [0]
        y = [num]
        while num != 1:
            num = num / 2 if num % 2 == 0 else num * 3 + 1
            y.append(num)
            x.append(len(x))
        return x, y

    def click_button(self):
        # если кнопка была нажата - приступаем к генерации графика (только если введено целое неотрицательное число)
        try:
            if self.txt.get().isdigit():
                self.create_image(int(self.txt.get()))
            else:
                messagebox.showerror('Ошибка', 'Нужно вводить целые неотрицательные числа!')
        except (Exception) as ex:
            messagebox.showerror('Ошибка', 'Упс!')

    def run(self):
        # запуск программы и настройка протокола для выхода
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.mainloop()

    def quit(self):
        # очищаем память и выключаем все элементы
        if os.path.isfile('saved_figure.png'):
            os.remove('saved_figure.png')
        plt.close(self.fig)
        self.window.destroy()


# запуск
if __name__ == '__main__':
    win = Window()
    win.run()
