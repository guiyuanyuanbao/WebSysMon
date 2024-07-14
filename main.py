import flask
from flask import Flask, render_template, jsonify
from flask_sse import sse, ServerSentEventsBlueprint
import psutil
import GPUtil
import time
import json

app = Flask(__name__)

# 创建 ServerSentEventsBlueprint 实例
sse = ServerSentEventsBlueprint('events', __name__)

# 注册 Blueprint
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    # 渲染前端页面
    return render_template('index.html')


def get_system_metrics():
    # 收集系统监控数据
    cpu_usage = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk_usage_all = get_disk_usage_all()
    net_io = psutil.net_io_counters()
    sent_speed, recv_speed = calculate_network_speed()
    gpu_usage = get_gpu_usage()

    return {
        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_usage': f"{cpu_usage}",
        'memory_usage': f"{memory_usage}",
        'disk_usage_all': disk_usage_all,
        'network_io': {
            'sent': f"{net_io.bytes_sent}",
            'recv': f"{net_io.bytes_recv}"
        },
        'network_speed': {
            'sent': f"{sent_speed}",
            'recv': f"{recv_speed}"
        },
        'gpu_usage': gpu_usage
    }


@app.route('/stream')
def stream():
    def generate():
        while True:
            # 获取系统监控数据
            system_data = get_system_metrics()
            # 使用 JSON 格式发送数据
            yield f"data: {json.dumps(system_data)}\n\n"
            time.sleep(2)  # 间隔一定时间推送一次数据

    return flask.Response(generate(), mimetype='text/event-stream')


disk_usage_cache = None
disk_usage_cache_time = 0


def get_disk_usage_all():
    global disk_usage_cache, disk_usage_cache_time
    current_time = time.time()
    # 缓存磁盘使用数据，减少系统调用频率
    if disk_usage_cache and (current_time - disk_usage_cache_time) < 10:
        return disk_usage_cache

    partitions = psutil.disk_partitions()
    disk_usage_all = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage_all[partition.device] = {
            'total': f"{usage.total / (1024 ** 3):.2f} GB",
            'used': f"{usage.used / (1024 ** 3):.2f} GB",
            'free': f"{usage.free / (1024 ** 3):.2f} GB",
            'percent': f"{usage.percent}"
        }

    disk_usage_cache = disk_usage_all
    disk_usage_cache_time = current_time
    return disk_usage_cache


net_io_prev = psutil.net_io_counters()
net_io_prev_time = time.time()


def calculate_network_speed():
    global net_io_prev, net_io_prev_time
    current_time = time.time()
    net_io = psutil.net_io_counters()
    interval = current_time - net_io_prev_time

    sent_speed = (net_io.bytes_sent - net_io_prev.bytes_sent) / interval
    recv_speed = (net_io.bytes_recv - net_io_prev.bytes_recv) / interval

    net_io_prev = net_io
    net_io_prev_time = current_time

    return sent_speed, recv_speed


def get_gpu_usage():
    gpu_info = []
    # 使用 GPUtil 获取独立显卡信息
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_info.append({
            'id': gpu.id,
            'name': gpu.name,
            'load': f"{gpu.load * 100}%",
            'memory_used': f"{gpu.memoryUsed} MB",
            'memory_total': f"{gpu.memoryTotal} MB",
            'memory_free': f"{gpu.memoryFree} MB",
            'temperature': f"{gpu.temperature} °C"
        })

    return gpu_info


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
