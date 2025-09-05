"""
测试每个对象的属性创建
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attio_objects.attribute_manager import AttributeManager
from attio_objects.deals.deals_manager import DealsManager
from attio_objects.users.users_manager import UsersManager
from attio_objects.people.people_manager import PeopleManager
from attio_objects.workspaces.workspaces_manager import WorkspacesManager


def test_deals_attributes():
    """测试Deals对象属性创建"""
    print("=== 测试Deals对象属性创建 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化属性管理器和Deals管理器
    attr_manager = AttributeManager(api_key)
    deals_manager = DealsManager(api_key)
    
    # 获取Deals属性定义
    deals_attributes = deals_manager.get_deal_attributes_definition()
    
    # 批量创建属性
    result = attr_manager.batch_create_attributes('deals', deals_attributes)
    
    print(f"Deals属性创建结果: 成功{result['success_count']}个, 失败{result['failed_count']}个")
    return result


def test_users_attributes():
    """测试Users对象属性创建"""
    print("\n=== 测试Users对象属性创建 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化属性管理器和Users管理器
    attr_manager = AttributeManager(api_key)
    users_manager = UsersManager(api_key)
    
    # 获取Users属性定义
    users_attributes = users_manager.get_user_attributes_definition()
    
    # 批量创建属性
    result = attr_manager.batch_create_attributes('users', users_attributes)
    
    print(f"Users属性创建结果: 成功{result['success_count']}个, 失败{result['failed_count']}个")
    return result


def test_people_attributes():
    """测试People对象属性创建"""
    print("\n=== 测试People对象属性创建 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化属性管理器和People管理器
    attr_manager = AttributeManager(api_key)
    people_manager = PeopleManager(api_key)
    
    # 获取People属性定义
    people_attributes = people_manager.get_people_attributes_definition()
    
    # 批量创建属性
    result = attr_manager.batch_create_attributes('people', people_attributes)
    
    print(f"People属性创建结果: 成功{result['success_count']}个, 失败{result['failed_count']}个")
    return result


def test_workspaces_attributes():
    """测试Workspaces对象属性创建"""
    print("\n=== 测试Workspaces对象属性创建 ===")
    
    api_key = "68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da"
    
    # 初始化属性管理器和Workspaces管理器
    attr_manager = AttributeManager(api_key)
    workspaces_manager = WorkspacesManager(api_key)
    
    # 获取Workspaces属性定义
    workspaces_attributes = workspaces_manager.get_workspaces_attributes_definition()
    
    # 批量创建属性
    result = attr_manager.batch_create_attributes('workspaces', workspaces_attributes)
    
    print(f"Workspaces属性创建结果: 成功{result['success_count']}个, 失败{result['failed_count']}个")
    return result


def main():
    """主测试函数"""
    print("开始测试所有对象的属性创建...")
    
    # 测试各个对象的属性创建
    deals_result = test_deals_attributes()
    users_result = test_users_attributes()
    people_result = test_people_attributes()
    workspaces_result = test_workspaces_attributes()
    
    # 汇总结果
    total_success = (deals_result['success_count'] + users_result['success_count'] + 
                    people_result['success_count'] + workspaces_result['success_count'])
    total_failed = (deals_result['failed_count'] + users_result['failed_count'] + 
                   people_result['failed_count'] + workspaces_result['failed_count'])
    
    print(f"\n=== 总体测试结果 ===")
    print(f"✅ 总成功: {total_success}个属性")
    print(f"❌ 总失败: {total_failed}个属性")
    print(f"📊 成功率: {total_success/(total_success+total_failed)*100:.1f}%")
    
    # 显示详细结果
    print(f"\n=== 详细结果 ===")
    print(f"Deals: {deals_result['success_count']}成功, {deals_result['failed_count']}失败")
    print(f"Users: {users_result['success_count']}成功, {users_result['failed_count']}失败")
    print(f"People: {people_result['success_count']}成功, {people_result['failed_count']}失败")
    print(f"Workspaces: {workspaces_result['success_count']}成功, {workspaces_result['failed_count']}失败")


if __name__ == "__main__":
    main()
