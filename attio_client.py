"""
Attio API 客户端类
"""
import requests
from typing import Dict, Any, Optional, List
from config import AttioConfig


class AttioClient:
    """Attio API 客户端"""
    
    def __init__(self, config: AttioConfig):
        """
        初始化客户端
        
        Args:
            config: AttioConfig配置实例
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.get_headers())
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点
            data: 请求体数据
            params: URL参数
            
        Returns:
            API响应数据
            
        Raises:
            requests.RequestException: 请求异常
        """
        url = f"{self.config.get_base_url()}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"响应状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text}")
            raise
    
    def get_workspaces(self) -> Dict[str, Any]:
        """
        获取工作空间列表
        
        Returns:
            工作空间数据
        """
        return self._make_request('GET', '/workspaces')
    
    def list_all_objects(self) -> Dict[str, Any]:
        """
        列出所有系统定义和用户定义的对象
        
        Returns:
            所有对象列表数据
        """
        return self._make_request('GET', '/objects')
    
    def list_object_attributes(self, object_identifier: str, limit: Optional[int] = None, offset: Optional[int] = None, show_archived: Optional[bool] = None) -> Dict[str, Any]:
        """
        列出指定对象的所有属性
        
        Args:
            object_identifier: 对象标识符 (UUID或slug，如 'people', 'companies')
            limit: 返回结果的最大数量
            offset: 跳过的结果数量
            show_archived: 是否包含已归档的属性
            
        Returns:
            对象属性列表数据
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if show_archived is not None:
            params['show_archived'] = show_archived
            
        return self._make_request('GET', f'/objects/{object_identifier}/attributes', params=params)
    
    def create_object_attribute(self, object_identifier: str, attribute_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        在指定对象上创建新属性
        
        Args:
            object_identifier: 对象标识符 (UUID或slug，如 'people', 'companies')
            attribute_data: 属性数据，包含以下字段：
                - title: 属性标题
                - description: 属性描述
                - api_slug: API slug
                - type: 属性类型 (text, number, email, phone, url, date, datetime, boolean, rating, currency, select, multiselect, record_reference)
                - is_required: 是否必需
                - is_unique: 是否唯一
                - is_multiselect: 是否多选
                - default_value: 默认值
                - config: 配置信息
                
        Returns:
            创建的属性数据
        """
        return self._make_request('POST', f'/objects/{object_identifier}/attributes', data={'data': attribute_data})
    
    def get_objects(self, object_type: str) -> Dict[str, Any]:
        """
        获取指定类型的对象列表
        
        Args:
            object_type: 对象类型 (如 'people', 'companies')
            
        Returns:
            对象列表数据
        """
        return self._make_request('GET', f'/objects/{object_type}')
    
    def get_object(self, object_type: str, object_id: str) -> Dict[str, Any]:
        """
        获取指定对象详情
        
        Args:
            object_type: 对象类型
            object_id: 对象ID
            
        Returns:
            对象详情数据
        """
        return self._make_request('GET', f'/objects/{object_type}/{object_id}')
    
    def create_object(self, object_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新对象
        
        Args:
            object_type: 对象类型
            data: 对象数据
            
        Returns:
            创建的对象数据
        """
        return self._make_request('POST', f'/objects/{object_type}', data=data)
    
    def update_object(self, object_type: str, object_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新对象
        
        Args:
            object_type: 对象类型
            object_id: 对象ID
            data: 更新数据
            
        Returns:
            更新后的对象数据
        """
        return self._make_request('PUT', f'/objects/{object_type}/{object_id}', data=data)
    
    def delete_object(self, object_type: str, object_id: str) -> Dict[str, Any]:
        """
        删除对象
        
        Args:
            object_type: 对象类型
            object_id: 对象ID
            
        Returns:
            删除结果
        """
        return self._make_request('DELETE', f'/objects/{object_type}/{object_id}')
    
    def search_objects(self, object_type: str, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        搜索对象
        
        Args:
            object_type: 对象类型
            query: 搜索查询
            limit: 结果限制数量
            
        Returns:
            搜索结果
        """
        params = {'q': query, 'limit': limit}
        return self._make_request('GET', f'/objects/{object_type}/search', params=params)
    
    def create_record(self, object_identifier: str, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新记录
        
        Args:
            object_identifier: 对象标识符 (UUID或slug，如 'people', 'companies', 'workspaces')
            values: 记录值字典，键为属性ID或API slug，值为属性值
            
        Returns:
            创建的记录数据
        """
        return self._make_request('POST', f'/objects/{object_identifier}/records', data={'data': {'values': values}})
    
    def get_record(self, object_identifier: str, record_id: str) -> Dict[str, Any]:
        """
        获取记录详情
        
        Args:
            object_identifier: 对象标识符
            record_id: 记录ID
            
        Returns:
            记录详情数据
        """
        return self._make_request('GET', f'/objects/{object_identifier}/records/{record_id}')
    
    def update_record(self, object_identifier: str, record_id: str, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新记录
        
        Args:
            object_identifier: 对象标识符
            record_id: 记录ID
            values: 要更新的值
            
        Returns:
            更新后的记录数据
        """
        return self._make_request('PUT', f'/objects/{object_identifier}/records/{record_id}', data={'data': {'values': values}})
    
    def delete_record(self, object_identifier: str, record_id: str) -> Dict[str, Any]:
        """
        删除记录
        
        Args:
            object_identifier: 对象标识符
            record_id: 记录ID
            
        Returns:
            删除结果
        """
        return self._make_request('DELETE', f'/objects/{object_identifier}/records/{record_id}')
