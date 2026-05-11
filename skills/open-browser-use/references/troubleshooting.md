# 故障排除

## 第一步检查
```sh
obu ping --session-id "$OBU_SESSION_ID"
obu info --session-id "$OBU_SESSION_ID"
obu user-tabs --session-id "$OBU_SESSION_ID"
```

## 常见问题

### 1. 连接失败
1. Chrome 是否安装并运行
2. Open Browser Use 扩展是否安装并启用
3. 原生主机清单是否注册（`obu install-manifest`）
4. 用户是否批准了 Chrome 扩展提示

### 2. Socket 失效
```sh
# 指定 socket
obu ping --socket /tmp/open-browser-use/example.sock
# 指定 socket 目录
obu ping --socket-dir /tmp/open-browser-use
# 超时
obu ping --timeout 20s
```

### 3. 扩展/主机不匹配
```sh
obu manifest          # 查看当前清单
obu install-manifest  # 修复注册
obu setup             # 重装
obu setup beta        # ZIP 版重装
```

### 4. 文件上传失败
检查 Chrome 扩展的"文件 URL 访问"权限是否开启：
`chrome://extensions` → Open Browser Use → 详情 → 启用文件 URL 访问。

## 何时需要用户介入
- Chrome 未安装
- Chrome 关闭且打开会打断用户
- 需要登录、CAPTCHA、硬件密钥、支付确认
- 涉及外部系统的浏览器操作

详情参见上游仓库：
https://github.com/iFurySt/open-codex-browser-use/blob/main/skills/open-browser-use/references/troubleshooting.md
