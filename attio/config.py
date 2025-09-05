"""
Attio API 配置类
"""
import os
from typing import Optional
from dotenv import load_dotenv


class AttioConfig:
    """Attio API 配置管理类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化配置
        
        Args:
            api_key: API密钥，如果不提供则从环境变量读取
            base_url: API基础URL，如果不提供则从环境变量读取
        """
        # 加载环境变量
        load_dotenv()
        
        self.api_key = api_key or os.getenv('ATTIO_API_KEY')
        self.base_url = base_url or os.getenv('ATTIO_BASE_URL', 'https://api.attio.com/v2')
        
        # MongoDB配置
        self.source_mongodb_uri = os.getenv("SOURCE_MONGODB_URI", "mongodb+srv://readonly:5uz1uJwET302R7HL@c0.e1lpzaz.mongodb.net/?readPreference=secondary")
        
        if not self.api_key:
            raise ValueError("API密钥未提供，请设置ATTIO_API_KEY环境变量或直接传入api_key参数")
    
    def get_headers(self) -> dict:
        """
        获取API请求头
        
        Returns:
            包含认证信息的请求头字典
        """
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def get_base_url(self) -> str:
        """
        获取API基础URL
        
        Returns:
            API基础URL字符串
        """
        return self.base_url
    
    def get_mongodb_uri(self) -> str:
        """
        获取MongoDB连接URI
        
        Returns:
            MongoDB连接URI字符串
        """
        return self.source_mongodb_uri
