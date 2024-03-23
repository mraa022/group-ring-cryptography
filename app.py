from flask import Flask 
from flask import request
import requests
import json
# template flask
from flask import render_template
app = Flask(__name__)

state = {'encrypt': '', 'decrypt': ''}
@app.route('/', methods=['GET'])
def home_get():
    return render_template('index.html', plain_text = '',encrypted_text = '')

@app.route('/', methods=['POST'])
def home_post():
    
    type  = request.form['submit-btn']
    if type == 'Encrypt':
        message = request.form['encrypt']
        code = f'''
G = CyclicPermutationGroup(5)
R = R = Integers(149813)
A = GroupAlgebra(G, R);
sigma = G.gen()
g = A(G.gen())
u = g-g^3-g^4
def split_message(message):
    chunk_size = 5  
    chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]  # Split the message into chunks
    return chunks
def msg_chunk_to_gr(chunk):
    group_ring_element = ord(chunk[0])*g^0
    i = 1
    for char in chunk[1:]:
        
        group_ring_element+=ord(char)*g^i
        i+=1
    return group_ring_element
def msg_to_gr(msg):
    return [msg_chunk_to_gr(chunk) for chunk in msg]

def encrypt_msg(msg):
    return [u*chunk for chunk in msg]
def decrypt_msg(msg):

    return [(u^-1)*chunk for chunk in msg]
def gr_to_msg_chunk(gr_message_chunk):
    coeffs = [gr_message_chunk.coefficient(sigma^i) for i in range(0,5)] # this makes sure the elements are ordered in e,g,g^1,g^2,g^3,g^4
    return ''.join([chr(unicode) for unicode in coeffs ])
def gr_to_msg(gr_msg):
    return ''.join([gr_to_msg_chunk(chunk) for chunk in gr_msg]);
    
chunk_pieces = split_message('{message}')
e_group_ring_chunks = msg_to_gr(chunk_pieces)
encrypted_group_ring_msg = encrypt_msg(e_group_ring_chunks)
encrtyped_str_msg = gr_to_msg(encrypted_group_ring_msg)
print(encrtyped_str_msg)'''
        result  = requests.post('https://sagecell.sagemath.org/service', data = {'code': code}).text
       
        encrypted_string = json.loads(result)['stdout'][:len(message)]
        # print([ord(c) for c in encrypted_string])
        state['encrypt'] = encrypted_string
        return render_template('index.html', plain_text = message,encrypted_text = encrypted_string)
    else:
        message = request.form['decrypt']
        code = f'''
G = CyclicPermutationGroup(5)
R = R = Integers(149813)
A = GroupAlgebra(G, R);
sigma = G.gen()
g = A(G.gen())
u = g-g^3-g^4
def split_message(message):
    chunk_size = 5  
    chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]  # Split the message into chunks
    return chunks
def msg_chunk_to_gr(chunk):
    group_ring_element = ord(chunk[0])*g^0
    i = 1
    for char in chunk[1:]:
        
        group_ring_element+=ord(char)*g^i
        i+=1
    return group_ring_element
def msg_to_gr(msg):
    return [msg_chunk_to_gr(chunk) for chunk in msg]

def encrypt_msg(msg):
    return [u*chunk for chunk in msg]
def decrypt_msg(msg):

    return [(u^-1)*chunk for chunk in msg]
def gr_to_msg_chunk(gr_message_chunk):
    coeffs = [gr_message_chunk.coefficient(sigma^i) for i in range(0,5)] # this makes sure the elements are ordered in e,g,g^1,g^2,g^3,g^4
    return ''.join([chr(unicode) for unicode in coeffs ])
def gr_to_msg(gr_msg):
    return ''.join([gr_to_msg_chunk(chunk) for chunk in gr_msg]);
    
chunk_pieces = split_message('{message}')
group_ring_chunks = msg_to_gr(chunk_pieces)
decrypted_group_ring_msg = decrypt_msg(group_ring_chunks)
decrypted_str_msg = gr_to_msg(decrypted_group_ring_msg)
print(decrypted_str_msg)'''
        result  = requests.post('https://sagecell.sagemath.org/service', data = {'code': code}).text
        decrypted_string = json.loads(result)['stdout'].rstrip().lstrip()[:len(message)]
        print([ord(c) for c in decrypted_string])
        return render_template('index.html', plain_text = decrypted_string, encrypted_text = message)
if __name__ == '__main__':
    app.run(template_folder='template')