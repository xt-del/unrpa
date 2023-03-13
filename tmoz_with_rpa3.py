import zlib
from _pickle import loads
import os
# A list containing archive handlers.
archive_handlers = [ ]

class TMOZv2ArchiveHandler(object):
    """
    Archive handler handling RPAv3 archives.
    """

    @staticmethod
    def get_supported_extensions():
        return [ ".rpa" ]

    @staticmethod
    def get_supported_headers():
        return [ b"TMOZ-02 " ]

    @staticmethod
    def read_index(infile):
        l = infile.read(40)
        offset = int(l[8:24], 16)
        key = int(l[25:33], 16)
        infile.seek(offset)
        index = loads(zlib.decompress(infile.read()))

        # Deobfuscate the index.

        for k in index.keys():

            if len(index[k][0]) == 2:
                # index[k] = [ (offset ^ key, dlen ^ key) for offset, dlen in index[k] ]
                index[k] = [ (offset ^ key, dlen ^ key) for dlen, offset in index[k] ]
            else:
                # index[k] = [ (offset ^ key, dlen ^ key, start) for offset, dlen, start in index[k] ]
                index[k] = [ (offset ^ key, dlen ^ key, start) for dlen, offset, start in index[k] ]
        return index


archive_handlers.append(TMOZv2ArchiveHandler)


class RPAv3ArchiveHandler(object):
    """
    Archive handler handling RPAv3 archives.
    """

    @staticmethod
    def get_supported_extensions():
        return [ ".rpa" ]

    @staticmethod
    def get_supported_headers():
        return [ b"RPA-3.0 " ]

    @staticmethod
    def read_index(infile):
        l = infile.read(40)
        offset = int(l[8:24], 16)
        key = int(l[25:33], 16)
        infile.seek(offset)
        index = loads(zlib.decompress(infile.read()))

        # Deobfuscate the index.

        for k in index.keys():

            if len(index[k][0]) == 2:
                index[k] = [ (offset ^ key, dlen ^ key) for offset, dlen in index[k] ]
            else:
                index[k] = [ (offset ^ key, dlen ^ key, start) for offset, dlen, start in index[k] ]
        return index


archive_handlers.append(RPAv3ArchiveHandler)


def creat_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


if __name__ == "__main__":

    filename = 'scripts_base.rpa'
    out_file_path = 'scripts_story'
    # 第几个class类里面的内容 0:TMOZ 1:RPA3
    num = 0


    if out_file_path:
        out_file_path = os.path.abspath(out_file_path)
    else:
        out_file_path = os.getcwd()

    creat_dir(out_file_path)    #创建文件夹

    infile_data = open(filename,'rb')

    return_data1 = archive_handlers[num].get_supported_headers()
    return_data2 = archive_handlers[num].read_index(infile_data)

    print(return_data2)
    print('编码格式',return_data1)

    #保存文件
    for _,(archive_path,archive_data) in enumerate(return_data2.items()):
        creat_dir(
            os.path.join(
                out_file_path,os.path.split(archive_path)[0]
            )
        )       #创建文件夹
        offset, length,_ = next(iter(archive_data))
        infile_data.seek(offset)
        with open(os.path.join(out_file_path,archive_path),'wb') as out_file:
            out_file.write(infile_data.read(length))

    print('done!')

