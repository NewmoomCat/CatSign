## CatSign Plugin

签到插件, 可自定义

由于技术原因，想要调整签到金额得通过修改源代码中的m变量

python:
```python
m = 50 #可调整签到数额
```

然后编译

bash:
``` bash
 pip install pipx
 pipx run build
```

PS: 你们只要碰m这个变量就行了