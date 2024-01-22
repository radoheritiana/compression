from node import Node
import heapq, os, json

class Huffman:
    def __init__(self):
        self.heap = []
        self.code = {}
        self.reverse_code = {}
    
    def compression(self, path):
        filename, file_extension = os.path.splitext(path)
        output_path = filename + ".rhja"
        
        with open(path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            #traitement
            frequency_dict = self.frequency_from_text(text)
            self.build_heap(frequency_dict)
            self.build_binary_tree()
            self.build_tree_code()
            encoded_text = self.build_encoded_text(text)
            padded_text = self.build_padded_text(encoded_text)
            bytes_array = self.build_byte_array(padded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
            
        with open(output_path, 'a') as fichier:
            separateur = '||'
            
            if fichier.tell() != 0:
                fichier.write(separateur)

            # Écriture du dictionnaire dans le fichier
            json.dump(self.reverse_code, fichier)
            
        return output_path
            
    # calculer la fréquence de chaque mot et le stocker dans un dictionnaire
    def frequency_from_text(self, text):
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0
            freq_dict[char] += 1
        return freq_dict
    
    def build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = Node(key, frequency)
            heapq.heappush(self.heap, binary_tree_node)
    
    def build_binary_tree(self):
        while len(self.heap) > 1:
            left_node = heapq.heappop(self.heap)
            right_node = heapq.heappop(self.heap)
            sum_of_frequency = left_node.frequency + right_node.frequency
            new_node = Node(None, sum_of_frequency)
            new_node.left = left_node
            new_node.right = right_node
            heapq.heappush(self.heap, new_node)
        return
    
    def build_tree_code_helper(self, root, curr_bits):
        if root is None:
            return
        
        if root.value is not None:
            self.code[root.value] = curr_bits
            self.reverse_code[curr_bits] = root.value
            return
        
        self.build_tree_code_helper(root.left, curr_bits+'0')
        self.build_tree_code_helper(root.right, curr_bits+'1')
    
    def build_tree_code(self):
        root = heapq.heappop(self.heap)
        self.build_tree_code_helper(root, '')
        
    def build_encoded_text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self.code[char]
        return encoded_text
    
    def build_padded_text(self, encoded_text):
        padding_value = 8 - len(encoded_text) % 8
        for i in range(padding_value):
            encoded_text += '0'
        
        padded_info = "{0:08b}".format(padding_value)
        padding_text = padded_info + encoded_text
        return padding_text
        
    def build_byte_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            array.append(int(byte, 2))
            
        return array
    
    def decompression(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ''
            bytes_string = file.read()
            
            separateur = '||'.encode('utf-8')

            # Trouver l'index du caractère de séparation
            separateur_index = bytes_string.index(separateur)

            # Séparer les données en bytes JSON et autres bytes
            encoded_data = bytes_string[:separateur_index]
            reverse_code = bytes_string[separateur_index + len(separateur):]
            reverse_code = reverse_code.decode('utf-8')
            reverse_code = json.loads(reverse_code)
                                    
            for byte in encoded_data:
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
            
            text_after_removing_padding = self.remove_padding(bit_string)
            actual_text = self.decode_text(text_after_removing_padding, reverse_code)
            output.write(actual_text)
    
        return output_path
            
    def remove_padding(self, text):
        padded_info = text[:8]
        padding_value = int(padded_info, 2)
        text = text[8:]
        text = text[:-1*padding_value]
        return text
    
    def decode_text(self, text, reverse_code):
        current_bits = ""
        decoded_text = ""
        for char in text:
            current_bits += char
            if current_bits in reverse_code:
                decoded_text += reverse_code[current_bits]
                current_bits = ""
        return decoded_text
        
