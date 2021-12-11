# MAC Address Databas 
MAC 地址厂商信息数据库

## 功能
通过 MAC 地址确定设备对应的制造商信息。 

TODO:
补充更多的厂商信息.
- [ ] 厂商通用称呼
- [ ] 厂商 LOGO
- [ ] 品牌信息

## 原理
常见的 48 位 MAC 地址事实上是由 IEEE （电气电子工程师学会）规定的，原本的正式名称是 EUI-48 (48 Bits Extended Unique Identifiers)。而 EUI-48 中包含有 OUI (Organizationally Unique Identifier)，这是 IEEE 管理并分配给相关硬件制造商的唯一标识符，通过对此部分的识别可以确定设备的制造商。

> EUI-48 和 EUI-64 标识符最普遍的用法是作为全球唯一的网络地址（有时称为 MAC 地址），如各种标准中规定的那样。例如，根据 IEEE 标准 802 ，EUI-48 通常被用作硬件接口的地址，历史上使用 "MAC-48"的名称。另一个例子是，根据 IEEE 标准 1588，EUI-64 可作为一个时钟的标识符。IEEE 标准 802 还规定了 EUI-64 用于 64 位全球唯一的网络地址。
>
> > EUI-48 and EUI-64 identifiers are most commonly used as globally unique network addresses (sometimes called MAC addresses), as specified in various standards. For example, an EUI- 48 is commonly used as the address of a hardware interface according to IEEE Std 802, historically using the name “MAC-48”. As another example, an EUI- 64 may serve as the identifier of a clock, per IEEE Std 1588. IEEE Std 802 also specifies EUI-64 use for 64-bit globally unique network addresses.

**本项目以 IEEE 官网作为数据源，整合数据库并每日自动同步。**

## 使用说明
### 支持的数据格式
- [CSV](mac.csv)
- [sqlite](mac.db)
rr
### 字段说明
| 字段名 | 字段含义 | 示例 |
| ----- | ------- | --- |
| `registry`| 分配的 OUI 类型 | MA-L |
| `assignment` | IEEE 分配的组织唯一识别码 | 002272 |
| `organization_name` | 制造商的注册名称 | American Micro-Fuel Device Corp. |
| `organization_address` | 制造商的注册地址 | 2181 Buchanan Loop Ferndale WA US 98248 |


### 查询步骤
1. 取 MAC 地址前 **24** 位（对应到常用的杠分十六进制表示就是前三组的 6 个 十六进制字符，如 AA-BB-CC-DD-EE-FF 的 AABBCC）\
   与数据库的 `assignment` 字段进行精确匹配。
2. 若匹配结果的 `organization_name` 字段为 `IEEE Registration Authority` ，则继续进行下一步；\
   否则直接返回当前匹配结果。
3. 取 MAC 地址前 **28** 位（对应到常用的杠分十六进制表示就是前三组的 7 个 十六进制字符，如 AA-BB-CC-DD-EE-FF 的 AABBCCD）\
   与数据库的 `assignment` 字段进行精确匹配。
4. 若匹配结果的 `organization_name` 字段为 `IEEE Registration Authority` ，则继续进行下一步；否则直接返回当前匹配结果。
5. 取 MAC 地址前 **36** 位（对应到常用的杠分十六进制表示就是前三组的 7 个 十六进制字符，如 AA-BB-CC-DD-EE-FF 的 AABBCCD）\
   与数据库的 `assignment` 字段进行精确匹配。
6. 若有结果直接返回，无结果返回空。

### 官方查询页面

https://regauth.standards.ieee.org/standards-ra-web/pub/view.html

### 官方数据发布

1. MAC Address Block Large (**MA-L**) [TXT](http://standards-oui.ieee.org/oui/oui.txt) [CSV](http://standards-oui.ieee.org/oui/oui.csv)
2. MAC Address Block Medium (**MA-M**) [TXT](http://standards-oui.ieee.org/oui28/mam.txt) [CSV](http://standards-oui.ieee.org/oui28/mam.csv)
3. MAC Address Block Small (**MA-S**) [TXT](http://standards-oui.ieee.org/oui36/oui36.txt) [CSV](http://standards-oui.ieee.org/oui36/oui36.csv)

### 官方匹配指导

> 如果前 24 位与分配给 IEEE RA 的 OUI 相匹配，那么对前 28 位或 36 位的搜索可能会显示出 MA-M 或 MA-S 的分配。\
> 如果在 MA-S 搜索中没有发现 OUI-36，那么对前 24 位或 28 位的搜索可能会发现一个 MA-L 或 MA-M 分配，OUI-36 是由分配块的一个成员创建的。
>
> > If the first 24 bits match an OUI assigned to the IEEE RA, then a search of the first 28 or 36 bits may reveal an MA-M or MA-S assignment. If the OUI-36 is not found in an MA-S search, then a search of the first 24 or 28 bits may reveal an MA-L or MA-M assignment from which the OUI-36 has been created from a member of the assigned block.
{% hint style="warning" %}
最终的查询结果也不总是完全准确的哦！

> 请您注意，所列的公司和编号在产品实施中可能并不总是很明显。一些制造商将部件制造分包出去，另一些制造商在其产品中包括注册公司的所有 MAC（MA-L、MA-M、MA-S）。
>
> > Your attention is called to the fact that the firms and numbers listed may not always be obvious in product implementation. Some manufacturers subcontract component manufacture and others include registered firms' All MAC (MA-L, MA-M, MA-S) in their products.
{% endhint %}