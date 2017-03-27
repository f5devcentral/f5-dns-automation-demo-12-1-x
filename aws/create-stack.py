#!/usr/bin/python
import boto3
import json
import sys
from pprint import pprint
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-s','--stack',dest='stack')
parser.add_option('-i','--input_stack',dest='input_stack')
parser.add_option('-t','--template',dest='template')
parser.add_option('-p','--parameters',dest='parameters')
parser.add_option('--password-file',dest='password_file')
parser.add_option('--sshkey',dest='sshkey')
(options,args) = parser.parse_args()

ec2 = boto3.resource('ec2')
cloudformation = boto3.client('cloudformation')

stack_name = options.stack
template_body = open(options.template).read()
parameters = json.load(open(options.parameters))

if options.input_stack:
    for param in parameters:
        if param['ParameterKey'] == 'EniStackName':
            param['ParameterValue'] = options.input_stack

if options.password_file:
    password = open(options.password_file).readline().strip()
    for param in parameters:
        if param['ParameterKey'] == 'adminPassword':
            param['ParameterValue'] = password
        if param['ParameterKey'] == 'bigiqPassword':
            param['ParameterValue'] = password

if options.sshkey:
    for param in parameters:
        if param['ParameterKey'] == 'sshKey':
            param['ParameterValue'] = options.sshkey

stack = {'StackName':stack_name,
         'TemplateBody':template_body,
         'Parameters':parameters}
#print stack
print cloudformation.create_stack(**stack)


