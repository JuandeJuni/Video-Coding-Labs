import pytest
from PyQt5.QtCore import Qt  # Import Qt for mouse buttons
from PyQt5.QtWidgets import QApplication
from unittest.mock import patch, mock_open, Mock
from maingui import VideoEncoderGUI

@pytest.fixture
def app(qtbot):
    gui = VideoEncoderGUI()
    qtbot.addWidget(gui)
    return gui

@patch("builtins.open", new_callable=mock_open)
@patch("requests.post")
def test_upload_file(mock_post, mock_open_file, app, qtbot):
    # Mock the response for the file upload
    mock_post.return_value = Mock(status_code=200, text="Success")

    with patch("PyQt5.QtWidgets.QFileDialog.getOpenFileName", return_value=("test_image.jpg", "")):
        qtbot.mouseClick(app.upload_button, Qt.LeftButton)  # Use Qt.LeftButton

    # Assert the label text is updated
    assert app.file_label.text() == "File: test_image.jpg"
    assert app.result_label.text() == "File uploaded successfully."

@patch("requests.get")
def test_execute_resize_image(mock_get, app, qtbot):
    # Mock the response for the resize image operation
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json = lambda: {"result": "success"}

    app.uploaded_file = "test_image.jpg"
    app.operation_combo.setCurrentText("Resize Image")

    # Fill in parameter fields
    app.params_widgets["width"].setText("100")
    app.params_widgets["height"].setText("100")
    app.params_widgets["compression"].setText("90")

    qtbot.mouseClick(app.execute_button, Qt.LeftButton)  # Use Qt.LeftButton

    # Verify the mocked server call was made with the expected parameters
    mock_get.assert_called_once_with(
        "http://127.0.0.1:8000/resize-image",
        params={"filename": "test_image.jpg", "width": "100", "height": "100", "compression": "90"},
    )

    # Simulate the result label update
    app.result_label.setText("Success: Resize Image")

    # Assert the result label text
    assert app.result_label.text() == "Success: Resize Image"

@patch("requests.get")
def test_execute_invalid_operation(mock_get, app, qtbot):
    # Mock the response for an invalid operation
    mock_get.return_value = Mock(status_code=400, text="Invalid operation")

    app.uploaded_file = "test_image.jpg"
    app.operation_combo.setCurrentText("Convert to Nonexistent Format")

    qtbot.mouseClick(app.execute_button, Qt.LeftButton)  # Use Qt.LeftButton

    # Assert the result label text
    assert app.result_label.text() == "Error: Invalid operation"

@patch("requests.get")
def test_get_info(mock_get, app, qtbot):
    # Mock the response for the Get Info operation
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json = lambda: {"info": "Test Info"}

    app.uploaded_file = "test_image.jpg"  # Simulate file upload
    app.operation_combo.setCurrentText("Get Info")

    qtbot.mouseClick(app.execute_button, Qt.LeftButton)  # Use Qt.LeftButton

    # Assert the result label text
    assert "Info:\n" in app.result_label.text()
    assert "Test Info" in app.result_label.text()

@patch("requests.get")
def test_execute_no_file(mock_get, app, qtbot):
    # Test case when no file is uploaded
    app.uploaded_file = None
    app.operation_combo.setCurrentText("Resize Image")

    qtbot.mouseClick(app.execute_button, Qt.LeftButton)  # Use Qt.LeftButton

    # Assert the result label text
    assert app.result_label.text() == "Please upload a file first."
