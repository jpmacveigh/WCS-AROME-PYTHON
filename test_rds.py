import boto3
client=boto3.client('rds-data')
response=client.execute_statement(
    database='meteo',
    resourceArn='arn:aws:rds:eu-west-1:062282685834:cluster:jpmv-databse',
    secretArn="arn:aws:secretsmanager:eu-west-1:062282685834:secret:rds-db-credentials/cluster-LSENPZZQFZTU2EEMIKD6PWOL5U/admin-rv6lry",
    sql='select * from previsions;'
)
#print (response)
for rec in response["records"]:
  print (rec)
