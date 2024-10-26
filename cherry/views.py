
from django.shortcuts import render


from django.http import HttpResponse

from cherry.models import *
from django.db.models.functions import Length
from django.db.models import Q
from django.db.models import Avg,Sum,Max,Min,Count
# Create your views here.




def insert_dept(request):
    dpn=input('enter deptno:')
    dna=input('enter dname:')
    loc=input('enter loc:')
    DO=Dept.objects.get_or_create(deptno=dpn,dname=dna,loc=loc)

    if DO[1]:
        return HttpResponse('one record is inserted into dept')
    else:
        return HttpResponse(' this record alredy exist')




def insert_emp(request):
    dn = input('deptno: ')
    eno = input('empno: ')
    en = input('ename: ')
    j = input('job: ')
    hd = input('hiredate: ')
    sal = input('sal: ')
    comm = input('comm: ')
    mg = input('enter mgrno (or leave blank for NULL): ')
    
    if comm ==0:
        comm=None
    if mg == '':
        MGOL=''


    else:
        MGO = Emp.objects.filter(empno=mg) 
        if MGO:
            MGOL = MGO[0]
        else:
            return HttpResponse('MGR no is not available')

    DO=Dept.objects.filter(deptno=dn)
    if DO:
        DOL=DO[0]
        EO=Emp.objects.get_or_create(empno=eno,ename=en,job=j,hiredate=hd,sal=sal,comm=comm,mgr=MGOL,deptno=DOL)
        return HttpResponse('One record inserted succeffuly')
    else: 
        return HttpResponse('dept no is not avalible')


def display_data(request):
   depts_list=Dept.objects.all()
  
   #emps=Emp.objects.filter(ename__range=('a','k'))
   #emps=Emp.objects.filter(ename__startswith='a')
   #emps=Emp.objects.filter(ename__endswith='e')
   #emps=Emp.objects.filter(ename__startswith='a')
   emps=Emp.objects.all()
   return render(request,'test1.html',context={'depts_list':depts_list,'emps':emps})

def empdept(request):
    EDO=Emp.objects.select_related('deptno').all()
    EDO=Emp.objects.select_related('mgr').all()
    EDO=Emp.objects.select_related('mgr','deptno').all()
    EDO=Emp.objects.select_related('deptno').filter(deptno__dname='SALES') 
    EDO=Emp.objects.select_related('deptno').filter(deptno__dname='ACCOUNTING')
    EDO=Emp.objects.select_related('mgr').filter(Q(deptno=30) | Q(deptno=20))
    EDO=Emp.objects.select_related('deptno','mgr').order_by('deptno__dname')
    EDO=Emp.objects.select_related('deptno','mgr').order_by('-deptno__dname')
    EDO=Emp.objects.select_related('deptno','mgr').order_by(Length('deptno__dname'))
    EDO=Emp.objects.select_related('deptno','mgr').order_by(Length('deptno__dname').desc())
    EDO=Emp.objects.select_related('deptno').filter(deptno__dname__startswith='S',ename__startswith='S')
    EDO=Emp.objects.select_related('deptno').filter(deptno__dname__contains='S')
    EDO=Emp.objects.select_related('deptno').filter(deptno__dname__iregex=r'^s',ename__iregex=r'^s')
    EDO=Emp.objects.select_related('deptno').filter(deptno__gt=20)
    EDO=Emp.objects.select_related('deptno').filter(deptno__lt=30)
    EDO=Emp.objects.select_related('deptno').filter(deptno__gte=20)
    EDO=Emp.objects.select_related('deptno').filter(deptno__lte=30)
    EDO=Emp.objects.select_related('deptno').filter(hiredate__year=2024)
    EDO=Emp.objects.select_related('deptno').filter(hiredate__month=6)
    EDO=Emp.objects.select_related('deptno').filter(hiredate__day=13)
    
    
    EDO=Emp.objects.filter(deptno__in=Dept.objects.all()).values('deptno__loc', 'ename')
    #EDO=Emp.objects.select_related('deptno').values('mgr', 'ename')
    EDO=Emp.objects.all()
    return render(request,'empdept.html',{'EDO':EDO})
    


    
def deptemp(request):
    
    LDEO=Dept.objects.prefetch_related('emp_set').all()
    
    d={'LDEO':LDEO}
    return render(request,'deptemp.html',d)
    
    
