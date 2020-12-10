from server.routes import *


if __name__ == "__main__":
	APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5001))
	