# Hướng Dẫn Cài Đặt `devkit-opencode`

Tài liệu này hướng dẫn chi tiết cách cài đặt **24 OpenCode Skills**, **8 Custom Slash Commands** (`commands/`), file quy tắc [AGENTS.md](AGENTS.md) và file cấu hình mẫu [config/opencode.jsonc.example](config/opencode.jsonc.example) vào OpenCode.

---

## Yêu Cầu Trước Khi Cài Đặt

- Đã cài đặt **OpenCode** (`opencode --version`).
- Có sẵn Git (hoặc Node.js `npx` nếu dùng `skills` CLI).

---

## Cách 1: Cài Tự Động Bằng Script (Khuyên Dùng)

Script cài đặt sẽ tự chép `skills/` + `commands/` và **tự động backup** (`*.bak.<timestamp>`) nếu máy bạn đã có sẵn `AGENTS.md` hoặc `opencode.jsonc`.

### Windows (PowerShell)

```powershell
git clone https://github.com/vuloc080611/DevKit-OpenCode.git
Set-Location DevKit-OpenCode

# Cài toàn cục (~/.config/opencode) đầy đủ 24 skills + 8 commands + config
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1

# Hoặc chỉ cài 9 skill cốt lõi (không ghi đè config sẵn có)
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CoreOnly -SkipConfig

# Hoặc cài riêng vào thư mục dự án hiện tại (.opencode/)
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Scope Project -ProjectDir "D:\path\to\your-project"
```

### Linux / macOS (Bash)

```bash
git clone https://github.com/vuloc080611/DevKit-OpenCode.git
cd DevKit-OpenCode
chmod +x scripts/install.sh

# Cài toàn cục (~/.config/opencode) đầy đủ 24 skills + 8 commands + config
./scripts/install.sh

# Hoặc chỉ cài 9 skill cốt lõi (bỏ qua config)
./scripts/install.sh --core-only --skip-config

# Hoặc cài riêng vào một dự án (.opencode/)
./scripts/install.sh --project /path/to/your-project
```

---

## Cách 2: Cài Nhanh Qua `skills` CLI

Nếu bạn đã cài Node.js, có thể cài trực tiếp bộ skill từ GitHub mà không cần clone:

```bash
# Xem danh sách skills có trong repo
npx skills add vuloc080611/DevKit-OpenCode --list

# Cài toàn cục cho OpenCode
npx skills add vuloc080611/DevKit-OpenCode -a opencode -g

# Hoặc cài chọn lọc từng skill vào dự án hiện tại
npx skills add vuloc080611/DevKit-OpenCode --skill grill-me --skill systematic-debugging -a opencode
```

*(Lưu ý: `npx skills add` chỉ cài thư mục `skills/`. Nếu muốn dùng thêm slash commands `/grill`, `/debug`, `/verify`... hãy copy thêm `commands/*.md` theo Cách 3.)*

---

## Cách 3: Cài Thủ Công (Global Hoặc Project-Local)

OpenCode tự động quét các skill và commands nằm tại thư mục global:
- **Linux / macOS:** `~/.config/opencode/skills/` và `~/.config/opencode/commands/`
- **Windows:** `%USERPROFILE%\.config\opencode\skills\` và `%USERPROFILE%\.config\opencode\commands\`

> [!IMPORTANT]
> Trên cả Linux/macOS lẫn Windows, OpenCode dùng thư mục `.config/opencode/`, **không** dùng `~/.opencode/skills/` hay `%APPDATA%\opencode\`.

### Linux / macOS

```bash
# 1. Clone repo
git clone https://github.com/vuloc080611/DevKit-OpenCode.git
cd DevKit-OpenCode

# 2. Tạo thư mục cấu hình OpenCode (nếu chưa có)
mkdir -p ~/.config/opencode/skills ~/.config/opencode/commands

