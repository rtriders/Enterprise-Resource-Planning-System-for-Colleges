import sqlite3
from tabulate import tabulate
import os
from getpass import getpass
import smtplib
import time

#making connection
connection=sqlite3.connect('erp_database.sqlite')

#cursor
cur=connection.cursor()

#creating table
sql_command='''CREATE TABLE IF NOT EXISTS Erp(
name VARCHAR(30),
admission_no VARCHAR(11),
roll_no INTEGER,
gender CHAR(1),
email VARCHAR(20),
address VARCHAR(20),
phone INTEGER);'''

#execute the table
cur.execute(sql_command)


#list of admission no.py
cur.execute('''SELECT admission_no FROM Erp''')
admm=cur.fetchall()
adm_list=[]
for i in admm:
    adm_list.append(i[0])
connection.commit()


#add record
def add():
    while True:
        ad=input('Press 1 to add record : ')
        if ad=='1':
            nam=input('Enter name : ').title()
            try:
                roll=int(input('Enter 13 digit Roll no. : '))
            except:
                print('roll no. must be integer value')
                continue
            gen=input('Enter the gender (M/F) : ').upper()
            if gen in 'MF':
                pass
            else:
                print('invalid gender (M/F) ')
                continue
            ema=input('enter the email : ')
            if '@' in ema:
                pass
            else:
                print('Invalid email')
                continue
            adr=input('enter the address : ')
            try:
                phon=int(input('enter 10 digit the phone no. : '))
            except:
                print('must be 10 digit integer')
                continue
            adm=input('Enter addmission no. : ')
            if adm not in adm_list:
                adm_list.append(adm)
            else:
                print('Admission no. already exist')
                continue
            cur.execute("""INSERT INTO Erp VALUES (?,?,?,?,?,?,?)""",(nam,adm,roll,gen,ema,adr,phon))
            connection.commit()
        else:
            print(os.system("cls"))
            break

