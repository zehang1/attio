"""
Users对象管理类
"""
from typing import Dict, Any, Optional, List
from ..base_object import BaseAttioObject


class UsersManager(BaseAttioObject):
    """Users对象管理器"""
    
    def __init__(self, api_key: str):
        """初始化Users管理器"""
        super().__init__(api_key, 'users')
        
        # 系统属性ID（从之前的测试中获取）
        self.system_attributes = {
            'primary_email_address': 'primary_email_address',  # 需要确认实际ID
            'user_id': 'user_id',  # 需要确认实际ID
            'name': 'name',  # 需要确认实际ID
            'created_at': 'created_at',
            'created_by': 'created_by'
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """
        创建用户记录
        
        Args:
            user_data: 用户数据，包含以下字段：
                - email: 邮箱地址
                - name: 姓名
                - user_id: 用户ID（可选，系统会自动生成）
                
        Returns:
            创建的记录ID
        """
        try:
            # 准备用户记录数据
            user_values = {}
            
            # 必需字段
            if 'email' in user_data:
                email_attr_id = self.get_attribute_id('primary_email_address')
                if email_attr_id:
                    user_values[email_attr_id] = user_data['email']
            
            if 'name' in user_data:
                name_attr_id = self.get_attribute_id('name')
                if name_attr_id:
                    user_values[name_attr_id] = user_data['name']
            
            if 'user_id' in user_data:
                user_id_attr_id = self.get_attribute_id('user_id')
                if user_id_attr_id:
                    user_values[user_id_attr_id] = user_data['user_id']
            
            # 过滤空值
            user_values = {k: v for k, v in user_values.items() if v is not None and v != ''}
            
            print(f"创建用户记录: {user_data.get('name', 'Unknown')} ({user_data.get('email', 'N/A')})")
            
            return self.create_record(user_values)
                
        except Exception as e:
            print(f"❌ 创建用户记录失败: {e}")
            return None
    
    def create_user_from_mongodb(self, mongodb_data: Dict[str, Any]) -> Optional[str]:
        """
        从MongoDB数据创建用户记录
        
        Args:
            mongodb_data: MongoDB用户数据
            
        Returns:
            创建的记录ID
        """
        try:
            # 提取用户信息
            user_data = {
                'email': mongodb_data.get('clerkPrimaryEmail', ''),
                'name': mongodb_data.get('clerkName', ''),
                'user_id': mongodb_data.get('clerkUserId', '')
            }
            
            return self.create_user(user_data)
                
        except Exception as e:
            print(f"❌ 从MongoDB数据创建用户记录失败: {e}")
            return None
    
    def get_user_attributes_definition(self) -> List[Dict[str, Any]]:
        """获取Users对象需要的自定义属性定义"""
        return [
            {
                'title': '用户头像',
                'api_slug': 'avatar_url',
                'type': 'url',
                'description': '用户的头像URL'
            },
            {
                'title': '最后活跃时间',
                'api_slug': 'last_active_at',
                'type': 'timestamp',
                'description': '用户最后活跃的时间'
            },
            {
                'title': '最后登录时间',
                'api_slug': 'last_sign_in_at',
                'type': 'timestamp',
                'description': '用户最后登录的时间'
            },
            {
                'title': '是否有IM账户',
                'api_slug': 'has_im_account',
                'type': 'boolean',
                'description': '用户是否有即时通讯账户'
            },
            {
                'title': '用户状态',
                'api_slug': 'user_status',
                'type': 'select',
                'description': '用户的状态',
                'options': ['Active', 'Inactive', 'Suspended', 'Pending']
            }
        ]
    
    def list_workspace_members(self) -> List[Dict[str, Any]]:
        """列出工作空间成员"""
        try:
            # 使用workspace_members端点
            result = self.client._make_request('GET', '/workspace_members')
            if result.get('data'):
                return result['data']
            return []
        except Exception as e:
            print(f"❌ 获取工作空间成员失败: {e}")
            return []
    
    def get_member_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱获取工作空间成员"""
        try:
            members = self.list_workspace_members()
            for member in members:
                if member.get('email_address') == email:
                    return member
            return None
        except Exception as e:
            print(f"❌ 根据邮箱获取成员失败: {e}")
            return None


