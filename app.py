from quart import Quart

app = Quart(__name__)

async def async_hello():
    return 'Hello, Async Quart!'

@app.route('/')
async def hello():
    return await async_hello()

if __name__ == '__main__':
    app.run(debug=True)
