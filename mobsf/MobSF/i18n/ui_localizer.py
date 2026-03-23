# -*- coding: utf_8 -*-
"""Localized UI text helpers for legacy MobSF templates."""

from collections import OrderedDict
import re

from bs4 import BeautifulSoup
from bs4 import NavigableString

SKIPPED_TAGS = {
    'code',
    'pre',
    'script',
    'style',
    'textarea',
}
TRANSLATABLE_ATTRS = {
    'alt',
    'aria-label',
    'data-original-title',
    'placeholder',
    'title',
    'value',
}
WHITESPACE_RE = re.compile(r'\s+')
HEADING_TEXT_RE = re.compile(r'^[A-Za-z0-9/&(),.: _-]+$')
ZH_HANS = 'zh-hans'
TOKEN_TRANSLATIONS = {
    'ABNORMAL': '异常',
    'ABUSED': '滥用',
    'ACCESS': '访问',
    'ACTION': '操作',
    'ACTIVITIES': 'Activity',
    'ACTIVITY': 'Activity',
    'ANALYSIS': '分析',
    'ANDROID': 'Android',
    'ANTI': '反',
    'API': 'API',
    'APP': '应用',
    'APPS': '应用',
    'APPLICATION': '应用',
    'APPX': 'APPX',
    'ARGUMENTS': '参数',
    'ATS': 'ATS',
    'AUTHENTICATION': '认证',
    'AV': 'AV',
    'AVERAGE': '平均',
    'AVAILABLE': '可用',
    'BASE64': 'Base64',
    'BEHAVIOUR': '行为',
    'BINARY': '二进制',
    'BIT': '位数',
    'BROWSABLE': 'Browsable',
    'BUILD': '构建',
    'BUNDLE': 'Bundle',
    'CALLED': '调用',
    'CANDIDATE': '候选',
    'CANDIDATES': '候选',
    'CATEGORIES': '类别',
    'CATEGORY': '分类',
    'CERTIFICATE': '证书',
    'CITY': '城市',
    'CLIPBOARD': '剪贴板',
    'CLEARTEXT': '明文',
    'CODE': '代码',
    'COMMENT': '备注',
    'COMPARE': '对比',
    'COMPILER': '编译器',
    'COMPONENT': '组件',
    'CONTENT': '内容',
    'COOKIES': 'Cookie',
    'CORELLIUM': 'Corellium',
    'COUNTRY': '国家',
    'CREATE': '创建',
    'CREDENTIAL': '凭据',
    'CRYPTO': '加密',
    'CUSTOM': '自定义',
    'DATA': '数据',
    'DATABASE': '数据库',
    'DECODED': '解码后',
    'DECOMPILED': '反编译',
    'DEBUG': '调试',
    'DELETE': '删除',
    'DEEPLINK': 'Deeplink',
    'DETECTION': '检测',
    'DETECTIONS': '检测结果',
    'DETAILS': '详情',
    'DESCRIPTION': '描述',
    'DEFAULT': '默认',
    'DEVELOPER': '开发者',
    'DEVICE': '设备',
    'DEVICES': '设备',
    'DIFF': '对比',
    'DIRECTORY': '目录',
    'DOMAIN': '域名',
    'DOWNLOAD': '下载',
    'DROPPER': 'Dropper',
    'DUMP': '转储',
    'DYNAMIC': '动态',
    'EMAIL': '邮箱',
    'EMAILS': '邮箱地址',
    'ENCRYPTED': '已加密',
    'EXPORTED': '导出',
    'EVIDENCE': '证据',
    'FILE': '文件',
    'FILES': '文件',
    'FILTER': '过滤',
    'FILTERS': '过滤器',
    'FINDINGS': '发现项',
    'FIREBASE': 'Firebase',
    'FRAMEWORK': 'Framework',
    'FRIDA': 'Frida',
    'FULL': '完整',
    'GENERATE': '生成',
    'GEOLOCATION': '地理位置',
    'GET': '获取',
    'GRADE': '等级',
    'HANDLER': '处理器',
    'HEADER': '头部',
    'HIGH': '高危',
    'HOST': '主机',
    'HOTSPOT': '热点',
    'HTTP': 'HTTP',
    'HTTPS': 'HTTPS',
    'IDENTIFIER': '标识符',
    'ID': 'ID',
    'INFO': '信息',
    'INFORMATION': '信息',
    'INVENTORY': '清单',
    'ISSUE': '问题',
    'ITEM': '项目',
    'ITEMS': '项目',
    'IOS': 'iOS',
    'JSON': 'JSON',
    'KEYCHAIN': '钥匙串',
    'LABEL': '标签',
    'LIBRARY': '库',
    'LIVE': '实时',
    'LOCATION': '位置',
    'LOCATIONS': '位置',
    'LOGCAT': 'Logcat',
    'LOGS': '日志',
    'LOOKUP': '查询',
    'LOW': '低危',
    'MAIN': '主',
    'MALWARE': '恶意软件',
    'MANAGEMENT': '管理',
    'MANIFEST': 'Manifest',
    'MATCHED': '匹配到的',
    'MAX': '最高',
    'MEDIUM': '中危',
    'METHOD': '方法',
    'METHODS': '方法',
    'MISCONFIGURATION': '配置错误',
    'MIME': 'MIME',
    'MIN': '最低',
    'MOBSFY': 'MobSFy',
    'MONITOR': '监控',
    'NAME': '名称',
    'NETWORK': '网络',
    'NIAP': 'NIAP',
    'NOTES': '说明',
    'OPTIONS': '选项',
    'OTHER': '其他',
    'PACKAGE': '包名',
    'PARAM': '参数',
    'PARAMS': '参数',
    'PASSWORD': '密码',
    'PASTEBOARD': '剪贴板',
    'PATH': '路径',
    'PATTERNS': '模式',
    'PDF': 'PDF',
    'PERMISSION': '权限',
    'PERMISSIONS': '权限',
    'PLATFORM': '平台',
    'POLICY': '策略',
    'PORT': '端口',
    'PREFIXES': '前缀',
    'PRICE': '价格',
    'PRINT': '打印',
    'PRIVACY': '隐私',
    'PROBE': '探测',
    'PROTECTION': '保护',
    'PROVIDERS': '内容提供者',
    'QUERIES': '查询',
    'QUEUE': '队列',
    'RAW': '原始',
    'REACHABLE': '可达',
    'REASON': '原因',
    'RECEIVERS': '接收器',
    'RECONNAISSANCE': '情报侦察',
    'REGION': '地区',
    'REPORT': '报告',
    'REPORTS': '报告',
    'REQUIRED': '必填',
    'RESULT': '结果',
    'RESULTS': '结果',
    'RESPONSE': '响应',
    'RETURN': '返回',
    'RISK': '风险',
    'RUNTIME': '运行时',
    'RUN': '运行',
    'RULE': '规则',
    'RULES': '规则',
    'SAMPLE': '示例',
    'SCAN': '扫描',
    'SCHEMES': 'Scheme',
    'SCORE': '评分',
    'SCORECARD': '评分卡',
    'SCREENSHOT': '截图',
    'SCREENSHOTS': '截图',
    'SEARCH': '搜索',
    'SECRETS': '密钥',
    'SECURE': '安全',
    'SECURITY': '安全',
    'SERVER': '服务器',
    'SERVICES': '服务',
    'SEVERITY': '严重程度',
    'SHARED': '共享',
    'SIGNATURE': '签名',
    'SIGNER': '签名者',
    'SMALI': 'Smali',
    'SOURCE': '源码',
    'STATIC': '静态',
    'STATUS': '状态',
    'STANDARDS': '标准',
    'STORE': '商店',
    'STORAGE': '存储',
    'STRING': '字符串',
    'STRINGS': '字符串',
    'SUMMARY': '摘要',
    'SUPPRESSION': '抑制',
    'SUPPRESSIONS': '抑制规则',
    'SUPPRESSED': '已抑制',
    'SUGGESTED': '建议的',
    'SUPPORTED': '支持的',
    'SYMBOLS': '符号',
    'SYSTEM': '系统',
    'TARGET': '目标',
    'TEST': '测试',
    'TESTER': '测试',
    'TESTS': '测试',
    'TEXT': '文本',
    'TLS': 'TLS',
    'TITLE': '标题',
    'TOTAL': '总计',
    'TRACKER': '跟踪器',
    'TRACKERS': '跟踪器',
    'TRANSPORT': '传输',
    'TYPE': '类型',
    'UPLOAD': '上传',
    'URL': 'URL',
    'URLS': 'URL',
    'USER': '用户',
    'USERDEFAULTS': 'UserDefaults',
    'VALUE': '值',
    'VERSION': '版本',
    'VIEW': '查看',
    'VIRUSTOTAL': 'VirusTotal',
    'WARNING': '警告',
    'WEBSITE': '网站',
    'WINDOWS': 'Windows',
    'XML': 'XML',
}

