import os

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

    # 没有 tag（如 fork 仓库）时使用兜底版本号
    if len(tag) >= 2 and tag.startswith('v'):
        version = str(tag[1:]).strip()
    else:
        version = '0.0.0'

    version_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../QtScrcpy/appversion"))
    with open(version_file, 'w') as file:
        file.write(version)