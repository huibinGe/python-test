from hashlib import sha256
import json
import time
from .extension import  db
from .models import BlockChain, Orders
import threading
from .zmqpublisher import publisher

import  base64
import qrcode
import io
import  os
_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"/conf.json"))

class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.result = self.func()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        #self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        #block_string = self.transactions+str(self.nonce)
        #print(self.__dict__)
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * 3):
            block.nonce += 1
            computed_hash = block.compute_hash()
            #print(computed_hash)
        #print("正在计算区块链2222222")
        #print('最终结果是:{}, 随机数:{}'.format(computed_hash,block.nonce))

        return computed_hash

def get_all_blocks(order_id):
    result = BlockChain.query.filter(BlockChain.order_id==order_id).order_by(BlockChain.chain_index).all()
    return result


    # first block of the chain
def add_new_block(message,order_id):

    block_data = ''
    block_in_chain = get_all_blocks(order_id)

    #qr list data

    #chain_index +1
    _index = len(block_in_chain) + 1

    #set transaction value
    new_block = Orders.query.get(order_id)
    transaction = "{}，商品名：{},时间：{},初始地：{},联系人：{},电话：{},目的地：{},物流公司：{}\n".format(message,new_block.o_name, new_block.o_time, new_block.location,
                                                new_block.person, new_block.tel, new_block.desc, new_block.comp)

    small_transaction = "{},{}，商品名：{},时间：{},".format(_index, message, new_block.o_name, new_block.o_time)

    #first block of the chain
    if(_index==1):

        block = Block(_index,transaction,'0')
        pre_hash = ''
        pub = publisher(conf['private_server'], conf['port'], 'new_block')
        # pub.publish_newblock(block)
        _pub_thread = threading.Thread(target=pub.publish_newblock, kwargs={'data': block})
        _pub_thread.start()

        # get finished status
        _status = publisher(conf['private_server'], conf['signal_port'], '')
        _status_thread = MyThread(_status.req_rep)
        _status_thread.run()


        # _pub_req.start()
        #print(block.proof_of_work(block),'---------',block.nonce)


        cur_hash = _status_thread.result['finished']['cur_hash']
        nonce = block.nonce
        history = transaction
        little_h = small_transaction + "当前区块:{}\n".format(cur_hash)

    else:
        #get last chain's hash
        pre_hash = block_in_chain[-1].current_hash
        history = block_in_chain[-1].history + transaction
        little_h = block_in_chain[-1].little_h + small_transaction

        block = Block(_index,transaction,pre_hash)
        pub = publisher(conf['private_server'], conf['port'], 'new_block')
        # pub.publish_newblock(block)
        _pub_thread = threading.Thread(target=pub.publish_newblock, kwargs={'data': block})
        _pub_thread.start()

        # get finished status
        _status = publisher(conf['private_server'], conf['signal_port'], '')
        _status_thread = MyThread(_status.req_rep)
        _status_thread.run()

        cur_hash = _status_thread.result['finished']['cur_hash']
        nonce = block.nonce
        little_h += "当前区块:{}\n".format(cur_hash)

    block_c = BlockChain()
    block_c.order_id = order_id
    block_c.current_hash = cur_hash
    block_c.pre_hash = pre_hash
    block_c.random_num = nonce
    block_c.chain_index = _index
    block_c.history = history
    block_c.little_h = little_h

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=30,
        border=1,
    )
    qr.make(fit=True)
    qr.add_data(block_c.little_h)
    img = qr.make_image()

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_stream = buf.getvalue()
    heximage = base64.b64encode(image_stream)
    b64img = 'data:image/png;base64,' + heximage.decode()
    new_block.qrcode = b64img

    db.session.add(block_c)
    db.session.commit()
    print(block_c.history)
    return