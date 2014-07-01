import misc
import crack
import sys

KEY="130>>"

def run_test(fun,args,chk,pts):
    try:
        rv=fun(*args)
        print("%s calling %s(%s)... " % \
              (KEY,fun.__name__,",".join([repr(x) for x in args])),rv)
    except Exception, e:
        print("Exception: "+str(e))
        return 0
    else:
        if chk(rv):
            print("Good")
            return pts
        else:
            print("Wrong")
            return 0

def chk_val(x):
    return lambda y: x==y

def chk_flt(x):
    return lambda y: abs(x-y)<1e-8

def chk_dict(qry,rslt,sz):
    return lambda d: len(d)==sz and qry in d and d[qry]==rslt

def chk_set(qry,sz):
    return lambda d: len(d)==sz and qry in d

def chk_file(fn):
    return lambda d: sys.stdout.write("\nSee file \"%s\"\n" % fn) or True

def run_tests(tests):
    score=0
    total=0
    for (fun,args,chk,pts) in tests:
        score+=run_test(fun,args,chk,pts)
        total+=pts
    return (score,total)

def run_all_tests():
    globals={}
    return run_tests([
        #problem 1
        (misc.closest_to,[[2,4,8,9],7],chk_val(8),1),
        (misc.closest_to,[[2,4,8,9],5],chk_val(4),1),
        (misc.make_dict,[["foo","baz"],["bar","blah"]],chk_val({'foo': 'bar', 'baz': 'blah'}),1),
        (misc.make_dict,[[1],[100]],chk_val({1: 100}),1),
        (misc.word_count,["news.txt"],chk_dict("edu",2,407),1),

        #problem 2
        (crack.load_words,["words",r"^[A-Z].{2}$"],chk_set("Tim",3893),1),
        (crack.load_words,["words",r"^xYx.*$"],chk_val([]),1),
        (lambda x: set(crack.transform_reverse(x)),["Moose"],chk_val(set(['Moose','esooM'])),1),
        (lambda x: set(crack.transform_capitalize(x)),["foo"],chk_val(set(['foo', 'Foo', 'fOo', 'FOo', 'foO', 'FoO', 'fOO', 'FOO'])),1),
        (lambda x: set(crack.transform_digits(x)),["Bow"],chk_val(set(['Bow', 'B0w', '6ow', '60w', '8ow', '80w'])),1),
        (crack.check_pass,["asarta","IqAFDoIjL2cDs"],chk_val(True),1),
        (crack.check_pass,["foo","AAbcdbcdzyxzy"],chk_val(False),1),
        (lambda x: crack.load_passwd(x)[3],["passwd"],chk_dict("GECOS",'Forkland Maskins',7),1),
        (crack.crack_pass_file,["passwd","words","passwd-out.txt"],chk_file("passwd-out.txt"),1),
        
        ])

(s,t)=run_all_tests()
print("%s Results: (%d/%d)" % (KEY,s,t))
print("%s Compiled" % KEY)
    

