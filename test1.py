import zlib
import struct
import numpy as np

class Image:

    def Recon_a(this, r, c):
        return this._Recon[r * this._stride + c - this._bytesPerPixel] if c >= this._bytesPerPixel else 0

    def Recon_b(this, r, c):
        return this._Recon[(r-1) * this._stride + c] if r > 0 else 0

    def Recon_c(this, r, c):
        return this._Recon[(r-1) * this._stride + c - this._bytesPerPixel] if r > 0 and c >= this._bytesPerPixel else 0

    def PaethPredictor(this, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            Pr = a
        elif pb <= pc:
            Pr = b
        else:
            Pr = c
        return Pr

    def read_chunk(this, f):
        # Returns (chunk_type, chunk_data)
        chunk_length = int.from_bytes(f.read(4), "big")
        chunk_type = f.read(4)
        chunk_data = f.read(chunk_length)
        f.read(4) #crc
        return chunk_type, chunk_data

    def imread(this, img_src):
        f = open(img_src, 'rb')

        # read header
        header = f.read(8)
        if(header == b'\x89PNG\r\n\x1a\n'):
            this._type = 'PNG'
        else:
            raise Exception("This format is not supported")

        chunks = []
        while True:
            chunk_type, chunk_data = this.read_chunk(f)
            chunks.append((chunk_type, chunk_data))
            if chunk_type == b'IEND':
                break

        _, IHDR_data = chunks[0]
        # read ihdr
        # big - Big byte-order is like the usual decimal notation, but in base 256:
        # data_lenght | chunk_type | chunk_data        | CRC
        # 4bytes      | 4bytes     | data_lenght bytes | 4bytes
        this._width, this._height, bitd, this._color_type, compm, this._filterm, interlacem = struct.unpack('>IIBBBBB', IHDR_data)

        # 1px contains rgba = 4bytes
        if(this._color_type == 6): this._bytesPerPixel = 4
        # stride = total pixel horizontal direction
        this._stride = this._bytesPerPixel * this._width

        this._IDAT_data = b''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == b'IDAT')
        
        # decompess data    
        this._IDAT_data = zlib.decompress(this._IDAT_data)
        # each bytes now be Filter Function -> Reconstruction

        # each byte be recontruct be store here
        this._Recon = []
        i = 0
        for r in range(this._height): # for each scanline
            filter_type = this._IDAT_data[i] # first byte of scanline is filter type
            i += 1
            for c in range(this._stride): # for each byte in scanline
                Filt_x = this._IDAT_data[i]
                i += 1
                if filter_type == 0: # None
                    Recon_x = Filt_x
                elif filter_type == 1: # Sub
                    Recon_x = Filt_x + this.Recon_a(r, c)
                elif filter_type == 2: # Up
                    Recon_x = Filt_x + this.Recon_b(r, c)
                elif filter_type == 3: # Average
                    Recon_x = Filt_x + (this.Recon_a(r, c) + this.Recon_b(r, c)) // 2
                elif filter_type == 4: # Paeth
                    Recon_x = Filt_x + this.PaethPredictor(this.Recon_a(r, c), this.Recon_b(r, c), this.Recon_c(r, c))
                else:
                    raise Exception('unknown filter type: ' + str(filter_type))
                this._Recon.append(Recon_x)
        this._rbga_array = np.array(this._Recon).reshape((this._height, this._width, 4))
        return this._rbga_array

    def get_pixel(this, pos):
        # return [i[pos[0]][pos[1]] for i in this._rbga_array]
        for i in this._rbga_array:
            print(i)

    def blur(this, ksize):

        def kernel_chooser(pos):
            kernel_index = []
            k_h = ksize[0] // 2
            for ky in range(ksize[0]):
                t = []
                k_w = ksize[1] // 2
                for kx in range(ksize[1]):
                    t.append([pos[0] - k_h, pos[1] - k_w])
                    k_w -= 1
                kernel_index.append(t)
                k_h -= 1 
            # [
            #     [[1, 1], [1, 1], [1, 1]],
            #     [[1, 1], [1, 1], [1, 1]],
            #     [[1, 1], [1, 1], [1, 1]]
            # ]
            return kernel_index

        def kernel_sum(pos, height, width):
            kernel_index = kernel_chooser(pos)
            
            times = 0
            s = 0
            for y in kernel_index:
                for e in y:
                    if(e[0] < 0 or e[0] >= height or e[1] < 0 or e[1] >= width):
                        continue
                    times += 1
                    s += sum(this.get_pixel([e[0], e[1]]))
            return s / times    

        kernel = np.ones(ksize, np.uint8)
        blur_rbga_array = np.zeros((this._height, this._width), dtype=np.uint8)
        for y in range(this._width):
            for x in range(this._height):
                blur_rbga_array[y][x] = kernel_sum([y, x], this._height, this._width)

        return blur_rbga_array        
                

                        

i = Image()

a = i.imread('./Capture.PNG')

b = i.blur((3, 3))

import matplotlib.pyplot as plt
import numpy as np
plt.imshow(b)
plt.show()