UI_TEXT_TRANSLATIONS = {
    ZH_HANS: {
        'Forbidden': '禁止访问',
        'Not Found': '未找到',
        'Internal Server Error': '服务器内部错误',
        'Server Error (500)': '服务器错误 (500)',
        'Error': '错误',
        'Version': '版本',
        'Search': '搜索',
        'DOCS': '文档',
        'ABOUT': '关于',
        'RECENT SCANS': '最近扫描',
        'STATIC ANALYZER': '静态分析',
        'DYNAMIC ANALYZER': '动态分析',
        'DONATE ♥': '捐赠 ♥',
        'SCANS': '扫描',
        'Admin': '管理员',
        'Viewer': '查看者',
        'Maintainer': '维护者',
        'Change Password': '修改密码',
        'User Management': '用户管理',
        'Logout': '退出登录',
        'Sign in to access': '登录以继续',
        'Remember Me': '记住我',
        'Sign In': '登录',
        'Sign in with SSO': '使用 SSO 登录',
        'Create a User': '创建用户',
        'Select Role': '选择角色',
        'Create User': '创建用户',
        'Add User': '添加用户',
        'No Users Available': '暂无用户',
        'Username': '用户名',
        'User': '用户',
        'Email': '邮箱',
        'Role': '角色',
        'Manage': '管理',
        'Delete': '删除',
        'Update Password': '更新密码',
        'Current Password': '当前密码',
        'New Password': '新密码',
        'Confirm Password': '确认密码',
        'Password': '密码',
        'About Mobile Security Framework': '关于 Mobile Security Framework',
        'Author:': '作者：',
        'Active Collaborators': '活跃协作者',
        'API Docs': 'API 文档',
        'API Key:': 'API Key：',
        'Static Analysis': '静态分析',
        'Upload a File': '上传文件',
        'Scan a File': '开始扫描',
        'Display Live Scan Logs': '显示实时扫描日志',
        'Search a Scan': '搜索扫描结果',
        'Display Recent Scans': '显示最近扫描记录',
        'Display Scan Tasks': '显示扫描任务',
        'Delete a Scan': '删除扫描结果',
        'App Scorecard': '应用评分卡',
        'Download PDF Report': '下载 PDF 报告',
        'Generate JSON Report': '生成 JSON 报告',
        'View Source Files': '查看源文件',
        'Donate to MobSF Project': '支持 MobSF 项目',
        "You're Awesome! Thank you for your support ♥": '感谢你的支持 ♥',
        'Github Sponsors': 'GitHub Sponsors',
        'Paypal Donations': 'PayPal 捐赠',
        'You can also donate to MobSF project through PayPal.': (
            '你也可以通过 PayPal 向 MobSF 项目捐赠。'
        ),
        'MobSF Dynamic Analyzer': 'MobSF 动态分析',
        'Android Dynamic Analyzer': 'Android 动态分析',
        'Perform Dynamic Analysis of Android Applications.': (
            '对 Android 应用执行动态分析。'
        ),
        'iOS Dynamic Analyzer': 'iOS 动态分析',
        'Perform Dynamic Analysis of iOS Applications.': (
            '对 iOS 应用执行动态分析。'
        ),
        'Drop anywhere!': '拖到任意位置即可上传！',
        'Upload & Analyze': '上传并分析',
        'Drag & Drop anywhere!': '可在任意位置拖放文件！',
        'Download & Scan Package': '输入应用包名并下载扫描',
        'Recent Scans': '最近扫描',
        'Scan Queue': '扫描队列',
        'APP': '应用',
        'FILE': '文件',
        'TYPE': '类型',
        'HASH': '哈希',
        'SCAN DATE': '扫描日期',
        'ACTIONS': '操作',
        'MobSF Scorecard': 'MobSF 评分卡',
        'Static Report': '静态报告',
        'Dynamic Report': '动态报告',
        'scan not completed': '扫描尚未完成',
        'Scan Task': '扫描任务',
        'Filename': '文件名',
        'Timeline': '时间线',
        'Status': '状态',
        'Zipped Source Code Instruction': '源码压缩包说明',
        'Eclipse Project:': 'Eclipse 项目：',
        'Android Studio Project:': 'Android Studio 项目：',
        'iOS Project:': 'iOS 项目：',
        'Dynamic Analyzer': '动态分析',
        'Information': '信息',
        'Scan Options': '扫描选项',
        'Signer Certificate': '签名证书',
        'Permissions': '权限',
        'Android API': 'Android API',
        'Deeplink Analysis': 'Deeplink 分析',
        'Browsable Activities': 'Browsable Activity',
        'Security Analysis': '安全分析',
        'Network Security': '网络安全',
        'Certificate Analysis': '证书分析',
        'Manifest Analysis': 'Manifest 分析',
        'Code Analysis': '代码分析',
        'Binary Analysis': '二进制分析',
        'NIAP Analysis': 'NIAP 分析',
        'File Analysis': '文件分析',
        'Firebase Analysis': 'Firebase 分析',
        'Malware Analysis': '恶意软件分析',
        'Malware Lookup': '恶意软件查询',
        'APKiD Analysis': 'APKiD 分析',
        'Behaviour Analysis': '行为分析',
        'VirusTotal': 'VirusTotal',
        'Abused Permissions': '滥用权限',
        'Server Locations': '服务器位置',
        'Domain Malware Check': '域名恶意检测',
        'Reconnaissance': '情报侦察',
        'URLs': 'URL',
        'Emails': '邮箱地址',
        'Trackers': '跟踪器',
        'Hardcoded Secrets': '硬编码密钥',
        'Strings': '字符串',
        'URL Schemes': 'URL Scheme',
        'iOS API': 'iOS API',
        'Transport Security': '传输安全',
        'Binary Code Analysis': '二进制代码分析',
        'Dylib & Framework Analysis': 'Dylib 与 Framework 分析',
        'Static Library Analysis': '静态库分析',
        'Files': '文件',
        'PDF Report': 'PDF 报告',
        'Print Report': '打印报告',
        'APP SCORES': '应用评分',
        'MobSF Application Security Scorecard': 'MobSF 应用安全评分卡',
        'Security Score': '安全评分',
        'Risk Rating': '风险等级',
        'Grade': '等级',
        'Severity Distribution (%)': '严重程度分布 (%)',
        'Privacy Risk': '隐私风险',
        'Findings': '发现项',
        'High': '高危',
        'Medium': '中危',
        'Info': '信息',
        'Secure': '安全',
        'Need to Investigate': '待进一步调查',
        'Hotspot': '热点',
        'Components': '组件',
        'Comparing': '对比',
        'APP INFORMATION': '应用信息',
        'File name': '文件名',
        'Certificate': '证书',
        'ICON': '图标',
        'COMPONENTS': '组件',
        'ACTIVITIES': 'Activity',
        'EXPORTED ACTIVITIES': '导出 Activity',
        'SERVICES': '服务',
        'EXPORTED SERVICES': '导出服务',
        'RECEIVERS': '接收器',
        'EXPORTED RECEIVERS': '导出接收器',
        'PROVIDERS': '内容提供者',
        'EXPORTED PROVIDERS': '导出内容提供者',
        'Common': '共同项',
        'Java Source': 'Java 源码',
        'Smali Source': 'Smali 源码',
        'Find by filename:': '按文件名查找：',
        'Find by content:': '按内容查找：',
        'Clear': '清空',
        'No results found': '未找到结果',
        'File:': '文件：',
        'App Name': '应用名称',
        'Publisher': '发布者',
        'Arch': '架构',
        'VirusTotal Detection': 'VirusTotal 检测',
        'FILE INFORMATION': '文件信息',
        'Show Screen': '显示屏幕',
        'Remove Root CA': '移除 Root CA',
        'Unset HTTP(S) Proxy': '取消 HTTP(S) 代理',
        'TLS/SSL Security Tester': 'TLS/SSL 安全测试',
        'Exported Activity Tester': '导出 Activity 测试',
        'Activity Tester': 'Activity 测试',
        'Get Dependencies': '获取依赖',
        'Take a Screenshot': '截屏',
        'Logcat Stream': 'Logcat 实时流',
        'Live API Monitor': '实时 API 监控',
        'Generate Report': '生成报告',
        'Errors': '错误',
        'Run App': '运行应用',
        'Default Frida Scripts': '默认 Frida 脚本',
        'API Monitoring': 'API 监控',
        'SSL Pinning Bypass': '绕过 SSL Pinning',
        'Root Detection Bypass': '绕过 Root 检测',
        'Debugger Check Bypass': '绕过调试器检测',
        'Clipboard Monitor': '剪贴板监控',
        'Auxiliary Frida Scripts': '辅助 Frida 脚本',
        'Frida API Monitor': 'Frida API 监控',
        'Xposed API Monitor': 'Xposed API 监控',
        'Screenshots': '截图',
        'Runtime Dependencies': '运行时依赖',
        'Base64 Strings': 'Base64 字符串',
        'Frida Logs': 'Frida 日志',
        'API Monitor': 'API 监控',
        'Data Snip:': '数据片段：',
        'NAME': '名称',
        'CLASS': '类',
        'METHOD': '方法',
        'ARGUMENTS': '参数',
        'RESULT': '结果',
        'RETURN VALUE': '返回值',
        'CALLED FROM': '调用来源',
        'Stop Streaming': '停止推流',
        'Cannot authenticate with Corellium. Please ensure that': (
            '无法通过 Corellium 鉴权，请确认已配置'
        ),
        'is configured.': '。',
        'Corellium Project ID:': 'Corellium 项目 ID：',
        'Refresh': '刷新',
        'Create VM': '创建虚拟机',
        'VM': '虚拟机',
        'VERSION': '版本',
        'STATE': '状态',
        'PROGRESS': '进度',
        'Start': '启动',
        'Stop': '停止',
        'Unpause': '恢复',
        'Reboot': '重启',
        'Destroy': '销毁',
        'Start Network Capture': '开始网络抓包',
        'Download Live Packet Capture': '下载实时抓包',
        'System Logs': '系统日志',
        'Jailbreak Detection Bypass': '绕过越狱检测',
        'Trace Frida Scripts': '追踪 Frida 脚本',
        'Network': '网络',
        'Crypto': '加密',
        'Cookies': 'Cookie',
        'File Access': '文件访问',
        'Json Data': 'JSON 数据',
        'Sqlite Query': 'SQLite 查询',
        'Data Directory': '数据目录',
        'Keychain': '钥匙串',
        'NSLog': 'NSLog',
        'Text Inputs': '文本输入',
        'URL Credential Storage': 'URL 凭据存储',
        'User Defaults': '用户默认配置',
        'Pasteboard': '剪贴板',
        'UserDefaults Data': 'UserDefaults 数据',
        'Keychain Data': '钥匙串数据',
        'App Data Directory': '应用数据目录',
        'URLs Invoked': '调用的 URL',
        'JSON Data': 'JSON 数据',
        'App Logs': '应用日志',
        'App Cookies': '应用 Cookie',
        'Crypto Operations': '加密操作',
        'Credential Storage': '凭据存储',
        'SQLite Queries': 'SQLite 查询',
        'SQLite Database': 'SQLite 数据库',
        'System logs': '系统日志',
        'MobSF Static Analysis Report': 'MobSF 静态分析报告',
        'ANDROID STATIC ANALYSIS REPORT': 'Android 静态分析报告',
        'IOS STATIC ANALYSIS REPORT': 'iOS 静态分析报告',
        'WINDOWS STATIC ANALYSIS REPORT': 'Windows 静态分析报告',
        'File Name:': '文件名：',
        'Package Name:': '包名：',
        'Identifier:': '标识符：',
        'Publisher:': '发布者：',
        'Scan Date:': '扫描日期：',
        'Average CVSS Score:': '平均 CVSS 分数：',
        'App Security Score:': '应用安全分：',
        'Trackers Detection:': '跟踪器检测：',
        'FINDINGS SEVERITY': '漏洞严重程度',
        'HIGH': '高危',
        'MEDIUM': '中危',
        'INFO': '信息',
        'Size:': '大小：',
        'MD5:': 'MD5：',
        'SHA1:': 'SHA1：',
        'SHA256:': 'SHA256：',
        'recommended': '推荐',
        'Detected Android Version:': '检测到的 Android 版本：',
        'Android instance:': 'Android 实例：',
        'MobSFy Android Runtime': 'MobSFy Android 运行环境',
        'Android Runtime not found!': '未找到 Android 运行环境！',
        'If this error persists, Please set': '如果此错误持续出现，请设置',
        'or via environment variable': '或通过环境变量设置',
        'MobSF Dynamic Analyzer Supports': 'MobSF 动态分析支持',
        '• Genymotion Android VM': '• Genymotion Android 虚拟机',
        '• Android Emulator AVD': '• Android Emulator AVD',
        '• Corellium Android VM': '• Corellium Android 虚拟机',
        'Application Security Scorecard': '应用安全评分卡',
        'Analyze': '分析',
        'Choose File': '选择文件',
        'Choose an instance for Dynamic Analysis:': '选择用于动态分析的实例：',
        'Compare Apps': '对比应用',
        'Delete Scan': '删除扫描结果',
        'Delete Suppressions': '删除抑制规则',
        'Destroy iOS VM in Corellium': '在 Corellium 中销毁 iOS 虚拟机',
        'Download ZIP': '下载 ZIP',
        'Dumpsys Logs': 'Dumpsys 日志',
        'Enter "help" for more information.': '输入 “help” 获取更多信息。',
        'Enumerate Class Methods': '枚举类方法',
        'Enumerate Classes': '枚举类',
        'Enumerate Loaded Classes': '枚举已加载类',
        'Execute ADB Commands': '执行 ADB 命令',
        'Externally Reachable Components': '外部可达组件',
        'Features': '特性',
        'Features:': '特性：',
        'File Upload': '文件上传',
        'File Name': '文件名',
        'For Android version': '对于 Android 版本',
        'Get Apps for Dynamic Analysis': '获取可用于动态分析的应用',
        'Google Map': 'Google 地图',
        'Handler Evidence': '处理器证据',
        'Handler Locations:': '处理器位置：',
        'Hosts:': '主机：',
        'Identifier': '标识符',
        'Info.plist': 'Info.plist',
        'Inject': '注入',
        'Injected Code': '已注入代码',
        'Injected Frida Script': '已注入的 Frida 脚本',
        'Install or Remove MobSF Root CA': '安装或移除 MobSF Root CA',
        'Libraries': '库',
        'List Suppressions': '列出抑制规则',
        'Locations:': '位置：',
        'Logcat Logs': 'Logcat 日志',
        'Name': '名称',
        'Next': '下一页',
        'No': '否',
        'OK': '确定',
        'Other Candidate Deeplinks': '其他候选深度链接',
        'Ports:': '端口：',
        'Previous': '上一页',
        'Privacy Policy': '隐私政策',
        'Providers': '内容提供者',
        'Providers:': '内容提供者：',
        'Raw Logs': '原始日志',
        'Receivers': '接收器',
        'Receivers:': '接收器：',
        'Region:': '地区：',
        'Remove App': '移除应用',
        'Rescan': '重新扫描',
        'Result:': '结果：',
        'Run': '运行',
        'Scan Logs': '扫描日志',
        'Score': '分数',
        'Score:': '分数：',
        'Search Class Pattern': '搜索类模式',
        'Select App to Compare': '选择要对比的应用',
        'Select a process': '选择一个进程',
        'Services': '服务',
        'Services:': '服务：',
        'Show Files': '显示文件',
        'Start Dynamic Analysis': '开始动态分析',
        'Status:': '状态：',
        'Stop App': '停止应用',
        'Supported Devices': '支持的设备',
        'Supported Platforms': '支持的平台',
        'Suppress by Files': '按文件抑制',
        'Suppress by Rule': '按规则抑制',
        'Suppression Rules': '抑制规则',
        'Take Screenshot': '截屏',
        'Text Input': '文本输入',
        'Timestamp': '时间戳',
        'Title': '标题',
        'Title:': '标题：',
        'Trackers Detection': '跟踪器检测',
        'Type:': '类型：',
        'Upload & Install': '上传并安装',
        'Upload to Device': '上传到设备',
        'View All': '查看全部',
        'View Logcat': '查看 Logcat',
        'View Report': '查看报告',
        'View Source': '查看源代码',
        'View Strings': '查看字符串',
        'View Suppressions': '查看抑制规则',
        'Warning': '警告',
        'Why:': '原因：',
        'XML Files': 'XML 文件',
        'Yes': '是',
        'English': '英语',
        'Content-Type:': '内容类型：',
        'Content:': '内容：',
        'Success Response:': '成功响应：',
        'Error Response:': '错误响应：',
        'Sample Call:': '调用示例：',
        'Param Name': '参数名',
        'Param Value': '参数值',
        'Required': '必填',
        'OR': '或',
        'Or': '或',
        'NO': '否',
        'IP:': 'IP：',
        'hash of the scan': '扫描结果的哈希',
        'iOS instance id (Available from /api/v1/ios/dynamic_analysis)': (
            'iOS 实例 ID（可从 /api/v1/ios/dynamic_analysis 获取）'
        ),
        'iOS VM instance identifier': 'iOS 虚拟机实例标识符',
        'Event': '事件',
        'Suppress the rule': '抑制该规则',
        'This app may communicate with the following OFAC sanctioned list of countries.': (  # noqa: E501
            '该应用可能与以下受 OFAC 制裁名单约束的国家进行通信。'
        ),
        'Latitude:': '纬度：',
        'Longitude:': '经度：',
        'STANDARDS': '标准',
        'CVSS V2:': 'CVSS V2：',
        'CWE:': 'CWE：',
        'OWASP Top 10:': 'OWASP Top 10：',
        'OWASP MASVS:': 'OWASP MASVS：',
        'SignatureOrSystem': '签名或系统级',
        'Mime Types:': 'MIME 类型：',
        'Paths:': '路径：',
        'SUPPRESSED': '已抑制',
        'SBOM': '软件物料清单',
        'Average CVSS': '平均 CVSS',
        'Manage Suppressions': '管理抑制规则',
        'POSSIBLE HARDCODED SECRETS': '可能存在的硬编码密钥',
        'Suppression Type': '抑制方式',
        'By Rule ID': '按规则 ID',
        'By Files': '按文件',
        'SUPPRESSED:': '已抑制：',
        'Attach': '附加',
        'Triage Report': '分诊报告',
        'MetaDefender Report': 'MetaDefender 报告',
        'PLAYSTORE INFORMATION': 'Play 商店信息',
        'Privacy link': '隐私链接',
        'SCOPE': '范围',
        'only from these files': '仅限以下文件',
        'REQUIREMENT': '要求',
        'FEATURE': '特性',
        'RULE ID': '规则 ID',
        'LIBRARIES': '库',
        'Developer ID': '开发者 ID',
        'Developer Website': '开发者网站',
        'TLS Pinning/Certificate Transparency Bypass Test': (
            'TLS Pinning / 证书透明度绕过测试'
        ),
        'comma separated default hooks to load': (
            '要加载的默认 Hook，使用逗号分隔'
        ),
        'comma separated auxiliary hooks to load': (
            '要加载的辅助 Hook，使用逗号分隔'
        ),
        'user defined frida code to load': '要加载的用户自定义 Frida 代码',
        'class name to perform method enumeration when `enum_methods` auxiliary_hook is specified': (  # noqa: E501
            '指定 `enum_methods` 辅助 Hook 时，用于执行方法枚举的类名'
        ),
        'pattern to search when `search_class` auxiliary_hook is specified': (
            '指定 `search_class` 辅助 Hook 时使用的搜索模式'
        ),
        'class name to trace when `trace_class` auxiliary_hook is specified': (
            '指定 `trace_class` 辅助 Hook 时要追踪的类名'
        ),
        'spawn/session/ps. The default action is spawn': (
            'spawn/session/ps。默认动作为 spawn'
        ),
        'New package name to attach': '要附加的新包名',
        'Process id of the new package to attach': '要附加的新包的进程 ID',
        'MD5 hash of the IPA file': 'IPA 文件的 MD5 哈希',
        'Main Activity': '主 Activity',
        'Target SDK': '目标 SDK',
        'Min SDK': '最低 SDK',
        'Max SDK': '最高 SDK',
        'Installs': '安装量',
        'Release Date': '发布日期',
        'View AndroidManifest.xml': '查看 AndroidManifest.xml',
        'CODE MAPPINGS': '代码映射',
        'Best-effort external entry inventory synthesized from manifest filters, exported components, code literals, and deeplink handler evidence.': (  # noqa: E501
            '基于 Manifest 过滤器、导出组件、代码字面量与深度链接处理证据综合生成的外部入口清单（尽力而为）。'
        ),
        'No externally reachable deeplink candidates were identified from the manifest, code, or bundled resources.': (  # noqa: E501
            '未在 Manifest、代码或打包资源中识别到外部可达的深度链接候选项。'
        ),
        'Literal Locations:': '字面量位置：',
        'HANDLER KIND': '处理器类型',
        'SNIPPET': '代码片段',
        'are the top permissions that are widely abused by known malware.': (
            '是已知恶意软件最常滥用的高风险权限。'
        ),
        'are permissions that are commonly abused by known malware.': (
            '是已知恶意软件常见的滥用权限。'
        ),
        'From Code': '来自代码',
        'SDK Name': 'SDK 名称',
        'Platform Version': '平台版本',
        'Min OS Version': '最低系统版本',
        'View Info.plist': '查看 Info.plist',
        'No URL Schemes found.': '未发现 URL Scheme。',
        'No Permissions required.': '无需权限。',
        'DYLIB/FRAMEWORK': 'Dylib / Framework',
        'STATIC OBJECT': '静态目标文件',
        'RELRO': 'RELRO（只读重定位）',
        'NX': 'NX（不可执行）',
        'STACK CANARY': '栈金丝雀保护',
        'RPATH': '运行时路径',
        'SYMBOLS STRIPPED': '已去除符号',
        'ARC': 'ARC（自动引用计数）',
        'PIE': 'PIE（地址无关可执行）',
        'SHARED OBJECT': '共享目标文件',
        'RUNPATH': '运行路径',
        'FORTIFY': 'FORTIFY 强化',
        'Obfuscator': '混淆器',
        'Protector': '保护器',
        'Packer Found': '发现加壳',
        'Dropper Found': '发现投递器',
        'Manipulator Found': '发现篡改器',
        'APKiD not enabled.': 'APKiD 未启用。',
        'OFAC SANCTIONED COUNTRIES': 'OFAC 制裁国家',
        'HARDCODED SECRETS': '硬编码密钥',
        'POSSIBLE SECRETS': '可能存在的密钥',
        'Start HTTPTools': '启动 HTTPTools',
        'HTTP(S) Traffic': 'HTTP(S) 流量',
        'SQLITE DATABASE': 'SQLite 数据库',
        'Capture Strings': '捕获字符串',
        'Capture String Comparisons': '捕获字符串比较',
        'Trace Class Methods': '追踪类方法',
        'Instrumentation': '插桩',
        'Spawn & Inject': 'Spawn 并注入',
        'Available Scripts (Use CTRL to choose multiple)': (
            '可用脚本（按住 CTRL 可多选）'
        ),
        'Load': '加载',
        'Data refreshed in every 3 seconds.': '数据每 3 秒刷新一次。',
        'Attach to a Running Process': '附加到运行中的进程',
        'Mobile Security Framework - MobSF': '移动应用安全框架 - MobSF',
        'Mobile Security Framework (MobSF) is a security research platform for mobile applications in Android, iOS and Windows Mobile. MobSF can be used for a variety of use cases such as mobile application security, penetration testing, malware analysis, and privacy analysis. The Static Analyzer supports popular mobile app binaries like APK, IPA, APPX and source code. Meanwhile, the Dynamic Analyzer supports both Android and iOS applications and offers a platform for interactive instrumented testing, runtime data and network traffic analysis. MobSF seamlessly integrates with your DevSecOps or CI/CD pipeline, facilitated by REST APIs and CLI tools, enhancing your security workflow with ease.': (  # noqa: E501
            'Mobile Security Framework（MobSF）是面向 Android、iOS 与 Windows Mobile 应用的安全研究平台。它可用于移动应用安全评估、渗透测试、恶意软件分析以及隐私分析。静态分析器支持 APK、IPA、APPX 及源码等常见输入；动态分析器支持 Android 与 iOS，并提供交互式插桩测试、运行时数据分析和网络流量分析能力。借助 REST API 与 CLI 工具，MobSF 还能顺畅接入 DevSecOps 或 CI/CD 流程，帮助你更高效地融入现有安全工作流。'  # noqa: E501
        ),
        'View scan progress in the': '在以下位置查看扫描进度',
        'Items per page': '每页条目数',
        'Mobile Security Framework supports iOS and Android (eclipse and Android Studio) project files.': (  # noqa: E501
            'Mobile Security Framework 支持 iOS 以及 Android（Eclipse 与 Android Studio）项目文件。'  # noqa: E501
        ),
        (
            'The file AndroidManifest.xml and the directory '
            "'src' must exist in the root directory of ZIPPED "
            'Source files for eclipse projects.'
        ): (
            '对于 Eclipse 项目，压缩后的源码根目录中必须包含 '
            'AndroidManifest.xml 文件以及 `src` 目录。'
        ),
        (
            'AndroidManifest.xml must be located at '
            "'app/src/main/AndroidManifest.xml' and the directory "
            "'app/src/main/java/' must exist for Android Studio projects."
        ): (
            '对于 Android Studio 项目，AndroidManifest.xml 必须位于 '
            '`app/src/main/AndroidManifest.xml`，且必须存在 '
            '`app/src/main/java/` 目录。'
        ),
        (
            'For iOS projects, the .xcodeproj file must exist in the '
            'root directory of the ZIPPED Source files.'
        ): (
            '对于 iOS 项目，压缩后的源码根目录中必须存在 `.xcodeproj` 文件。'
        ),
        'MobSFy VM/Emulator/Device': 'MobSFy 虚拟机 / 模拟器 / 设备',
        'Set or Unset MobSF HTTP(S) Proxy': '设置或取消 MobSF HTTP(S) 代理',
        'Start an Activity or Exported Activity': (
            '启动 Activity 或导出 Activity'
        ),
        'Frida List Scripts': '列出 Frida 脚本',
        'Create an iOS VM in Corellium': '在 Corellium 中创建 iOS 虚拟机',
        'Start iOS VM in Corellium': '在 Corellium 中启动 iOS 虚拟机',
        'Stop iOS VM in Corellium': '在 Corellium 中停止 iOS 虚拟机',
        'Unpause iOS VM in Corellium': '在 Corellium 中恢复 iOS 虚拟机',
        'Reboot iOS VM in Corellium': '在 Corellium 中重启 iOS 虚拟机',
        'List Apps in Corellium iOS VM': '列出 Corellium iOS 虚拟机中的应用',
        'Network Capture': '网络抓包',
        'SSH Execute': '执行 SSH 命令',
        'Instance Input': '实例输入',
        'API to upload a file. Supported file types are apk, zip, ipa and appx.': (
            '用于上传文件的 API。支持 apk、zip、ipa 和 appx 文件。'
        ),
        'API to scan a file that is already uploaded. Supports scanning apk, xapk, apks, jar, aar, zip, ipa, so, dylib, a, and appx extensions.': (  # noqa: E501
            '用于扫描已上传文件的 API。支持 apk、xapk、apks、jar、aar、zip、ipa、so、dylib、a 和 appx 等扩展名。'  # noqa: E501
        ),
        '0 or 1, default is 0': '可选 0 或 1，默认值为 0',
        '0 or 1, default is 1': '可选 0 或 1，默认值为 1',
        'API that provides live and latest scan logs.': (
            '提供实时及最新扫描日志的 API。'
        ),
        'API for querying scan results. You can search using an MD5 checksum, app name, package name, or file name. The API returns the closest match based on your search term.': (  # noqa: E501
            '用于查询扫描结果的 API。你可以使用 MD5 校验值、应用名称、包名或文件名进行搜索，接口会返回与检索词最接近的匹配结果。'  # noqa: E501
        ),
        'hash of the scan or text': '扫描结果哈希或搜索文本',
        'Display Recent Scans API': '最近扫描 API',
        'API to Display Recent Scans.': '用于展示最近扫描记录的 API。',
        'the number of page': '页码',
        'per page size': '每页大小',
        'Displays the scan tasks queue, accessible only when the asynchronous scan queue is enabled.': (  # noqa: E501
            '显示扫描任务队列，仅在启用异步扫描队列时可用。'
        ),
        'first scan hash': '第一份扫描的哈希',
        'second scan hash to compare with': '用于对比的第二份扫描哈希',
        'Suppress findings by rule id.': '按规则 ID 抑制发现项。',
        'Suppress findings by files.': '按文件抑制发现项。',
        'View suppressions associated with a scan.': '查看与某次扫描关联的抑制规则。',
        'Delete suppressions.': '删除抑制规则。',
        'Get Apps available for Dynamic Analysis. You must perform static analysis before attempting dynamic analysis.': (  # noqa: E501
            '获取可用于动态分析的应用。执行动态分析前必须先完成静态分析。'
        ),
        'Start MobSF Dynamic Analyzer. Ensure that dynamic analysis environment (Android VM/Emulator/Device) is configured and running before calling this API.': (  # noqa: E501
            '启动 MobSF 动态分析器。调用此 API 前，请确保动态分析环境（Android 虚拟机 / 模拟器 / 设备）已配置并正在运行。'  # noqa: E501
        ),
        'ADB identifier of Android VM/Emulator/Device': (
            'Android 虚拟机 / 模拟器 / 设备的 ADB 标识符'
        ),
        'Execute ADB Commands API': '执行 ADB 命令 API',
        'Execute ADB commands inside VM/Emulator/Device.': (
            '在虚拟机 / 模拟器 / 设备内部执行 ADB 命令。'
        ),
        'non blocking adb commands': '非阻塞 ADB 命令',
        'Install or Remove Root CA API': '安装或移除 Root CA API',
        'API to install or remove MobSF Root CA to or from the Android VM/Emulator/Device.': (  # noqa: E501
            '用于在 Android 虚拟机 / 模拟器 / 设备中安装或移除 MobSF Root CA 的 API。'  # noqa: E501
        ),
        'Set or Unset MobSF Global HTTP(S) Proxy API': (
            '设置或取消 MobSF 全局 HTTP(S) 代理 API'
        ),
        'API to apply or remove global HTTP(S) proxy configuration to Android VM/Emulator/Device.': (  # noqa: E501
            '用于向 Android 虚拟机 / 模拟器 / 设备应用或移除全局 HTTP(S) 代理配置的 API。'  # noqa: E501
        ),
        'API to manually launch an Activity or Exported Activity.': (
            '用于手动启动 Activity 或导出 Activity 的 API。'
        ),
        'Fully qualified name of the activity or exported activity': (
            'Activity 或导出 Activity 的完整限定名'
        ),
        'API to run TLS/SSL Security Tester.': (
            '用于运行 TLS/SSL 安全测试器的 API。'
        ),
        'API to start Frida Instrumentation.': '用于启动 Frida 插桩的 API。',
        'API to collect runtime dependencies.': '用于收集运行时依赖的 API。',
        'API to view Frida log output.': '用于查看 Frida 日志输出的 API。',
        'Frida List Scripts API': 'Frida 脚本列表 API',
        'API to list available frida scripts.': (
            '用于列出可用 Frida 脚本的 API。'
        ),
        'API to generate frida script based on selection.': (
            '用于根据选择生成 Frida 脚本的 API。'
        ),
        'name of the script from the output of Frida List Scripts (/api/v1/frida/list_scripts) API.': (  # noqa: E501
            '来自 Frida 脚本列表 API（/api/v1/frida/list_scripts）输出中的脚本名称。'  # noqa: E501
        ),
        'Stop MobSF Dynamic Analyzer. This API must be called to stop dynamic analysis and prior to report generation.': (  # noqa: E501
            '停止 MobSF 动态分析器。停止动态分析并生成报告前，必须先调用此 API。'  # noqa: E501
        ),
        'Generate JSON Report of Dynamic Analysis. Stop Dynamic Analysis (/api/v1/dynamic/stop_analysis) API must be called before calling this API.': (  # noqa: E501
            '生成动态分析的 JSON 报告。调用本 API 前，必须先调用停止动态分析 API（/api/v1/dynamic/stop_analysis）。'  # noqa: E501
        ),
        'API to view source of files dumped from device after dynamic analysis. Stop Dynamic Analysis (/api/v1/dynamic/stop_analysis) API must be called before calling this API.': (  # noqa: E501
            '用于查看动态分析后从设备导出的文件源码的 API。调用本 API 前，必须先调用停止动态分析 API（/api/v1/dynamic/stop_analysis）。'  # noqa: E501
        ),
        'relative path of the file': '文件的相对路径',
        'List out supported iOS Corellium VMs.': (
            '列出受支持的 Corellium iOS 虚拟机。'
        ),
        'List out supported iOS versions for a device.': (
            '列出指定设备支持的 iOS 版本。'
        ),
        'iOS model': 'iOS 机型',
        'Create a jailbroken iOS instance in Corellium with desired flavor and iOS version.': (  # noqa: E501
            '在 Corellium 中创建指定 flavor 和 iOS 版本的越狱 iOS 实例。'
        ),
        'Corellium Project ID': 'Corellium 项目 ID',
        'Name of the VM': '虚拟机名称',
        'iOS Flavor': 'iOS 风味',
        'List iOS Instance & Apps Available for Dynamic Analysis.': (
            '列出可用于动态分析的 iOS 实例与应用。'
        ),
        'Start iOS VM in previously created in Corellium by instance identifier.': (
            '通过实例标识符启动先前在 Corellium 中创建的 iOS 虚拟机。'
        ),
        'Stop iOS VM in Corellium by instance identifier.': (
            '通过实例标识符停止 Corellium 中的 iOS 虚拟机。'
        ),
        'Unpause iOS VM in Corellium by instance identifier.': (
            '通过实例标识符恢复 Corellium 中的 iOS 虚拟机。'
        ),
        'Reboot iOS VM in Corellium by instance identifier.': (
            '通过实例标识符重启 Corellium 中的 iOS 虚拟机。'
        ),
        'Destroy iOS VM in Corellium by instance identifier.': (
            '通过实例标识符销毁 Corellium 中的 iOS 虚拟机。'
        ),
        'Corellium List Apps in Instance API': 'Corellium 实例内应用列表 API',
        'List all apps present in the Corellium iOS VM.': (
            '列出 Corellium iOS 虚拟机中的全部应用。'
        ),
        'Setup iOS Dynamic Analysis Environment for an IPA. This API call is required for apps not installed in the Corellium iOS VM.': (  # noqa: E501
            '为 IPA 配置 iOS 动态分析环境。若应用尚未安装到 Corellium iOS 虚拟机，则必须先调用此 API。'  # noqa: E501
        ),
        'iOS instance id': 'iOS 实例 ID',
        'Start iOS Dynamic Analyzer with an app. Setup environment (api/v1/ios/setup_environment) API should be called before running dynamic analyzer for IPAs not installed in the Corellium VM.': (  # noqa: E501
            '使用指定应用启动 iOS 动态分析器。对于未安装在 Corellium 虚拟机中的 IPA，应先调用环境配置 API（api/v1/ios/setup_environment）。'  # noqa: E501
        ),
        'Run the app in the Corellium VM.': '在 Corellium 虚拟机中运行该应用。',
        'Kill the app in the Corellium VM.': '在 Corellium 虚拟机中结束该应用。',
        'Remove an app from the Corellium VM.': '从 Corellium 虚拟机中移除应用。',
        'Take a screenshot.': '截取屏幕截图。',
        'Get App container path. App must be instrumented before calling this API.': (
            '获取应用容器路径。调用此 API 前，应用必须已完成插桩。'
        ),
        'Enable/Disable Network Capture.': '启用或禁用网络抓包。',
        'Download live packet capture.': '下载实时抓包文件。',
        'SSH Execute API': 'SSH 执行 API',
        'Execute OS Commands inside the VM over SSH.': (
            '通过 SSH 在虚拟机内部执行操作系统命令。'
        ),
        'OS Command': '操作系统命令',
        'Download app data from the VM.': '从虚拟机下载应用数据。',
        'Instance Input API': '实例输入 API',
        'Provide text, swipe and touch events to the VM': (
            '向虚拟机发送文本、滑动和触摸事件。'
        ),
        'x-axis integer / Text input text when': 'x 轴整数值 / 文本输入内容，当',
        'parameter is set to': '参数设置为',
        'y-axis integer': 'y 轴整数值',
        'Max Screen size x-axis': '屏幕 x 轴最大值',
        'Max Screen size y-axis': '屏幕 y 轴最大值',
        'Get VM system logs.': '获取虚拟机系统日志。',
        'Upload a file to the the VM.': '上传文件到虚拟机。',
        'Download a file from the VM.': '从虚拟机下载文件。',
        'Path to the file in VM': '虚拟机中的文件路径',
        'Instrument iOS App.': '对 iOS 应用进行插桩。',
        'comma separated dump hooks to load (network,crypto,cookies,file-access,json,sqlite,data-dir,keychain,nslog,text-inputs,nsurlcredentialstorage,nsuserdefaults,pasteboard)': (  # noqa: E501
            '要加载的转储 Hook，使用逗号分隔（network、crypto、cookies、file-access、json、sqlite、data-dir、keychain、nslog、text-inputs、nsurlcredentialstorage、nsuserdefaults、pasteboard）。'  # noqa: E501
        ),
        'look for classes with this method': '查找包含该方法的类',
        'Donate to MobSF project through Github Sponsors. Github will match the first $5000 in donations.': (  # noqa: E501
            '通过 GitHub Sponsors 向 MobSF 项目捐赠。GitHub 会为前 5000 美元的捐赠提供配捐。'
        ),
        'Total Common': '共同项总数',
        'ANTI-VM': '反虚拟机',
        'OBFUSCATOR': '混淆器',
        'PACKER': '壳',
        'MANIPULATOR': '篡改器',
        'ANTI-ASSEMBLY': '反汇编',
        'ABNORMAL PATTERN': '异常模式',
        'Error/ No APKiD result for one of the apps': (
            '错误：其中一个应用没有 APKiD 结果'
        ),
        'Error/ No browsable activities': '错误：未发现 Browsable Activity',
        'Static Analyzer': '静态分析器',
        'Visual Studio Version': 'Visual Studio 版本',
        'Visual Studio Edition': 'Visual Studio 版本类型',
        'Target OS': '目标操作系统',
        'Proj GUID': '项目 GUID',
        'Opti Tool': '优化工具',
        'Size': '大小',
        'INTENT': 'Intent',
        'MobSF Application Security Scorecard generated for': (
            '为以下应用生成的 MobSF 应用安全评分卡'
        ),
        'Sub Arch': '子架构',
        'Endian': '字节序',
        'DECOMPILED ASSETS': '反编译资源',
        'From APK Resource': '来自 APK 资源',
        'From Shared Objects': '来自共享对象',
        'Visual Studio Version:': 'Visual Studio 版本：',
        'Visual Studio Edition:': 'Visual Studio 版本类型：',
        'Target OS:': '目标操作系统：',
        'Proj GUID:': '项目 GUID：',
        'Opti Tool:': '优化工具：',
        'Arch:': '架构：',
        'SDK Name:': 'SDK 名称：',
        'Supported Platforms:': '支持的平台：',
        'Sub Arch:': '子架构：',
        'Endian:': '字节序：',
        'Target SDK:': '目标 SDK：',
        'Min SDK:': '最低 SDK：',
        'Max SDK:': '最高 SDK：',
        'APP COMPONENTS': '应用组件',
        'Failed to read Code Signing Certificate or none available.': (
            '无法读取代码签名证书，或当前没有可用证书。'
        ),
        'APKID ANALYSIS': 'APKiD 分析',
        'APKiD ANALYSIS': 'APKiD 分析',
        'Developer Address': '开发者地址',
        'COMPONENT / URI': '组件 / URI',
        'MATCHES': '匹配项',
        'Top permissions that are widely abused by known malware.': (
            '已知恶意软件最常滥用的高风险权限。'
        ),
        'Installs:': '安装量：',
        'Release Date:': '发布日期：',
        'Plist Files': 'Plist 文件',
        'Network Pcap': '网络 Pcap',
        'KEY': '键',
        'CREATE DATE': '创建日期',
        'MODIFICATION DATE': '修改日期',
        'Entitlement Group:': 'Entitlement 组：',
        'Item Class:': '条目类别：',
        'Accessible Attribute:': '可访问属性：',
        'Generic:': '通用：',
        'Service:': '服务：',
        'Account:': '账户：',
        'Protected:': '受保护：',
        'Access Control:': '访问控制：',
        'Creator:': '创建者：',
        'Script Code:': '脚本代码：',
        'Alias:': '别名：',
        'Invisible:': '隐藏：',
        'Negative:': '负值：',
        'Custom Icon:': '自定义图标：',
        'URLS INVOKED': '调用的 URL',
        'TEXT INPUTS': '文本输入',
        'KEYSTROKES': '按键记录',
        'EXPIRY': '过期时间',
        'HTTPONLY': 'HTTPOnly',
        'CRYPTO OPERATIONS': '加密操作',
        'PROTOCOL': '协议',
        'SQLITE QUERIES': 'SQLite 查询',
        'PLIST FILES': 'Plist 文件',
        'MobSF iOS Dynamic Analyzer': 'MobSF iOS 动态分析器',
        'ENCRYPTED IPA': '已加密 IPA',
        'You need decrypted IPA for dynamic analysis.': (
            '进行动态分析前，你需要先准备已解密的 IPA。'
        ),
        'Enumerate Classes & Methods': '枚举类与方法',
        'Find all classes with Specific Method': '查找包含指定方法的所有类',
        'MobSF cannot find android instance identifier. Make sure that an android instance is running and refresh this page.': (  # noqa: E501
            'MobSF 无法找到 Android 实例标识符。请确认已有 Android 实例正在运行，然后刷新此页面。'  # noqa: E501
        ),
        'Start Dynamic Analysis (No reinstall)': '开始动态分析（不重新安装）',
        'MobSFy!': 'MobSFy！',
        'Enumerate Class methods': '枚举类方法',
        'User Interface': '用户界面',
        'Called From:': '调用来源：',
        'RUNTIME DEPENDENCIES': '运行时依赖',
        '♢ Start Activity': '♢ 启动 Activity',
        'Deep Links': '深度链接',
        '▶ Deeplink': '▶ 深度链接',
        '▶ Probe Candidate Deeplinks': '▶ 探测候选深度链接',
        'TLS/SSL Security test helps you to evaluate the security of your application\'s network connections. These tests are applicable only for applications that performs network connections over HTTP protocol. We run multiple TLS/SSL tests against the application.': (  # noqa: E501
            'TLS/SSL 安全测试可帮助你评估应用网络连接的安全性。这些测试仅适用于通过 HTTP 协议发起网络连接的应用。系统会针对该应用执行多项 TLS/SSL 测试。'  # noqa: E501
        ),
        '- Enable HTTPS MITM Proxy, Remove Root CA, Run the App for 25 seconds.': (
            '- 启用 HTTPS MITM 代理，移除 Root CA，并运行应用 25 秒。'
        ),
        '- Enable HTTPS MITM Proxy, Install Root CA, Run the App for 25 seconds.': (
            '- 启用 HTTPS MITM 代理，安装 Root CA，并运行应用 25 秒。'
        ),
        '- Enable HTTPS MITM Proxy, Install Root CA, Bypass Certificate/Public Key Pinning or Certificate Transparency.': (  # noqa: E501
            '- 启用 HTTPS MITM 代理，安装 Root CA，并绕过证书 / 公钥 Pinning 或证书透明度校验。'
        ),
        'NOTE:': '注意：',
        'For Better results, while the application is running, navigate through different business logic flows that will trigger network connections over HTTP protocol. Make sure that no other applications are running during the test.': (  # noqa: E501
            '为了获得更好的结果，请在应用运行期间尽量操作不同的业务流程，以触发更多通过 HTTP 协议发起的网络连接。测试过程中请确保没有其他应用同时运行。'  # noqa: E501
        ),
        'Test Progress': '测试进度',
        'Mobile Security Framework (MobSF) is an automated, all-in-one mobile application (Android/iOS/Windows) pen-testing, malware analysis and security assessment framework capable of performing static and dynamic analysis.': (  # noqa: E501
            'Mobile Security Framework（MobSF）是一体化的自动化移动应用（Android / iOS / Windows）渗透测试、恶意软件分析与安全评估框架，能够执行静态与动态分析。'  # noqa: E501
        ),
    },
}

