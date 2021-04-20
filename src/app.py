from appCreator import app

DEBUG = False
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

if __name__ == "__main__":
	app.run(HOST, debug=DEBUG) 