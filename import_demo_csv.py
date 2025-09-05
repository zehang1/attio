"""
导入demo.csv文件到Attio
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from attio_objects.deals.deals_manager import DealsManager
from attio_objects.attribute_manager import AttributeManager
from attio_objects.workspace_members.workspace_members_manager import WorkspaceMembersManager
import csv
import re
from typing import Dict, Any, List, Optional


def generate_api_slug(text: str) -> str:
    """生成API slug"""
    if not text:
        return ""
    
    # 移除特殊字符，保留字母、数字、下划线
    slug = re.sub(r'[^\w\s-]', '', text)
    # 替换空格为下划线
    slug = re.sub(r'\s+', '_', slug)
    # 转换为小写
    slug = slug.lower()
    # 移除开头和结尾的下划线
    slug = slug.strip('_')
    # 如果以数字开头，添加前缀
    if slug and slug[0].isdigit():
        slug = 'field_' + slug
    
    return slug




def get_or_create_deal_attributes(attr_manager: AttributeManager) -> Dict[str, str]:
    """获取或创建Deal属性"""
    print("=== 获取或创建Deal属性 ===")
    
    # 定义需要的属性
    required_attributes = [
        'industry', 'customer_scale', 'customer_position', 'need_follow_up', 'conversion_status',
        'priority', 'business_description', 'region', 'customer_name', 'has_campaign',
        'budget', 'customer_email', 'concerns', 'unmet_needs', 'todo', 'follow_up_reason',
        'first_contact_date', 'group_created'
    ]
    
    # 先获取现有属性
    from attio_objects.deals.deals_manager import DealsManager
    deals_manager = DealsManager(attr_manager.api_key)
    existing_attributes = deals_manager.list_attributes()
    
    attribute_mapping = {}
    
    if existing_attributes and existing_attributes.get('data'):
        print("找到现有属性:")
        for attr in existing_attributes['data']:
            api_slug = attr.get('api_slug', '')
            attr_id = attr.get('id', {}).get('attribute_id', '')
            title = attr.get('title', '')
            
            if api_slug in required_attributes:
                attribute_mapping[api_slug] = attr_id
                print(f"  ✅ {title} ({api_slug}) - {attr_id}")
    
    # 检查缺失的属性
    missing_attributes = set(required_attributes) - set(attribute_mapping.keys())
    
    if missing_attributes:
        print(f"\n缺失的属性: {missing_attributes}")
        print("需要手动创建这些属性或使用不同的API slug")
    else:
        print(f"\n✅ 所有需要的属性都已存在: {len(attribute_mapping)}个")
    
    return attribute_mapping


def parse_csv_file(file_path: str) -> List[Dict[str, str]]:
    """解析CSV文件"""
    print(f"=== 解析CSV文件: {file_path} ===")
    
    records = []
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            # 读取第一行作为标题
            first_line = file.readline().strip()
            print(f"CSV标题行: {first_line}")
            
            # 重新定位到文件开头
            file.seek(0)
            
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, start=2):
                # 跳过空行
                if not any(row.values()):
                    continue
                
                # 清理数据
                cleaned_row = {}
                for key, value in row.items():
                    if value is None:
                        cleaned_row[key] = ""
                    else:
                        cleaned_row[key] = str(value).strip()
                
                records.append(cleaned_row)
                print(f"解析第{row_num}行: {cleaned_row.get('公司名称', 'Unknown')}")
            
            print(f"✅ 成功解析CSV文件: {len(records)}条记录")
            return records
            
    except Exception as e:
        print(f"❌ 解析CSV文件失败: {e}")
        return []


def map_owner(负责人: str, workspace_manager: WorkspaceMembersManager) -> str:
    """映射负责人到workspace成员"""
    return workspace_manager.map_owner(负责人)


def create_deal_records(deals_manager: DealsManager, records: List[Dict[str, str]], 
                       attributes: Dict[str, str], workspace_manager: WorkspaceMembersManager, 
                       members_dict: Dict[str, str]) -> Dict[str, Any]:
    """创建Deal记录"""
    print("=== 创建Deal记录 ===")
    
    created_count = 0
    failed_count = 0
    created_deals = []
    
    for i, record in enumerate(records, 1):
        company_name = record.get('公司名称', f'Record_{i}')
        print(f"\n创建记录 {i}/{len(records)}: {company_name}")
        
        try:
            # 构建记录数据
            deal_values = {
                'name': company_name
            }
            
            # 映射负责人
            owner_email = map_owner(record.get('负责人', ''), workspace_manager)
            deal_values['owner'] = owner_email
            
            # 设置默认stage
            deal_values['stage'] = "In Progress"
            
            # 添加自定义属性
            field_mapping = {
                '公司名称': 'name',
                '优先级': 'priority',
                '公司业务介绍': 'business_description',
                '行业': 'industry',
                '地区': 'region',
                '客户规模': 'customer_scale',
                '客户姓名': 'customer_name',
                '客户方对接人职位': 'customer_position',
                '是否已创建campaign名称': 'has_campaign',
                '预算（如有）': 'budget',
                '客户邮箱': 'customer_email',
                '产品使用顾虑（付费卡点）': 'concerns',
                '未满足的功能需求（如有则填写）': 'unmet_needs',
                '是否需要跟进': 'need_follow_up',
                '会后 to do': 'todo',
                '跟进/不跟进原因': 'follow_up_reason',
                '初次沟通日期': 'first_contact_date',
                '1个月内转化情况': 'conversion_status',
                '是否拉群（微信 / 飞书 / Slack）': 'group_created'
            }
            
            for csv_field, attr_slug in field_mapping.items():
                value = record.get(csv_field, '').strip()
                if value and attr_slug in attributes:
                    deal_values[attr_slug] = value
            
            # 创建记录
            record_id = deals_manager.create_record(deal_values)
            
            if record_id:
                created_count += 1
                created_deals.append({
                    'record_id': record_id,
                    'name': company_name,
                    'owner': owner_email
                })
                print(f"✅ 记录创建成功: {company_name} ({record_id})")
            else:
                failed_count += 1
                print(f"❌ 记录创建失败: {company_name}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ 记录创建异常: {company_name} - {e}")
    
    print(f"\n=== 记录创建完成 ===")
    print(f"✅ 成功创建: {created_count}条记录")
    print(f"❌ 创建失败: {failed_count}条记录")
    
    return {
        'created_count': created_count,
        'failed_count': failed_count,
        'created_deals': created_deals
    }


def main():
    """主函数"""
    print("=== 开始导入demo.csv到Attio ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 1. 获取workspace成员
    workspace_manager = WorkspaceMembersManager(api_key)
    members = workspace_manager.get_workspace_members_dict()
    if not members:
        print("❌ 无法获取workspace成员，退出")
        return
    
    # 2. 创建属性管理器
    attr_manager = AttributeManager(api_key)
    
    # 3. 获取或创建Deal属性
    attributes = get_or_create_deal_attributes(attr_manager)
    if not attributes:
        print("❌ 没有找到任何属性，退出")
        return
    
    # 4. 解析CSV文件
    csv_file = "demo.csv"
    records = parse_csv_file(csv_file)
    if not records:
        print("❌ 没有解析到任何记录，退出")
        return
    
    # 5. 创建Deal管理器
    deals_manager = DealsManager(api_key)
    
    # 6. 创建Deal记录
    result = create_deal_records(deals_manager, records, attributes, workspace_manager, members)
    
    print(f"\n=== 导入完成 ===")
    print(f"总记录数: {len(records)}")
    print(f"成功创建: {result['created_count']}条记录")
    print(f"创建失败: {result['failed_count']}条记录")
    print(f"创建属性: {len(attributes)}个")


if __name__ == "__main__":
    main()
