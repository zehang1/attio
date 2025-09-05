"""
Attio属性管理类
用于创建和管理各种类型的属性
"""
from typing import Dict, Any, List, Optional
from .base_object import BaseAttioObject


class AttributeManager:
    """属性管理器"""
    
    def __init__(self, api_key: str):
        """初始化属性管理器"""
        self.api_key = api_key
        
        # 属性类型配置 - 支持所有Attio属性类型
        self.attribute_configs = {
            'text': {
                'config': {'text': {}}
            },
            'number': {
                'config': {'number': {}}
            },
            'checkbox': {
                'config': {'checkbox': {}}
            },
            'currency': {
                'config': {'currency': {'default_currency_code': 'USD', 'display_type': 'symbol'}}
            },
            'date': {
                'config': {'date': {}}
            },
            'timestamp': {
                'config': {'timestamp': {}}
            },
            'rating': {
                'config': {'rating': {}}
            },
            'status': {
                'config': {'status': {}}
            },
            'select': {
                'config': {'select': {}}
            },
            'record-reference': {
                'config': {'record_reference': {'allowed_objects': []}}
            },
            'actor-reference': {
                'config': {'actor_reference': {}}
            },
            'location': {
                'config': {'location': {}}
            },
            'domain': {
                'config': {'domain': {}}
            },
            'email-address': {
                'config': {'email_address': {}}
            },
            'phone-number': {
                'config': {'phone_number': {}}
            }
        }
    
    def create_text_attribute(self, object_name: str, title: str, api_slug: str, 
                            description: str = "", is_required: bool = False, 
                            is_unique: bool = False) -> Optional[str]:
        """创建文本属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='text',
            description=description,
            is_required=is_required,
            is_unique=is_unique
        )
    
    def create_select_attribute(self, object_name: str, title: str, api_slug: str,
                              options: List[str] = None, description: str = "",
                              is_required: bool = False, is_unique: bool = False,
                              is_multiselect: bool = False) -> Optional[str]:
        """创建选择属性"""
        if options is None:
            options = []
            
        attribute_data = {
            'title': title,
            'api_slug': api_slug,
            'type': 'select',
            'description': description,
            'is_required': is_required,
            'is_unique': is_unique,
            'is_multiselect': is_multiselect,
            'config': {
                'select': {
                    'options': [{'title': option} for option in options]
                }
            }
        }
        
        try:
            base_obj = BaseAttioObject(self.api_key, object_name)
            return base_obj.create_attribute(attribute_data)
        except Exception as e:
            print(f"❌ 创建select属性失败: {e}")
            return None
    
    def create_multiselect_attribute(self, object_name: str, title: str, api_slug: str,
                                   options: List[str] = None, description: str = "",
                                   is_required: bool = False, is_unique: bool = False) -> Optional[str]:
        """创建多选属性"""
        if options is None:
            options = []
            
        attribute_data = {
            'title': title,
            'api_slug': api_slug,
            'type': 'select',
            'description': description,
            'is_required': is_required,
            'is_unique': is_unique,
            'is_multiselect': True,  # 多选
            'config': {
                'select': {
                    'options': [{'title': option} for option in options]
                }
            }
        }
        
        try:
            base_obj = BaseAttioObject(self.api_key, object_name)
            return base_obj.create_attribute(attribute_data)
        except Exception as e:
            print(f"❌ 创建multiselect属性失败: {e}")
            return None
    
    def create_date_attribute(self, object_name: str, title: str, api_slug: str,
                            description: str = "", is_required: bool = False) -> Optional[str]:
        """创建日期属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='date',
            description=description,
            is_required=is_required
        )
    
    def create_timestamp_attribute(self, object_name: str, title: str, api_slug: str,
                                 description: str = "", is_required: bool = False) -> Optional[str]:
        """创建时间戳属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='timestamp',
            description=description,
            is_required=is_required
        )
    
    def create_currency_attribute(self, object_name: str, title: str, api_slug: str,
                                description: str = "", is_required: bool = False) -> Optional[str]:
        """创建货币属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='currency',
            description=description,
            is_required=is_required
        )
    
    def create_number_attribute(self, object_name: str, title: str, api_slug: str,
                              description: str = "", is_required: bool = False) -> Optional[str]:
        """创建数字属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='number',
            description=description,
            is_required=is_required
        )
    
    def create_checkbox_attribute(self, object_name: str, title: str, api_slug: str,
                                description: str = "", is_required: bool = False) -> Optional[str]:
        """创建复选框属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='checkbox',
            description=description,
            is_required=is_required
        )
    
    def create_rating_attribute(self, object_name: str, title: str, api_slug: str,
                              description: str = "", is_required: bool = False) -> Optional[str]:
        """创建评分属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='rating',
            description=description,
            is_required=is_required
        )
    
    def create_status_attribute(self, object_name: str, title: str, api_slug: str,
                              options: List[str] = None, description: str = "", 
                              is_required: bool = False) -> Optional[str]:
        """创建状态属性"""
        if options is None:
            options = []
            
        attribute_data = {
            'title': title,
            'api_slug': api_slug,
            'type': 'status',
            'description': description,
            'is_required': is_required,
            'is_unique': False,
            'is_multiselect': False,
            'config': {
                'status': {
                    'options': [{'title': option} for option in options]
                }
            }
        }
        
        try:
            base_obj = BaseAttioObject(self.api_key, object_name)
            return base_obj.create_attribute(attribute_data)
        except Exception as e:
            print(f"❌ 创建status属性失败: {e}")
            return None
    
    def create_record_reference_attribute(self, object_name: str, title: str, api_slug: str,
                                        allowed_objects: List[str], description: str = "",
                                        is_required: bool = False) -> Optional[str]:
        """创建记录引用属性"""
        attribute_data = {
            'title': title,
            'api_slug': api_slug,
            'type': 'record-reference',
            'description': description,
            'is_required': is_required,
            'is_unique': False,
            'is_multiselect': False,
            'config': {
                'record_reference': {
                    'allowed_object_ids': allowed_objects
                }
            }
        }
        
        try:
            base_obj = BaseAttioObject(self.api_key, object_name)
            return base_obj.create_attribute(attribute_data)
        except Exception as e:
            print(f"❌ 创建record-reference属性失败: {e}")
            return None
    
    def create_actor_reference_attribute(self, object_name: str, title: str, api_slug: str,
                                       description: str = "", is_required: bool = False) -> Optional[str]:
        """创建参与者引用属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='actor-reference',
            description=description,
            is_required=is_required
        )
    
    def create_location_attribute(self, object_name: str, title: str, api_slug: str,
                                description: str = "", is_required: bool = False) -> Optional[str]:
        """创建位置属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='location',
            description=description,
            is_required=is_required
        )
    
    def create_domain_attribute(self, object_name: str, title: str, api_slug: str,
                              description: str = "", is_required: bool = False) -> Optional[str]:
        """创建域名属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='domain',
            description=description,
            is_required=is_required
        )
    
    def create_email_address_attribute(self, object_name: str, title: str, api_slug: str,
                                     description: str = "", is_required: bool = False) -> Optional[str]:
        """创建邮箱地址属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='email-address',
            description=description,
            is_required=is_required
        )
    
    def create_phone_number_attribute(self, object_name: str, title: str, api_slug: str,
                                    description: str = "", is_required: bool = False) -> Optional[str]:
        """创建电话号码属性"""
        return self._create_attribute(
            object_name=object_name,
            title=title,
            api_slug=api_slug,
            attr_type='phone-number',
            description=description,
            is_required=is_required
        )
    
    def _create_attribute(self, object_name: str, title: str, api_slug: str,
                         attr_type: str, description: str = "", is_required: bool = False,
                         is_unique: bool = False) -> Optional[str]:
        """创建属性的通用方法"""
        if attr_type not in self.attribute_configs:
            print(f"❌ 不支持的属性类型: {attr_type}")
            return None
        
        attribute_data = {
            'title': title,
            'api_slug': api_slug,
            'type': attr_type,
            'description': description,
            'is_required': is_required,
            'is_unique': is_unique,
            'is_multiselect': False,
            'config': self.attribute_configs[attr_type]['config']
        }
        
        try:
            base_obj = BaseAttioObject(self.api_key, object_name)
            return base_obj.create_attribute(attribute_data)
        except Exception as e:
            print(f"❌ 创建{attr_type}属性失败: {e}")
            return None
    
    def batch_create_attributes(self, object_name: str, 
                              attribute_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量创建属性
        
        Args:
            object_name: 对象名称
            attribute_definitions: 属性定义列表
            
        Returns:
            创建结果统计
        """
        print(f"=== 开始为{object_name}对象批量创建属性 ===")
        
        success_count = 0
        failed_count = 0
        results = {}
        
        for attr_def in attribute_definitions:
            attr_type = attr_def.get('type', 'text')
            title = attr_def.get('title', '')
            api_slug = attr_def.get('api_slug', '')
            
            print(f"\n--- 创建属性: {title} ({api_slug}) ---")
            
            if attr_type == 'select':
                attr_id = self.create_select_attribute(
                    object_name=object_name,
                    title=title,
                    api_slug=api_slug,
                    options=attr_def.get('options', []),
                    description=attr_def.get('description', ''),
                    is_required=attr_def.get('is_required', False),
                    is_unique=attr_def.get('is_unique', False),
                    is_multiselect=attr_def.get('is_multiselect', False)
                )
            else:
                attr_id = self._create_attribute(
                    object_name=object_name,
                    title=title,
                    api_slug=api_slug,
                    attr_type=attr_type,
                    description=attr_def.get('description', ''),
                    is_required=attr_def.get('is_required', False),
                    is_unique=attr_def.get('is_unique', False)
                )
            
            if attr_id:
                success_count += 1
                results[api_slug] = {'status': 'success', 'id': attr_id}
            else:
                failed_count += 1
                results[api_slug] = {'status': 'failed'}
        
        print(f"\n=== 批量创建完成 ===")
        print(f"✅ 成功创建: {success_count}个")
        print(f"❌ 创建失败: {failed_count}个")
        
        return {
            'success_count': success_count,
            'failed_count': failed_count,
            'results': results
        }
