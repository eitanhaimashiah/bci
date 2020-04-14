from bci.client import upload_sample

if __name__ == '__main__':
    upload_sample(host='127.0.0.1', port=8000, path='test_sample.mind', format='binary')
