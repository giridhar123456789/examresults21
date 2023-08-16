from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.http import HttpResponse
from.models import Student

def index(request):
    return render(request,'index.html')

def result(request):
    if request.method=='POST':
        rollNo=int(request.POST['roll_no'])
        student=Student.objects.get(roll_no=rollNo)
        telugu=student.telugu
        sanskrit=student.sanskrit
        english=student.english
        maths=student.maths
        science=student.science
        social=student.social
        total=telugu+sanskrit+english+maths+science+social
        percent=total/400*100
        if percent>90:
            status='S grade'
        elif percent>80:
            status='A grade'
        elif percent>70:
            status='B grade'
        elif percent>60:
            status='C grade'
        elif percent>50:
            status='D grade'
        else :
            status='fail apply for supplimentary'
        params={
            'roll_no': rollNo,
            'name':student.name,
            'telugu':telugu,
            'sanskrit':sanskrit,
            'english':english,
            'maths':maths,
            'science':science,
            'social':social,
            'total':total,
            'percent':percent,
            'status':status
       }
        return render(request, 'result.html', params)
    else:
        print('get method')
    return render(request, 'result.html')



def admin_login(request):
    if 'user' in request.session:
        return render(request, 'admin_panel.html')
    else:
        return render(request, 'admin-login.html')

def admin_panel(request):
        if 'user' in request.session:
            students = Student.objects.all()
            params = {'students': students}
            return render(request, 'admin_panel.html', params)
        else:
            if request.method == 'POST':
                user_name = request.POST['uname']
                pass_word = request.POST['pwd']
                if user_name == 'giridhar' and pass_word == 'giri143':
                    request.session['user'] = user_name
                    students = Student.objects.all()
                    params = {'students':students}
                    return render(request, 'admin_panel.html', params)
                else:
                    return render(request, 'admin-login.html')
            else:
                return render(request, 'admin-login.html')

def delete_student(request, id):
    get_stu = Student.objects.get(id=id)
    get_stu.delete()
    return redirect('/admin_panel')

def edit_student(request, id):
    get_stu = Student.objects.get(id=id)
    params = {'student': get_stu}
    return render(request, 'edit.html', params)

def edit_confirm(request, id):
        if request.method == 'POST':
            get_stu = Student.objects.get(id=id)
            get_stu.name = request.POST['sname']
            get_stu.roll_no = request.POST['roll-no']
            get_stu.telugu = request.POST['telugu']
            get_stu.sanskrit= request.POST['sanskrit']
            get_stu.english = request.POST['english']
            get_stu.maths = request.POST['maths']
            get_stu.science = request.POST['science']
            get_stu.social = request.POST['social']
            total = int(request.POST['telugu'])+int(request.POST['sanskrit'])+int(request.POST['english'])+(request.POST['maths']) + int(request.POST['science'])+int(request.POST['social'])
            get_stu.total = total
            get_stu.percent = total / 6

            get_stu.save()
            return redirect('/admin_panel')
        else:
            return redirect('/admin_login')

def admin_logout(request):
    del request.session['user']
    return redirect('/')

def add_student(request):
    return render(request,'add_student.html')
def add_confirm(request):
    if request.method == 'POST':
        sname = request.POST['sname']
        roll_no = request.POST['roll-no']
        telugu = int(request.POST['telugu'])
        sanskrit= int(request.POST['sanskrit'])
        english= int(request.POST['english'])
        maths= int(request.POST['maths'])
        science = int(request.POST['science'])
        social = int(request.POST['social'])
        total = telugu+sanskrit+english+maths+science+social
        percent = total/400*100
        add_student = Student.objects.create(name=sname,roll_no=roll_no,
                        telugu=telugu,sanskrit=sanskrit,english=english,maths=maths,science=science,social=social,
                        total=total,percent=percent,)
        add_student.save()
        return redirect('/admin_panel')
    else:
        return redirect('/admin_panel')