# Image Search Project

## 项目结构

```
├── img_capt_api # 基于 Django REST Framework 的后端 API
│   ├── img_capt_api # Django Project
│   ├── img_capt_lib # Model Lib
│   ├── img_capt_web # Django App
├── img-capt-app # 基于 Electron + Vue 的 app
```

## 项目环境配置

### `img_capt_api`

需要 `Python >= 3.6`，建议使用 `Python 3.9`

#### 创建虚拟环境

```bash
cd img_capt_api # 进入 img_capt_api 文件夹
python -m venv venv # 创建虚拟环境
```

#### 激活虚拟环境

```bash
source venv/bin/activate # Linux/Mac 用户执行这个
# Windows 用户使用 cmd.exe 执行 venv\Scripts\activate.bat
# Powershell 用户执行 venv\Scripts\Activate.ps1
```

之后执行 `pip list`，如果显示只有 `pip setuptools` 这两个包的话则进入成功。执行 `deactive` 退出虚拟环境。之后的操作都需要在激活虚拟环境的状态下执行。

#### 安装依赖

执行 `pip install -r requirements.txt` 安装依赖。

如果网络状况不佳建议更换国内镜像源

```shell
# 执行下面的命令配置使用清华的镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 初始化数据库

Django 开发环境默认使用的数据库是 SQLite，不需要额外安装其它数据库软件，依次执行下列命令来初始化数据库，执行完后会生成一个 `db.sqlite3` 文件，之后可以用可视化工具或者 JB 家的 IDE 打开查看数据库内容。

```shell
python manage.py migrate
```

#### 启动服务器

执行 `python manage.py runserver` 即可，默认开放在 8000 端口。

#### 已实现 API

- `GET /model_init`: 初始化模型，使用其它 API 之前必须执行一次，加载模型可能需要一段时间，之后才会收到响应
- `GET /folders`: 获取已经添加的文件夹路径
- `POST /folders`: 需要以 form-data 的形式传入参数 `name=/dir`，将文件夹路径添加到数据库，同时将文件夹内的图片的信息也添加到数据库内，执行可能也需要一段时间，之后才会收到响应，传入的路径如果带 `~` 会自动展开到用户目录下面
- `GET /images`: 需要以 query parameter 的形式传入参数 `path=/dir`, 获取该文件夹下面的已经添加到数据库的图片路径，必须传入文件夹的绝对路径

具体用法与返回的数据看下面用 `httpie` 做的演示

<details>
  <summary>点我展开</summary>

```bash
$ http GET "http://localhost:8000/model_init"
HTTP/1.1 200 OK
Allow: OPTIONS, POST, GET
Content-Length: 37
Content-Type: application/json
Date: Wed, 07 Jul 2021 05:55:23 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 200,
    "data": {
        "msg": "success"
    }
}
```  

```bash
$ http --form POST "http://localhost:8000/folders" "path=~/Downloads/TMP/pics"
HTTP/1.1 200 OK
Allow: OPTIONS, POST, GET, DELETE
Content-Length: 37
Content-Type: application/json
Date: Wed, 07 Jul 2021 05:56:39 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 200,
    "data": {
        "msg": "success"
    }
}
```

```bash
$ http GET "http://localhost:8000/folders"
HTTP/1.1 200 OK
Allow: OPTIONS, POST, GET, DELETE
Content-Length: 112
Content-Type: application/json
Date: Wed, 07 Jul 2021 05:59:04 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 200,
    "data": [
        {
            "path": "/home/tunkshif/Downloads/TMP/pics"
        },
        {
            "path": "/home/tunkshif/Pictures/Wallpapers"
        }
    ]
}
```

```bash
$ http GET "http://localhost:8000/images?path=/home/tunkshif/Downloads/TMP/pics"
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Content-Length: 609
Content-Type: application/json
Date: Wed, 07 Jul 2021 06:04:28 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 200,
    "data": [
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/platypus.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/two white ducks.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/mountains views.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/cute kitty coverd.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/strawberries on the table.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/big ben tower.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/red poppy flower.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/cheetahs.jpg"
        },
        {
            "path": "/home/tunkshif/Downloads/TMP/pics/girl wearing a fedora.jpg"
        }
    ]
}
```

```bash
$ http --form POST "http://localhost:8000/folders" "path=~/Pictures/Wallpapers"
HTTP/1.1 400 Bad Request
Allow: DELETE, POST, OPTIONS, GET
Content-Length: 49
Content-Type: application/json
Date: Wed, 07 Jul 2021 06:06:04 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 400,
    "data": {
        "msg": "Model Not Initiated"
    }
}

