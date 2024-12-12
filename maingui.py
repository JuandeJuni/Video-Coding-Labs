import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QComboBox, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QPixmap


class VideoEncoderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Encoder API GUI")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

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
            "Convert to VP9", "Convert to H265", "Convert to AV1"
        ])
        self.layout.addWidget(self.operation_combo)

        # Input parameters
        self.params_label = QLabel("Enter Parameters (comma-separated if multiple):")
        self.layout.addWidget(self.params_label)
        self.params_input = QLineEdit()
        self.layout.addWidget(self.params_input)

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

    def execute_operation(self):
        operation = self.operation_combo.currentText()
        params = self.params_input.text().split(",")
        endpoint = self.get_endpoint(operation)

        if not self.uploaded_file:
            self.result_label.setText("Please upload a file first.")
            return

        if endpoint:
            # Call the endpoint with parameters
            try:
                if "filename" in endpoint:
                    params_dict = {"filename": self.uploaded_file.split("/")[-1]}
                    if params:
                        for i, param in enumerate(params):
                            key = f"param{i + 1}"  # Example parameter names
                            params_dict[key] = param
                    response = requests.get(f"{self.api_url}{endpoint}", params=params_dict)
                else:
                    response = requests.get(f"{self.api_url}{endpoint}")

                if response.status_code == 200:
                    self.result_label.setText(f"Success: {operation}")
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
        }
        return operations.get(operation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEncoderGUI()
    window.show()
    sys.exit(app.exec_())