#to update any thing
def update():
    while True:
        chek=input('''press 1 to update :
        press 2 to send updation email : ''')
        if chek=='1':
            up=input('enter Admission No. : ')
            if up in adm_list:
                cur.execute('''SELECT * FROM Erp WHERE admission_no=(?)''',(up,) )
                prin=cur.fetchall()
                print(tabulate(prin,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
                connection.commit()
                print("Name , Admission no. ,Gender and Roll no. couldn't be update")
                emai=input('enter email to be update : ')
                addre=input('enter address to be update : ')
                pho=input('enter phone no. to be update : ')
                cur.execute('''UPDATE Erp SET email=?,address=?,phone=? WHERE admission_no=(?)''',(emai,addre,pho,up,))
                connection.commit()

            else:
                print('Admission no. not exist')
                continue
        elif chek=='2':
            e=input("enter Admission no. :")
            if e in adm_list:
                print('>>>>>>>>>>>> processing .....')
                try:
                    cur.execute('''SELECT email FROM Erp WHERE admission_no=(?)''',(e,) )
                    cnfrm=cur.fetchall()
                    cur.execute('''SELECT name FROM Erp WHERE admission_no=(?)''',(e,) )
                    namva=cur.fetchall()
                    smtp_obj=smtplib.SMTP('smtp.gmail.com',587)
                    smtp_obj.ehlo()
                    smtp_obj.starttls()
                    emaill='**YOUR EMAIL**' #enter first admin email
                    password='**app password**' #enter the gmail app password
                    smtp_obj.login(emaill,password)
                    from_address=emaill
                    to_address=cnfrm
                    subject='no_reply'
                    msg='subject : '+subject+'\n'+'please update your complete details on College Erp\n\n\n\n'+'''this is computer generated email.So don't reply on this.'''

                    smtp_obj.sendmail(from_address,to_address,msg)
                    print('message sent successfully')
                except:
                    print('sorry ! server not found , try again')
            else:
                print('Sorry ! admission no. not exist')
                continue


        else:
            break


#FUNC TO DELETE record
def delete():
    while True:
        dele=input('press 1 to delete record : ')
        if dele=='1':
            de=input('enter admission no. : ')
            if de in adm_list:
                cur.execute('''SELECT * FROM Erp WHERE admission_no=(?)''',(de,) )
                pr=cur.fetchall()
                print(tabulate(pr,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
                connection.commit()
                sure=input('Are you sure (y/n): ')
                if sure=='Y' or sure=='y':
                    cur.execute('''DELETE FROM Erp WHERE admission_no=?''',(de,))
                    connection.commit()
                    print(f'record deleted of admission no. {de}')
                else:
                    continue
            else:
                print('Admission no. not exists')
                continue
        else:
            break


#func to display
def search():
    while True:
        sear=input('press 1 to seach : ')
        if sear=='1':
            sre=input('enter the admission no. : ')
            if sre in adm_list:
                cur.execute('''SELECT * FROM Erp WHERE admission_no=(?)''',(sre,) )
                ser=cur.fetchall()
                print(tabulate(ser,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
                connection.commit()
            else:
                print('sorry , data not found')
                continue
        else:
            break


#func to display records
def display():
    while True:
        dis=input('''press 1 to display all records :
        press 2 to display specific record : ''' )
        if dis=='1':
            cur.execute('''SELECT * FROM Erp ORDER BY name''')
            disp=cur.fetchall()
            print(tabulate(disp,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
        elif dis=='2':
            displ=input('''=> press 1 to display contacts : \n=> press 2 to display academics details : \n=> press 3 to display all boys details : \n=> press 4 to display all girls details : ''')
            if displ=='1':
                cur.execute('''SELECT name,admission_no,email,address,phone FROM Erp ORDER BY name''')
                di=cur.fetchall()
                print(tabulate(di,headers=["Name","Ad_no","Email","Address","Phone_no"],tablefmt="fancy_grid"))
            elif displ=='2':
                cur.execute('''SELECT name,admission_no,roll_no,gender FROM Erp ORDER BY name''')
                di=cur.fetchall()
                print(tabulate(di,headers=["Name","Ad_no",'roll_no','gender'],tablefmt="fancy_grid"))
            elif displ=='3':
                p='M'
                cur.execute('''SELECT * FROM Erp WHERE gender=(?) ORDER BY name''',(p ,))
                di=cur.fetchall()
                print(tabulate(di,headers=["Name","Ad_no",'roll_no','gender',"Email","Address","Phone_no"],tablefmt="fancy_grid"))
            elif displ=='4':
                p='F'
                cur.execute('''SELECT * FROM Erp WHERE gender=(?) ORDER BY name''',(p,))
                di=cur.fetchall()
                print(tabulate(di,headers=["Name","Ad_no",'roll_no','gender',"Email","Address","Phone_no"],tablefmt="fancy_grid"))
            else:
                print('invalid choice')
                continue
        else:
            break

#main function
def runagain():
    os.system("cls")
    print("""

    -----------------------------------------------------------------
    |================================================================|
    |======== Welcome To Enterprise Resource Planning System ========|
    |================================================================|
    ------------------------------------------------------------------

    Enter 1 : To Login as Student
    Enter 2 : To Login as Administrater

        """)
    try:
        choice=int(input("enter your choice : "))
    except:
        print('==== wrong input ====')
        q=int(input("press '0' to try again : "))
        if q==0:
            runagain()
    else:
        user=input("enter your registered unique ID : ")
        import random
        otp=random.randint(100000,999999)
        import smtplib
        print('>>>>>>>>>>>> processing .....')
        try:
            cur.execute('''SELECT email FROM Erp WHERE admission_no=(?)''',(user,) )
            cnfrm=cur.fetchall()
            smtp_obj=smtplib.SMTP('smtp.gmail.com',587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            emaill='**YOUR EMAIL' #enter the first admin email id
            password='**app password' #enter first admin gmail app password
            smtp_obj.login(emaill,password)
            from_address=emaill
            to_address=cnfrm
            subject='no_reply'
            msg='subject : '+subject+'\n'+'One Time Password\n\n\n\n'+"your OTP for college erp login is "+str(otp)+'''this is computer generated email.So don't reply on this.'''

            smtp_obj.sendmail(from_address,to_address,msg)
            print('otp sent successfully')
            password=int(input("enter the otp sent to your registered email : "))
        except:
            print('sorry ! server not found or unique Id is not registered , try again')
            time.sleep(5)
        if password==otp:
            print("===========login successful==========")
            if choice==2:
                while True:
                    os.system("cls")
                    print("""

                    |================================================================|
                    |======== Welcome To Enterprise Resource Planning System ========|
                    |================================================================|

                    Enter 1 : To Add Student's details
                    Enter 2 : To Delete Student's details
                    Enter 3 : To Search Student's details
                    Enter 4 : To Update Student's details
                    Enter 5 : To Display Student's details
                    Enter 6 : To Exit

                        """)
                    chic=int(input("enter your choice : "))
                    if chic==1:
                        try:
                            add()
                            continue
                        except:
                            runagain()
                    elif chic==2:
                        try:
                            delete()
                            continue
                        except:
                            runagain()
                    elif chic==3:
                        try:
                            search()
                            continue
                        except:
                            runagain()
                    elif chic==4:
                        try:
                            update()
                            continue
                        except:
                            runagain()
                    elif chic==5:
                        try:
                            display()
                            continue
                        except:
                            runagain()
                    else:
                        runagain()

            else:
                while True:
                    os.system("cls")
                    print("""

                    |================================================================|
                    |======== Welcome To Enterprise Resource Planning System ========|
                    |================================================================|

                    Enter 1 : To Display your Details
                    Enter 2 : To Update your Details
                    Enter 3 : To Exit

                         """)
                    choose=int(input("enter your choice : "))
                    if choose==2:
                         cur.execute('''SELECT * FROM Erp WHERE admission_no=(?)''',(user,) )
                         prin=cur.fetchall()
                         print(tabulate(prin,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
                         connection.commit()
                         print("Name , Admission no. ,Gender and Roll no. couldn't be update")
                         emai=input('enter email to be update : ')
                         addre=input('enter address to be update : ')
                         pho=input('enter phone no. to be update : ')
                         cur.execute('''UPDATE Erp SET email=?,address=?,phone=? WHERE admission_no=(?)''',(emai,addre,pho,user,))
                         connection.commit()
                         oo=input("press any key : ")
                         if oo!='q':
                             continue
                    elif choose==1:
                         use=input("enter your admission no. : ")
                         cur.execute('''SELECT * FROM Erp WHERE admission_no=(?)''',(use,) )
                         prin=cur.fetchall()
                         print(tabulate(prin,headers=["Name","Ad_no","Roll_no","Gender","Email","Address","Phone_no"],tablefmt="fancy_grid"))
                         connection.commit()
                         continue
                    else:
                         break
        else:
            print("======wrong otp======")
            runagain()
runagain()

connection.close()
