import boto3, datetime, botocore, os, re

bucket_name = 'optimizely-export-ng'
object_key = '10561433763/10561433763/2.0/2018/10/06/10611140972/10611140972-0-2018-10-06-r-00453.gz'

# https://optimizely-export-ng.s3.amazonaws.com/10561433763/10561433763/2.0/2018/10/06/10611140972/10611140972-0-2018-10-06-r-00453.gz

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
client = boto3.client('s3')

#print('bucket')
#print(bucket.objects.all())
#
#print(s3.list_objects(Bucket=bucket_name)['Contents'])

start_date = '2018-10-01'
end_date = '2018-10-24'
exp_id = '11366201340'

start_split = start_date.split('-')
start = datetime.date(int(start_split[0]), int(start_split[1]), int(start_split[2]))

end_split = end_date.split('-')
end = datetime.date(int(end_split[0]), int(end_split[1]), int(end_split[2]))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)

for d in daterange(start, end):
    file_key = '10561433763/10561433763/2.0/'+d.year+'/'+d.strftime('%m')+'/'+d.strftime('%d')+'/'+exp_id+'/'\
        +exp_id+'-0-'+d.year+'-'+d.strftime('%m')+'-'+d.strftime('%d')+'-r-'

    print(d.year,d.strftime('%m'),d.strftime('%d'))

#paginator = client.get_paginator('list_objects')
#for result in paginator.paginate(Bucket=bucket_name):
#    print('blah')


#def download_dir(client, resource, dist, local='/tmp', bucket=bucket_name):
#    paginator = client.get_paginator('list_objects')
#    for result in paginator.paginate(Bucket=bucket, Delimiter='/'):
#        if result.get('CommonPrefixes') is not None:
#            for subdir in result.get('CommonPrefixes'):
#                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
#        if result.get('Contents') is not None:
#            for file in result.get('Contents'):
#                if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
#                     os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
#                resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))
#
#def _start():
#    client = boto3.client('s3')
#    resource = boto3.resource('s3')
#    download_dir(client, resource, 'clientconf/', '/tmp')

#s3 = session.resource('s3')

#for obj in bucket.objects.all():
#    print(os.path.split(obj.key))
    #bucket.download_file(obj.key, filename)

#try:
#    s3.Bucket(bucket_name).download_file(object_key, 'test_townload.gz')
#except botocore.exceptions.ClientError as e:
#    if e.response['Error']['Code'] == '404':
#        print('This object does not exist')
#    else:
#        raise