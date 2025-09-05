# Attio API 工程化项目

这是一个工程化的Attio API集成项目，按照Attio对象来组织代码结构。

## 📁 项目结构

```
attio/
├── config.py                    # API配置类
├── attio_client.py              # 基础API客户端
├── attio_objects/               # 对象管理模块
│   ├── base_object.py          # 基础对象管理类
│   ├── attribute_manager.py    # 属性管理器
│   ├── deals/                  # Deals对象管理
│   │   └── deals_manager.py
│   ├── users/                  # Users对象管理
│   │   └── users_manager.py
│   ├── people/                 # People对象管理
│   │   └── people_manager.py
│   └── workspaces/             # Workspaces对象管理
│       └── workspaces_manager.py
├── tests/                      # 测试模块
│   ├── test_attributes_creation.py
│   └── test_deals_csv_import.py
├── demo.csv                    # 示例CSV数据
└── requirements.txt            # 项目依赖
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

在 `config.py` 中设置您的Attio API密钥：

```python
api_key = "your_api_key_here"
```

### 3. 使用示例

#### 创建Deals记录

```python
from attio_objects.deals.deals_manager import DealsManager

# 初始化Deals管理器
deals_manager = DealsManager("your_api_key")

# 从CSV文件批量创建Deal记录
result = deals_manager.batch_create_from_csv('demo.csv', limit=10)
print(f"成功创建: {result['created_count']}条记录")
```

#### 创建自定义属性

```python
from attio_objects.attribute_manager import AttributeManager

# 初始化属性管理器
attr_manager = AttributeManager("your_api_key")

# 创建文本属性
attr_id = attr_manager.create_text_attribute(
    object_name='deals',
    title='客户备注',
    api_slug='customer_notes',
    description='客户的备注信息'
)

# 创建选择属性
attr_id = attr_manager.create_select_attribute(
    object_name='deals',
    title='优先级',
    api_slug='priority',
    options=['高', '中', '低'],
    description='Deal的优先级'
)
```

## 📋 对象管理器功能

### DealsManager
- ✅ CSV文件解析和导入
- ✅ 批量创建Deal记录
- ✅ 负责人自动分配
- ✅ 预算金额处理
- ✅ 自定义属性支持

### UsersManager
- ✅ 用户记录创建
- ✅ 工作空间成员管理
- ✅ MongoDB数据导入

### PeopleManager
- ✅ 人员记录创建
- ✅ 联系信息管理
- ✅ 自定义属性支持

### WorkspacesManager
- ✅ 工作空间创建
- ✅ 用户关联管理
- ✅ 唯一ID生成

## 🧪 测试

运行属性创建测试：

```bash
python3 tests/test_attributes_creation.py
```

运行Deals CSV导入测试：

```bash
python3 tests/test_deals_csv_import.py
```

## 📊 测试结果

最新的属性创建测试结果：
- **Deals**: 16个属性已存在
- **Users**: 3个新属性创建成功
- **People**: 7个新属性创建成功
- **Workspaces**: 6个新属性创建成功
- **总体成功率**: 41%（主要是已存在属性冲突）

## 🔧 配置说明

### 负责人映射
在 `DealsManager` 中配置负责人邮箱映射：

```python
self.owner_mapping = {
    "黄晓敏": "ines@ahalab.ai",
    "Wels": "zehang.tian@ahalab.ai",
    "姚昱臣": "zehang.tian@ahalab.ai",
    "孙若婷": "zehang.tian@ahalab.ai",
}
```

### 选项字段默认值
配置select类型字段的默认值：

```python
self.option_defaults = {
    "行业": "Other",
    "客户规模": "Startup", 
    "客户方对接人职位": "Unknown",
    "是否需要跟进": "Yes",
    "1个月内转化情况": "Not Converted"
}
```

## 📝 注意事项

1. **API密钥安全**: 请妥善保管您的API密钥，不要提交到版本控制系统
2. **属性冲突**: 如果属性已存在，会返回409冲突错误，这是正常现象
3. **数据类型**: 确保CSV数据格式正确，特别是日期和数字字段
4. **批量限制**: 建议分批处理大量数据，避免API限制

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

MIT License