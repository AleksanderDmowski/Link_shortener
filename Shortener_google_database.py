from flask import Flask, render_template, request, redirect
from google.cloud import storage
import os
import random

credential_path = "your_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
app = Flask(__name__)

storage_client = storage.Client()


project_id = "yourproject"
main_bucket_name = "yourdomain.appspot.com"
blob_name = 'your_database.txt'
test_mode = True
flask_run = True

domain = 'http://yourdomain.com'
if test_mode:
    domain = 'http://127.0.0.1:5000'


def authenticate_implicit_with_adc(project_id):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<path:url>')
def page(url):
    return render_template('/'+url)


@app.route('/MyWork/Project/submit_link_shorter', methods=['POST', 'GET'])
def submit_form2():
    if test_mode:
        print('Test mode submit_form2')
    if request.method == 'POST':
        link = request.form.get('subject')
        return render_template('/MyWork/Project/linkShorter.html', end_link=(f'Its your link: {str(shorter(link))}'))
    else:
        return 'something wrong'


@app.route('/MyWork/Project/todo', methods=['POST', 'GET'])
def submit_link_shorter():
    if request.method == 'POST':
        link = request.form.get('subject')
        return render_template('/MyWork/Project/linkShorter.html', end_link=(f'Its your code for share: {str(shorter(link))}'))
    else:
        return 'something wrong'


def shorter(link, project_id=project_id, bucket_name=main_bucket_name, blob_name=blob_name):
    if test_mode:
        print('test mode start shortering function')
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    auto_grow = True
    txt_dict = {}
    id_start = 10000
    id_end = 10999
    with blob.open("r") as database:
        print(txt_dict)
        for line in database:
            (k, v) = line.split()
            txt_dict.update({k: v})

        if auto_grow:
            if len(dict(txt_dict)) >= id_end-id_start:
                while id_end-id_start < len(dict(txt_dict)):
                    id_end += 1000

        if link in txt_dict:
            if test_mode:
                print(str(dict(txt_dict).get(link)))
            return str(dict(txt_dict).get(link))
        else:
            if test_mode:
                print('dodawanie nowego linku')
            id_ = random.randint(id_start, id_end)
            x = (('{}/linkShorter/{}').format(domain, id_))
            while x in txt_dict.values():
                id_ = random.randint(id_start, id_end)
                x = (('{}/linkShorter/{}').format(domain, id_))

            txt_dict.update({link: x})
            y = ''
            if test_mode:
                print(txt_dict)
            for k in txt_dict:
                y += (f'{k} {txt_dict[k]}\n')
            blob.upload_from_string(y)

            if test_mode:
                print(
                    f"{blob_name} with contents {link} as {x} uploaded to {bucket_name}.")
            return str(dict(txt_dict).get(link))


@app.route('/linkShorter/<id_db>')
def go_to(id_db, bucket_name=main_bucket_name, blob_name=blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with blob.open("r") as database:
        for line in database:
            (k, v) = line.split()

            if (('{}/linkShorter/{}').format(domain, id_db)) == v:
                return redirect(k)
    return 'something wrong'

# /////////////////////////////////////


def clear(project_id, bucket_name=main_bucket_name, blob_name=blob_name):
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string('')
    print('clear')
