"""
Deals对象管理类
"""
from typing import Dict, Any, Optional, List
import csv
import re
from ..base_object import BaseAttioObject


class DealsManager(BaseAttioObject):
    """Deals对象管理器"""
    
    def __init__(self, api_key: str):
        """初始化Deals管理器"""
        super().__init__(api_key, 'deals')
        
        # 负责人映射
        self.owner_mapping = {
            "黄晓敏": "ines@ahalab.ai",
            "Wels": "zehang.tian@ahalab.ai",
            "姚昱臣": "zehang.tian@ahalab.ai",
            "孙若婷": "zehang.tian@ahalab.ai",
        }
        
        # 选项字段的默认值
        self.option_defaults = {
            "行业": "Other",
            "客户规模": "Startup", 
            "客户方对接人职位": "Unknown",
            "是否需要跟进": "Yes",
            "1个月内转化情况": "Not Converted"
        }
        
        # 系统属性ID（从之前的测试中获取）
        self.system_attributes = {
            'name': '885adcc2-b2c0-4109-b76c-50c53143591e',
            'owner': 'a9c85f18-7375-418e-b7ae-bdae1379d4cb',
            'stage': 'd48f3368-9fad-4965-8e6f-cc7aa574c5d1',
            'value': 'a22e3ec2-ccbc-42cf-b9a7-0b0e57e84a86',
            'associated_people': 'c6322091-5b9f-467c-a3e8-b6ac592c5e9b',
            'associated_company': '2600913d-d611-411c-a20a-7db79058e8e4'
        }
    
    def create_deal_from_csv(self, csv_data: Dict[str, Any]) -> Optional[str]:
        """
        从CSV数据创建Deal记录
        
        Args:
            csv_data: CSV行数据
            
        Returns:
            创建的记录ID
        """
        try:
            # 生成Deal名称
            company = csv_data.get('公司', '').strip()
            customer = csv_data.get('客户', '').strip()
            deal_name = f"{company} - {customer or 'Unknown'}"
            
            # 根据负责人分配owner
            owner_name = csv_data.get('负责人', '').strip()
            owner_email = self.owner_mapping.get(owner_name, "zehang.tian@ahalab.ai")
            
            # 处理预算金额
            deal_value = None
            budget_str = csv_data.get('预算', '')
            if budget_str:
                numbers = re.findall(r'\d+', budget_str)
                if numbers:
                    try:
                        deal_value = float(numbers[0])
                    except ValueError:
                        pass
            
            # 准备Deal记录数据
            deal_values = {
                # 系统属性
                self.system_attributes['name']: deal_name,
                self.system_attributes['owner']: owner_email,
                self.system_attributes['stage']: "In Progress",
            }
            
            # 添加预算金额
            if deal_value:
                deal_values[self.system_attributes['value']] = deal_value
            
            # 添加自定义属性
            self._add_custom_attributes(deal_values, csv_data)
            
            # 过滤空值
            deal_values = {k: v for k, v in deal_values.items() if v is not None and v != ''}
            
            print(f"创建Deal记录: {deal_name}")
            print(f"  负责人: {owner_name} -> {owner_email}")
            print(f"  预算: {deal_value if deal_value else 'N/A'}")
            
            return self.create_record(deal_values)
                
        except Exception as e:
            print(f"❌ 创建Deal记录失败: {e}")
            return None
    
    def _add_custom_attributes(self, deal_values: Dict[str, Any], csv_data: Dict[str, Any]):
        """添加自定义属性到deal_values"""
        # 字段映射
        field_mapping = {
            '公司业务介绍': 'business_description',
            '客户邮箱': 'customer_email',
            '地区': 'region',
            '行业': 'industry',
            '客户规模': 'customer_scale',
            '客户方对接人职位': 'customer_position',
            '是否需要跟进': 'need_follow_up',
            '1个月内转化情况': 'conversion_status',
            '产品使用顾虑': 'concerns',
            '未满足的功能需求': 'unmet_needs',
            '会后待办事项': 'todo',
            '跟进/不跟进原因': 'follow_up_reason',
            '初次沟通日期': 'first_contact_date',
            '是否拉群': 'group_created',
            '是否已创建campaign': 'has_campaign',
            '优先级': 'priority'
        }
        
        for csv_field, attr_slug in field_mapping.items():
            value = csv_data.get(csv_field, '').strip()
            
            # 如果是选项字段且为空，使用默认值
            if not value and csv_field in self.option_defaults:
                value = self.option_defaults[csv_field]
            
            if value:
                # 获取属性ID
                attr_id = self.get_attribute_id(attr_slug)
                if attr_id:
                    deal_values[attr_id] = value
    
    def parse_csv_file(self, filename: str) -> List[Dict[str, Any]]:
        """解析CSV文件"""
        try:
            records = []
            
            with open(filename, 'r', encoding='utf-8-sig') as file:
                lines = file.readlines()
            
            # 找到标题行（跳过空行和注释）
            header_line = None
            data_start = 0
            
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith('#'):
                    # 检查是否包含CSV标题
                    if '公司' in line and '客户' in line:
                        header_line = line.strip()
                        data_start = i + 1
                        break
            
            if not header_line:
                print("❌ 未找到CSV标题行")
                return []
            
            # 解析标题
            reader = csv.DictReader([header_line] + lines[data_start:])
            
            for row in reader:
                if any(row.values()):  # 跳过空行
                    records.append(row)
            
            print(f"✅ 成功解析CSV文件: {len(records)}条记录")
            return records
            
        except Exception as e:
            print(f"❌ 解析CSV文件失败: {e}")
            return []
    
    def batch_create_from_csv(self, csv_file: str, limit: int = None) -> Dict[str, Any]:
        """
        从CSV文件批量创建Deal记录
        
        Args:
            csv_file: CSV文件路径
            limit: 限制处理数量
            
        Returns:
            创建结果统计
        """
        print("=== 开始批量创建Deal记录 ===")
        
        # 解析CSV文件
        csv_records = self.parse_csv_file(csv_file)
        if not csv_records:
            return {'created_count': 0, 'failed_count': 0, 'created_deals': []}
        
        # 限制处理数量
        if limit:
            csv_records = csv_records[:limit]
            print(f"限制处理前{limit}条记录")
        
        created_count = 0
        failed_count = 0
        created_deals = []
        
        for i, csv_data in enumerate(csv_records, 1):
            print(f"\n--- 处理第{i}条记录 ---")
            print(f"公司: {csv_data.get('公司', 'N/A')}")
            print(f"客户: {csv_data.get('客户', 'N/A')}")
            print(f"优先级: {csv_data.get('优先级', 'N/A')}")
            print(f"负责人: {csv_data.get('负责人', 'N/A')}")
            
            record_id = self.create_deal_from_csv(csv_data)
            
            if record_id:
                created_count += 1
                created_deals.append({
                    'company': csv_data.get('公司', ''),
                    'customer': csv_data.get('客户', ''),
                    'record_id': record_id
                })
            else:
                failed_count += 1
        
        print(f"\n=== 批量创建完成 ===")
        print(f"✅ 成功创建: {created_count}条")
        print(f"❌ 创建失败: {failed_count}条")
        
        return {
            'created_count': created_count,
            'failed_count': failed_count,
            'created_deals': created_deals
        }
    
    def delete_all_deal_records(self) -> Dict[str, Any]:
        """删除所有Deal记录"""
        print("=== 开始删除所有Deal记录 ===")
        
        try:
            # 获取所有记录
            records = self.list_records(limit=1000)  # 获取更多记录
            
            if not records:
                print("✅ 没有找到Deal记录")
                return {'deleted_count': 0, 'failed_count': 0}
            
            print(f"找到 {len(records)} 条记录，开始删除...")
            
            deleted_count = 0
            failed_count = 0
            
            for record in records:
                record_id = record['id']['record_id']
                record_name = record.get('values', {}).get('name', [{}])[0].get('value', 'Unknown')
                
                print(f"删除记录: {record_name} ({record_id})")
                
                if self.delete_record(record_id):
                    deleted_count += 1
                    print(f"✅ 删除成功: {record_name}")
                else:
                    failed_count += 1
                    print(f"❌ 删除失败: {record_name}")
            
            print(f"\n=== 删除记录完成 ===")
            print(f"✅ 成功删除: {deleted_count}条记录")
            print(f"❌ 删除失败: {failed_count}条记录")
            
            return {
                'deleted_count': deleted_count,
                'failed_count': failed_count
            }
            
        except Exception as e:
            print(f"❌ 删除记录失败: {e}")
            return {'deleted_count': 0, 'failed_count': 0}
    
    def delete_specific_records(self, record_ids: List[str]) -> Dict[str, Any]:
        """删除指定的记录"""
        print(f"=== 开始删除 {len(record_ids)} 条指定记录 ===")
        
        deleted_count = 0
        failed_count = 0
        
        for record_id in record_ids:
            print(f"删除记录: {record_id}")
            
            if self.delete_record(record_id):
                deleted_count += 1
                print(f"✅ 删除成功: {record_id}")
            else:
                failed_count += 1
                print(f"❌ 删除失败: {record_id}")
        
        print(f"\n=== 删除完成 ===")
        print(f"✅ 成功删除: {deleted_count}条记录")
        print(f"❌ 删除失败: {failed_count}条记录")
        
        return {
            'deleted_count': deleted_count,
            'failed_count': failed_count
        }
    
    def delete_all_custom_attributes(self) -> Dict[str, Any]:
        """删除所有自定义属性（通过存档实现）"""
        print("=== 开始删除所有自定义属性 ===")
        print("📝 通过设置 is_archived: true 来存档属性")
        
        try:
            # 获取所有属性
            attributes = self.list_attributes()
            
            if not attributes.get('data'):
                print("✅ 没有找到属性")
                return {'deleted_count': 0, 'failed_count': 0}
            
            custom_attributes = []
            system_attributes = []
            
            for attr in attributes['data']:
                if not attr.get('is_system_attribute', True):
                    custom_attributes.append(attr)
                else:
                    system_attributes.append(attr)
            
            print(f"找到 {len(custom_attributes)} 个自定义属性需要存档")
            print(f"保留 {len(system_attributes)} 个系统属性")
            
            deleted_count = 0
            failed_count = 0
            
            for attr in custom_attributes:
                attr_id = attr['id']['attribute_id']
                attr_title = attr.get('title', 'Unknown')
                attr_slug = attr.get('api_slug', 'Unknown')
                
                print(f"存档属性: {attr_title} ({attr_slug})")
                
                try:
                    # 使用PATCH方法更新属性，设置is_archived为true
                    payload = {
                        'data': {
                            'is_archived': True
                        }
                    }
                    
                    result = self.client._make_request(
                        'PATCH', 
                        f'/objects/deals/attributes/{attr_id}', 
                        data=payload
                    )
                    
                    if result:
                        deleted_count += 1
                        print(f"✅ 属性存档成功: {attr_title}")
                    else:
                        failed_count += 1
                        print(f"❌ 属性存档失败: {attr_title}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"❌ 属性存档异常: {attr_title} - {e}")
            
            print(f"\n=== 属性存档完成 ===")
            print(f"✅ 成功存档: {deleted_count}个属性")
            print(f"❌ 存档失败: {failed_count}个属性")
            
            return {
                'deleted_count': deleted_count,
                'failed_count': failed_count,
                'custom_attributes': custom_attributes,
                'system_attributes': system_attributes
            }
            
        except Exception as e:
            print(f"❌ 获取属性失败: {e}")
            return {'deleted_count': 0, 'failed_count': 0}
    
    def cleanup_all_deals(self) -> Dict[str, Any]:
        """清理所有Deals数据（记录和自定义属性）"""
        print("=== 开始清理所有Deals数据 ===")
        
        # 先删除所有记录
        records_result = self.delete_all_deal_records()
        
        # 再删除所有自定义属性
        attributes_result = self.delete_all_custom_attributes()
        
        total_deleted = records_result['deleted_count'] + attributes_result['deleted_count']
        total_failed = records_result['failed_count'] + attributes_result['failed_count']
        
        print(f"\n=== 清理完成 ===")
        print(f"✅ 总删除: {total_deleted}个")
        print(f"❌ 总失败: {total_failed}个")
        
        return {
            'records': records_result,
            'attributes': attributes_result,
            'total_deleted': total_deleted,
            'total_failed': total_failed
        }
    
    def get_deal_attributes_definition(self) -> List[Dict[str, Any]]:
        """获取Deal对象需要的自定义属性定义"""
        return [
            {
                'title': '公司业务介绍',
                'api_slug': 'business_description',
                'type': 'text',
                'description': '公司的业务介绍和描述'
            },
            {
                'title': '客户邮箱',
                'api_slug': 'customer_email',
                'type': 'text',
                'description': '客户的邮箱地址'
            },
            {
                'title': '地区',
                'api_slug': 'region',
                'type': 'text',
                'description': '客户所在地区'
            },
            {
                'title': '行业',
                'api_slug': 'industry',
                'type': 'select',
                'description': '客户所属行业',
                'options': ['AI', 'Agency', 'Enterprise Services', 'Toys', 'Healthcare', 
                           'Internet', 'Cryptocurrency', 'E-commerce', 'Finance', 
                           'Manufacturing', 'Exhibition', 'Brand', 'Other']
            },
            {
                'title': '客户规模',
                'api_slug': 'customer_scale',
                'type': 'select',
                'description': '客户的规模大小',
                'options': ['Startup', 'Medium', 'Large']
            },
            {
                'title': '客户方对接人职位',
                'api_slug': 'customer_position',
                'type': 'select',
                'description': '客户方对接人的职位',
                'options': ['CEO', 'Co-founder', 'Overseas KOL Manager', 'Marketing Manager', 
                           'Operations Manager', 'Product Manager', 'Marketing Executive', 'Unknown']
            },
            {
                'title': '是否需要跟进',
                'api_slug': 'need_follow_up',
                'type': 'select',
                'description': '是否需要跟进此客户',
                'options': ['Yes', 'No']
            },
            {
                'title': '1个月内转化情况',
                'api_slug': 'conversion_status',
                'type': 'select',
                'description': '1个月内的转化情况',
                'options': ['Converted', 'Not Converted']
            },
            {
                'title': '产品使用顾虑',
                'api_slug': 'concerns',
                'type': 'text',
                'description': '客户对产品使用的顾虑'
            },
            {
                'title': '未满足的功能需求',
                'api_slug': 'unmet_needs',
                'type': 'text',
                'description': '客户未满足的功能需求'
            },
            {
                'title': '会后待办事项',
                'api_slug': 'todo',
                'type': 'text',
                'description': '会议后的待办事项'
            },
            {
                'title': '跟进/不跟进原因',
                'api_slug': 'follow_up_reason',
                'type': 'text',
                'description': '跟进或不跟进的原因'
            },
            {
                'title': '初次沟通日期',
                'api_slug': 'first_contact_date',
                'type': 'date',
                'description': '与客户的初次沟通日期'
            },
            {
                'title': '是否拉群',
                'api_slug': 'group_created',
                'type': 'text',
                'description': '是否已创建微信群或其他群组'
            },
            {
                'title': '是否已创建campaign',
                'api_slug': 'has_campaign',
                'type': 'select',
                'description': '是否已创建campaign名称',
                'options': ['是', '否']
            },
            {
                'title': '优先级',
                'api_slug': 'priority',
                'type': 'select',
                'description': '客户的优先级',
                'options': ['P0—已付费', 'P2—未下单高意愿', 'P5—未下单低意愿/低预算', '非目标客户']
            }
        ]
