import responder

api = responder.API()


@api.route("/")
def hello_world(req, resp):
    """helloworld
    """
    resp.text = "hello, world!"
    


@api.route("/hello/{who}")
def hello_to(req, resp, *, who):
    """ルート引数を受け入れる
    """
    resp.text = f"hello, {who}!"
    
@api.route("/hello/{who}/json")
def hello_to(req, resp, *, who):
    """JSON/YAMLを返す
    クライアントが代わりに（ヘッダーが[Accept: application/x-yaml]）
    YAMLをリクエストするとYAMLが送信されます。
    """
    resp.media = {"hello": who}
    
@api.route("/hello/{who}/html")
def hello_html(req, resp, *, who):
    """テンプレートのレンダリング
    """
    resp.html = api.template('hello.html', who=who)
    
@api.route("/416")
def teapot(req, resp):
    """応答ステータスコードの設定"""
    resp.status_code = api.status_codes.HTTP_416   # ...or 416
    
@api.route("/pizza")
def pizza_pizza(req, resp):
    """応答ヘッダーの設定"""
    resp.headers['X-Pizza'] = '42'

import time

@api.route("/incoming")
async def receive_incoming(req, resp):
    # データとバックグラウンドタスクの受信

    @api.background.task
    def process_data(data):
        """Just sleeps for three seconds, as a demo."""
        time.sleep(3)


    # Parse the incoming data as form-encoded.
    # Note: 'json' and 'yaml' formats are also automatically supported.
    data = await req.media()

    # Process the data (in the background).
    process_data(data)

    # Immediately respond that upload was successful.
    resp.media = {'success': True}
    
@api.route("/file")
async def upload_file(req, resp):

    @api.background.task
    def process_data(data):
        f = open('./{}'.format(data['file']['filename']), 'w')
        f.write(data['file']['content'].decode('utf-8'))
        f.close()

    data = await req.media(format='files')
    process_data(data)

    resp.media = {'success': 'ok'}

# サーバーを実行する 
api.run()