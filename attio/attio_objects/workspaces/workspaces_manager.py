"""
Workspaces对象管理类
"""
from typing import Dict, Any, Optional, List
import time
import random
from ..base_object import BaseAttioObject


class WorkspacesManager(BaseAttioObject):
    """Workspaces对象管理器"""
    
    def __init__(self, api_key: str):
        """初始化Workspaces管理器"""
        super().__init__(api_key, 'workspaces')
        
        # 系统属性ID（从之前的测试中获取）
        self.system_attributes = {
            'name': 'name',  # 需要确认实际ID
            'workspace_id': 'workspace_id',  # 需要确认实际ID
            'users': 'users',  # 需要确认实际ID
            'created_at': 'created_at',
            'created_by': 'created_by'
        }
    
    def create_workspace(self, workspace_data: Dict[str, Any]) -> Optional[str]:
        """
        创建工作空间记录
        
        Args:
            workspace_data: 工作空间数据，包含以下字段：
                - name: 工作空间名称
                - workspace_id: 工作空间ID（可选，系统会自动生成）
                - users: 关联的用户列表（可选）
                
        Returns:
            创建的记录ID
        """
        try:
            # 准备工作空间记录数据
            workspace_values = {}
            
            # 必需字段
            if 'name' in workspace_data:
                name_attr_id = self.get_attribute_id('name')
                if name_attr_id:
                    workspace_values[name_attr_id] = workspace_data['name']
            
            # 生成唯一的workspace_id
            if 'workspace_id' not in workspace_data:
                workspace_data['workspace_id'] = f"workspace_{int(time.time())}_{random.randint(1000, 9999)}"
            
            workspace_id_attr_id = self.get_attribute_id('workspace_id')
            if workspace_id_attr_id:
                workspace_values[workspace_id_attr_id] = workspace_data['workspace_id']
            
            # 关联用户
            if 'users' in workspace_data and workspace_data['users']:
                users_attr_id = self.get_attribute_id('users')
                if users_attr_id:
                    # 将用户ID转换为record-reference格式
                    user_references = []
                    for user_id in workspace_data['users']:
                        user_references.append({
                            'target_object': 'users',
                            'target_record_id': user_id
                        })
                    workspace_values[users_attr_id] = user_references
            
            # 过滤空值
            workspace_values = {k: v for k, v in workspace_values.items() if v is not None and v != ''}
            
            print(f"创建工作空间记录: {workspace_data.get('name', 'Unknown')} ({workspace_data.get('workspace_id', 'N/A')})")
            
            return self.create_record(workspace_values)
                
        except Exception as e:
            print(f"❌ 创建工作空间记录失败: {e}")
            return None
    
    def create_workspace_from_mongodb(self, mongodb_data: Dict[str, Any], user_record_ids: List[str] = None) -> Optional[str]:
        """
        从MongoDB数据创建工作空间记录
        
        Args:
            mongodb_data: MongoDB组织数据
            user_record_ids: 关联的用户记录ID列表
            
        Returns:
            创建的记录ID
        """
        try:
            # 提取工作空间信息
            workspace_data = {
                'name': mongodb_data.get('clerkOrgName', ''),
                'workspace_id': mongodb_data.get('clerkOrgId', ''),
                'users': user_record_ids or []
            }
            
            return self.create_workspace(workspace_data)
                
        except Exception as e:
            print(f"❌ 从MongoDB数据创建工作空间记录失败: {e}")
            return None
    
    def get_workspaces_attributes_definition(self) -> List[Dict[str, Any]]:
        """获取Workspaces对象需要的自定义属性定义"""
        return [
            {
                'title': '工作空间描述',
                'api_slug': 'description',
                'type': 'text',
                'description': '工作空间的描述信息'
            },
            {
                'title': '工作空间类型',
                'api_slug': 'workspace_type',
                'type': 'select',
                'description': '工作空间的类型',
                'options': ['Personal', 'Team', 'Enterprise', 'Organization']
            },
            {
                'title': '行业',
                'api_slug': 'industry',
                'type': 'select',
                'description': '工作空间所属行业',
                'options': ['Technology', 'Healthcare', 'Finance', 'Education', 'Retail', 'Manufacturing', 'Other']
            },
            {
                'title': '规模',
                'api_slug': 'size',
                'type': 'select',
                'description': '工作空间的规模',
                'options': ['1-10', '11-50', '51-200', '201-500', '500+']
            },
            {
                'title': '地区',
                'api_slug': 'region',
                'type': 'text',
                'description': '工作空间所在地区'
            },
            {
                'title': '时区',
                'api_slug': 'timezone',
                'type': 'text',
                'description': '工作空间的时区'
            },
            {
                'title': '状态',
                'api_slug': 'status',
                'type': 'select',
                'description': '工作空间的状态',
                'options': ['Active', 'Inactive', 'Suspended', 'Trial', 'Paid']
            },
            {
                'title': '创建来源',
                'api_slug': 'source',
                'type': 'select',
                'description': '工作空间的创建来源',
                'options': ['Direct', 'Invitation', 'Import', 'API', 'Other']
            },
            {
                'title': '备注',
                'api_slug': 'notes',
                'type': 'text',
                'description': '工作空间的备注信息'
            }
        ]