# 3. Copy toàn bộ 24 skills & 8 slash commands
cp -r skills/* ~/.config/opencode/skills/
cp commands/*.md ~/.config/opencode/commands/

# 4. Copy AGENTS.md và file cấu hình mẫu (kiểm tra trước nếu bạn đã có file riêng!)
cp AGENTS.md ~/.config/opencode/AGENTS.md
cp config/opencode.jsonc.example ~/.config/opencode/opencode.jsonc
```

**Mẹo dùng symlink trên Linux / macOS** (tiện khi cập nhật `git pull`):

```bash
for d in "$(pwd)"/skills/*; do
  ln -sfn "$d" ~/.config/opencode/skills/"$(basename "$d")"
done
for f in "$(pwd)"/commands/*.md; do
  ln -sfn "$f" ~/.config/opencode/commands/"$(basename "$f")"
done
```

### Windows (PowerShell)

```powershell
# 1. Clone repo
git clone https://github.com/vuloc080611/DevKit-OpenCode.git
Set-Location DevKit-OpenCode

# 2. Tạo thư mục global OpenCode
$openCodeDir = Join-Path $env:USERPROFILE ".config\opencode"
$skillsDir = Join-Path $openCodeDir "skills"
$commandsDir = Join-Path $openCodeDir "commands"
New-Item -ItemType Directory -Force $skillsDir, $commandsDir | Out-Null

# 3. Copy toàn bộ 24 skills & 8 commands
Copy-Item -Recurse -Force ".\skills\*" $skillsDir
Copy-Item -Force ".\commands\*.md" $commandsDir

# 4. Copy AGENTS.md và config mẫu (cẩn thận nếu bạn đã có file cũ cần giữ lại)
Copy-Item -Force ".\AGENTS.md" (Join-Path $openCodeDir "AGENTS.md")
Copy-Item -Force ".\config\opencode.jsonc.example" (Join-Path $openCodeDir "opencode.jsonc")
```

### Cài Riêng Cho Từng Dự Án (Project-Local)

OpenCode tự động tìm skill và command trong `.opencode/skills/`, `.opencode/commands/` cùng `AGENTS.md` và `opencode.jsonc` ở thư mục gốc repo:

```bash
# Chạy tại thư mục gốc dự án của bạn
mkdir -p .opencode/skills .opencode/commands
cp -r /path/to/DevKit-OpenCode/skills/* .opencode/skills/
cp /path/to/DevKit-OpenCode/commands/*.md .opencode/commands/
cp /path/to/DevKit-OpenCode/AGENTS.md ./AGENTS.md
cp /path/to/DevKit-OpenCode/config/opencode.jsonc.example ./opencode.jsonc
```

*(Nếu dự án của bạn đã có `AGENTS.md` hoặc `opencode.jsonc` riêng, hãy mở [AGENTS.md](AGENTS.md) và [config/opencode.jsonc.example](config/opencode.jsonc.example) để gộp thủ công các phần cần thiết thay vì ghi đè.)*

---

## Cài Chọn Lọc Theo Nhóm Ưu Tiên (Thủ Công)

Nếu bạn chỉ muốn bắt đầu với bộ kỷ luật cốt lõi để giữ context gọn:

```bash
mkdir -p ~/.config/opencode/skills
for s in grill-me project-planner systematic-debugging verification-before-done tdd-workflow code-review security-review git-commit readme-generator; do
  cp -r "skills/$s" ~/.config/opencode/skills/
done
```

---

## Cấu Hình Quyền & Kiểm Tra Trong `opencode.jsonc`

Trong [config/opencode.jsonc.example](config/opencode.jsonc.example):
- Mục `"permission.skill"` mặc định để `"allow"` cho cả 24 skill để agent tự load khi đúng ngữ cảnh. Nếu muốn OpenCode hỏi xác nhận trước khi nạp skill nào, đổi giá trị đó thành `"ask"`; nếu muốn ẩn hẳn một skill (ví dụ nhóm học tập khi dùng ở repo công ty), đổi thành `"deny"`:

```jsonc
"permission": {
  "skill": {
    "*": "allow",
    "dsa-explainer": "deny",
    "leetcode-helper": "deny",
    "assignment-helper": "deny"
  }
}
```

- Mục `"permission.bash"` cho phép sẵn các lệnh đọc an toàn (`git status`, `git diff`, `git log`) và hỏi xác nhận (`"ask"`) với các lệnh shell khác.
- Nhớ bỏ comment và chỉnh `"model"` nếu muốn cố định model mặc định theo provider bạn đang đăng nhập.

---

## Kiểm Tra Sau Khi Cài Đặt

1. Mở terminal trong một dự án bất kỳ và khởi chạy `opencode`.
2. Hỏi thử OpenCode: *"Bạn đang nhìn thấy những skills nào trong session này?"* hoặc dùng một câu trigger cụ thể:
   - *"Hãy dùng `grill-me` hỏi rõ yêu cầu cho tính năng export PDF."*
   - *"Chạy `verification-before-done` để kiểm tra dự án hiện tại."*
3. Đảm bảo toàn bộ thư mục con dưới `skills/` đều chứa đúng tên file viết hoa chuẩn `SKILL.md`.

---

## Khắc Phục Sự Cố Thường Gặp

1. **OpenCode không thấy skill đã copy:**
   - Kiểm tra đúng đường dẫn `~/.config/opencode/skills/<tên-skill>/SKILL.md` (hoặc `.opencode/skills/<tên-skill>/SKILL.md` trong repo).
   - Kiểm tra tên thư mục phải khớp chính xác với trường `name:` trong YAML frontmatter của `SKILL.md`.
2. **Lỗi parse file cấu hình:**
   - Nếu bạn đặt tên file là `opencode.json` thay vì `opencode.jsonc`, trình đọc JSON thuần sẽ không chấp nhận comment `//`. Hãy giữ đuôi `.jsonc` hoặc xóa comment `//`.
3. **Đã có `AGENTS.md` sẵn trong dự án:**
   - Không ghi đè file của dự án; hãy copy phần **Skill Routing Guide** trong [AGENTS.md](AGENTS.md) nối thêm vào cuối file `AGENTS.md` hiện có.
