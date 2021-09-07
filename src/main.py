from flask import Flask

from hotspot.hotspot import hotspot_bp

class Main:
    def __init__(self):        
        self.app = Flask(__name__)
        self.app.register_blueprint(hotspot_bp, url_prefix='/')
    
    def __del__(self):
        print("Goodbye wold !")

    def main(self):
        self.app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main = Main()
    main.main()