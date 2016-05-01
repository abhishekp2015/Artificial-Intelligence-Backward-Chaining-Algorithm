'''
Created on Mar 2, 2016

@author: ABHISHEK PRASAD
'''
import sys
import copy

def Standardize_Variables(rule):
    r=Rule()
    r.lhs[:]=[]
    global index
    global goal
    #print rule.lhs
    #print rule.rhs
    if rule.lhs:
        for lf in rule.lhs:
            newfunc=lf.split('(')[0];
            lparameter=lf.split('(')[1].split(')')[0].split(', ')
            strn=newfunc+'('
            j=0
            for fp in lparameter:
                j=j+1
                if fp[0].islower():
                    if j<len(lparameter):
                        strn=strn+fp+str(index)+', '
                    else:
                        strn=strn+fp+str(index)+')'
                else:
                    if j<len(lparameter):
                        strn=strn+fp+', '
                    else:
                        strn=strn+fp+')'
                                
            r.lhs.append(strn)        
        rparameter=rule.rhs.split('(')[1].split(')')[0].split(', ')
        newfunc=rule.rhs.split('(')[0];
        strn=newfunc+'('
        j=0
        for fp in rparameter:
            j=j+1
            if fp[0].islower():
                if j<len(rparameter):
                    strn=strn+fp+str(index)+', '
                else:
                    strn=strn+fp+str(index)+')'
            else:
                if j<len(rparameter):
                    strn=strn+fp+', '
                else:
                    strn=strn+fp+')'
                        
        r.rhs=strn   
        index=index+1;
        return r
    else:
        return rule

def IS_VARIABLE(x):
    if not isinstance(x, list) and x[0].islower():
        return True
    else:
        return False
def IS_COMPOUND(x):
    if '(' in x and ')' in x:
        return True
    else:
        return False
def IS_LIST(x):
    if isinstance(x,list) and len(x)>0:
        return True
    else:
        return False
#def IS_OCCUR_CHECK():
                  
def UNIFY_VAR(var,x,theta):
    #print var+str(1)
    if theta==None:
        return None
    if var in theta:
        return UNIFY(theta[var], x, theta)
    elif x in theta:
        return UNIFY(var, theta[x], theta)
    else:
        theta[var]=x
        return theta                   
    
def UNIFY(x,y,theta={}):
    
    
    if theta==None:
        return None
    elif x==y:
        return theta
    elif IS_VARIABLE(x):
        return UNIFY_VAR(x,y,theta)
    elif IS_VARIABLE(y):
        return UNIFY_VAR(y,x,theta)
    elif IS_COMPOUND(x) and IS_COMPOUND(y):
        newfunc1=x.split('(')[0];
        parameter1=x.split('(')[1].split(')')[0].split(', ')
        newfunc2=y.split('(')[0];
        parameter2=y.split('(')[1].split(')')[0].split(', ')
        return UNIFY(parameter1, parameter2, UNIFY(newfunc1, newfunc2, theta))
    elif IS_LIST(x) and IS_LIST(y):
        #print y
        v1=x.pop(0)
        v2=y.pop(0)
        return UNIFY(x,y,UNIFY(v1, v2, theta))
    else:
        return None       

def print_format(x):
    parameter=x.split('(')[1].split(')')[0].split(', ')
    newfunc=x.split('(')[0];
    strn=newfunc+'('
    j=0
    for fp in parameter:
        j=j+1
        if fp[0].islower():
            if j<len(parameter):
                strn=strn+'_'+', '
            else:
                strn=strn+'_'+')'
        else:
            if j<len(parameter):
                strn=strn+fp+', '
            else:
                strn=strn+fp+')'
    return strn
    
                  
def FOL_BC_ASK(KB,query):
    return FOL_BC_OR(KB,query,{})

    
def FOL_BC_OR(KB,query,theta):
    print "FOL_BC_ORAsk: %s"%(print_format(query[0]))
    for rules in KB:
        r=copy.deepcopy(Standardize_Variables(rules))
        #print r.lhs
        #print r.rhs
        #print UNIFY(r.rhs.split(' && '),query,theta)
        q1=copy.deepcopy(query)
        thetan=copy.deepcopy(theta)
        #if UNIFY(r.rhs.split(' && '),q1,theta)==None:
        #print "False: %s"%(query[0])
        #else:
        #print "True: %s"%(query[0])
        u={}
        #u=UNIFY(r.rhs.split(' && '),q1,thetan)
        
        #if q1:
        #   if t>0:
        #        print "FOL_BC_ORTRUE: %s"%(print_format(q1[0]))
        #    else:
        #       print "FOL_BC_ORFALSE: %s"%(print_format(q1[0]))
        flag1=0
        for rtheta_dash in FOL_BC_AND(KB, r.lhs, UNIFY(r.rhs.split(' && '),copy.deepcopy(query),thetan)):
            #if q1:
            
            flag1=1   #print "True: %s"%(q1[0])
            if query:
                print "fuckhard",query
                print("True: %s"%(print_format(SUBST(copy.deepcopy(rtheta_dash), query[0])[0])))
                qa=copy.deepcopy(query)
                
            yield rtheta_dash
            print qa
        if flag1==1:
            flag1=0
            if (UNIFY(copy.deepcopy(qa), copy.deepcopy(goal), rtheta_dash))!=None:
                return

        #if u!= None:
         #   if query:
          #      print("Ask: %s"%(print_format(query[0])))
    
    #print "FOL_BC_ORFalse: %s"%(print_format(query[0]))   
   
               
