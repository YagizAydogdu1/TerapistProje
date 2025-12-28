import sys
from PyQt5.QtWidgets import QApplication
from ui import TerapistSistemi

def main():
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    pencere = TerapistSistemi()
    pencere.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()