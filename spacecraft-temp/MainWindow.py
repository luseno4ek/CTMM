from pathlib import Path
from LoadingWindow import *
from PyQt6.QtWidgets import (
    QMainWindow, 
    QLabel, 
    QLineEdit, 
    QGridLayout, 
    QWidget, 
    QPushButton, 
    QFileDialog,
    QCheckBox
)
from PyQt6.QtCore import QThread
from Worker import *
from HeatBalanceEquation import *
from scipy.integrate import solve_ivp
from MplCanvas import *


class MainWindow(QMainWindow):
    def __init__(self):
        # ------ FINITE ELEMENT MODEL LOGIC ------
        self.fe_model = None

        # ------ USER INTERFACE LOGIC ------
        super().__init__()
        self.setWindowTitle("Spacecraft Temperature Distribution")
        # ------ WIDGETS ------
        # Path to model.obj input widget
        model_file_path_input_label = QLabel("Model file: ")
        self.model_file_path_input = QLineEdit()
        self.model_file_path_input.resize(250,20)
        model_file_browse_button = QPushButton("Browse")
        model_file_browse_button.clicked.connect(self.open_file_dialog_model)
        self.model_ready_input_label = QLabel("Model is not loaded yet.")
        self.model_ready_input_label.setStyleSheet('color: red')
        # Path to params.json input widget
        param_file_path_input_label = QLabel("Param file: ")
        self.param_file_path_input = QLineEdit()
        self.param_file_path_input.resize(250, 20)
        param_file_browse_button = QPushButton("Browse")
        param_file_browse_button.clicked.connect(self.open_file_dialog_params)
        self.param_ready_input_label = QLabel("Params are not loaded yet.")
        self.param_ready_input_label.setStyleSheet('color: red')
        # Time
        time_input_label = QLabel("Calculation time: ")
        self.time_input = QLineEdit()
        self.time_input.resize(250, 20)
        self.infinite_time_checkbox = QCheckBox("Infinite time")
        self.infinite_time_checkbox.toggled.connect(self.set_infinite_time)
        # Solution
        start_calculation_button = QPushButton("Start calculations")
        start_calculation_button.clicked.connect(self.start_calculations)
        self.solution_graphics = MplCanvas(self, width=5, height=4, dpi=100)

        # ------ LAYOUT ------
        layout = QGridLayout()
        # Model
        layout.addWidget(model_file_path_input_label, 0, 0)
        layout.addWidget(self.model_file_path_input, 0, 1)
        layout.addWidget(model_file_browse_button, 0, 2)
        layout.addWidget(self.model_ready_input_label, 1, 0)
        # Params
        layout.addWidget(param_file_path_input_label, 2, 0)
        layout.addWidget(self.param_file_path_input, 2, 1)
        layout.addWidget(param_file_browse_button, 2, 2)
        layout.addWidget(self.param_ready_input_label, 3, 0)
        # Time
        layout.addWidget(time_input_label, 4, 0)
        layout.addWidget(self.time_input, 4, 1)
        layout.addWidget(self.infinite_time_checkbox, 4, 2)
        # Solution
        layout.addWidget(start_calculation_button, 5, 0, 1, 3)
        layout.addWidget(self.solution_graphics, 6, 0, 1, 3)

        # ------ CONTAINER ------
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


    def open_file_dialog_model(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a obj File", 
            filter="*.obj"
        )
        if filename:
            self.model_ready_input_label.setText("Model is not loaded yet.")
            self.model_ready_input_label.setStyleSheet('color: red')
            path = str(Path(filename))
            self.model_file_path_input.setText(path)
            # clean param path in order to reselect params if model is changed 
            self.param_file_path_input.setText('')
            # parse model
            self.parse_model(path)


    def open_file_dialog_params(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a JSON File", 
            filter="*.json"
        )
        if filename:
            self.param_ready_input_label.setText("Params are not loaded yet.")
            self.param_ready_input_label.setStyleSheet('color: red')
            path = str(Path(filename))
            self.param_file_path_input.setText(path)
            # read parameters from json-file
            if self.fe_model is not None:
                self.fe_model.read_params_from_file(path)
                self.param_ready_input_label.setText("Params are successfully read and stored into model!")
                self.param_ready_input_label.setStyleSheet('color: green')


    def parse_model(self, path):
        # Show loading window
        self.loading_window = LoadingWindow()
        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = Worker(self.fe_model, path)
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()
        # Final resets
        self.thread.finished.connect(self.model_loaded)


    def model_loaded(self):
        self.fe_model = self.worker.fe_model
        self.loading_window.stop_animation()
        self.model_ready_input_label.setText("Model is successfully loaded and parsed!")
        self.model_ready_input_label.setStyleSheet('color: green')


    def set_infinite_time(self):
        check_box = self.infinite_time_checkbox
        if (check_box.isChecked()):
            self.time_input.setReadOnly(True)
            self.time_input.setText("Infinite")
        else:
            self.time_input.setReadOnly(False)
            self.time_input.setText('')

    
    def start_calculations(self):
        t_max = self.time_input.text()
        if t_max == 'Infinite':
            pass
        else:
            t_max = int(t_max)
            eq = HeatBalanceEquation(self.fe_model).equation
            sol = solve_ivp(fun=eq, 
                    t_span=[0, t_max], 
                    y0=self.fe_model.t0, 
                    args=(50,),
                    dense_output=True)
            t = np.linspace(0, t_max, 100)
            y = sol.sol(t).T
            print("Solution = ", y[0])
            self.solution_graphics.axes.cla()
            self.solution_graphics.axes.plot(t, y)
            self.solution_graphics.axes.set_xlabel('t')
            self.solution_graphics.axes.legend(['T1', 'T2', 'T3', 'T4', 'T5'], shadow=True)
            self.solution_graphics.axes.set_title('Heat Equation')
            self.solution_graphics.draw()
