# Git忽略文件配置说明

## 已配置的忽略规则

### Python相关文件
- `__pycache__/` - Python字节码缓存目录
- `*.py[cod]` - Python编译文件
- `*.so` - 共享对象文件
- `build/`, `dist/` - 构建和分发目录
- `*.egg-info/` - Python包信息
- `.env`, `.venv`, `venv/` - 虚拟环境

### 开发工具相关
- `.idea/` - PyCharm IDE配置
- `.vscode/` - VS Code配置
- `*.swp`, `*.swo` - Vim临时文件

### 项目特定文件

#### 上传文件目录
- `uploads/*` - 忽略所有上传的文件
- `!uploads/.gitkeep` - 但保留.gitkeep文件以维持目录结构

#### 图片文件
忽略所有常见的图片格式：
- `*.jpg`, `*.jpeg`, `*.png`, `*.gif`
- `*.tiff`, `*.tif`, `*.bmp`, `*.webp`
- `*.raw`, `*.cr2`, `*.nef`, `*.arw` (相机RAW格式)

#### 日志和临时文件
- `*.log` - 日志文件
- `logs/` - 日志目录
- `*.tmp`, `*.temp` - 临时文件
- `temp/`, `tmp/` - 临时目录

#### 配置和数据库文件
- `config_local.py` - 本地配置文件
- `.env.local`, `.env.production` - 环境配置
- `*.db`, `*.sqlite`, `*.sqlite3` - 数据库文件

#### 备份和打包文件
- `*.bak`, `*.backup` - 备份文件
- `*.zip`, `*.tar.gz`, `*.rar` - 压缩文件

#### 系统文件
- `.DS_Store` - macOS系统文件
- `Thumbs.db` - Windows缩略图缓存
- `*.lnk` - Windows快捷方式

#### 开发和测试文件
- `local_*`, `dev_*`, `debug_*` - 本地开发文件
- `test_images/`, `sample_photos/` - 测试图片目录

## 重要操作记录

### 已执行的清理操作
1. **移除已追踪的__pycache__文件**：
   ```bash
   git rm -r --cached __pycache__
   ```
   这些文件现在会被忽略，不会再被Git追踪。

2. **创建uploads/.gitkeep**：
   保持uploads目录结构，但忽略其中的上传文件。

## 使用建议

### 添加新的忽略规则
如果需要忽略其他文件类型，在`.gitignore`中添加相应规则：
```
# 例如忽略特定的配置文件
my_config.json

# 忽略特定目录
my_temp_dir/

# 忽略特定扩展名
*.custom_ext
```

### 检查文件是否被忽略
```bash
# 检查特定文件是否被忽略
git check-ignore filename

# 查看所有被忽略的文件
git status --ignored
```

### 强制添加被忽略的文件
如果确实需要追踪某个被忽略的文件：
```bash
git add -f filename
```

## 注意事项

1. **已追踪的文件**：`.gitignore`只对未被Git追踪的文件生效。如果文件已经被追踪，需要先用`git rm --cached`移除。

2. **全局忽略**：可以设置全局的`.gitignore`文件：
   ```bash
   git config --global core.excludesfile ~/.gitignore_global
   ```

3. **目录结构**：使用`.gitkeep`文件可以保持空目录在Git中被追踪。

4. **敏感信息**：确保包含密码、API密钥等敏感信息的文件被正确忽略。

## 当前项目状态

- ✅ Python缓存文件已被移除并忽略
- ✅ 上传目录配置正确（保留结构，忽略内容）
- ✅ 开发工具配置文件被忽略
- ✅ 图片和媒体文件被忽略
- ✅ 日志和临时文件被忽略

这个配置确保了仓库的干净性，只追踪源代码和必要的配置文件。
