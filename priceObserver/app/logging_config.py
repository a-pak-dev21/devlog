from app.settings import settings, BASE_DIR
import logging

def root_logger_config():
    
    root = logging.getLogger()
    root.setLevel(settings.log_level)
    formatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(name)s: %(message)s')

    file_dir = BASE_DIR / 'artifacts'
    file_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(filename=file_dir / 'gen_logs.log', mode='a')
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    if not root.handlers:
        root.addHandler(file_handler)
        root.addHandler(stream_handler)

