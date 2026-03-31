# -*- coding: utf-8 -*-
"""
GitHub Profile README 自动生成脚本
运行于 GitHub Actions 环境
"""

import os
import urllib.request
import json

# GitHub 用户名
USERNAME = "nacayu"

def get_github_stats():
    """获取GitHub用户统计数据"""
    
    # 获取用户信息
    with urllib.request.urlopen(f"https://api.github.com/users/{USERNAME}") as resp:
        user_data = json.loads(resp.read().decode())
    
    # 获取仓库列表
    with urllib.request.urlopen(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed") as resp:
        repos_data = json.loads(resp.read().decode())
    
    # 计算总stars和forks
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    total_forks = sum(repo['forks_count'] for repo in repos_data)
    
    # 统计语言
    lang_count = {}
    for repo in repos_data:
        lang = repo.get('language')
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1
    
    # 6个主要仓库的stars和forks
    pinned_names = [
        'awesome-deeplearning-based-radar-perception',
        'CRFNet_Tensorflow2.4.1', 
        'ARS_408_ROS_Toolkit',
        'SAF-FCOS',
        'SOAR-Shanghaijiankangyun-OCR-Automatic-Recognization-',
        'ImageSetToRosbag'
    ]
    
    repo_stats = {}
    for repo in repos_data:
        if repo['name'] in pinned_names:
            repo_stats[repo['name']] = {
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count']
            }
    
    return {
        'repos': user_data['public_repos'],
        'stars': total_stars,
        'forks': total_forks,
        'followers': user_data['followers'],
        'following': user_data['following'],
        'lang_python': lang_count.get('Python', 0),
        'lang_cpp': lang_count.get('C++', 0),
        'lang_c': lang_count.get('C', 0),
        'lang_lua': lang_count.get('Lua', 0),
        'repo_stats': repo_stats,
        'update_date': '2026-04-01'
    }

def generate_readme():
    """生成README.md"""
    
    print("📊 获取GitHub数据...")
    data = get_github_stats()
    
    print(f"✅ 获取成功 - {data['repos']} repos, {data['stars']} stars")
    
    # 读取当前README模板
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换占位符
    replacements = {
        '<!-- repo_count -->': str(data['repos']),
        '<!-- star_count -->': str(data['stars']),
        '<!-- fork_count -->': str(data['forks']),
        '<!-- follower_count -->': str(data['followers']),
        '<!-- following_count -->': str(data['following']),
        '<!-- py_count -->': str(data['lang_python']),
        '<!-- cpp_count -->': str(data['lang_cpp']),
        '<!-- c_count -->': str(data['lang_c']),
        '<!-- lua_count -->': str(data['lang_lua']),
        '<!-- repos -->': str(data['repos']),
        '<!-- stars -->': str(data['stars']),
        '<!-- update_date -->': data['update_date']
    }
    
    # 替换仓库统计
    repo_map = {
        'awesome-deeplearning-based-radar-perception': ('repo1_stars', 'repo1_forks'),
        'CRFNet_Tensorflow2.4.1': ('repo2_stars', 'repo2_forks'),
        'ARS_408_ROS_Toolkit': ('repo3_stars', 'repo3_forks'),
        'SAF-FCOS': ('repo4_stars', 'repo4_forks'),
        'SOAR-Shanghaijiankangyun-OCR-Automatic-Recognization-': ('repo5_stars', 'repo5_forks'),
        'ImageSetToRosbag': ('repo6_stars', 'repo6_forks')
    }
    
    for repo_name, (stars_key, forks_key) in repo_map.items():
        if repo_name in data['repo_stats']:
            stats = data['repo_stats'][repo_name]
            replacements[f'<!-- {stars_key} -->'] = str(stats['stars'])
            replacements[f'<!-- {forks_key} -->'] = str(stats['forks'])
        else:
            replacements[f'<!-- {stars_key} -->'] = '0'
            replacements[f'<!-- {forks_key} -->'] = '0'
    
    # 执行替换
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    # 写回文件
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md 生成完成!")

if __name__ == "__main__":
    generate_readme()