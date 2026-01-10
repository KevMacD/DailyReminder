import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Screen PyQt Window")
        
        # Set the window to full screen mode using setWindowState
        # self.setWindowState(Qt.WindowStates.WindowFullScreen)
        
        # Alternatively, you can use the showFullScreen() method
        self.showFullScreen() 
        
        # Add a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add a label to show it's working
        label = QLabel("This window is full screen. Press 'Esc' to exit.", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
    def keyPressEvent(self, event):
        """Handle key press events to allow exiting full screen with Escape."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            # Or use self.showNormal() to exit full screen mode without closing the window

def main():
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show() # Note: self.showFullScreen() has already been called in the __init__
    sys.exit(app.exec())

if __name__ == '__main__':
    main()