def FOL_BC_AND(KB,query,theta):
    if theta is None:
        return
    elif not query:
        yield theta
    else:
        first=query.pop(0)
        rest=[]
        rest[:]=[]
        rest=copy.deepcopy(query)
        
        #print("-->Ask: %s"%(print_format(SUBST(theta,first)[0])))
        #ta1=tee(ta)
        #if len(list(ta1))>0:
        #sum(1 for i in ta)
        #if i>0:
        #print "FOL_BC_ANDTrue: %s"%(print_format(SUBST(theta,first)[0])),theta
        #else:
        #    print "FOL_BC_ANDFalse: %s"%(print_format(SUBST(theta,first)[0]))
        flag=0
        thetan1=copy.deepcopy(theta)
        for theta_dash in FOL_BC_OR(KB, SUBST(thetan1,first), thetan1):
            
            if flag==0:
                #print "FOL_BC_ANDTrue: %s"%(print_format(SUBST(theta,first)[0]))
                flag=1
            #if SUBST(theta,first):
            #    print "FOL_BC_ANDTrue:",theta
            #    print "FOL_BC_ANDTrue: %s"%(SUBST(theta,first)[0])
            for theta_dash_dash in FOL_BC_AND(KB, copy.deepcopy(rest), theta_dash):
                #if SUBST(theta,first):
                #   print "True: %s"%(SUBST(theta,first)[0])
                yield theta_dash_dash
            #print("-->HaloAsk: %s"%(print_format(SUBST(thetan1,first)[0])))
                 
        if flag==0:
            print("False: %s"%(print_format(SUBST(thetan1,first)[0])))
            if (UNIFY(copy.deepcopy(query), copy.deepcopy(goal), thetan1))!=None:
                return
            
def SUBST(theta,x):
    #print x
    for v1 in theta:
        if theta.has_key(theta.get(v1)):
            if theta.get(theta.get(v1))[0].isupper():
                theta[v1]=theta.get(theta.get(v1))
    parameter=x.split('(')[1].split(')')[0].split(', ')
    newfunc=x.split('(')[0];
    strn=newfunc+'('
    j=0
    for fp in parameter:
        j=j+1
        if fp[0].islower():
            if theta.has_key(fp):
                if theta.get(fp)[0].isupper():
                    fp=theta.get(fp)
            if j<len(parameter):
                strn=strn+fp+', '
            else:
                strn=strn+fp+')'
        else:
            if j<len(parameter):
                strn=strn+fp+', '
            else:
                strn=strn+fp+')'
    return strn.split(' && ')
                
        
    
class Rule(object):
    lhs=[]
    rhs=None
index=1
f = open(sys.argv[len(sys.argv)-1],"r")

inputlines=f.read().splitlines();
Query=inputlines[0];
n=inputlines[1];
#if ' && ' in Query:
q1=Query.split(' && ')
#else:
    #q1=Query
kbrule = [0 for x in range(int(n))]
for i in range(0,int(n)):
    kbrule[i]=Rule()
    if(' => ' in inputlines[2+i]):
        val=inputlines[2+i].split(' => ')
        kbrule[i].rhs=val[1]
        kbrule[i].lhs=val[0].split(' && ')
    else:
        kbrule[i].lhs=[]
        kbrule[i].rhs=inputlines[2+i]
   
#for i in range(0,int(n)):
#    print kbrule[i].lhs
#    print kbrule[i].rhs
fo = open("output.txt", "w")
print len(q1)
if len(q1)>1:
    flag=0
    for q in q1:
        goal= copy.deepcopy(q.split(' && '))
        if len(list(FOL_BC_ASK(kbrule,q.split(' && '))))>0:
            print("True")
        else:
            print("False")
        #if len(list(FOL_BC_ASK(kbrule,q.split(' && '))))<=0:
         #   print ("false")
          #  flag=1
           # break
    if flag==0:
        print ("true")  
else:
    goal=q1
    if len(list(FOL_BC_ASK(kbrule,q1)))>0:
        print("True")
    else:
        print("False")       

fo.close()    