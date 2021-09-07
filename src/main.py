import time 
import threading
from queue import PriorityQueue
from flask import Flask, request, jsonify

from hotspot.hotspot import hotspot_bp
import animation as anim

class Main:
    def __init__(self):        
        print("Hello world !")
        self.app = Flask(__name__)
        self.app.register_blueprint(hotspot_bp, url_prefix='/')

        self.th_animation = threading.Thread(target=anim.init_animation, args=(self.app.logger,))
    
    def __del__(self):
        print("Goodbye wold !")

    def main(self):
        self.th_animation.start()
        self.app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main = Main()
    main.main()