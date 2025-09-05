"""
测试Deals CSV导入功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attio_objects.deals.deals_manager import DealsManager


def test_deals_csv_import():
    """测试Deals CSV导入功能"""
    print("=== 测试Deals CSV导入功能 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化Deals管理器
    deals_manager = DealsManager(api_key)
    
    # 测试CSV解析
    print("\n--- 测试CSV解析 ---")
    csv_records = deals_manager.parse_csv_file('demo.csv')
    print(f"解析到 {len(csv_records)} 条记录")
    
    if csv_records:
        print("前3条记录预览:")
        for i, record in enumerate(csv_records[:3], 1):
            print(f"  记录{i}: {record.get('公司', 'N/A')} - {record.get('客户', 'N/A')}")
    
    # 测试单条记录创建
    print("\n--- 测试单条记录创建 ---")
    if csv_records:
        test_record = csv_records[0]
        print(f"测试记录: {test_record.get('公司', 'N/A')} - {test_record.get('客户', 'N/A')}")
        
        record_id = deals_manager.create_deal_from_csv(test_record)
        if record_id:
            print(f"✅ 成功创建记录: {record_id}")
            
            # 验证创建结果
            created_record = deals_manager.get_record(record_id)
            if created_record:
                print("✅ 记录验证成功")
                values = created_record.get('values', {})
                print(f"  Deal名称: {values.get('name', [{}])[0].get('value', 'N/A')}")
                print(f"  负责人: {values.get('owner', [{}])[0].get('referenced_actor_id', 'N/A')}")
            else:
                print("❌ 记录验证失败")
        else:
            print("❌ 记录创建失败")
    
    # 测试批量创建（限制3条）
    print("\n--- 测试批量创建（限制3条） ---")
    result = deals_manager.batch_create_from_csv('demo.csv', limit=3)
    
    print(f"批量创建结果:")
    print(f"  成功: {result['created_count']}条")
    print(f"  失败: {result['failed_count']}条")
    
    if result['created_deals']:
        print("  创建的记录:")
        for deal in result['created_deals']:
            print(f"    - {deal['company']} ({deal['customer']}): {deal['record_id']}")


def main():
    """主测试函数"""
    test_deals_csv_import()


if __name__ == "__main__":
    main()
