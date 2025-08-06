import uvicorn
from icecream import install

from api.app import app

install()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
