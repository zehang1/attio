"""
People对象管理类
"""
from typing import Dict, Any, Optional, List
from ..base_object import BaseAttioObject


class PeopleManager(BaseAttioObject):
    """People对象管理器"""
    
    def __init__(self, api_key: str):
        """初始化People管理器"""
        super().__init__(api_key, 'people')
        
        # 系统属性ID（需要从实际API获取）
        self.system_attributes = {
            'name': 'name',  # 需要确认实际ID
            'email_addresses': 'email_addresses',  # 需要确认实际ID
            'phone_numbers': 'phone_numbers',  # 需要确认实际ID
            'created_at': 'created_at',
            'created_by': 'created_by'
        }
    
    def create_person(self, person_data: Dict[str, Any]) -> Optional[str]:
        """
        创建人员记录
        
        Args:
            person_data: 人员数据，包含以下字段：
                - name: 姓名
                - email: 邮箱地址
                - phone: 电话号码（可选）
                - company: 公司（可选）
                
        Returns:
            创建的记录ID
        """
        try:
            # 准备人员记录数据
            person_values = {}
            
            # 必需字段
            if 'name' in person_data:
                name_attr_id = self.get_attribute_id('name')
                if name_attr_id:
                    person_values[name_attr_id] = person_data['name']
            
            if 'email' in person_data:
                email_attr_id = self.get_attribute_id('email_addresses')
                if email_attr_id:
                    person_values[email_attr_id] = person_data['email']
            
            if 'phone' in person_data:
                phone_attr_id = self.get_attribute_id('phone_numbers')
                if phone_attr_id:
                    person_values[phone_attr_id] = person_data['phone']
            
            # 过滤空值
            person_values = {k: v for k, v in person_values.items() if v is not None and v != ''}
            
            print(f"创建人员记录: {person_data.get('name', 'Unknown')} ({person_data.get('email', 'N/A')})")
            
            return self.create_record(person_values)
                
        except Exception as e:
            print(f"❌ 创建人员记录失败: {e}")
            return None
    
    def create_person_from_mongodb(self, mongodb_data: Dict[str, Any]) -> Optional[str]:
        """
        从MongoDB数据创建人员记录
        
        Args:
            mongodb_data: MongoDB用户数据
            
        Returns:
            创建的记录ID
        """
        try:
            # 提取人员信息
            person_data = {
                'name': mongodb_data.get('clerkName', ''),
                'email': mongodb_data.get('clerkPrimaryEmail', ''),
                'phone': '',  # MongoDB数据中没有电话信息
                'company': ''  # MongoDB数据中没有公司信息
            }
            
            return self.create_person(person_data)
                
        except Exception as e:
            print(f"❌ 从MongoDB数据创建人员记录失败: {e}")
            return None
    
    def get_people_attributes_definition(self) -> List[Dict[str, Any]]:
        """获取People对象需要的自定义属性定义"""
        return [
            {
                'title': '职位',
                'api_slug': 'job_title',
                'type': 'text',
                'description': '人员的职位'
            },
            {
                'title': '公司',
                'api_slug': 'company',
                'type': 'text',
                'description': '人员所在的公司'
            },
            {
                'title': '部门',
                'api_slug': 'department',
                'type': 'text',
                'description': '人员所在的部门'
            },
            {
                'title': '地区',
                'api_slug': 'region',
                'type': 'text',
                'description': '人员所在的地区'
            },
            {
                'title': '时区',
                'api_slug': 'timezone',
                'type': 'text',
                'description': '人员所在的时区'
            },
            {
                'title': '语言',
                'api_slug': 'language',
                'type': 'select',
                'description': '人员的语言偏好',
                'options': ['中文', 'English', '日本語', '한국어', 'Other']
            },
            {
                'title': '状态',
                'api_slug': 'status',
                'type': 'select',
                'description': '人员的状态',
                'options': ['Active', 'Inactive', 'Lead', 'Customer', 'Prospect']
            },
            {
                'title': '来源',
                'api_slug': 'source',
                'type': 'select',
                'description': '人员的来源',
                'options': ['Website', 'Referral', 'Social Media', 'Email', 'Phone', 'Other']
            },
            {
                'title': '备注',
                'api_slug': 'notes',
                'type': 'text',
                'description': '人员的备注信息'
            }
        ]
