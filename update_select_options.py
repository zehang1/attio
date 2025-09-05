"""
更新Select属性的选项
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from attio_objects.deals.deals_manager import DealsManager
from attio_client import AttioClient
from config import AttioConfig


def update_select_options():
    """更新Select属性的选项"""
    print("=== 更新Select属性选项 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    config = AttioConfig(api_key)
    client = AttioClient(config)
    deals_manager = DealsManager(api_key)
    
    # 定义需要更新的select属性及其选项
    select_attributes = {
        'industry': {
            'title': '行业',
            'options': ['AI', 'Agency', '企服', '互联网', 'crypto', '医疗', '电商', '品牌', '金融', '玩具', '其他', '制造', '会展']
        },
        'customer_scale': {
            'title': '客户规模',
            'options': ['startup', '中型', '巨型', '大型', '其他']
        },
        'customer_position': {
            'title': '客户方对接人职位',
            'options': ['海外KOL负责人', 'Cofounder', 'CEO', '运营负责人', '市场负责人', '产品负责人', '市场执行', '未知']
        },
        'need_follow_up': {
            'title': '是否需要跟进',
            'options': ['是', '否']
        },
        'conversion_status': {
            'title': '1个月内转化情况',
            'options': ['已转化', '未转化']
        },
        'has_campaign': {
            'title': '是否已创建campaign',
            'options': ['是', '否']
        },
        'priority': {
            'title': '优先级',
            'options': ['P0—已付费', 'P2—未下单高意愿', 'P5—未下单低意愿/低预算', '非目标客户']
        },
        'group_created': {
            'title': '是否拉群',
            'options': ['微信', '飞书', 'Slack', 'No']
        }
    }
    
    # 获取现有属性
    attributes = deals_manager.list_attributes()
    
    if not attributes or not attributes.get('data'):
        print("❌ 没有找到属性")
        return
    
    # 找到需要更新的属性（包括被存档的）
    for attr in attributes['data']:
        api_slug = attr.get('api_slug', '')
        attr_id = attr.get('id', {}).get('attribute_id', '')
        title = attr.get('title', '')
        is_archived = attr.get('is_archived', False)
        
        if api_slug in select_attributes:
            print(f"\n更新属性: {title} ({api_slug})")
            
            # 准备更新数据 - 根据API文档格式
            update_data = {
                'data': {
                    'title': title,  # 保持原有标题
                    'is_archived': False,  # 确保属性不被存档
                    'config': {
                        'select': {
                            'options': [{'title': option} for option in select_attributes[api_slug]['options']]
                        }
                    }
                }
            }
            
            try:
                # 更新属性
                result = client._make_request('PATCH', f'/objects/deals/attributes/{attr_id}', data=update_data)
                
                if result:
                    print(f"✅ 成功更新: {title}")
                    print(f"   选项: {', '.join(select_attributes[api_slug]['options'])}")
                else:
                    print(f"❌ 更新失败: {title}")
                    
            except Exception as e:
                print(f"❌ 更新异常: {title} - {e}")
    
    print("\n=== 更新完成 ===")


if __name__ == "__main__":
    update_select_options()
