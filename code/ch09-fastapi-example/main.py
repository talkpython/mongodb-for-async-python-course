import fastapi
import uvicorn

api = fastapi.FastAPI()


def main():
    uvicorn.run(api)


@api.get('/')
def hello_world():
    return {'message': "Greetings to the world!"}


if __name__ == '__main__':
    main()
