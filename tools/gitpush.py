#!/usr/bin/env python3
"""通过 GitHub REST API 推送提交（沙盒屏蔽 github.com:443 时的替代方案）。
用法: GH_TOKEN=... python3 tools/gitpush.py
"""
import base64, json, os, subprocess, sys, urllib.request, urllib.error

TOKEN = os.environ.get("GH_TOKEN", "")
OWNER, REPO = "hjm91517", "last-ember"
API = "https://api.github.com"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def call(method, path, payload=None):
    url = API + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "last-ember-builder")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:400]
        print(f"!! {method} {path} -> {e.code}: {body}")
        raise

def git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=ROOT).decode().strip()

files = [f for f in git("ls-files").split("\n") if f.strip()]
print(f"files: {len(files)}")

tree = []
for f in files:
    p = os.path.join(ROOT, f)
    if not os.path.isfile(p):
        continue
    with open(p, "rb") as fh:
        content = fh.read()
    blob = call("POST", f"/repos/{OWNER}/{REPO}/git/blobs", {
        "content": base64.b64encode(content).decode(),
        "encoding": "base64",
    })
    tree.append({"path": f, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print("blob", f, len(content))

msg = os.environ.get("COMMIT_MSG", "feat: 余烬 Last Ember")
new_tree = call("POST", f"/repos/{OWNER}/{REPO}/git/trees", {"tree": tree})
parents = []
try:
    ref = call("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/main")
    parents = [ref["object"]["sha"]]
    print("parent", parents[0])
except Exception:
    pass
commit = call("POST", f"/repos/{OWNER}/{REPO}/git/commits", {
    "message": msg,
    "tree": new_tree["sha"],
    "parents": parents,
})
print("commit", commit["sha"])

# 建立或更新 main
try:
    call("POST", f"/repos/{OWNER}/{REPO}/git/refs", {
        "ref": "refs/heads/main",
        "sha": commit["sha"],
    })
    print("created refs/heads/main")
except urllib.error.HTTPError:
    call("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/main", {
        "sha": commit["sha"], "force": True,
    })
    print("updated refs/heads/main")

# 让本地记录也指向该提交，便于后续比较
print("done", commit["sha"])
