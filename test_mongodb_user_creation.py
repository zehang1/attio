"""
从MongoDB读取members数据并创建Attio user对象
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from config import AttioConfig
from attio_objects.users.users_manager import UsersManager
import json


def test_mongodb_user_creation():
    """测试从MongoDB读取一个用户并创建user对象"""
    print("=== 测试MongoDB用户创建 ===")
    
    # 初始化配置
    config = AttioConfig('68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da')
    
    # 连接MongoDB
    try:
        client = MongoClient(config.get_mongodb_uri())
        # 指定数据库名称，通常MongoDB URI中会包含数据库名，或者使用默认的数据库名
        db = client.get_database('aha-prod')  # 或者使用其他数据库名
        members_collection = db.members
        
        print(f"✅ 成功连接到MongoDB")
        print(f"数据库: {db.name}")
        print(f"集合: members")
        
        # 读取一个用户进行测试
        member = members_collection.find_one()
        
        if member:
            print(f"\n=== 找到测试用户 ===")
            print(f"用户ID: {member.get('_id')}")
            print(f"姓名: {member.get('clerkName', 'N/A')}")
            print(f"邮箱: {member.get('clerkPrimaryEmail', 'N/A')}")
            print(f"创建时间: {member.get('createdAt', 'N/A')}")
            
            # 准备user数据
            user_data = {
                'email': member.get('clerkPrimaryEmail', ''),
                'user_id': str(member.get('_id', '')),
                'name': member.get('clerkName', '')
            }
            
            print(f"\n=== 准备创建User对象 ===")
            print(f"User数据: {json.dumps(user_data, indent=2, ensure_ascii=False)}")
            
            # 创建UsersManager并创建user
            users_manager = UsersManager(config.api_key)
            
            try:
                result = users_manager.create_user(user_data)
                if result:
                    print(f"✅ 成功创建User对象: {result}")
                else:
                    print(f"❌ 创建User对象失败")
            except Exception as e:
                print(f"❌ 创建User对象异常: {e}")
                
        else:
            print("❌ 没有找到任何用户数据")
            
    except Exception as e:
        print(f"❌ MongoDB连接失败: {e}")
    finally:
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    test_mongodb_user_creation()
