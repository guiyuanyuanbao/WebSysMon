# WebSysMon

[![中文](https://img.shields.io/badge/lang-中文-blue)](README_CN.md)
[![English](https://img.shields.io/badge/lang-English-red)](README.md)

WebSysMon is a tool for real-time monitoring of system status through a web interface. It uses HTML and ECharts to monitor CPU, memory, disk, network, and GPU usage, displaying them visually in charts.

### Features
- Real-time CPU usage monitoring
- Real-time memory usage monitoring
- Real-time disk usage monitoring
- Real-time network traffic and speed monitoring
- Real-time GPU usage and temperature monitoring

### Installation and Usage

#### Prerequisites
- Python 3.6+
- pip

#### Installation Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/WebSysMon.git
    cd WebSysMon
    ```

2. Create and activate a virtual environment (optional):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the application:
    ```sh
    python main.py
    ```

5. Open your browser and visit `http://127.0.0.1:8000` to view the system monitoring dashboard.

### Configuration
By default, WebSysMon runs on port `8000`. You can change the port settings in the `main.py` file.

### Usage
After starting the application, open your browser and visit `http://127.0.0.1:8000`. The system monitoring information will be displayed in real-time charts on the webpage.

![Main Page](doc/img/home.png)

### License
This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more information.

### Contributing
Feel free to submit issues and pull requests to improve the project. If you have any suggestions or find any issues, please create an issue on GitHub.

---

For Chinese version, click [这里](README_CN.md).
