from PySide6.QtWidgets import QMainWindow, QMessageBox

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from GUI.vtn_principal import Ui_vtn_principal
from dominio.servicio_bancario import ServicioBancario


class PersonaServicio(QMainWindow):

    def __init__(self):
        super(PersonaServicio, self).__init__()
        self.ui = Ui_vtn_principal()
        self.ui.setupUi(self)

        # 1. Titular: Solo letras (incluye mayúsculas, minúsculas, espacios, tildes y la 'ñ')
        regex_titular = QRegularExpression(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$")
        validador_titular = QRegularExpressionValidator(regex_titular)
        self.ui.txt_titular.setValidator(validador_titular)

        # 2. Código: Solo números decimales (ej: 123 o 123.45)
        # Permite números del 0-9 y opcionalmente un punto seguido de más números.
        regex_codigo = QRegularExpression(r"^[0-9]+(\.[0-9]+)?$")
        validador_codigo = QRegularExpressionValidator(regex_codigo)
        self.ui.txt_codigo.setValidator(validador_codigo)

        # 3. Año de apertura: Solo enteros, máximo 4 dígitos
        regex_anio = QRegularExpression(r"^\d{1,4}$")
        validador_anio = QRegularExpressionValidator(regex_anio)
        self.ui.txt_anioapertura.setValidator(validador_anio)

        # Como medida extra de seguridad y UX, bloqueamos la longitud del QLineEdit
        self.ui.txt_anioapertura.setMaxLength(4)

        self.ui.btn_guardar.clicked.connect(self.guardar)
        self.ui.btn_limpiar.clicked.connect(self.limpiar)

    def guardar(self):
        print("Se hizo clic en el boton guardar")
        # Capturar datos
        titular = self.ui.txt_titular.text()
        codigo = self.ui.txt_codigo.text()
        anioapertura = self.ui.txt_anioapertura.text()
        # Validar los campos obligatorios
        if titular == '' or codigo == '' or anioapertura == '':
            print("Completar todos los datos")
            QMessageBox.information(self, "Advertencia", "Completar todos los datos")
        else:
            # Procesar datos
            print("Guardando persona...")
            persona = ServicioBancario(titular=titular, codigo=codigo, anio_apertura=anioapertura)
            print(persona)
            archivo= None
            # print(f'titular: {titular}')
            # print(f'codigo: {codigo}')
            # print(f'anioapertura: {anioapertura}')
            try:
                with open('usuario.txt', 'a') as archivo:
                    archivo.write(str(persona))
                    archivo.write('***********************\n')
            except Exception as e:
                print(e)
            finally:
                archivo.close()

        # Limpiar formulario
        self.limpiar()



    def limpiar(self):
        print("Se hizo clic en el boton limpiar")
        self.ui.txt_titular.setText('')
        self.ui.txt_codigo.setText('')
        self.ui.txt_anioapertura.setText('')