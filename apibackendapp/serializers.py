from rest_framework import serializers #import module
from .models import Employee, Department
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):                    
  #creating a custom field called group_name
  group_name=serializers.CharField(write_only=True, required=False)
  #write_only means the field will be used for input

  #function to create the user
  def create(self, validated_data):
    #we will receiving username,password and group_name
    #at first remove the group_name from the validated_data
    #so that we have only username and password to create the user
    group_name= validated_data.pop("group_name", None)
    #as part of the security, encyrpt the password and save it
    validated_data['password'] = make_password(validated_data.get("password"))
    #create the user using the validated_data containing username and password
    user = super(SignupSerializer,self).create(validated_data)
    #now we can add the created user to the group
    if group_name:
        group, created = Group.objects.get_or_create(name=group_name)
        #attempting create a group object with the specified group name if not exists
        user.groups.add(group) #add the user to the group
    return user #return the newly created user

  class Meta:
        model = User
        fields =  ['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #creating the custom field for username
    username = serializers.CharField()
    class Meta:
        model = User
        fields =  ['username','password']




#create serializer by inheriting ModelSerializer class
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: #will provide metadata to the model
       model = Department
       fields = ('DepartmentId','DepartmentName')
     

def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("Name must be atleast 3 chars")
    return employee_name

class EmployeeSerializer(serializers.ModelSerializer):
    #Department is a custom field in this serializer
    #source='DepartmentId says that the field should get data about
    #the DepartmentId of that employee in the model
    Department = DepartmentSerializer(source='DepartmentId', read_only=True)
    #adding validation fn called 'name_validation' to the field EmployeeName
    #add the validator
    EmployeeName = serializers.CharField(max_length=200,validators=[name_validation])
    class Meta:
        model = Employee
        fields = ('EmployeeId','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentId','Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username') #get only these two fields