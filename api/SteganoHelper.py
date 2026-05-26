import os;

from PIL import Image;
from Crypto.Random import get_random_bytes;

class SteganoHelper():
    def __init__(self, crypt=None):
        self.crypt = crypt;

    def genData(self, data):
        newd = [];
        for i in data:
            newd.append(format(ord(i), '08b'));
        return newd;

    def modPix(self, pix, data):
        datalist = self.genData(data);
        lendata = len(datalist);
        imdata = iter(pix) ;
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]];
            for j in range(0, 8):
                if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                    pix[j] -= 1;
                elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                    if(pix[j] != 0):
                        pix[j] -= 1;
                    else:
                        pix[j] += 1;
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    if(pix[-1] != 0):
                        pix[-1] -= 1;
                    else:
                        pix[-1] += 1;
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1;
            pix = tuple(pix)
            yield pix[0:3];
            yield pix[3:6];
            yield pix[6:9];
    
    def encode_enc(self, newimg, data):
        w = newimg.size[0];
        (x, y) = (0, 0);
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel);
            if (x == w - 1):
                x = 0;
                y += 1;
            else:
                x += 1;

    def encode(self, path_img, message, prefix="stegano"):
        if not os.path.exists(path_img):
            return False;
        if self.crypt != None:
            message = self.crypt.encrypt(message);
        
        image = Image.open(path_img, 'r');
        newimg = image.copy();
        self.encode_enc(newimg, message);
        new_image_name = path_img[:path_img.rfind(".")] + "_" + prefix + "_" + path_img[path_img.rfind("."):];
        if os.path.exists(new_image_name):
            os.unlink(new_image_name);
        newimg.save(new_image_name, str(new_image_name.split(".")[1].upper()));
        return True;
    
    def decode(self, path_img):
        if not os.path.exists(path_img):
            return None;
        image = Image.open(path_img, 'r');
        data = "";
        imgdata = iter(image.getdata());
        while (True):
            pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]];
            binstr = ''
            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0';
                else:
                    binstr += '1';
            data += chr(int(binstr, 2));
            if (pixels[-1] % 2 != 0):
                if self.crypt != None:
                    data = self.crypt.decrypt(data);  
                return data;

