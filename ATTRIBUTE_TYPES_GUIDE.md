# Attio属性类型创建指南

## 支持的属性类型

### ✅ 完全支持的属性类型

| 属性类型 | 方法名 | 是否需要选项 | 说明 |
|---------|--------|-------------|------|
| `text` | `create_text_attribute` | ❌ | 文本属性 |
| `number` | `create_number_attribute` | ❌ | 数字属性 |
| `checkbox` | `create_checkbox_attribute` | ❌ | 复选框属性 |
| `currency` | `create_currency_attribute` | ❌ | 货币属性（已配置USD默认值） |
| `date` | `create_date_attribute` | ❌ | 日期属性 |
| `timestamp` | `create_timestamp_attribute` | ❌ | 时间戳属性 |
| `rating` | `create_rating_attribute` | ❌ | 评分属性 |
| `select` | `create_select_attribute` | ✅ | 单选属性 |
| `multiselect` | `create_multiselect_attribute` | ✅ | 多选属性 |
| `actor-reference` | `create_actor_reference_attribute` | ❌ | 参与者引用属性 |
| `location` | `create_location_attribute` | ❌ | 位置属性 |
| `phone-number` | `create_phone_number_attribute` | ❌ | 电话号码属性 |

### ⚠️ 有限支持的属性类型

| 属性类型 | 方法名 | 限制 | 说明 |
|---------|--------|------|------|
| `status` | `create_status_attribute` | 只能在自定义对象使用 | 状态属性（deals等标准对象不支持） |
| `record-reference` | `create_record_reference_attribute` | 需要对象ID | 记录引用属性 |

### ❌ 不支持的属性类型

| 属性类型 | 原因 |
|---------|------|
| `domain` | Attio暂不支持此类型 |
| `email-address` | Attio暂不支持此类型 |

## 使用示例

### 1. 创建文本属性

```python
from attio_objects.attribute_manager import AttributeManager

attr_manager = AttributeManager("your_api_key")
attr_id = attr_manager.create_text_attribute(
    object_name="deals",
    title="客户备注",
    api_slug="customer_notes",
    description="客户的备注信息"
)
```

### 2. 创建单选属性

```python
attr_id = attr_manager.create_select_attribute(
    object_name="deals",
    title="优先级",
    api_slug="priority",
    options=["高", "中", "低"],
    description="Deal的优先级"
)
```

### 3. 创建多选属性

```python
attr_id = attr_manager.create_multiselect_attribute(
    object_name="deals",
    title="标签",
    api_slug="tags",
    options=["重要", "紧急", "跟进", "已完成"],
    description="Deal的标签"
)
```

### 4. 创建状态属性（仅限自定义对象）

```python
attr_id = attr_manager.create_status_attribute(
    object_name="custom_object",  # 必须是自定义对象
    title="状态",
    api_slug="status",
    options=["进行中", "已完成", "已取消"],
    description="对象状态"
)
```

### 5. 创建记录引用属性

```python
attr_id = attr_manager.create_record_reference_attribute(
    object_name="deals",
    title="关联公司",
    api_slug="associated_company",
    allowed_objects=["company_object_id"],  # 需要实际的对象ID
    description="关联的公司记录"
)
```

## 测试

运行所有属性类型测试：

```bash
python3 tests/test_all_attribute_types.py --all
```

测试特定属性类型：

```bash
python3 tests/test_all_attribute_types.py --type select
python3 tests/test_all_attribute_types.py --type multiselect
```

## 注意事项

1. **API Slug唯一性**: 每个对象内的api_slug必须唯一
2. **选项配置**: select、multiselect、status属性需要提供options参数
3. **对象限制**: status属性只能在自定义对象上使用
4. **记录引用**: record-reference需要提供有效的对象ID列表
5. **货币配置**: currency属性已预配置USD作为默认货币

## 成功率统计

- **总体成功率**: 73.3% (11/15)
- **完全支持**: 11种属性类型
- **有限支持**: 2种属性类型  
- **不支持**: 2种属性类型
