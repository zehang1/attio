"""
Workspace成员管理器
"""
from typing import Dict, List, Any, Optional
from ..base_object import BaseAttioObject


class WorkspaceMembersManager:
    """Workspace成员管理器"""
    
    def __init__(self, api_key: str):
        """
        初始化Workspace成员管理器
        
        Args:
            api_key: Attio API密钥
        """
        self.api_key = api_key
        self.config = None
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化客户端"""
        import sys
        import os
        
        # 添加项目根目录到Python路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        from config import AttioConfig
        from attio_client import AttioClient
        
        self.config = AttioConfig(api_key=self.api_key)
        self.client = AttioClient(self.config)
    
    def list_workspace_members(self) -> List[Dict[str, Any]]:
        """列出所有workspace成员"""
        try:
            result = self.client._make_request('GET', '/workspace_members')
            return result.get('data', [])
        except Exception as e:
            print(f"❌ 获取workspace成员列表失败: {e}")
            return []
    
    def get_workspace_members_dict(self) -> Dict[str, str]:
        """获取workspace成员字典，key为邮箱，value为member_id"""
        print("=== 获取Workspace成员信息 ===")
        
        members = self.list_workspace_members()
        
        if not members:
            print("❌ 没有找到workspace成员")
            return {}
        
        members_dict = {}
        for member in members:
            email = member.get('email_address', '')
            member_id = member.get('id', {}).get('workspace_member_id', '')
            if email and member_id:
                members_dict[email] = member_id
        
        print(f"找到 {len(members_dict)} 个workspace成员:")
        for email in members_dict.keys():
            print(f"  - {email}")
        
        return members_dict
    
    def get_workspace_member_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱获取workspace成员信息"""
        members = self.list_workspace_members()
        
        for member in members:
            if member.get('email_address') == email:
                return member
        
        return None
    
    def map_owner(self, 负责人: str) -> str:
        """映射负责人到workspace成员邮箱"""
        if 负责人 == "黄晓敏":
            return "ines@ahalab.ai"
        else:
            return "zehang.tian@ahalab.ai"
    
    def validate_owner_email(self, email: str, members_dict: Dict[str, str] = None) -> bool:
        """验证负责人邮箱是否在workspace成员中"""
        if members_dict is None:
            members_dict = self.get_workspace_members_dict()
        return email in members_dict
