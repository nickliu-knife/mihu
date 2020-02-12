import os
import json
import glob

from cloudant.client import Cloudant
from cloudant.adapters import Replay429Adapter

# Cloudant API reference: https://python-cloudant.readthedocs.io/en/latest/
with open('webhook.json',  'r') as f:
    cred = json.load(f)
cloudant_user_name = cred['cloudant_user_name']
cloudant_api_key = cred['cloudant_api_key']
client = Cloudant.iam(
            cloudant_user_name,
            cloudant_api_key,
            adapter=Replay429Adapter(),
            timeout=60, connect=True)

math_result_db = client.get('math_result', remote=True)

def add_new_record(user, timestamp, duration, correct, wrong):

    if user not in math_result_db:
        print('Document for %s dosenot exist, creating....' % user)
        doc = math_result_db.create_document(
            {
                '_id': user
            }
        )
        if doc.exists():
            print('Document %s is created sucessfully' % user)
        else:
            # TODO add retry logic here
            raise Exception('Failed to create document for %s' % user)
    else:
        doc = math_result_db[user]

    # doc[timestamp] = [duration, correct, wrong]
    doc[timestamp] = '%s %s %s' % (duration, correct, wrong)
    doc.save()
    print('The new result for %s is saved' % user)


def list_users():
    users = []
    for doc in math_result_db:
        if doc['_id'] not in ['schemal']:
            users.append(doc['_id'])
    return users

def load_user_records(user, sorted_by_time=True):
    
    if user not in math_result_db:
        return None
    
    doc = math_result_db[user]
    if sorted_by_time is True:
        sorted(doc.keys())
    results = []
    for key in doc:
        if key in ['_id', '_rev']:
            continue
        elems = doc[key].split(' ')
        results.append(
            {
                'timestamp': key, 
                'duration': elems[0],
                'correct': elems[1],
                'wrong': elems[2]
            }
        )
    return results
    

# --------------------------------------------------------------------------------
# DONOT USE IN CODE
# --------------------------------------------------------------------------------
def file_db_migrate():
    users_data = {}
    files = glob.glob('.' + '/**/*.txt', recursive=True)
    for f_path in files:
        f_name = os.path.basename(f_path)
        user = f_name.split('.')[0]
        if user not in users_data:
            users_data[user] = {
                'files' : [
                    f_path
                ]
            }
        else:
            users_data[user]['files'].append(f_path)

    for user, data in users_data.items():
        for f_path in data['files']:
            with open(f_path, 'r') as f:
                current_records = f.readlines()
            for record in current_records:
                record_elems = record.split(' ')
                add_new_record(
                    user=user, timestamp=record_elems[0], duration=record_elems[1], correct=record_elems[2], wrong=record_elems[3])



# Run python db.py only for dubugging purpose
if __name__ == '__main__':
    print(json.dumps(load_user_records('julie'), indent=4, sort_keys=True))
    print(list_users())