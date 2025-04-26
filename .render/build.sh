#!/usr/bin/env bash
# 初始化 SQLite 数据库（首次部署时执行）
python -c 'from app import db; db.create_all()'