RAW_HTML_TRANSLATIONS = {
    ZH_HANS: OrderedDict([
        (
            'This request caused an Internal Server error. '
            'Check the server logs for more details. For debugging, try setting ',
            '该请求触发了服务器内部错误。请检查服务端日志获取更多信息。调试时可将 ',
        ),
        (
            'You do not have required permissions to perform this action.',
            '你没有执行此操作所需的权限。',
        ),
        (
            "We couldn't find the resource you are looking for.",
            '未找到你请求的资源。',
        ),
        (
            'Analysis started! Please wait to be redirected or check '
            'recent scans after sometime.',
            '分析已开始！请等待自动跳转，或稍后到最近扫描中查看。',
        ),
        (
            'This is a demo MobSF instance. Anything uploaded here will '
            'be publicly available. Do you want to continue?',
            '这是一个演示版 MobSF 实例。你上传的内容会公开可见，是否继续？',
        ),
        ('Trying to download ...', '正在尝试下载……'),
        ('You do not have permission to download and scan!', '你没有下载并扫描的权限！'),
        ('You do not have permission to upload!', '你没有上传权限！'),
        ('Failed to get scan status', '获取扫描状态失败'),
        ('Generating Report...Please Wait!', '正在生成报告，请稍候！'),
        ('Generating report', '正在生成报告'),
        ('Data refreshed in every 10 seconds.', '数据每 10 秒刷新一次。'),
        ('The scan results will appear in', '扫描结果将显示在'),
        ('once completed.', '中，任务完成后可查看。'),
        ('Current Password', '当前密码'),
        ('New Password', '新密码'),
        ('Confirm Password', '确认密码'),
        ('Delete Failed', '删除失败'),
        ('Deleted!', '已删除！'),
        ('The user is deleted!', '用户已删除！'),
        ('The scan result is deleted!', '扫描结果已删除！'),
        (
            'This will permanently remove the scan results from MobSF',
            '此操作会从 MobSF 中永久删除该扫描结果',
        ),
        (
            'This will permanently remove the user from MobSF',
            '此操作会从 MobSF 中永久删除该用户',
        ),
        (
            'This scan task has already been added to the scan queue.',
            '该扫描任务已加入扫描队列。',
        ),
        ('Scan Task Already Added!', '扫描任务已存在！'),
        ('Scan Task Recently Completed!', '扫描任务刚刚完成！'),
        ('The scan was recently processed.', '该扫描刚刚处理完成。'),
        ('Environment is ready for Dynamic Analysis.', '动态分析环境已就绪。'),
        (
            'Setting up MobSF Dynamic Analysis environment...',
            '正在配置 MobSF 动态分析环境……',
        ),
        (
            'Sucessfully created MobSF Dynamic Analysis environment.',
            '已成功创建 MobSF 动态分析环境。',
        ),
        ('Corellium iOS VM Creation Errored', 'Corellium iOS 虚拟机创建失败'),
        ('Start Errored', '启动失败'),
        ('Stop Errored', '停止失败'),
        ('Unpause Errored', '恢复失败'),
        ('Reboot Errored', '重启失败'),
        ('Destroy Errored', '销毁失败'),
        ('IPA Install Errored', 'IPA 安装失败'),
        ('Uninstall Errored', '卸载失败'),
        ('Downloading logs.', '正在下载日志。'),
        ('Downloading application data.', '正在下载应用数据。'),
        ('Downloaded application data', '已下载应用数据'),
        ('Failed to download application data', '下载应用数据失败'),
        ('Please select the second scan result for comparison', '请选择第二个扫描结果进行对比'),
        ('Cannot delete the user', '无法删除该用户'),
        ('Error:', '错误：'),
        ('For Android version', '对于 Android 版本'),
        (', SDK: API level', '，SDK：API 级别'),
        ('and SDK', '以及 SDK'),
        (', set Android VM proxy as', '，请将 Android 虚拟机代理设置为'),
        ('<Host IP>', '<主机 IP>'),
        (
            'version 4.1 - 11.0 (arm64, x86, and x86_64 upto API 30)',
            '版本 4.1 - 11.0（arm64、x86 和 x86_64，最高至 API 30）',
        ),
        (
            '(non production) version 5.0 - 11.0 (arm, arm64, x86, and '
            'x86_64 upto API 30)',
            '（非生产环境）版本 5.0 - 11.0（arm、arm64、x86 和 x86_64，最高至 API 30）',
        ),
        (
            '(userdebug builds) version 7.1.2 - 11.0 (arm64 upto API 30)',
            '（userdebug 构建）版本 7.1.2 - 11.0（arm64，最高至 API 30）',
        ),
    ]),
}