```

```bash
$ http GET "http://localhost:8000/images?path=/hocsackahsj"
HTTP/1.1 404 Not Found
Allow: OPTIONS, GET
Content-Length: 46
Content-Type: application/json
Date: Wed, 07 Jul 2021 06:05:32 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.9.6
Vary: Origin, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "code": 404,
    "data": {
        "msg": "Folder Not Found"
    }
}

```

</details>

### `img-capt-app`

简单糊了个 demo，主要写了个打开文件夹获取文件夹路径的演示

我测试环境的版本号：`nodejs v14.16.0` `npm 7.17.0`

#### 安装依赖

```bash
cd img-capt-app
npm install
```

之后执行 `npm run elctron:serve` 启动


#### 可能遇到的问题

- `Electron failed to install correctly`: 尝试删除 `node_modules/electron` 和 `package-lock.json` 后执行 `npm install --save-dev electron@latest`
- 卡在 `Launching Electron` 的提示信息上：首次启动的时候因为会下载 `Vue Dev Tools` 这个 Chrome 扩展，所以需要科学上网一下

#### 如何快速自己搭建 Vue + Electron 开发环境

最方便的办法是使用 `vue-cli`

```bash
npm install -g @vue/cli # 安装 vue-cli 工具
vue create <project-name> # 创建一个新的 vue 项目，建议选择 Vue2
vue add electron-builder # 安装 vue-cli-plugin 快速将 Electron 集成到 Vue 项目当中
# 之后可以自行 npm install 其它需要的包
```

#### 如何调用选择文件的窗口

Electron 提供了一个 [Dialog API][0]，可以弹出一个对话框供用户选择文件和文件夹，具体演示如下，其返回值是一个 Promise，里面的数据中的 `filePaths` 字段是一个包含所选文件夹的数组。

```js
dialog.showOpenDialog({ properties: ['openFolder', 'multiSelections'] }).then(data => console.log(data.filePaths))
```

另外需要了解下 Electron 的[进程模型][1]，其包含一个运行在 Node.js 环境里的主进程，对应的是项目里的 `background.js` 文件，有关应用程序窗口的管理，生命周期以及调用文件系统的相关操作需要在主进程里完成。

另外可以有多个渲染进程，即打开的浏览器窗口，对应的是项目里的 `main.js`，这里就跟正常的 Web 项目一样写就行了。

主进程跟渲染进程之间通过 Electron 提供的 [ipcMain][2] 和 [ipcRenderer][3] 两个 API 来进行进程间通信。

下面是一个简单的栗子：

```js
// background.js

/**
 * 主进程里监听 'openFolder' 这个频道（名字可以随意取
 * 当收到向这个频道发送来的信息的时候，执行后面的回调函数
 * 在回调函数里将读取到的文件路径发送给了 'filePaths' 这个频道
 * 这里用了 async/await 避免用 Promise（
*/
ipcMain.on('openFolder', async (event, path) => {
   const result = await dialog.showOpenDialog({ properties: ['openDirectory'] })
   event.sender.send('filePaths', result.filePaths)
})
```

```js
// SideBar.vue

/**
 * 下面是写在 Vue 组件里的点击事件
 * 先通过 ipcRenderer 向 'openFolder' 频道发送信息
 * 主进程打开一个选择文件夹的对话框，渲染进程这里继续监听 'filePaths' 频道的信息
 * 当接受到传来的信息的时候调用后面的回调函数
 * 回调函数里执行了向后端 API 发送请求
 *
*/

export default {
  name: "SideBar",
  methods: {
    addFolder: function() {
      ipcRenderer.send('openFolder')
      ipcRenderer.on('filePaths', (event, filePaths) => {
        if (filePaths.length != 0) {
          fetch('http://localhost:8000/folders', {
            method: 'POST',
            body: new URLSearchParams('path=' + filePaths[0])
          }).then(response => response.json()).then(data => console.log(data))
        }
      })
    }
  }
}
```

[0]: https://www.electronjs.org/docs/api/dialog
[1]: https://www.electronjs.org/docs/tutorial/process-model
[2]: https://www.electronjs.org/docs/api/ipc-maine
[3]: https://www.electronjs.org/docs/api/ipc-renderer