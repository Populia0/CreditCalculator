import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from CREDIT1 import Ui_MainWindow
from decimal import Decimal, ROUND_HALF_UP


class Calculator(QtWidgets.QMainWindow):

    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.calc.clicked.connect(self.calculate)        # При нажатии на кнопку выполняется функция calculate
        self.ui.choose_sum.textChanged.connect(
            self.text_sum)      # Изменение текста в поле ввода суммы кредита связано с функцией text_sum
        self.ui.choose_pct.textChanged.connect(
            self.text_pct)      # Изменение текста в поле ввода процентной ставки связано с функцией text_prc

    def init(self):
        self.setWindowTitle("Кредитный калькулятор")  # Добавление заголовка приложения
        self.setWindowIcon(QIcon("calculator_icon-icons.com_54044.ico"))  # Добавление иконки приложения

    def calculate(self):
        # Создание новых вкладок с графиком платежей
        table = QtWidgets.QTableWidget()
        layout = QtWidgets.QVBoxLayout()
        table.setLayout(layout)
        # Оформление таблицы
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(12)
        table.setFont(font)
        table.setColumnCount(5)             # Добавление колонок в таблицу
        # Называем колонки
        item = QtWidgets.QTableWidgetItem()
        item.setText("Дата")
        table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Сумма")
        table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Основной \n долг")
        table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Проценты")
        table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Остаток \n основного \n долга")
        table.setHorizontalHeaderItem(4, item)
        # Изменение ширины колонок
        table.setColumnWidth(0, 160)
        table.setColumnWidth(1, 160)
        table.setColumnWidth(2, 160)
        table.setColumnWidth(3, 160)
        table.setColumnWidth(4, 160)
        # Называем новые вкладки
        index = self.ui.tabWidget.count()   # Получаем количество вкладок для названия новых вкладок с учетом их порядка
        self.ui.tabWidget.addTab(table, "График " + str(index))

        self.ui.output.setIndent(15)  # Добавить отступ перед текстом
        # Проводим рассчеты
        sum = int(self.ui.choose_sum.text())  # Переменная, принимающая значение суммы кредита
        if self.ui.pct_year.currentText() == "% в мес":    # Если выбрана процентная ставка в месяц
            pct = float(self.ui.choose_pct.text()) / 100   # Значение процентной ставки
        else:
            pct = float(self.ui.choose_pct.text()) / 1200  # Иначе перевести проценты в год в проценты в месяц
        if self.ui.month.currentText() == "месяцев":       # Если срок кредита указан в месяцах
            period = self.ui.choose_time.value()           # Количество месяцев
        else:
            period = self.ui.choose_time.value() * 12      # Иначе перевести количество лет в количество месяцев
        table.setRowCount(period)                          # Количество строк в таблице равно сроку кредита в месяцах
        if self.ui.choose_type.currentText() == "Аннуитетные":      # Вычисление аннуитетных платежей
            pay = sum * (pct + pct / ((1 + pct) ** period - 1))     # Рассчет ежемесячного платежа
            # Здесь и далее следующие две строки округляют переменную до двух знаков после точки
            pay = Decimal(str(pay))                                
            pay = str(pay.quantize(Decimal("1.00"), ROUND_HALF_UP)) 
            overpay = float(pay) * period - sum                     # Переплата по процентам
            overpay = Decimal(str(overpay))                         
            overpay = str(overpay.quantize(Decimal("1.00"), ROUND_HALF_UP))
            all = sum + float(overpay)                              # Общая сумма
            all = Decimal(str(all))
            all = str(all.quantize(Decimal("1.00"), ROUND_HALF_UP))
            # Вывод результата с разделением на строки
            self.ui.output.setText("Ежемесячный платеж: \n" + pay + "\nПереплата: \n" + overpay + "\nОбщая сумма: \n" + all)
            # Заполняем график по аннуитетному кредиту
            row = 0                 # Номер строчки
            ost = sum               # Остаток основного долга
            for i in range(1, period + 1):
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(pay))      # Заполненение колонки с суммой платежа
                proc = ost * pct            # Процентная часть платежа
                osn = float(pay) - proc     # Основная часть платежа
                ost = Decimal(str(ost))
                ost = str(ost.quantize(Decimal("1.00"), ROUND_HALF_UP))
                table.setItem(row, 4, QtWidgets.QTableWidgetItem(ost))  # Заполненение колонки остаток основного долга
                ost = float(ost) - osn                                  # Остаток основного долга
                proc = Decimal(str(proc))                                           
                proc = str(proc.quantize(Decimal("1.00"), ROUND_HALF_UP))
                table.setItem(row, 3, QtWidgets.QTableWidgetItem(proc))     # Заполненение колонки проценты
                osn = Decimal(str(osn))                                   
                osn = str(osn.quantize(Decimal("1.00"), ROUND_HALF_UP))
                table.setItem(row, 2, QtWidgets.QTableWidgetItem(osn))      # Заполненение колонки основной долг
                date = self.ui.choose_date.date().addMonths(row)        # Увеличиваем номер месяца на 1 в каждой строчке
                date = date.toString("dd.MM.yyyy")                      # Дата в тип string
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(date))     # Заполненение колонки с датой
                row += 1
        else:                                       # Вычисление дифференцированных платежей
            pay1 = sum / period + sum * pct                                     # Первый платеж
            pay1 = Decimal(str(pay1))                                           
            pay1 = str(pay1.quantize(Decimal("1.00"), ROUND_HALF_UP))
            pay2 = sum / period + sum * pct / period                            # Последний платеж
            pay2 = Decimal(str(pay2))
            pay2 = str(pay2.quantize(Decimal("1.00"), ROUND_HALF_UP))
            osn = sum / period                                                  # Основная часть платежа
            osn = Decimal(str(osn))  
            osn = str(osn.quantize(Decimal("1.00"), ROUND_HALF_UP))
            ost = sum                                                           # Остаток основного долга
            s = 0                                                               # Сумма всех платежей
            row = 0
            for i in range(1, period + 1):
                proc = float(ost) * pct
                pay = float(osn) + float(proc)
                s += float(pay)
                pay = Decimal(str(pay))  
                pay = str(pay.quantize(Decimal("1.00"), ROUND_HALF_UP))
                proc = Decimal(str(proc))  
                proc = str(proc.quantize(Decimal("1.00"), ROUND_HALF_UP))
                ost = Decimal(str(ost))  
                ost = str(ost.quantize(Decimal("1.00"), ROUND_HALF_UP))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(pay))
                table.setItem(row, 2, QtWidgets.QTableWidgetItem(osn))
                table.setItem(row, 3, QtWidgets.QTableWidgetItem(proc))
                table.setItem(row, 4, QtWidgets.QTableWidgetItem(ost))
                ost = float(ost) - float(osn)
                date = self.ui.choose_date.date().addMonths(row)
                date = date.toString("dd.MM.yyyy")
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(date))
                row += 1

            overpay = s - sum                                                   # Переплата
            overpay = Decimal(str(overpay))                                     
            overpay = str(overpay.quantize(Decimal("1.00"), ROUND_HALF_UP))
            all = sum + float(overpay)                                          # Общая цена кредита
            all = Decimal(str(all))                                             
            all = str(all.quantize(Decimal("1.00"), ROUND_HALF_UP))
            self.ui.output.setText("Ежемесячный платеж: \n" + pay1 + "\n" + pay2 + "\nПереплата: \n" + overpay + "\nОбщая сумма: \n" + all)

    # Редактирование значений поступающих в поле ввода суммы кредита
    def text_sum(self):
        str = self.ui.choose_sum.text()
        str = str[0:-1]  # Удаление одного введенного символа
        if not self.ui.choose_sum.text().isdigit():  # Если символ не цифра удалить символ
            self.ui.choose_sum.setText(str)
        if self.ui.choose_sum.text() == "0":
            self.ui.choose_sum.setText(str)

    # Редактирование значений поступающих в поле ввода процентной ставки
    def text_pct(self):
        str = self.ui.choose_pct.text()
        if "," in str:  # Замена запятой на точку
            str = str[0:-1]
            str += "."
            self.ui.choose_pct.setText(str)
        str = str[0:-1]  # Удаление одного введенного символа
        if self.ui.choose_pct.text().isdigit() is False and "." not in self.ui.choose_pct.text():  # Если символ не цифра и не точка удалить символ
            self.ui.choose_pct.setText(str)
        if self.ui.choose_pct.text() == "00":
            self.ui.choose_pct.setText(str)
        if self.ui.choose_pct.text().count(".") > 1:  # Можно ввести только одну точку в поле
            self.ui.choose_pct.setText(str)
        if self.ui.choose_pct.text() == ".":  # Если введена только точка не писать ничего
            self.ui.choose_pct.setText(str)

    def close_tab(self, ind):
        if ind > 0:
            self.ui.tabWidget.removeTab(ind)




app = QtWidgets.QApplication([])
application = Calculator()
application.show()

sys.exit(app.exec())
