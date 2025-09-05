"""
MongoDB用户数据同步到Attio的业务逻辑类
"""
import sys
import os
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import AttioConfig
from attio_objects.users.users_manager import UsersManager


class MongoDBUserSync:
    """MongoDB用户数据同步到Attio的业务逻辑类"""
    
    def __init__(self, api_key: str, mongodb_uri: Optional[str] = None):
        """
        初始化同步器
        
        Args:
            api_key: Attio API密钥
            mongodb_uri: MongoDB连接URI，如果不提供则从配置中读取
        """
        self.config = AttioConfig(api_key)
        self.mongodb_uri = mongodb_uri or self.config.get_mongodb_uri()
        self.users_manager = UsersManager(api_key)
        self.client = None
        self.db = None
        
    def connect_mongodb(self) -> bool:
        """
        连接到MongoDB
        
        Returns:
            连接是否成功
        """
        try:
            self.client = MongoClient(self.mongodb_uri)
            # 测试连接
            self.client.admin.command('ping')
            
            # 获取数据库
            self.db = self.client.get_database('aha-prod')
            print(f"✅ 成功连接到MongoDB: {self.db.name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB连接失败: {e}")
            return False
        except Exception as e:
            print(f"❌ MongoDB连接异常: {e}")
            return False
    
    def disconnect_mongodb(self):
        """断开MongoDB连接"""
        if self.client:
            self.client.close()
            print("✅ 已断开MongoDB连接")
    
    def get_mongodb_users(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        从MongoDB获取用户数据
        
        Args:
            limit: 限制返回的用户数量，None表示获取所有用户
            
        Returns:
            用户数据列表
        """
        if self.db is None:
            print("❌ MongoDB未连接")
            return []
        
        try:
            members_collection = self.db.members
            
            # 构建查询
            query = {}
            cursor = members_collection.find(query)
            
            if limit:
                cursor = cursor.limit(limit)
            
            users = list(cursor)
            print(f"✅ 从MongoDB获取到 {len(users)} 个用户")
            return users
            
        except Exception as e:
            print(f"❌ 获取MongoDB用户数据失败: {e}")
            return []
    
    def transform_mongodb_user_to_attio(self, mongodb_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        将MongoDB用户数据转换为Attio用户数据格式
        
        Args:
            mongodb_user: MongoDB用户数据
            
        Returns:
            Attio用户数据格式
        """
        return {
            'email': mongodb_user.get('clerkPrimaryEmail', ''),
            'user_id': str(mongodb_user.get('_id', '')),
            'name': mongodb_user.get('clerkName', ''),
            # 可以添加更多字段映射
            'avatar_url': mongodb_user.get('clerkAvatarUrl', ''),
            'last_active_at': mongodb_user.get('clerkLastActiveAt'),
            'last_sign_in_at': mongodb_user.get('clerkLastSignInAt'),
            'has_im_account': mongodb_user.get('hasIMAccount', False)
        }
    
    def check_user_exists(self, email: str) -> Optional[str]:
        """
        检查用户是否已存在
        
        Args:
            email: 用户邮箱
            
        Returns:
            如果用户存在返回用户ID，否则返回None
        """
        try:
            # 查询现有用户
            result = self.users_manager.client._make_request(
                'POST', 
                '/objects/users/records/query',
                data={
                    'data': {
                        'values': {
                            'primary_email_address': email
                        },
                        'limit': 1
                    }
                }
            )
            
            if result and result.get('data'):
                user_id = result['data'][0].get('id', {}).get('record_id')
                return user_id
            
            return None
            
        except Exception as e:
            print(f"❌ 检查用户存在性失败: {e}")
            return None
    
    def sync_single_user(self, mongodb_user: Dict[str, Any], skip_existing: bool = True) -> Optional[str]:
        """
        同步单个用户到Attio
        
        Args:
            mongodb_user: MongoDB用户数据
            skip_existing: 是否跳过已存在的用户
            
        Returns:
            创建的Attio用户记录ID，失败返回None
        """
        try:
            # 转换数据格式
            attio_user_data = self.transform_mongodb_user_to_attio(mongodb_user)
            
            # 验证必需字段
            if not attio_user_data.get('email'):
                print(f"❌ 用户缺少邮箱地址: {mongodb_user.get('_id')}")
                return None
            
            if not attio_user_data.get('name'):
                print(f"❌ 用户缺少姓名: {mongodb_user.get('_id')}")
                return None
            
            # 检查用户是否已存在
            if skip_existing:
                existing_user_id = self.check_user_exists(attio_user_data['email'])
                if existing_user_id:
                    print(f"⏭️  用户已存在，跳过: {attio_user_data['name']} ({attio_user_data['email']}) -> {existing_user_id}")
                    return existing_user_id
            
            # 创建用户
            user_id = self.users_manager.create_user(attio_user_data)
            
            if user_id:
                print(f"✅ 成功同步用户: {attio_user_data['name']} ({attio_user_data['email']}) -> {user_id}")
            else:
                print(f"❌ 同步用户失败: {attio_user_data['name']} ({attio_user_data['email']})")
            
            return user_id
            
        except Exception as e:
            print(f"❌ 同步用户异常: {mongodb_user.get('_id')} - {e}")
            return None
    
    def sync_all_users(self, limit: Optional[int] = None, dry_run: bool = False) -> Dict[str, Any]:
        """
        同步所有用户到Attio
        
        Args:
            limit: 限制同步的用户数量，None表示同步所有用户
            dry_run: 是否为试运行模式（只显示将要同步的数据，不实际创建）
            
        Returns:
            同步结果统计
        """
        print(f"=== 开始同步MongoDB用户到Attio ===")
        print(f"模式: {'试运行' if dry_run else '实际同步'}")
        print(f"限制: {limit if limit else '无限制'}")
        
        # 连接MongoDB
        if not self.connect_mongodb():
            return {'success': False, 'error': 'MongoDB连接失败'}
        
        try:
            # 获取用户数据
            mongodb_users = self.get_mongodb_users(limit)
            
            if not mongodb_users:
                print("❌ 没有找到任何用户数据")
                return {'success': False, 'error': '没有找到用户数据'}
            
            # 统计信息
            stats = {
                'total': len(mongodb_users),
                'success': 0,
                'failed': 0,
                'skipped': 0,
                'created_users': []
            }
            
            # 同步每个用户
            for i, mongodb_user in enumerate(mongodb_users, 1):
                user_id = mongodb_user.get('_id')
                user_name = mongodb_user.get('clerkName', 'Unknown')
                user_email = mongodb_user.get('clerkPrimaryEmail', 'N/A')
                
                print(f"\n处理用户 {i}/{len(mongodb_users)}: {user_name} ({user_email})")
                
                if dry_run:
                    # 试运行模式：只显示将要同步的数据
                    attio_user_data = self.transform_mongodb_user_to_attio(mongodb_user)
                    print(f"  将要创建的用户数据: {attio_user_data}")
                    stats['skipped'] += 1
                else:
                    # 实际同步
                    created_user_id = self.sync_single_user(mongodb_user)
                    
                    if created_user_id:
                        stats['success'] += 1
                        stats['created_users'].append({
                            'mongodb_id': str(user_id),
                            'attio_id': created_user_id,
                            'name': user_name,
                            'email': user_email
                        })
                    else:
                        stats['failed'] += 1
            
            # 输出统计结果
            print(f"\n=== 同步完成 ===")
            print(f"总用户数: {stats['total']}")
            print(f"成功同步: {stats['success']}")
            print(f"同步失败: {stats['failed']}")
            print(f"跳过处理: {stats['skipped']}")
            
            return {
                'success': True,
                'stats': stats
            }
            
        except Exception as e:
            print(f"❌ 同步过程异常: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            self.disconnect_mongodb()
    
    def test_single_user_sync(self) -> bool:
        """
        测试同步单个用户
        
        Returns:
            测试是否成功
        """
        print("=== 测试单个用户同步 ===")
        
        if not self.connect_mongodb():
            return False
        
        try:
            # 获取一个用户进行测试
            mongodb_users = self.get_mongodb_users(limit=1)
            
            if not mongodb_users:
                print("❌ 没有找到测试用户")
                return False
            
            # 同步测试用户
            result = self.sync_single_user(mongodb_users[0])
            
            if result:
                print("✅ 单个用户同步测试成功")
                return True
            else:
                print("❌ 单个用户同步测试失败")
                return False
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            return False
        finally:
            self.disconnect_mongodb()


def main():
    """主函数 - 用于测试"""
    # 初始化同步器
    sync = MongoDBUserSync('68ffdf41d1a437041cd0bb08b1e42c1545af3de1a0885615bd5de5d72e7279da')
    
    # 测试单个用户同步
    if sync.test_single_user_sync():
        print("\n" + "="*50)
        
        # 询问是否继续同步所有用户
        response = input("单个用户测试成功，是否继续同步所有用户？(y/n): ")
        if response.lower() == 'y':
            # 先进行试运行
            print("\n=== 试运行模式 ===")
            sync.sync_all_users(limit=5, dry_run=True)
            
            # 询问是否实际同步
            response = input("\n试运行完成，是否进行实际同步？(y/n): ")
            if response.lower() == 'y':
                sync.sync_all_users(limit=10)  # 限制同步10个用户进行测试


if __name__ == "__main__":
    main()
