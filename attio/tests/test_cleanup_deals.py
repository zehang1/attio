"""
测试Deals清理功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attio_objects.deals.deals_manager import DealsManager


def test_cleanup_deals():
    """测试清理所有Deals数据"""
    print("=== 测试Deals清理功能 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化Deals管理器
    deals_manager = DealsManager(api_key)
    
    # 清理所有Deals数据
    result = deals_manager.cleanup_all_deals()
    
    print(f"\n=== 清理结果 ===")
    print(f"记录删除: {result['records']['deleted_count']}成功, {result['records']['failed_count']}失败")
    print(f"属性删除: {result['attributes']['deleted_count']}成功, {result['attributes']['failed_count']}失败")
    print(f"总计: {result['total_deleted']}成功, {result['total_failed']}失败")


def test_delete_records_only():
    """只测试删除记录"""
    print("=== 测试只删除Deal记录 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化Deals管理器
    deals_manager = DealsManager(api_key)
    
    # 只删除记录
    result = deals_manager.delete_all_deal_records()
    
    print(f"\n=== 删除记录结果 ===")
    print(f"成功删除: {result['deleted_count']}条记录")
    print(f"删除失败: {result['failed_count']}条记录")


def test_delete_attributes_only():
    """只测试删除属性"""
    print("=== 测试只删除自定义属性 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化Deals管理器
    deals_manager = DealsManager(api_key)
    
    # 只删除自定义属性
    result = deals_manager.delete_all_custom_attributes()
    
    print(f"\n=== 删除属性结果 ===")
    print(f"成功删除: {result['deleted_count']}个属性")
    print(f"删除失败: {result['failed_count']}个属性")


def test_delete_specific_records():
    """测试删除指定记录"""
    print("=== 测试删除指定记录 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化Deals管理器
    deals_manager = DealsManager(api_key)
    
    # 示例记录ID列表（请替换为实际的记录ID）
    record_ids = [
        # "record_id_1",
        # "record_id_2",
        # "record_id_3"
    ]
    
    if not record_ids:
        print("⚠️  请在record_ids列表中添加要删除的记录ID")
        print("示例：")
        print('record_ids = ["1eec4535-30a1-4bc0-be24-e255d3fb5ac5", "another-record-id"]')
        return
    
    # 删除指定记录
    result = deals_manager.delete_specific_records(record_ids)
    
    print(f"\n=== 删除记录结果 ===")
    print(f"成功删除: {result['deleted_count']}条记录")
    print(f"删除失败: {result['failed_count']}条记录")


def main():
    """主测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='测试Deals清理功能')
    parser.add_argument('--all', action='store_true', help='清理所有数据（记录和属性）')
    parser.add_argument('--records', action='store_true', help='只删除记录')
    parser.add_argument('--attributes', action='store_true', help='只删除属性')
    parser.add_argument('--specific', action='store_true', help='删除指定记录')
    
    args = parser.parse_args()
    
    if args.all:
        test_cleanup_deals()
    elif args.records:
        test_delete_records_only()
    elif args.attributes:
        test_delete_attributes_only()
    elif args.specific:
        test_delete_specific_records()
    else:
        # 默认显示帮助信息
        print("=== Deals清理工具 ===")
        print("使用方法：")
        print("  python3 tests/test_cleanup_deals.py --all          # 清理所有数据")
        print("  python3 tests/test_cleanup_deals.py --records      # 只删除记录")
        print("  python3 tests/test_cleanup_deals.py --attributes   # 只删除属性")
        print("  python3 tests/test_cleanup_deals.py --specific     # 删除指定记录")
        print("\n注意：")
        print("- 记录删除需要手动提供记录ID")
        print("- 属性删除需要在Attio界面手动操作")
        print("- 建议先使用 --attributes 查看需要删除的属性列表")


if __name__ == "__main__":
    main()
