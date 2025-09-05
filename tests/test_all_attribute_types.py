"""
测试所有Attio属性类型的创建
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attio_objects.attribute_manager import AttributeManager


def test_all_attribute_types():
    """测试所有Attio属性类型的创建"""
    print("=== 测试所有Attio属性类型创建 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    attr_manager = AttributeManager(api_key)
    
    # 测试对象名称
    test_object = "deals"
    
    # 定义所有属性类型的测试用例
    test_cases = [
        {
            'name': 'text',
            'title': '测试文本属性',
            'api_slug': 'test_text',
            'description': '这是一个测试文本属性'
        },
        {
            'name': 'number',
            'title': '测试数字属性',
            'api_slug': 'test_number',
            'description': '这是一个测试数字属性'
        },
        {
            'name': 'checkbox',
            'title': '测试复选框属性',
            'api_slug': 'test_checkbox',
            'description': '这是一个测试复选框属性'
        },
        {
            'name': 'currency',
            'title': '测试货币属性',
            'api_slug': 'test_currency',
            'description': '这是一个测试货币属性'
        },
        {
            'name': 'date',
            'title': '测试日期属性',
            'api_slug': 'test_date',
            'description': '这是一个测试日期属性'
        },
        {
            'name': 'timestamp',
            'title': '测试时间戳属性',
            'api_slug': 'test_timestamp',
            'description': '这是一个测试时间戳属性'
        },
        {
            'name': 'rating',
            'title': '测试评分属性',
            'api_slug': 'test_rating',
            'description': '这是一个测试评分属性'
        },
        {
            'name': 'status',
            'title': '测试状态属性',
            'api_slug': 'test_status',
            'description': '这是一个测试状态属性',
            'options': ['进行中', '已完成', '已取消']
        },
        {
            'name': 'select',
            'title': '测试选择属性',
            'api_slug': 'test_select',
            'description': '这是一个测试选择属性',
            'options': ['选项1', '选项2', '选项3']
        },
        {
            'name': 'multiselect',
            'title': '测试多选属性',
            'api_slug': 'test_multiselect',
            'description': '这是一个测试多选属性',
            'options': ['标签1', '标签2', '标签3', '标签4']
        },
        {
            'name': 'record-reference',
            'title': '测试记录引用属性',
            'api_slug': 'test_record_reference',
            'description': '这是一个测试记录引用属性',
            'allowed_objects': ['people', 'companies']  # 需要实际的对象ID
        },
        {
            'name': 'actor-reference',
            'title': '测试参与者引用属性',
            'api_slug': 'test_actor_reference',
            'description': '这是一个测试参与者引用属性'
        },
        {
            'name': 'location',
            'title': '测试位置属性',
            'api_slug': 'test_location',
            'description': '这是一个测试位置属性'
        },
        {
            'name': 'domain',
            'title': '测试域名属性',
            'api_slug': 'test_domain',
            'description': '这是一个测试域名属性'
        },
        {
            'name': 'email-address',
            'title': '测试邮箱地址属性',
            'api_slug': 'test_email_address',
            'description': '这是一个测试邮箱地址属性'
        },
        {
            'name': 'phone-number',
            'title': '测试电话号码属性',
            'api_slug': 'test_phone_number',
            'description': '这是一个测试电话号码属性'
        }
    ]
    
    success_count = 0
    failed_count = 0
    results = {}
    
    for test_case in test_cases:
        print(f"\n--- 测试 {test_case['name']} 属性 ---")
        
        try:
            # 根据属性类型调用不同的方法
            if test_case['name'] == 'text':
                attr_id = attr_manager.create_text_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'number':
                attr_id = attr_manager.create_number_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'checkbox':
                attr_id = attr_manager.create_checkbox_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'currency':
                attr_id = attr_manager.create_currency_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'date':
                attr_id = attr_manager.create_date_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'timestamp':
                attr_id = attr_manager.create_timestamp_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'rating':
                attr_id = attr_manager.create_rating_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'status':
                attr_id = attr_manager.create_status_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    options=test_case.get('options', []),
                    description=test_case['description']
                )
            elif test_case['name'] == 'select':
                attr_id = attr_manager.create_select_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    options=test_case.get('options', []),
                    description=test_case['description']
                )
            elif test_case['name'] == 'multiselect':
                attr_id = attr_manager.create_multiselect_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    options=test_case.get('options', []),
                    description=test_case['description']
                )
            elif test_case['name'] == 'record-reference':
                attr_id = attr_manager.create_record_reference_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    allowed_objects=test_case['allowed_objects'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'actor-reference':
                attr_id = attr_manager.create_actor_reference_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'location':
                attr_id = attr_manager.create_location_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'domain':
                attr_id = attr_manager.create_domain_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'email-address':
                attr_id = attr_manager.create_email_address_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            elif test_case['name'] == 'phone-number':
                attr_id = attr_manager.create_phone_number_attribute(
                    object_name=test_object,
                    title=test_case['title'],
                    api_slug=test_case['api_slug'],
                    description=test_case['description']
                )
            else:
                print(f"❌ 不支持的属性类型: {test_case['name']}")
                attr_id = None
            
            if attr_id:
                success_count += 1
                results[test_case['name']] = {'status': 'success', 'id': attr_id}
                print(f"✅ {test_case['name']} 属性创建成功: {attr_id}")
            else:
                failed_count += 1
                results[test_case['name']] = {'status': 'failed'}
                print(f"❌ {test_case['name']} 属性创建失败")
                
        except Exception as e:
            failed_count += 1
            results[test_case['name']] = {'status': 'failed', 'error': str(e)}
            print(f"❌ {test_case['name']} 属性创建异常: {e}")
    
    # 输出测试结果
    print(f"\n=== 测试结果汇总 ===")
    print(f"✅ 成功创建: {success_count}个属性")
    print(f"❌ 创建失败: {failed_count}个属性")
    print(f"📊 成功率: {success_count/(success_count+failed_count)*100:.1f}%")
    
    print(f"\n=== 详细结果 ===")
    for attr_type, result in results.items():
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"  {status_icon} {attr_type}: {result['status']}")
        if result['status'] == 'success':
            print(f"      ID: {result['id']}")
        elif 'error' in result:
            print(f"      错误: {result['error']}")
    
    return results


def test_specific_attribute_type(attr_type: str):
    """测试特定属性类型"""
    print(f"=== 测试 {attr_type} 属性类型 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    attr_manager = AttributeManager(api_key)
    
    test_object = "deals"
    
    # 根据属性类型调用相应方法
    if attr_type == 'text':
        attr_id = attr_manager.create_text_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'number':
        attr_id = attr_manager.create_number_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'checkbox':
        attr_id = attr_manager.create_checkbox_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'currency':
        attr_id = attr_manager.create_currency_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'date':
        attr_id = attr_manager.create_date_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'timestamp':
        attr_id = attr_manager.create_timestamp_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'rating':
        attr_id = attr_manager.create_rating_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'status':
        attr_id = attr_manager.create_status_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'select':
        attr_id = attr_manager.create_select_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            options=['选项1', '选项2', '选项3'],
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'record-reference':
        attr_id = attr_manager.create_record_reference_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            allowed_objects=['people', 'companies'],
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'actor-reference':
        attr_id = attr_manager.create_actor_reference_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'location':
        attr_id = attr_manager.create_location_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'domain':
        attr_id = attr_manager.create_domain_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'email-address':
        attr_id = attr_manager.create_email_address_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    elif attr_type == 'phone-number':
        attr_id = attr_manager.create_phone_number_attribute(
            object_name=test_object,
            title=f'测试{attr_type}属性',
            api_slug=f'test_{attr_type}',
            description=f'这是一个测试{attr_type}属性'
        )
    else:
        print(f"❌ 不支持的属性类型: {attr_type}")
        return None
    
    if attr_id:
        print(f"✅ {attr_type} 属性创建成功: {attr_id}")
    else:
        print(f"❌ {attr_type} 属性创建失败")
    
    return attr_id


def main():
    """主测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='测试Attio属性类型创建')
    parser.add_argument('--type', type=str, help='测试特定属性类型')
    parser.add_argument('--all', action='store_true', help='测试所有属性类型')
    
    args = parser.parse_args()
    
    if args.type:
        test_specific_attribute_type(args.type)
    elif args.all:
        test_all_attribute_types()
    else:
        # 默认测试所有属性类型
        test_all_attribute_types()


if __name__ == "__main__":
    main()
