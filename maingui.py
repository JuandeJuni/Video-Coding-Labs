import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QComboBox, QWidget, QHBoxLayout, QFormLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap


class VideoEncoderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Encoder API GUI")
        self.setGeometry(100, 100, 800, 600)

        # Scroll area setup
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        self.setCentralWidget(scroll_area)

        # Central widget and layout
        self.layout = QVBoxLayout(scroll_widget)

        # File upload
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        # File path display
        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        # Operation selection
        self.operation_label = QLabel("Select Operation:")
        self.layout.addWidget(self.operation_label)
        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "Resize Image", "Convert to Black and White", "Chroma Subsampling",
            "DCT Compression", "Run-Length Encoding", "Convert to VP8",
            "Convert to VP9", "Convert to H265", "Convert to AV1", "Encoding Ladder", "Get Info", "Get Tracks"
        ])
        self.operation_combo.currentTextChanged.connect(self.update_parameter_fields)
        self.layout.addWidget(self.operation_combo)

        # Dynamic parameter fields
        self.params_layout = QFormLayout()
        self.params_widgets = {}
        self.layout.addLayout(self.params_layout)

        # Execute button
        self.execute_button = QPushButton("Execute Operation")
        self.execute_button.clicked.connect(self.execute_operation)
        self.layout.addWidget(self.execute_button)

        # Result display
        self.result_label = QLabel("Result:")
        self.layout.addWidget(self.result_label)
        self.result_image = QLabel()
        self.layout.addWidget(self.result_image)

        self.api_url = "http://127.0.0.1:8000"  # Your FastAPI server URL
        self.uploaded_file = None

        self.update_parameter_fields()  # Initialize parameter fields

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_label.setText(f"File: {file_path}")
            self.uploaded_file = file_path
            # Upload file to the server
            with open(file_path, "rb") as f:
                files = {"image": f}
                response = requests.post(f"{self.api_url}/upload-image/", files=files)
                if response.status_code == 200:
                    self.result_label.setText("File uploaded successfully.")
                else:
                    self.result_label.setText(f"Error: {response.text}")

    def update_parameter_fields(self):
        # Clear existing widgets
        for widget in self.params_widgets.values():
            widget.setParent(None)
        self.params_widgets.clear()

        operation = self.operation_combo.currentText()
        if operation == "Resize Image":
            self.add_parameter_field("width", QLineEdit(), "Width (int):")
            self.add_parameter_field("height", QLineEdit(), "Height (int):")
            self.add_parameter_field("compression", QLineEdit(), "Compression (int):")
        elif operation == "Encoding Ladder":
            self.add_parameter_field("codec", QLineEdit(), "Codec (str):")
        elif operation == "Chroma Subsampling":
            self.add_parameter_field("chroma_subsampling", QLineEdit(), "Chroma Subsampling (str):")
        elif operation == "Convert to Black and White":
            self.add_parameter_field("compression", QLineEdit(), "Compression (int):")

    def add_parameter_field(self, name, widget, label):
        self.params_layout.addRow(label, widget)
        self.params_widgets[name] = widget

    def execute_operation(self):
        operation = self.operation_combo.currentText()
        endpoint = self.get_endpoint(operation)

        if operation != "Get Info" and not self.uploaded_file:
            self.result_label.setText("Please upload a file first.")
            return

        if endpoint:
            # Collect parameters
            params_dict = {"filename": self.uploaded_file.split("/")[-1]}
            for name, widget in self.params_widgets.items():
                value = widget.text()
                if value:
                    params_dict[name] = value

            try:
                response = requests.get(f"{self.api_url}{endpoint}", params=params_dict)
                if response.status_code == 200:
                    self.result_label.setText(f"Success: {operation}")
                    if operation == "Encoding Ladder":
                        # Save and handle the zip file
                        with open("encoding_ladder.zip", "wb") as f:
                            f.write(response.content)
                        self.result_label.setText("Encoding Ladder file saved as encoding_ladder.zip.")
                    elif operation == "Get Info" or operation == "Get Tracks":
                        beautified_json = json.dumps(response.json(), indent=4)
                        self.result_label.setText(f"Info:\n{beautified_json}")
                    else:
                        if "outputs" in response.url:
                            pixmap = QPixmap(response.url)
                            self.result_image.setPixmap(pixmap.scaled(400, 400))
                else:
                    self.result_label.setText(f"Error: {response.text}")
            except Exception as e:
                self.result_label.setText(f"Error: {str(e)}")
        else:
            self.result_label.setText("Invalid operation selected.")

    def get_endpoint(self, operation):
        # Map operations to endpoints
        operations = {
            "Resize Image": "/resize-image",
            "Convert to Black and White": "/blackandwhite",
            "Chroma Subsampling": "/chroma-subsampling",
            "DCT Compression": "/dct",
            "Run-Length Encoding": "/runlength",
            "Convert to VP8": "/convert-to-vp8",
            "Convert to VP9": "/convert-to-vp9",
            "Convert to H265": "/convert-to-h265",
            "Convert to AV1": "/convert-to-av1",
            "Encoding Ladder": "/encoding-ladder",
            "Get Info": "/get-info",
            "Get Tracks": "/number-of-tracks"
        }
        return operations.get(operation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEncoderGUI()
    window.show()
    sys.exit(app.exec_())
