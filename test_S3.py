#coding: utf8
import boto3
import datetime
s3=boto3.client("s3")
s3.download_file("elasticbeanstalk-eu-west-1-062282685834","resultS3.txt","resultS3.txt")  # download du fichier depuis S3
print (str(datetime.datetime.now()))
fic = open("resultS3.txt", "a")  # Ouverture locale du fichier
fic.writelines(str(datetime.datetime.now())+"\n")   # Ajout d'une ligne dans le fchier local
fic.close()  # fermeture du fichier local
s3.upload_file("resultS3.txt", "elasticbeanstalk-eu-west-1-062282685834", "resultS3.txt") # upload du fichier modifié vers S3