def aggregate_functions(request):
    #Displaying the avg sal of all the employess
    print(Emp.objects.all().aggregate(Avg('sal')))
    #Diplaying the avg sal of all the employees by changing the key name
    print(Emp.objects.all().aggregate(avg_salary=Avg('sal')))
    #Displaying the avg salary of employees department wise separately
    print(Emp.objects.values('deptno').annotate(Avg('sal')))
    #Displaying the avg sal of a particular department
    print(Emp.objects.filter(deptno=40).aggregate(Avg('sal')))
    #Printing the details of employee whose salary is > than the avg salary of all the employees
    DOAVS=Emp.objects.all().aggregate(avg_salary=Avg('sal'))
    print(DOAVS)
    emps=Emp.objects.select_related('deptno').filter(sal__gt=DOAVS['avg_salary'])
    #Printing the details of employee whose salary is >= than the avg salary of all the employees
    emps=Emp.objects.select_related('deptno').filter(sal__gte=DOAVS['avg_salary'])
    #Printing the details of employee whose salary is < than the avg salary of all the employees
    emps=Emp.objects.select_related('deptno').filter(sal__lt=DOAVS['avg_salary'])
    #Printing the details of employee whose salary is <= than the avg salary of all the employees
    emps=Emp.objects.select_related('deptno').filter(sal__lte=DOAVS['avg_salary'])
    #MAX sal of the employees
    print(Emp.objects.all().aggregate(Max('sal')))
    #printing the details of the employees whose sal is >= avg and max of the employees
    DOMS=Emp.objects.all().aggregate(Max('sal'))
    emps=Emp.objects.select_related('deptno').filter(sal__gte=DOAVS['avg_salary'],sal__lte=DOMS['sal__max'])
    #Min sal of the employees
    print(Emp.objects.all().aggregate(Min('sal')))
    #printing the details of the employees whose sal is <= avg and max of the employees
    DOMS=Emp.objects.all().aggregate(Min('sal'))
    emps=Emp.objects.select_related('deptno').filter(sal__lte=DOAVS['avg_salary'],sal__gte=DOMS['sal__min'])
    #sum of sal of all the employees
    print(Emp.objects.all().aggregate(Sum('sal')))
    #Sum of sal of all the employees department wise separately
    print(Emp.objects.values('deptno').annotate(Sum('sal')))
    #Displaying the sum of  sal of a particular department
    print(Emp.objects.filter(deptno=40).aggregate(Sum('sal')))
    #counting of employees 
    print(Emp.objects.all().aggregate(Count('ename')))
    #Counting employess in a particular department
    print(Emp.objects.filter(deptno=30).aggregate(Count('ename')))
    #Counting of employees by checking a specific condition
    print(Emp.objects.filter(sal__lt=DOAVS['avg_salary']).aggregate(Count('sal')))
    

    d={"emps":emps}
    return render(request,'test1.html',d)

    
    
def update_data(request):
    from django.db.models import Q
    #HERE changing of salary whose name Aafiya Thabasum and empno is 143
    #Emp.objects.filter(empno=143,ename='Aafiya Thabasum').update(sal=52390)

    #updating the deptno's of employees who's designations are satisfying below condition
    #Emp.objects.filter(Q(job='DATA ANALYST') | Q(job='SQL DEVELOPER') | Q(job='DJANGO DEVELOER')).update(deptno=20)

    #Now updating parent table column data
    #Emp.objects.filter(ename='ANIKETH SHARMA').update(deptno=50)
    '''It will throw an error becoz whenever we r modifying parent
      table data we should provide the data which is present in parent table'''
    
    #if the condition zero rows satisfy .....
    #Emp.objects.filter(job='LOVE BIRD').update(ename='Aafiya charan')
    '''If the zero rows  satisfy the condition in case of update method nothing it will do
    (i mean it will not perform any operation and it will not thorw any eeor)'''

    #BY USING UPDATE OR CREATE updating the commission whose name is CHARAN KUMAR
    #Emp.objects.update_or_create(ename='CHARAN KUMAR',defaults={'comm':1680})
    #By using the update or create method i am going to change the mgr to 12345 emp who r working as FULL STACK DEVELOER
   # Emp.objects.update_or_create(job='FULL STACK DEVELOER',defaults={'mgr':56789})
    '''ERROR IS ANSWER BCOZ HERE THE CONDITON SATISFYES MORE THANE ONE ROW
      (IN case of up_or_cr method we can not update if condition staisfies more than one row)'''

    #Now if we r going to update parent table coumns data
   # Emp.objects.update_or_create(ename='CHARAN KUMAR',defaults={'deptno':40})
    #Error is answer becozz...
    '''whenever we r modifying  parent table data we should provide an object of parent table'''

    #Here it will update the parent table coumns data
    do=Dept.objects.get(deptno=40)
    #Emp.objects.update_or_create(ename='CHARAN KUMAR',defaults={'deptno':do})

    eo=Emp.objects.get(empno=12345)
    Emp.objects.update_or_create(ename='CHARANn ',defaults={'deptno':do})

    #Emp.objects.update_or_create(ename='CHARAN ',defaults={'deptno':do,'job':'PYTHON ENGINEER','empno':1323,'mgr':eo,'hiredate':'2024-2-7','sal':25456})
    '''If we are providing the values for updation we should provide the values based on the constraints or else rules and regiulations'''
    
    emps=Emp.objects.all()
    d={'emps':emps}
    return render(request,'test1.html',d)

    

    

    
def deletion_data(request):
    #Emp.objects.filter( deptno=40).delete()
    Dept.objects.filter(deptno=50).delete()
    #Emp.objects.filter(ename='PARVEZ').delete()
    #Emp.objects.all().delete()
    emps=Emp.objects.all()
    d={'emps':emps}
    return render(request,'test1.html',d)