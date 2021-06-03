from flask import Blueprint

# create blueprint
bp=Blueprint('bp_1_0',__name__)
# 要写在下面防止循环导入
from . import user, verify
#第一次引用包内模块或包时，都会执行包的初始化代码，即包内的__init__.py的代码
