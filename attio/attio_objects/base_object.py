"""
Attio对象管理基类
"""
from typing import Dict, Any, Optional, List
from config import AttioConfig
from attio_client import AttioClient


class BaseAttioObject:
    """Attio对象管理基类"""
    
    def __init__(self, api_key: str, object_name: str):
        """
        初始化对象管理器
        
        Args:
            api_key: Attio API密钥
            object_name: 对象名称 (如 'deals', 'users', 'people', 'workspaces')
        """
        self.config = AttioConfig(api_key=api_key)
        self.client = AttioClient(self.config)
        self.object_name = object_name
        self.attributes = {}  # 缓存属性信息
        
    def list_attributes(self) -> Dict[str, Any]:
        """获取对象的所有属性"""
        try:
            result = self.client.list_object_attributes(self.object_name)
            if result.get('data'):
                # 缓存属性信息
                for attr in result['data']:
                    attr_id = attr['id']['attribute_id']
                    self.attributes[attr_id] = {
                        'title': attr.get('title', ''),
                        'api_slug': attr.get('api_slug', ''),
                        'type': attr.get('type', ''),
                        'is_system_attribute': attr.get('is_system_attribute', True)
                    }
            return result
        except Exception as e:
            print(f"❌ 获取{self.object_name}属性失败: {e}")
            return {}
    
    def get_attribute_id(self, api_slug: str) -> Optional[str]:
        """根据api_slug获取属性ID"""
        if not self.attributes:
            self.list_attributes()
        
        for attr_id, attr_info in self.attributes.items():
            if attr_info['api_slug'] == api_slug:
                return attr_id
        return None
    
    def get_attribute_slug(self, attribute_id: str) -> Optional[str]:
        """根据属性ID获取api_slug"""
        if not self.attributes:
            self.list_attributes()
        
        return self.attributes.get(attribute_id, {}).get('api_slug')
    
    def create_attribute(self, attribute_data: Dict[str, Any]) -> Optional[str]:
        """
        创建对象属性
        
        Args:
            attribute_data: 属性数据
            
        Returns:
            创建的属性ID，失败返回None
        """
        try:
            result = self.client.create_object_attribute(self.object_name, attribute_data)
            if result.get('data'):
                attr_id = result['data']['id']['attribute_id']
                print(f"✅ 成功创建{self.object_name}属性: {attribute_data.get('title', '')} ({attr_id})")
                # 更新缓存
                self.attributes[attr_id] = {
                    'title': attribute_data.get('title', ''),
                    'api_slug': attribute_data.get('api_slug', ''),
                    'type': attribute_data.get('type', ''),
                    'is_system_attribute': False
                }
                return attr_id
            else:
                print(f"❌ 创建{self.object_name}属性失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 创建{self.object_name}属性失败: {e}")
            return None
    
    def create_record(self, record_data: Dict[str, Any]) -> Optional[str]:
        """
        创建记录
        
        Args:
            record_data: 记录数据
            
        Returns:
            创建的记录ID，失败返回None
        """
        try:
            result = self.client.create_record(self.object_name, record_data)
            if result.get('data'):
                record_id = result['data']['id']['record_id']
                print(f"✅ 成功创建{self.object_name}记录: {record_id}")
                return record_id
            else:
                print(f"❌ 创建{self.object_name}记录失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 创建{self.object_name}记录失败: {e}")
            return None
    
    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """获取记录"""
        try:
            result = self.client.get_record(self.object_name, record_id)
            return result.get('data')
        except Exception as e:
            print(f"❌ 获取{self.object_name}记录失败: {e}")
            return None
    
    def update_record(self, record_id: str, record_data: Dict[str, Any]) -> bool:
        """更新记录"""
        try:
            result = self.client.update_record(self.object_name, record_id, record_data)
            if result.get('data'):
                print(f"✅ 成功更新{self.object_name}记录: {record_id}")
                return True
            else:
                print(f"❌ 更新{self.object_name}记录失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 更新{self.object_name}记录失败: {e}")
            return False
    
    def delete_record(self, record_id: str) -> bool:
        """删除记录"""
        try:
            result = self.client.delete_record(self.object_name, record_id)
            # 根据Attio API文档，删除成功的响应是空的 {}
            if result == {} or result is None:
                print(f"✅ 成功删除{self.object_name}记录: {record_id}")
                return True
            else:
                print(f"❌ 删除{self.object_name}记录失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 删除{self.object_name}记录失败: {e}")
            return False
    
    def list_records(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出记录"""
        try:
            # 根据Attio API文档，使用POST /objects/{object}/records/query来列出记录
            payload = {
                'limit': limit,
                'offset': 0
            }
            result = self.client._make_request('POST', f'/objects/{self.object_name}/records/query', data=payload)
            return result.get('data', [])
        except Exception as e:
            print(f"❌ 获取{self.object_name}记录列表失败: {e}")
            return []
