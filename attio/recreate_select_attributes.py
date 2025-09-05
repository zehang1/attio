"""
重新创建Select属性
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from attio_objects.deals.deals_manager import DealsManager
from attio_objects.attribute_manager import AttributeManager


def recreate_select_attributes():
    """重新创建Select属性"""
    print("=== 重新创建Select属性 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    deals_manager = DealsManager(api_key)
    attr_manager = AttributeManager(api_key)
    
    # 定义需要创建的select属性及其选项
    select_attributes = {
        'industry': {
            'title': '行业',
            'description': '客户所属行业',
            'options': ['AI', 'Agency', '企服', '互联网', 'crypto', '医疗', '电商', '品牌', '金融', '玩具', '其他', '制造', '会展']
        },
        'customer_scale': {
            'title': '客户规模',
            'description': '客户公司规模',
            'options': ['startup', '中型', '巨型', '大型', '其他']
        },
        'customer_position': {
            'title': '客户方对接人职位',
            'description': '客户方对接人的职位',
            'options': ['海外KOL负责人', 'Cofounder', 'CEO', '运营负责人', '市场负责人', '产品负责人', '市场执行', '未知']
        },
        'need_follow_up': {
            'title': '是否需要跟进',
            'description': '是否需要跟进此客户',
            'options': ['是', '否']
        },
        'conversion_status': {
            'title': '1个月内转化情况',
            'description': '1个月内的转化情况',
            'options': ['已转化', '未转化']
        },
        'has_campaign': {
            'title': '是否已创建campaign',
            'description': '是否已为此客户创建campaign',
            'options': ['是', '否']
        },
        'priority': {
            'title': '优先级',
            'description': '客户优先级',
            'options': ['P0—已付费', 'P2—未下单高意愿', 'P5—未下单低意愿/低预算', '非目标客户']
        },
        'group_created': {
            'title': '是否拉群',
            'description': '是否已拉群',
            'options': ['微信', '飞书', 'Slack', 'No']
        }
    }
    
    # 创建属性
    for api_slug, config in select_attributes.items():
        print(f"\n创建属性: {config['title']} ({api_slug})")
        
        try:
            result = attr_manager.create_select_attribute(
                object_name='deals',
                title=config['title'],
                api_slug=api_slug,
                description=config['description'],
                options=config['options']
            )
            
            if result:
                print(f"✅ 成功创建: {config['title']}")
                print(f"   选项: {', '.join(config['options'])}")
            else:
                print(f"❌ 创建失败: {config['title']}")
                
        except Exception as e:
            print(f"❌ 创建异常: {config['title']} - {e}")
    
    print("\n=== 创建完成 ===")


if __name__ == "__main__":
    recreate_select_attributes()
