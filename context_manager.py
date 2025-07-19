from contextlib import contextmanager

@contextmanager
def open_file(name):
    f = open(name, 'w')
    try:
        yield f 

    finally:
        f.close()

# with open_file('demo.txt') as f:
#     f.write('Hello World!')


# class-based context managers

def __enter__(self):
    return self.file_obj

def __exit__(self, type, value, traceback):
    self.file_obj.close()

'''t = True
if t is True:
    print("DAvid")
    if t is True:
        print("Amobi")
        if t is True:
            print("Dave2")
print("Dave Again!!!")
'''

