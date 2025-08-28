"""
日志管理模块

提供统一的日志配置和管理功能
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str,
    level: str = 'INFO',
    log_dir: str = 'logs',
    max_bytes: int = 10*1024*1024,  # 10MB
    backup_count: int = 5,
    console: bool = True
) -> logging.Logger:
    """
    设置日志配置
    
    Args:
        name: 日志名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: 日志目录
        max_bytes: 单个日志文件最大大小
        backup_count: 保留的日志文件数量
        console: 是否输出到控制台
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器
    log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

class LoggerMixin:
    """日志混入类，为类提供日志功能"""
    
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)

if __name__ == "__main__":
    # 测试日志功能
    logger = setup_logger('test')
    
    logger.debug('这是调试信息')
    logger.info('这是信息消息')
    logger.warning('这是警告消息')
    logger.error('这是错误消息')
    logger.critical('这是严重错误')