def normalize_spaces(text):
    """Collapse runs of whitespace to a single space."""
    return WHITESPACE_RE.sub(' ', text).strip()


def active_language(language):
    """Normalize Django language codes."""
    if not language:
        return ''
    return language.lower().replace('_', '-')


def should_localize(language):
    """Return True when the response should be translated."""
    return active_language(language).startswith('zh')


def translate_ui_text(text, language):
    """Translate an exact UI text fragment while preserving padding."""
    if not text or not should_localize(language):
        return text
    normalized = normalize_spaces(text)
    if not normalized:
        return text
    translated = UI_TEXT_TRANSLATIONS.get(ZH_HANS, {}).get(normalized)
    if not translated:
        translated = translate_heading_text(normalized, language)
    if not translated:
        return text
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    return f'{leading}{translated}{trailing}'


def translate_heading_text(text, language):
    """Translate short heading-like strings with token mapping."""
    if not should_localize(language):
        return None
    if len(text) > 70 or not HEADING_TEXT_RE.fullmatch(text):
        return None
    if not any(ch.isalpha() for ch in text):
        return None
    chunks = re.split(r'(\s+|[/:()&,\-]+)', text)
    translated = []
    changed = False
    alpha_tokens = 0
    translated_tokens = 0
    for chunk in chunks:
        upper = chunk.upper()
        replacement = TOKEN_TRANSLATIONS.get(upper)
        if replacement:
            translated.append(replacement)
            changed = True
            translated_tokens += 1
        else:
            translated.append(chunk)
        if any(ch.isalpha() for ch in chunk):
            alpha_tokens += 1
    if not changed:
        return None
    if not alpha_tokens or translated_tokens / alpha_tokens < 0.6:
        return None
    return ''.join(translated)


def localize_html(html, language):
    """Translate rendered HTML for the active language."""
    if not html or not should_localize(language):
        return html
    soup = BeautifulSoup(html, 'lxml')
    if soup.html:
        soup.html['lang'] = 'zh-Hans'
    for text_node in list(soup.find_all(string=True)):
        if not isinstance(text_node, NavigableString):
            continue
        parent = getattr(text_node.parent, 'name', '') or ''
        if parent.lower() in SKIPPED_TAGS:
            continue
        translated = translate_ui_text(str(text_node), language)
        if translated != str(text_node):
            text_node.replace_with(translated)
    for element in soup.find_all(True):
        for attr in TRANSLATABLE_ATTRS:
            value = element.attrs.get(attr)
            if isinstance(value, str):
                element.attrs[attr] = translate_ui_text(value, language)
    localized = str(soup)
    for source, replacement in RAW_HTML_TRANSLATIONS.get(ZH_HANS, {}).items():
        localized = localized.replace(source, replacement)
    return localized
