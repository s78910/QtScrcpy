import os
import re

if __name__ == '__main__':
    tag = ''
    try:
        p = os.popen('git rev-list --tags --max-count=1')
        commit = p.read()
        p.close()

        if commit.strip():
            p = os.popen('git describe --tags ' + commit)
            tag = p.read()
            p.close()
    except Exception:
        tag = ''

    # 没有 tag（如 fork 仓库）时使用兜底版本号；同时清洗非数字后缀，满足 CMake VERSION 格式
    if len(tag) >= 2 and tag.startswith('v'):
        version = str(tag[1:]).strip()
    else:
        version = '3.3.3'

    # 例如 v4.2.1-custom -> 4.2.1
    matched = re.match(r'(\d+(?:\.\d+)*)', version)
    if matched:
        version = matched.group(1)
    else:
        version = '3.3.3'

    # CMake 要求至少 major.minor.patch
    parts = version.split('.')
    while len(parts) < 3:
        parts.append('0')
    version = '.'.join(parts[:3])

    version_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../QtScrcpy/appversion"))
    with open(version_file, 'w') as file:
        file.write(version)