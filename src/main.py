import time 
import werkzeug

from flask import Flask, request, jsonify

import threading
from queue import PriorityQueue

from hotspot import hotspot_bp
import animation as anim



#app.logger.debug('This is a DEBUG message')
#app.logger.info('This is an INFO message')
#app.logger.warning('This is a WARNING message')
#app.logger.error('This is an ERROR message')


class Main:
    def __init__(self):        
        print("Born wold !")
        self.app = Flask(__name__)
        self.app.register_blueprint(hotspot_bp, url_prefix='/')

        self.th_animation = threading.Thread(target=anim.init_animation, args=(self.app.logger,))
    
    def __del__(self):
        print("Goodbye wold !")

    def main(self):
        self.th_animation.start()
        self.app.run(host='0.0.0.0', port=81)

        

if __name__ == '__main__':
    main = Main()
    main.main()